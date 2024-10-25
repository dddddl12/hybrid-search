from typing import Any
from typing_extensions import TypedDict, NotRequired

from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel, model_validator

from app.core.config import settings
from app.schemas import MagazineContentHit

es_client = AsyncElasticsearch(
    settings.elasticsearch_url,
    api_key=settings.elasticsearch_api_key,
    verify_certs=not settings.is_local
)


class ElasticsearchIndices(BaseModel):
    magazine_contents: str = "magazine_contents"


es_indices = ElasticsearchIndices()


# Request
class ESBoolQueryFilterRange(TypedDict):
    lte: NotRequired[str]
    gte: NotRequired[str]


class ESBoolQueryFilter(TypedDict):
    match: NotRequired[dict[str, str]]
    terms: NotRequired[dict[str, list[str]]]
    range: NotRequired[dict[str, ESBoolQueryFilterRange]]


# Response
class ESRawHitTotal(TypedDict):
    value: int
    relation: str


class ESRawHitItem(TypedDict):
    _score: int
    _source: dict[str, Any]


class ESRawHits(TypedDict):
    total: ESRawHitTotal
    hits: list[ESRawHitItem]


class ESRawResp(TypedDict):
    hits: ESRawHits


class ESMagazineContentResponse(BaseModel):
    total: int
    hits: list[MagazineContentHit]

    @model_validator(mode='before')
    @classmethod
    def restructure(cls, v: ESRawResp) -> dict[str, Any]:
        hits_object = v['hits']
        hits = [dict(
            score=hit["_score"],
            **hit["_source"]
        ) for hit in hits_object['hits']]
        return {
            "total": hits_object['total']['value'],
            "hits": hits
        }
