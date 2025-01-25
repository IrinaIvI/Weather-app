from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from rb import RBCityWeather
from dao_weather import (
    api_get_city,
    api_get_cities,
    api_get_actual_weather,
    api_add_city,
)
from dao_user import api_registration
from schemas import (
    ActualWeatherSchemeResponse,
    UserSchemeRequest,
    CitySchemeResponse,
    CityWeatherSchemeResponse,
    CitySchemeRequest,
    UserSchemeResponse,
    ActualWeatherSchemeRequest,
)
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from typing import Annotated

router = APIRouter(prefix="/weather_app")


@router.post("/registration/", response_model=UserSchemeResponse)
async def registration(
    request_body: UserSchemeRequest, db: Annotated[AsyncSession, Depends(get_db)]
):
    response = await api_registration(request_body=request_body, db=db)
    return response


@router.post("/forecast/", response_model=ActualWeatherSchemeResponse)
async def get_actual_weather(request_body: ActualWeatherSchemeRequest):
    response = await api_get_actual_weather(request_body=request_body)
    return response


@router.post("/added_new_city")
async def add_city(
    request_body: CitySchemeRequest, db: Annotated[AsyncSession, Depends(get_db)]
) -> JSONResponse:
    response = await api_add_city(request_body=request_body, db=db)
    return response


@router.get("/cities", response_model=list[CitySchemeResponse])
async def get_cities(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await api_get_cities(user_id=user_id, db=db)
    return result


@router.get("/weather/{city_name}/{time}", response_model=CityWeatherSchemeResponse)
async def get_city(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    request_body: RBCityWeather = Depends(),
):
    result = await api_get_city(user_id=user_id, request_body=request_body, db=db)
    return result
