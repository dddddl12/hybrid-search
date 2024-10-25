import asyncio
import random
from datetime import datetime

from sqlalchemy import select

from src.db import SessionLocal
from src.models import MagazineModel, MagazineContentModel, WikiPage
from src.elastic import es_client, es_indices

from src.schemas import CategoryEnum, Magazine, MagazineContent
from src.utils import transformer_model


def get_random_category() -> CategoryEnum:
    return random.choice(list(CategoryEnum))


async def insert_record(content_title: str, author: str, author_id: int, publication_date: datetime,
                        content: str) -> None:
    session = SessionLocal()
    try:
        # Generate vector representation for the content
        vector = transformer_model.encode(content).tolist()
        vector_representation = ",".join(map(str, vector))

        # Insert into the database
        title = str(author_id)
        stmt = select(MagazineModel).where(MagazineModel.title == title)
        magazine = session.scalars(stmt).first()
        if not magazine:
            category = get_random_category()
            magazine = MagazineModel(
                title=title,
                author=author,
                publication_date=publication_date,
                category=category
            )
            session.add(magazine)
            session.commit()

        magazine_content = MagazineContentModel(
            magazine=magazine,
            title=content_title,
            content=content,
            vector_representation=vector_representation
        )
        session.add(magazine_content)
        session.commit()

        # Insert into Elasticsearch
        doc = {
            "magazine_id": magazine.id,
            "title": content_title,
            "content": content,
            # "category":
            "vector": vector
        }
        await es_client.index(index="magazine_contents", id=str(magazine_content.id), document=doc)
        print(f"Record inserted successfully with ID: {magazine.id}")
    except Exception as e:
        session.rollback()
        print(f"Error inserting record: {e}")
        raise Exception("ㅁㅁ")
    finally:
        session.close()


async def migrate() -> None:
    session = SessionLocal()
    i = 0
    while True:
        pages = session.query(WikiPage).limit(1000).offset(i * 1000).all()
        for page in pages:
            await insert_record(
                content_title=page.title,
                author=page.author or "Anonymous",
                author_id=page.author_id or 0,
                publication_date=page.publication_date,
                content=page.content
            )
        break
        # i += 1
        # if len(pages) < 1000:
        #     break


async def migrate2() -> None:
    session = SessionLocal()
    # magazine_records = session.query(MagazineModel).all()
    # for magazine_record in magazine_records:
    #     magazine = Magazine(
    #         id=magazine_record.id,
    #         title=magazine_record.title,
    #         author=magazine_record.author,
    #         publication_date=magazine_record.publication_date,
    #         category=magazine_record.category,
    #         contents=[]
    #     )
    #     print(magazine)
    #     magazine_serialized = magazine.model_dump()
    #     # magazine_serialized['publication_date'] = magazine_serialized['publication_date']
    #     await es_client.index(
    #         index=es_indices.magazines, id=str(magazine.id), document=magazine_serialized)

    content_records = session.query(MagazineContentModel).all()
    for content_record in content_records:
        content = MagazineContent(
            id=content_record.id,
            title=content_record.title,
            content=content_record.content,
            vector_representation=[
                float(el) for el in content_record.vector_representation.split(',')]
        )
        print(content)
        await es_client.index(
            index=es_indices.magazines,
            id=str(content.id),
            document={
                "script": {
                    "source": """
      ctx._source.contents.add(params.new_content);
    """,
                    "params": {
                        "new_content": content.model_dump()
                    }
                }
            })


# Example usage
if __name__ == "__main__":
    asyncio.run(migrate2())
