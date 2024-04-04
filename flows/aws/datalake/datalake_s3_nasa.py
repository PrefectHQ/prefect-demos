import httpx
import json
import pendulum
import time
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect.blocks.system import Secret
from prefect_aws import S3Bucket



#Get starting date
@task()
def get_time_frame(n_days: int):
        today = pendulum.now().to_date_string()
        end_date = pendulum.now().add(days=n_days).to_date_string()
        time.sleep(5)
        return today, end_date

#Retrieve a list of asteroids based on their closest approach date to Earth.
#Caching is used here to avoid hitting the API if the same date range is used.
@task(cache_key_fn=task_input_hash, retries=5)
def neo_feed_request(start_date, end_date):
    secret_block = Secret.load("nasa-api-key")
    nasa_api_key = secret_block.get()
    base_url = f"""https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={nasa_api_key}"""

    request_result = httpx.get(
        base_url
    )
    request_result.raise_for_status()

    neo_result = request_result.json()
    return neo_result

#Write NEO data to a json file in designated location
@task()
def write_to_file(neo_result, file_location, date):
    time.sleep(5)
    neo_result_formatted = json.dumps(neo_result, indent=4, sort_keys=True)
    se_dev_bucket = S3Bucket.load("webhook-test-se-dev")
    
    with open(f"./neo_result.json", 'w') as outfile:
        outfile.write(neo_result_formatted)
        pass
    se_dev_bucket.upload_from_path(f"./neo_result.json", f"{file_location}/{date}-neo_result.json")

#First child flow:
@flow(retries=3)
def write_transform_load(neo_result, file_location):
    write_to_file(neo_result, file_location)

#Parent Flow
@flow(log_prints=True)
def fetch_neo_by_date(n_days: int = 1, file_location: str = "RAW_DATA"):
    time_frame = get_time_frame(n_days)
    neos = neo_feed_request(time_frame[0], time_frame[1])
    print("I'm writing the file now!!!")
    write_to_file(neos, file_location, time_frame[0])

if __name__ == "__main__":
    fetch_neo_by_date()