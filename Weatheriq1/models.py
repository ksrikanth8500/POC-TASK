from pydantic import BaseModel
from typing import Optional

class WeatherRequest(BaseModel):
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
