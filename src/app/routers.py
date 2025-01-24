from fastapi import APIRouter, Depends
from dao import (
    api_get_city,
    api_get_cities,
    api_get_actual_weather,
    api_add_city
)
from schemas import ActualWeatherScheme, CityScheme, CityWeatherScheme
from sqlalchemy.ext.asyncio import AsyncSession
from rb import RBCityWeather
from database import get_db
from typing import Annotated

router = APIRouter(prefix="/weather_app")


@router.get("/forecast/", response_model=ActualWeatherScheme)
async def get_actual_weather(latitude: float, longitude: float):
    response = await api_get_actual_weather(
        latitude=latitude,
        longitude=longitude
    )
    return response


@router.post("/added_new_city")
async def add_city(
    city_name: str,
    latitude: float,
    longitude: float,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await api_add_city(
        city_name=city_name, latitude=latitude, longitude=longitude, db=db
    )


@router.get("/cities", response_model=list[CityScheme])
async def get_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await api_get_cities(db=db)
    return result


@router.get("/weather/{city_name}/{time}", response_model=CityWeatherScheme)
async def get_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    request_body: RBCityWeather = Depends(),
):
    result = await api_get_city(request_body=request_body, db=db)
    return result
