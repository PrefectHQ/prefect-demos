import httpx  # requests capability, but can work with async
from prefect import flow, task


@task(name="Fetch Weather", retries=2, retry_delay_seconds=10)
def fetch_weather(lat: float, lon: float):
    """get weather data"""
    # base_url = "https://api.open-meteo.com/v1/forecast/"
    # buggy_api_result = random.choice([True, False])
    # if buggy_api_result:
    #     raise Exception("API Failure. 😢")
    # weather = httpx.get(
    #     base_url,
    #     params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    # )
    # most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    # return most_recent_temp


@task(name="Save Weather", retries=3, retry_delay_seconds=3)
def save_weather(temp: float):
    with open("weather.csv", "w+") as w:
        w.write(str(temp))
    return "Successfully wrote temp"


@flow(name="Weather Flow")
def pipeline(lat: float, lon: float):
    temp = fetch_weather(lat, lon)
    if not temp:
        result = save_weather(temp)
    sub_flow()
    return result


@flow
def sub_flow():
    print("this is a subflow")


if __name__ == "__main__":
    pipeline(38.9, -77.0)
