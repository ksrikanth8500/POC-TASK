import unittest
from unittest.mock import patch, MagicMock
from phase4.embeddings import storage

class TestStorage(unittest.TestCase):

    @patch("phase4.embeddings.get_weather_and_embedding")
    @patch("psycopg2.connect")
    def test_store_weather_data_and_embedding_success(self, mock_connect, mock_get_weather_embedding):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_get_weather_embedding.return_value = (
            {
                "city": "TestCity",
                "type": "Clear",
                "timestamp": "2025-04-29 10:00:00",
                "temperature": 25,
                "humidity": 60,
                "pressure": 1010,
                "wind_speed": 5,
                "description": "Clear sky"
            },
            "Weather in TestCity: Clear sky.",
            [0.1, 0.2, 0.3]  # Mock embedding vector
        )

        storage.store_weather_data_and_embedding("TestCity")

        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
