from typing import Any

from sentence_transformers import SentenceTransformer
from src.elastic import es_client, es_indices
from src.schemas import SearchQuery, SearchQueryResponse

transformer_model = SentenceTransformer('all-MiniLM-L6-v2')


async def hybrid_search_logic(q: SearchQuery) -> SearchQueryResponse:
    searches: list[dict[str, Any]] = []
    if q.keyword:
        query_vector = transformer_model.encode(q.keyword)
        result = await es_client.search(
            index=es_indices.magazines,
            query={
                "match_all": {}
            },
            script_fields={
                "script_score": {
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector_representation') + 1.0",
                        "params": {
                            "query_vector": [float(n) for n in query_vector]
                        }
                    }
                }
            }
        )

    # Apply magazine filters
    filters = q.magazine_filters.model_dump(exclude_none=True)
    matches = [{"match": {key: value}} for key, value in filters.items() if value]
    if matches:
        searches.append({
            "index": es_indices.magazines,
            "query": {
                "bool": {
                    "must": matches
                }
            }
        })

    # searches = [{"index": "magazine_contents"},
    #             {"query": {"match": {"title": "the"}}}]
    # response = await es_client.msearch(body="\n".join([json.dumps(s) for s in searches]))
    # response = await es_client.msearch(searches=searches)

    # assert q.keyword
    # query_vector = transformer_model.encode(q.keyword)
    # response = await es_client.search(
    #     index=es_indices.magazine_contents, query={
    #
    #     }
    # )
    # aa = response["hits"]["hits"]
    # for hit in aa:
    #     print(hit['_source']['content'])
    return response
