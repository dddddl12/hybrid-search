from datetime import datetime
from enum import Enum

from pydantic import BaseModel, PlainSerializer
from typing import Optional, Annotated


class CategoryEnum(str, Enum):
    fashion = "FASHION"
    technology = "TECHNOLOGY"
    science = "SCIENCE"
    travel = "TRAVEL"
    sports = "SPORTS"
    food = "FOOD"


class MagazineContent(BaseModel):
    id: int
    title: str
    content: str
    vector_representation: list[float]


class Magazine(BaseModel):
    id: int
    title: str
    author: str
    publication_date: Annotated[
        datetime, PlainSerializer(lambda x: x.strftime("%Y-%m-%d"), return_type=str)]
    category: CategoryEnum
    contents: list[MagazineContent]


class SearchQueryFilters(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: list[CategoryEnum] = []


class SearchQuery(BaseModel):
    keyword: Optional[str] = None
    magazine_filters: SearchQueryFilters = SearchQueryFilters()
    limit: int = 10
    offset: int = 0


class SearchQueryResponse(BaseModel):
    magazines: list[Magazine]
    contents: list[MagazineContent]
