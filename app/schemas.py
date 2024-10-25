from datetime import date
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


class Magazine(BaseModel):
    id: int
    title: str
    author: str
    publication_date: date
    category: CategoryEnum


class MagazineContentBase(BaseModel):
    id: int
    title: str
    content: str
    metadata: Magazine


class MagazineContent(MagazineContentBase):
    vector_representation: list[float]


class MagazineContentHit(MagazineContentBase):
    score: float


class SearchQueryFilters(BaseModel):
    title: Optional[str]
    author: Optional[str]
    category: list[CategoryEnum]
    min_date: Optional[date]
    max_date: Optional[date]


class SearchQuery(BaseModel):
    keyword: Optional[str]
    filters: SearchQueryFilters
    limit: int
    offset: int


class SearchQueryResponse(BaseModel):
    total: int
    contents: list[MagazineContentHit]
