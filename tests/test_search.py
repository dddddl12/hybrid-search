from datetime import date

import pytest
from app.schemas import SearchQuery, SearchQueryResponse, CategoryEnum, SearchQueryFilters
from app.services.search import hybrid_search_logic


@pytest.mark.asyncio
async def test_hybrid_search_logic() -> None:
    # Mocking dependencies

    q = SearchQuery(
        keyword="test",
        filters=SearchQueryFilters(
            title=None,
            author=None,
            category=[CategoryEnum.sports],
            min_date=date(year=1999, month=1, day=1),
            max_date=None
        ),
        offset=0,
        limit=10
    )

    search_response = await hybrid_search_logic(q)

    # Now we can perform our asserts
    assert isinstance(search_response, SearchQueryResponse)
