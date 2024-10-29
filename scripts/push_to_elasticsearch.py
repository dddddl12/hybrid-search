import asyncio
from typing import Any

from elasticsearch import NotFoundError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db import engine
from app.models import MagazineContentModel
from app.services.elasticsearch import es_client, es_indices

from app.schemas import Magazine, MagazineContent
from app.services.search import transformer_model


async def init_elasticsearch_index() -> None:
    try:
        await es_client.indices.delete(
            index=es_indices.magazine_contents
        )
    except NotFoundError:
        # In the case of no index was found.
        pass
    await es_client.indices.create(
        index=es_indices.magazine_contents,
        settings={
            "index.mapping.coerce": False
        },
        mappings={
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "content": {
                    "type": "text"
                },
                "metadata": {
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "title": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword"
                                }
                            }
                        },
                        "author": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword"
                                }
                            }
                        },
                        "publication_date": {
                            "type": "date",
                            "format": "yyyy-MM-dd"
                        },
                        "category": {
                            "type": "keyword"
                        }
                    }
                },
                "vector_representation": {
                    "type": "dense_vector",
                    "dims": 384
                }
            }
        }
    )


async def push_to_elasticsearch() -> None:
    limit = 300
    async with AsyncSession(engine) as session:
        seq = 0
        while True:
            print(f"Page: {seq}")
            stmt = select(MagazineContentModel).limit(limit).offset(limit * seq).options(
                selectinload(MagazineContentModel.magazine))
            result = await session.scalars(stmt)
            content_records = result.fetchall()
            operations: list[dict[str, Any]] = []
            for i, content_record in enumerate(content_records):
                print(f"Page: {seq} - {i}")
                magazine_record = content_record.magazine
                text = f"{content_record.title}\n{content_record.content}"
                operations += [
                    {
                        "index": {
                            "_index": es_indices.magazine_contents,
                            "_id": str(content_record.id),
                        }
                    },
                    MagazineContent(
                        id=content_record.id,
                        title=content_record.title,
                        content=content_record.content,
                        metadata=Magazine(
                            id=magazine_record.id,
                            title=magazine_record.title,
                            author=magazine_record.author,
                            publication_date=magazine_record.publication_date,
                            category=magazine_record.category
                        ),
                        vector_representation=transformer_model.encode(text).tolist()
                    ).model_dump()
                ]
            await es_client.bulk(operations=operations)
            seq += 1
            is_complete = len(content_records) < limit
            if is_complete:
                break


async def migrate() -> None:
    es_client.connect()
    print("Initializing Elasticsearch index")
    await init_elasticsearch_index()
    print("Pushing to Elasticsearch...")
    await push_to_elasticsearch()
    print("Migration completed.")
    await es_client.close()


# Example usage
if __name__ == "__main__":
    asyncio.run(migrate())
