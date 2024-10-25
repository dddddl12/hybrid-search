import pytest
from fastapi.testclient import TestClient

from app.schemas import CategoryEnum
from main import app

client = TestClient(app)


def test_hybrid_search() -> None:
    response = client.get('/hybrid_search')
    assert response.is_success


def test_hybrid_search_keyword() -> None:
    response = client.get('/hybrid_search', params={'keyword': 'test'})
    assert response.is_success


def test_hybrid_search_title_filter() -> None:
    response = client.get('/hybrid_search', params={'filters.title': 'test_title'})
    assert response.is_success


def test_hybrid_search_author_filter() -> None:
    response = client.get('/hybrid_search', params={'filters.author': 'test_author'})
    assert response.is_success


def test_hybrid_search_category_filter() -> None:
    response = client.get('/hybrid_search', params={'filters.category': [CategoryEnum.sports, CategoryEnum.food]})
    assert response.is_success


def test_hybrid_search_date_filter() -> None:
    response = client.get('/hybrid_search', params={
        'filters.min_date': "2001-01-01",
        'filters.max_date': "2021-01-01",
    })
    assert response.is_success


def test_hybrid_search_pagination() -> None:
    response = client.get('/hybrid_search', params={'offset': 10, 'limit': 20})
    assert response.is_success


def test_hybrid_search_invalid_pagination() -> None:
    response = client.get('/hybrid_search', params={'offset': -10, 'limit': 200})
    assert response.status_code == 422
