import requests
import json
from db import get_connection
from config import OPENWEATHER_API_KEY

def fetch_realtime_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
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
    cities = ["London", "New York", "Tokyo", "Mumbai"]
    for city in cities:
        print(f"Fetching real-time weather for {city}...")
        data = fetch_realtime_weather(city)
        save_weather_data(city, "real_time", data)
