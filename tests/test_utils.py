import unittest
from unittest.mock import patch, AsyncMock

from src.schemas import SearchQuery
from src import utils


class TestUtils(unittest.IsolatedAsyncioTestCase):

    @patch("src.utils.transformer_model.encode", return_value=[1, 2, 3, 4, 5])
    @patch("src.utils.es_indices.magazine_contents", return_value="test_magazine_contents")
    @patch("src.utils.es_client.msearch")
    async def test_empty_search_query(self, mock_msearch, mock_contents_index, mock_encode):
        mock_msearch.return_value = AsyncMock(return_value={"status": "ok"})
        q = SearchQuery()
        assert utils.hybrid_search_logic(q) == {"status": "ok"}

    async def test_with_keyword(self):
        q = SearchQuery(keyword="relating to")
        result = await utils.hybrid_search_logic(q)
        print(result)
        assert result == {"status": "ok"}

    @patch("src.utils.transformer_model.encode", return_value=[1, 2, 3, 4, 5])
    @patch("src.utils.es_indices.magazine_contents", return_value="test_magazine_contents")
    @patch("src.utils.es_indices.magazines", return_value="test_magazines")
    @patch("src.utils.es_client.msearch")
    async def test_with_filters(self, mock_msearch, mock_magazines_index, mock_contents_index, mock_encode):
        mock_msearch.return_value = AsyncMock(return_value={"status": "ok"})
        q = SearchQuery(magazine_filters={"test_filter": "test_value"})
        assert utils.hybrid_search_logic(q) == {"status": "ok"}


if __name__ == '__main__':
    unittest.main()
