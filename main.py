from fastapi import FastAPI
from starlette.requests import Request

from src.schemas import SearchQueryResponse
from src.utils import hybrid_search_logic

# FastAPI setup
app = FastAPI()


@app.get("/hybrid_search/", response_model=SearchQueryResponse)
async def hybrid_search(request: Request):
    return await hybrid_search_logic(request)
