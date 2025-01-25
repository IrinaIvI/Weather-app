from pydantic import BaseModel, field_validator
from typing import Optional


def validate_latitude_func(latitude: float) -> float:
    if not (-90 <= latitude <= 90):
        raise ValueError(
            f"Неверная широта: {latitude}. Должна быть в пределах от -90 до 90."
        )
    return latitude


def validate_longitude_func(longitude: float) -> float:
    if not (-180 <= longitude <= 180):
        raise ValueError(
            f"Неверная долгота: {longitude}. Должна быть в пределах от -180 до 180."
        )
    return longitude


def validate_city_name_func(name: str) -> str:
    if not name.isalpha() or not name.istitle():
        raise ValueError(
            f"Неверное название города: {name}. Название должно начинаться с заглавной буквы и содержать только буквы."
        )
    return name


def validate_user_name_func(name: str) -> str:
    if not name.isalpha() or not name.istitle():
        raise ValueError(
            f"Неверное имя: {name}. Имя должно начинаться с заглавной буквы и содержать только буквы."
        )
    return name


class ActualWeatherSchemeResponse(BaseModel):
    temperature: float
    wind_speed: float
    pressure_msl: float


class ActualWeatherSchemeRequest(BaseModel):
    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, latitude: float) -> float:
        return validate_latitude_func(latitude=latitude)

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, longitude: float) -> float:
        return validate_longitude_func(longitude=longitude)


class CitySchemeResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float


class CitySchemeRequest(BaseModel):
    name: str
    user_id: int
    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, latitude: float) -> float:
        return validate_latitude_func(latitude=latitude)

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, longitude: float) -> float:
        return validate_longitude_func(longitude=longitude)

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        return validate_city_name_func(name=name)


class CityWeatherSchemeResponse(BaseModel):
    name: str
    temperature: Optional[float]
    relative_humidity: Optional[float]
    wind_speed: Optional[float]
    precipitation: Optional[float]


class UserSchemeResponse(BaseModel):
    id: int


class UserSchemeRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        return validate_user_name_func(name=name)
