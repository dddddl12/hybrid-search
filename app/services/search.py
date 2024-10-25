from sentence_transformers import SentenceTransformer
from app.services.elasticsearch import es_client, es_indices, ESMagazineContentResponse, ESBoolQueryFilter, \
    ESBoolQueryFilterRange
from app.schemas import SearchQuery, SearchQueryResponse, SearchQueryFilters

transformer_model = SentenceTransformer('all-MiniLM-L6-v2')


def set_bool_query_filter(raw_filters: SearchQueryFilters) -> list[ESBoolQueryFilter]:
    query_filter: list[ESBoolQueryFilter] = []
    if raw_filters.title:
        query_filter.append({
            "match": {"metadata.title": raw_filters.title}
        })
    if raw_filters.author:
        query_filter.append({
            "match": {"metadata.author": raw_filters.author}
        })
    if raw_filters.category:
        query_filter.append({
            "terms": {"metadata.category": [
                c.value for c in raw_filters.category]}
        })
    date_range: ESBoolQueryFilterRange = {}
    if raw_filters.min_date:
        date_range["gte"] = raw_filters.min_date.strftime("%Y-%m-%d")
    if raw_filters.max_date:
        date_range["lte"] = raw_filters.max_date.strftime("%Y-%m-%d")
    if date_range:
        query_filter.append({
            "range": {
                "metadata.publication_date": date_range
            }
        })
    return query_filter


async def hybrid_search_logic(q: SearchQuery) -> SearchQueryResponse:
    query_filter = set_bool_query_filter(q.filters)
    if q.keyword:
        query_vector = transformer_model.encode(q.keyword).tolist()
        query_param = {
            "script_score": {
                "query": {
                    "bool": {
                        "must": query_filter,
                        "should": [
                            {"match": {"title.keyword": q.keyword}},
                            {"match": {"content": q.keyword}}
                        ]
                    },
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector_representation') + 1.0",
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        }
    else:
        query_param = {
            "bool": {
                "must": query_filter,
            },
        }
    es_response = await es_client.search(
        index=es_indices.magazine_contents,
        query=query_param,
        source_excludes=["vector_representation"],
        from_=q.offset,
        size=q.limit
    )
    es_response_parsed = ESMagazineContentResponse.model_validate(es_response.body)
    return SearchQueryResponse(
        total=es_response_parsed.total,
        contents=es_response_parsed.hits,
    )
