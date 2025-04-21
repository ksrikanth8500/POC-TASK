# phase4/embeddings/embedder.py

import requests
from sentence_transformers import SentenceTransformer
from datetime import datetime

# Hardcoded API key
OPENWEATHER_API_KEY = "c4af157e9bcb318f3f4e49eec7eeb130"
model = SentenceTransformer("all-MiniLM-L6-v2")

def fetch_weather(city: str):
    """Fetch current weather from OpenWeatherMap for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Weather fetch failed for {city}: {response.text}")

    data = response.json()
    weather_info = {
        "city": city,
        "type": data['weather'][0]['main'],
        "timestamp": datetime.utcfromtimestamp(data['dt']),
        "temperature": data['main']['temp'],
        "humidity": data['main']['humidity'],
        "pressure": data['main']['pressure'],
        "wind_speed": data['wind']['speed'],
        "description": data['weather'][0]['description'],
    }

    # Text for embedding
    text = (
        f"Weather in {city}: {weather_info['description']}. "
        f"Temperature: {weather_info['temperature']}°C. "
        f"Humidity: {weather_info['humidity']}%. "
        f"Pressure: {weather_info['pressure']} hPa. "
        f"Wind Speed: {weather_info['wind_speed']} m/s."
    )

    return weather_info, text

def generate_embedding(text: str):
    return model.encode(text).tolist()

def get_weather_and_embedding(city: str):
    weather_info, text = fetch_weather(city)
    embedding = generate_embedding(text)
    return weather_info, text, embedding
