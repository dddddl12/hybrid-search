from datetime import date
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List


class CategoryEnum(str, Enum):
    fashion = "FASHION"
    technology = "TECHNOLOGY"
    science = "SCIENCE"
    travel = "TRAVEL"
    sports = "SPORTS"
    food = "FOOD"


class Magazine(BaseModel):
    id: int = Field(..., description="Unique identifier for the magazine")
    title: str = Field(..., description="Title of the magazine")
    author: str = Field(..., description="Author of the magazine")
    publication_date: date = Field(..., description="Publication date of the magazine")
    category: CategoryEnum = Field(..., description="Category of the magazine")


class MagazineContentBase(BaseModel):
    id: int = Field(..., description="Unique identifier for the content")
    title: str = Field(..., description="Title of the content")
    content: str = Field(..., description="Text content of the magazine article")
    metadata: Magazine = Field(..., description="Metadata of the magazine associated with the content")


class MagazineContent(MagazineContentBase):
    vector_representation: List[float] = Field(..., description="Vector representation of the content")


class MagazineContentHit(MagazineContentBase):
    score: float = Field(..., description="Relevance score of the content hit")


class SearchQueryFilters(BaseModel):
    title: Optional[str] = Field(None, description="Filter by title")
    author: Optional[str] = Field(None, description="Filter by author")
    category: List[CategoryEnum] = Field(..., description="Filter by categories")
    min_date: Optional[date] = Field(None, description="Filter by the minimum publication date")
    max_date: Optional[date] = Field(None, description="Filter by the maximum publication date")


class SearchQuery(BaseModel):
    keyword: Optional[str] = Field(None, description="Keyword to search in the contents")
    filters: SearchQueryFilters = Field(..., description="Filters to apply to the search query")
    limit: int = Field(..., description="Limit the number of results")
    offset: int = Field(..., description="Offset for pagination")


class SearchQueryResponse(BaseModel):
    total: int = Field(..., description="The total number of results found")
    contents: List[MagazineContentHit] = Field(...,
                                               description="A list of magazine content hits matching the search query")
