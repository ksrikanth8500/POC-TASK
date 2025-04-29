import unittest
from unittest.mock import patch, MagicMock
from phase4.embeddings import embedder

class TestEmbedder(unittest.TestCase):

    @patch("requests.get")
    def test_fetch_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 25, "humidity": 50, "pressure": 1010},
            "wind": {"speed": 5},
            "dt": 1714399923
        }
        mock_get.return_value = mock_response

        weather_info, text = embedder.fetch_weather("London")
        self.assertEqual(weather_info["city"], "London")
        self.assertIn("Weather in London", text)
