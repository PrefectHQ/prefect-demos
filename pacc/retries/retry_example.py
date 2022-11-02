import httpx  # requests capability, but can work with async
from prefect import flow, task
import random

# adds retries to task


@task(name="Fetch API", retries=3)
def fetch_generic(lat: float, lon: float):
    """get generic data"""
    code = random.choice([200, 400, 500])
    base_url = f"https://httpbin.org/status/{code}"
    response = httpx.get(base_url)
    response.raise_for_status()
    return response


@task
def save_generic(temp: float):
    buggy_saving = random.choice([True, False])
    if buggy_saving:
        raise Exception("API Failure. 😢")
    with open("generic.csv", "w+") as w:
        w.write(str(temp))
    return "Successfully wrote temp"


@flow(retries=2)
def pipeline(lat: float, lon: float):
    temp = fetch_generic(lat, lon)
    result = save_generic(temp)
    return result


if __name__ == "__main__":
    pipeline(38.9, -77.0)
