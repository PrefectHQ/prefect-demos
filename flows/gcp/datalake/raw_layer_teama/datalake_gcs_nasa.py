import json
import time
import os

import httpx
import pendulum
from prefect import flow, task, deploy
from prefect.assets import materialize, Asset
from prefect.blocks.system import Secret
from prefect_gcp import GcsBucket

from prefect.client.schemas.schedules import CronSchedule

schedules_active = os.getenv("SCHEDULES_ACTIVE", "False")


# Get starting date
@task()
def get_time_frame(n_days: int):
    today = pendulum.now().to_date_string()
    end_date = pendulum.now().add(days=n_days).to_date_string()
    time.sleep(5)
    return today, end_date


# Retrieve a list of asteroids based on their closest approach date to Earth.
@materialize(Asset(key="local://neo-result.json"),retries=5)
def neo_feed_request(start_date, end_date):
    secret_block = Secret.load("nasa-api-key")
    nasa_api_key = secret_block.get()
    base_url = f"""https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={nasa_api_key}"""

    request_result = httpx.get(base_url)
    request_result.raise_for_status()

    neo_result = request_result.json()

    return neo_result


# Write NEO data to a json file in designated location
@materialize(Asset(key="gcs://RAW_DATA/neo_result.json"))
def write_to_file(neo_result, file_location, date):
    time.sleep(5)
    neo_result_formatted = json.dumps(neo_result, indent=4, sort_keys=True)
    shared_bucket = GcsBucket.load("shared-team-bucket")
    

    with open("./neo_result.json", "w") as outfile:
        outfile.write(neo_result_formatted)
        pass
    shared_bucket.upload_from_path(
        "./neo_result.json", f"{file_location}/{date}-neo_result.json"
    )


# First child flow:
@flow(retries=3)
def write_transform_load(neo_result, file_location):
    write_to_file(neo_result, file_location)


# Parent Flow
@flow(log_prints=True)
def fetch_neo_by_date(n_days: int = 1, file_location: str = "RAW_DATA"):
    time_frame = get_time_frame(n_days)
    neos = neo_feed_request(time_frame[0], time_frame[1])
    print("I'm writing the file now!!!")
    write_to_file(neos, file_location, time_frame[0])


if __name__ == "__main__":
    # fetch_neo_by_date()
    fetch_neo_by_date_deployment = fetch_neo_by_date.from_source(
        source="./flows/gcp/datalake/raw_layer_teama/",
        entrypoint="datalake_gcs_nasa.py:fetch_neo_by_date"
    ).to_deployment(
        name="gcs_nasa_fetch",
        schedules=[
            {
                "schedule": CronSchedule(cron="0 10 * * *"),
                "active": schedules_active,
            }
        ],
    )

    deploy(
        fetch_neo_by_date_deployment,
        work_pool_name="project2"
    )
