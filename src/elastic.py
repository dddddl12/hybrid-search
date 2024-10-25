from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel

from src.config import settings

es_client = AsyncElasticsearch(
    settings.elasticsearch_url,
    api_key=settings.elasticsearch_api_key,
    verify_certs=not settings.is_local
)


class ElasticsearchIndices(BaseModel):
    magazines: str = "magazines"


es_indices = ElasticsearchIndices()
