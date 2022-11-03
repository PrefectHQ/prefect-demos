import httpx  # requests capability, but can work with async
from prefect import flow, task
import random

# adds retries to task


@task
def fetch_weather(lat: float, lon: float):
    """get weather data"""
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp


@task
def save_weather(temp: float):
    buggy_saving = random.choice([True, False])
    if buggy_saving:
        raise Exception("API Failure. 😢")
    with open("weather.csv", "w+") as w:
        w.write(str(temp))
    return "Successfully wrote temp"


@flow(retries=2)
def pipeline(lat: float, lon: float):
    temp = fetch_weather(lat, lon)
    result = save_weather(temp)
    return result


if __name__ == "__main__":
    pipeline(38.9, -77.0)
