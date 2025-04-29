import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from phase4.api import rag_api

client = TestClient(rag_api.app)

class TestRAGAPI(unittest.TestCase):

    @patch("phase4.api.rag_api.store_weather_data_and_embedding")
    @patch("phase4.api.rag_api.model.encode")
    @patch("psycopg2.connect")
    def test_search_weather_info_success(self, mock_connect, mock_encode, mock_store_weather):
        mock_encode.return_value = [0.1, 0.2, 0.3]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ("City1", "Clear sky today", 0.01),
            ("City2", "Cloudy day", 0.02),
            ("City3", "Sunny and bright", 0.03),
        ]

        response = client.get("/query/?query=London")
        self.assertEqual(response.status_code, 200)
        self.assertIn("matches", response.json())
        self.assertEqual(len(response.json()["matches"]), 3)
