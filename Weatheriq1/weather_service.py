import httpx

API_KEY = "c4af157e9bcb318f3f4e49eec7eeb130"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def fetch_weather(city: str = None, lat: float = None, lon: float = None) -> dict:
    params = {"appid": API_KEY, "units": "metric"}

    if city:
        params["q"] = city
    elif lat is not None and lon is not None:
        params["lat"] = lat
        params["lon"] = lon
    else:
        raise ValueError("Provide either city or both latitude and longitude.")

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
