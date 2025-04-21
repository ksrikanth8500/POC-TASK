import requests


API_KEY = "c4af157e9bcb318f3f4e49eec7eeb130"

def fetch_realtime_weather(city):
    """
    Fetch real-time weather for a given city from OpenWeatherMap.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return {}