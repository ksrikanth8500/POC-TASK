from fastapi import FastAPI, HTTPException, Query
from weather_service import fetch_weather

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Weather API is running"}

@app.get("/weather")
async def get_weather(
        city: str = Query(default=None, description="City name (e.g., London)"),
        lat: float = Query(default=None, description="Latitude (e.g., 40.7128)"),
        lon: float = Query(default=None, description="Longitude (e.g., -74.0060)")
):
    try:
        if not city and (lat is None or lon is None):
            raise HTTPException(status_code=400, detail="Provide either city or both lat and lon.")

        weather_data = await fetch_weather(city=city, lat=lat, lon=lon)

        return {
            "location": city or f"{lat}, {lon}",
            "temperature": weather_data["main"]["temp"],
            "description": weather_data["weather"][0]["description"],
            "humidity": weather_data["main"]["humidity"],
            "wind_speed": weather_data["wind"]["speed"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
