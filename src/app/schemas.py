from pydantic import BaseModel
from typing import Optional


class ActualWeatherScheme(BaseModel):
    temperature: float
    wind_speed: float
    pressure_msl: float


class CityScheme(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float


class CityWeatherScheme(BaseModel):
    name: str
    temperature: Optional[float]
    relative_humidity: Optional[float]
    wind_speed: Optional[float]
    precipitation: Optional[float]
