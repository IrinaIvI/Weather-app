from fastapi import APIRouter, Depends
from src.app.dao.dao_weather import (
    api_get_city, api_get_cities, api_get_actual_weather, api_add_city,
)
from src.app.dao.dao_user import api_registration
from src.app.schemas import ActualWeatherScheme, CityScheme, CityWeatherScheme, UserScheme
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.rb import RBCityWeather
from src.app.database import get_db
from typing import Annotated

router = APIRouter(prefix="/weather_app")


@router.get("/registation/", response_model=UserScheme)
async def registration(user_name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    response = await api_registration(user_name=user_name, db=db)
    return response


@router.get("/forecast/", response_model=ActualWeatherScheme)
async def get_actual_weather(latitude: float, longitude: float):
    response = await api_get_actual_weather(
        latitude=latitude,
        longitude=longitude
    )
    return response


@router.post("/added_new_city")
async def add_city(
    user_id: int,
    city_name: str,
    latitude: float,
    longitude: float,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await api_add_city(
        user_id=user_id, city_name=city_name, latitude=latitude, longitude=longitude, db=db
    )


@router.get("/cities", response_model=list[CityScheme])
async def get_cities(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await api_get_cities(user_id=user_id, db=db)
    return result


@router.get("/weather/{city_name}/{time}", response_model=CityWeatherScheme)
async def get_city(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    request_body: RBCityWeather = Depends(),
):
    result = await api_get_city(user_id=user_id, request_body=request_body, db=db)
    return result
