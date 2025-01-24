from datetime import time


class RBCityWeather:
    def __init__(
        self,
        city_name: str,
        actual_time: time,
        temperature: bool | None = None,
        relative_humidity: bool | None = None,
        wind_speed: bool | None = None,
        precipitation: bool | None = None,
    ):
        self.city_name = city_name
        self.actual_time = actual_time
        self.temperature = temperature
        self.relative_humidity = relative_humidity
        self.wind_speed = wind_speed
        self.precipitation = precipitation

    def to_dict(self) -> dict:
        data = {
            "city_name": self.city_name,
            "actual_time": self.actual_time,
            "temperature": self.temperature,
            "relative_humidity": self.relative_humidity,
            "wind_speed": self.wind_speed,
            "precipitation": self.precipitation,
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
