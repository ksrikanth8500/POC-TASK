import requests
import json
from db import get_connection
from config import OPENWEATHER_API_KEY

# Map cities to lat/lon
CITY_COORDS = {
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
    "Tokyo": (35.6895, 139.6917),
    "Mumbai": (19.0760, 72.8777)
}

def fetch_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    return response.json()

def save_weather_data(city, data_type, data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO weather_data (city, type, data) VALUES (%s, %s, %s)",
        (city, data_type, json.dumps(data))
    )
    conn.commit()
    cur.close()
    conn.close()

def collect():
    for city, (lat, lon) in CITY_COORDS.items():
        print(f"Fetching air quality for {city}...")
        data = fetch_air_quality(lat, lon)
        save_weather_data(city, "air_quality", data)
