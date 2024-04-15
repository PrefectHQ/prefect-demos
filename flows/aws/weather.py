"""A flow for efficiently fetching the weather in multiple locations"""
import httpx
from prefect import flow, get_run_logger, task
from prefect.tasks import task_input_hash
from prefect_aws.s3 import S3Bucket

# TODO: use a Pydantic class
# TODO: fill in coordinates
CITIES = {
    "New York, NY": (),
    "Chicago, IL": (),
    "San Franciso, CA": (),
}

# TODO: Handle instantiation
STORAGE = S3Bucket.load("result-storage")


@task(
    cache_key_fn=task_input_hash,
    result_storage=STORAGE,
    persist_result=True,
    retries=3,
)
def fetch_temperature_for_coordinates(latitude: float, longitude: float):
    resp = httpx.get(
        "https://api.open-meteo.com/v1/forecast/",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m",
        },
    )
    temperature = float(resp.json()["hourly"]["temperature_2m"][0])
    return temperature


# TODO: this is untested... no idea if it works yet
@flow
def report_weather(cities: dict[str, tuple[int, int]] = CITIES) -> None:
    # Fetch temperatures concurrently
    temperatures = fetch_temperature_for_coordinates.map(cities.values())

    # Log each temperature
    for city, temperature in zip(cities.keys(), temperatures):
        get_run_logger().info(f"The current temperature in {city} is {temperature}")


if __name__ == "__main__":
    report_weather()
