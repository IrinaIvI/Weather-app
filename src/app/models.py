from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, DATETIME
from datetime import datetime
from typing import Annotated

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "city"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    weather: Mapped["Weather"] = relationship("Weather", back_populates="city")


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int_pk]
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"), nullable=False
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    relative_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    precipitation: Mapped[float] = mapped_column(Float, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False)

    city: Mapped[list["City"]] = relationship("City", back_populates="weather")
