import unittest
from unittest.mock import patch, MagicMock
from phase3.ingestion import bulk_trans_val
import json

class TestBulkTest(unittest.TestCase):

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='[{"id": 1, "name": "City1"}, {"id": 2, "name": "City2"}]')
    def test_load_cities_success(self, mock_open):
        cities = bulk_trans_val.load_cities(limit=2)
        self.assertEqual(len(cities), 2)
        self.assertEqual(cities[0]["id"], 1)

    @patch("requests.get")
    def test_fetch_bulk_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"list": [{"id": 1}, {"id": 2}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = bulk_trans_val.fetch_bulk_weather([1, 2])
        self.assertEqual(len(result), 2)

    @patch("requests.get")
    def test_fetch_air_quality_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"list": [{"main": {"aqi": 2}}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = bulk_trans_val.fetch_air_quality(10, 20)
        self.assertEqual(result, 2)

    def test_transform_weather_success(self):
        data = {
            "dt": 1714399923,
            "main": {"temp": 25, "humidity": 80, "pressure": 1010},
            "wind": {"speed": 5},
            "weather": [{"description": "clear sky"}]
        }
        aqi = 2
        result = bulk_trans_val.transform_weather(data, aqi)
        self.assertIsNotNone(result)
        self.assertEqual(result["temperature"], 25)
        self.assertEqual(result["air_quality_index"], 2)

    def test_is_valid_weather_success(self):
        weather_data = {
            "temperature": 25,
            "humidity": 50,
            "pressure": 1000
        }
        self.assertTrue(bulk_trans_val.is_valid_weather(weather_data))

    @patch("psycopg2.connect")
    def test_insert_into_db_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        weather_data = {
            "temperature": 25,
            "humidity": 50,
            "description": "sunny",
            "air_quality_index": 2,
            "timestamp": "2025-04-29 10:00:00"
        }
        bulk_trans_val.insert_into_db(weather_data, "City1", "State1")

        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
