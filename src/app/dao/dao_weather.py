from fastapi import HTTPException, Depends
from httpx import AsyncClient
from src.app.schemas import ActualWeatherScheme, CityScheme, CityWeatherScheme
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import City, Weather
from sqlalchemy.future import select
from src.app.rb import RBCityWeather
from src.app.database import async_session
from sqlalchemy import func, delete
from src.app.scheduler import async_scheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from src.app.dao.dao_user import exist_user

URL = "https://api.open-meteo.com/v1/forecast?"


async def fetch_weather_data(latitude: float, longitude: float) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "precipitation",
            "relative_humidity_2m",
            "pressure_msl"
        ],
    }
    async with AsyncClient() as client:
        response = await client.get(url=URL, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Не удалось загрузить данные из API"
        )

    return response.json()


async def delete_old_weather_report():
    async with async_session() as db:
        yesterday = datetime.now() - timedelta(days=1)
        query = delete(Weather).where(func.date(Weather.updated_at) == yesterday)
        await db.execute(query)
        await db.commit()

async_scheduler.add_job(delete_old_weather_report, CronTrigger(hour=0, minute=0))


async def api_get_actual_weather(
    latitude: float, longitude: float
) -> ActualWeatherScheme:
    response = await fetch_weather_data(latitude=latitude, longitude=longitude)

    return ActualWeatherScheme(
        temperature=response["current"]["temperature_2m"],
        wind_speed=response["current"]["wind_speed_10m"],
        pressure_msl=response["current"]["pressure_msl"],
    )


async def update_weather_params(
    city_name: str, latitude: float, longitude: float
):
    async with async_session() as db:
        query = await db.execute(select(City).filter(City.name == city_name))
        city = query.scalars().first()
        response = await fetch_weather_data(latitude, longitude)

        new_weather_report = Weather(
            city_id=city.id,
            temperature=response["current"]["temperature_2m"],
            relative_humidity=response["current"]["relative_humidity_2m"],
            wind_speed=response["current"]["wind_speed_10m"],
            precipitation=response["current"]["precipitation"],
            updated_at=datetime.now()
        )

        db.add(new_weather_report)
        await db.commit()
        await db.refresh(new_weather_report)


async def api_add_city(
    city_name: str, latitude: float, longitude: float, user_id: int, db: AsyncSession
):
    user = await exist_user(user_id=user_id, db=db)
    query = await db.execute(select(City).filter(City.name == city_name))
    city = query.scalars().first()

    if city:
        raise HTTPException(status_code=404, detail="Данный город уже есть в БД")

    response = await fetch_weather_data(latitude, longitude)

    new_city = City(
        name=city_name,
        user_id=user.id,
        latitude=latitude,
        longitude=longitude,
    )

    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)

    city_weather = Weather(
        city_id=new_city.id,
        temperature=response["current"]["temperature_2m"],
        relative_humidity=response["current"]["relative_humidity_2m"],
        wind_speed=response["current"]["wind_speed_10m"],
        precipitation=response["current"]["precipitation"],
        updated_at=datetime.now()
    )
    db.add(city_weather)
    await db.commit()
    await db.refresh(city_weather)

    async_scheduler.add_job(
        update_weather_params,
        trigger=IntervalTrigger(minutes=15),
        args=[city_name, latitude, longitude],
        id=f'update_weather_{city_name}',
        replace_existing=True,
    )


async def api_get_cities(user_id: int, db: AsyncSession) -> list[CityScheme]:
    user = await exist_user(user_id=user_id, db=db)

    query = await db.execute(select(City).filter(City.user_id == user.id))
    cities = query.scalars().all()

    if not cities:
        raise HTTPException(status_code=400, detail="Доступные города отсутствуют")

    cities = [
        CityScheme(
            id=city.id, name=city.name, latitude=city.latitude, longitude=city.longitude
        )
        for city in cities
    ]

    return cities


async def api_get_city(
    db: AsyncSession, user_id: int, request_body: RBCityWeather = Depends()
) -> CityWeatherScheme:
    user = await exist_user(user_id=user_id, db=db)
    query = await db.execute(select(City).filter(
        City.name == request_body.city_name,
        City.user_id == user_id)
    )
    city = query.scalars().first()
    if not city:
        raise HTTPException(status_code=400, detail="Данный город не найден")

    weather_query = await db.execute(
        select(Weather).filter(Weather.city_id == city.id)
    )
    weather = weather_query.scalars().first()
    time_with_data = datetime.combine(datetime.now().date(), request_body.actual_time)
    if abs(weather.updated_at - time_with_data) >= timedelta(minutes=15):
        raise HTTPException(status_code=404, detail="Актуальных данных нет")

    return CityWeatherScheme(
        name=request_body.city_name,
        temperature=weather.temperature if request_body.temperature else None,
        relative_humidity=(
            weather.relative_humidity if request_body.relative_humidity else None
        ),
        wind_speed=weather.wind_speed if request_body.wind_speed else None,
        precipitation=weather.precipitation if request_body.precipitation else None,
    )
