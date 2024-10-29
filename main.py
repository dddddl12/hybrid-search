from datetime import date
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import SearchQueryResponse, CategoryEnum, SearchQuery, SearchQueryFilters
from app.services.search import hybrid_search_logic

# FastAPI setup
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hybrid_search", response_model=SearchQueryResponse)
async def hybrid_search(
        keyword: Optional[str] = Query(
            default=None,
            description="Search keyword to match against magazine content text. This parameter is subject to vector search."
        ),
        title: Optional[str] = Query(
            default=None,
            alias="filters.title",
            description="Filter by parent magazine title"
        ),
        author: Optional[str] = Query(
            default=None,
            alias="filters.author",
            description="Filter by parent magazine author"
        ),
        category: list[CategoryEnum] = Query(
            default_factory=list,
            alias="filters.category",
            description="Filter by parent magazine category/categories"
        ),
        min_date: Optional[date] = Query(
            default=None,
            alias="filters.min_date",
            description="Filter by parent magazine publication date (from)"
        ),
        max_date: Optional[date] = Query(
            default=None,
            alias="filters.max_date",
            description="Filter by parent magazine publication date (to)"
        ),
        offset: int = Query(
            default=0,
            ge=0,
            description="Number of content results to skip for pagination"
        ),
        limit: int = Query(
            default=30,
            ge=1,
            le=100,
            description="Maximum number of content results to return"
        )
) -> SearchQueryResponse:
    query = SearchQuery(
        keyword=keyword,
        offset=offset,
        limit=limit,
        filters=SearchQueryFilters(
            title=title,
            author=author,
            category=category,
            min_date=min_date,
            max_date=max_date
        )
    )
    return await hybrid_search_logic(query)
