# This module gathers all the weather data
# open-meteo.com makes this free and easy
# Do this OO for fun ig

import openmeteo_requests
from retry_requests import retry
from dataclasses import dataclass


@dataclass(frozen=True)
class Weather:
    maxtemp: float
    mintemp: float
    precipitation: float
    weather_code: int
    weather_text: str


WEATHER_CODES = {
    "0": "Clear sky",
    "1": "Mainly clear",
    "2": "Partly cloudy",
    "3": "Overcast",
    "45": "Fog",
    "48": "Depositing rime fog",
    "51": "Light drizzle",
    "53": "Moderate drizzle",
    "55": "Dense drizzle",
    "56": "Light freezing drizzle",
    "57": "Dense freezing drizzle",
    "61": "Slight rain",
    "63": "Moderate rain",
    "65": "Heavy rain",
    "66": "Light freezing rain",
    "67": "Heavy freezing rain",
    "71": "Slight snowfall",
    "73": "Moderate snowfall",
    "75": "Heavy snowfall",
    "77": "Snow grains",
    "80": "Slight rain showers",
    "81": "Moderate rain showers",
    "82": "Violent rain showers",
    "85": "Slight snow showers",
    "86": "Heavy snow showers",
    "95": "Thunderstorm",
    "96": "Thunderstorm with slight hail",
    "97": "Heavy thunderstorm",
    "99": "Thunderstorm with heavy hail",
}


def fetch(xcoordinate: float, ycoordinate: float):
    params = {
        "latitude": xcoordinate,
        "longitude": ycoordinate,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weather_code",
        ],
        "timezone": "America/Los_Angeles",
        "forecast_days": 1,
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }
    url = "https://api.open-meteo.com/v1/forecast"
    retry_session = retry()
    openmeteo = openmeteo_requests.Client(session=retry_session)  # pyright: ignore[reportArgumentType] This don't matter
    responses = openmeteo.weather_api(url, params=params)
    res = responses[0]
    daily = res.Daily()
    if not daily:
        raise ConnectionError("Not able to get data for the day from OpenMeteo")
    maxtemp, mintemp, precipitation_sum, weather_code = [
        daily.Variables(i).ValuesAsNumpy()[0]  # pyright: ignore[reportOptionalMemberAccess] Can't be bothered
        for i in range(daily.VariablesLength())
    ]
    return Weather(maxtemp=float(maxtemp), mintemp=float(mintemp), precipitation=float(precipitation_sum), weather_code=int(weather_code), weather_text=WEATHER_CODES[str(int(weather_code))])
