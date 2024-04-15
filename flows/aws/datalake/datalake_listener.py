import csv
import json

from prefect import flow, task
from prefect_aws import S3Bucket


@task
def flatten_near_earth_object(object: dict):
    """
    Flatten this object and only choose one unit of measurement for each set of nested measurements
    """

    flat_object = {
        "absolute_magnitude_h": object["absolute_magnitude_h"],
        "is_potentially_hazardous_asteroid": object[
            "is_potentially_hazardous_asteroid"
        ],
        "is_sentry_object": object["is_sentry_object"],
        "name": object["name"],
        "nasa_jpl_url": object["nasa_jpl_url"],
        "neo_reference_id": object["neo_reference_id"],
    }

    close_approach_data = object["close_approach_data"][0]
    flat_object.update(
        {
            "close_approach_date": close_approach_data["close_approach_date"],
            "close_approach_date_full": close_approach_data["close_approach_date_full"],
            "epoch_date_close_approach": close_approach_data[
                "epoch_date_close_approach"
            ],
            "miss_distance_kilometers": close_approach_data["miss_distance"][
                "kilometers"
            ],
            "orbiting_body": close_approach_data["orbiting_body"],
            "relative_velocity_kilometers_per_hour": close_approach_data[
                "relative_velocity"
            ]["kilometers_per_hour"],
        }
    )

    estimated_diameter = object["estimated_diameter"]["kilometers"]
    flat_object.update(
        {
            "estimated_diameter_max_kilometers": estimated_diameter[
                "estimated_diameter_max"
            ],
            "estimated_diameter_min_kilometers": estimated_diameter[
                "estimated_diameter_min"
            ],
        }
    )

    return flat_object


@flow
def datalake_listener(bucket: str, key: str):
    s3_bucket_block: S3Bucket = S3Bucket.load(bucket)

    near_earth_objects_by_date = json.loads(s3_bucket_block.read_path(key))

    file_name = key.split("/")[-1]

    date = file_name[:10]
    near_eath_objects = near_earth_objects_by_date["near_earth_objects"][date]

    hazardous_objects = [
        obj for obj in near_eath_objects if obj["is_potentially_hazardous_asteroid"]
    ]

    flattened_objs = [flatten_near_earth_object(obj) for obj in hazardous_objects]

    if hazardous_objects:
        writer = csv.DictWriter(
            open("hazardous_objects.csv", "w"), flattened_objs[0].keys()
        )
        writer.writeheader()
        writer.writerows(flattened_objs)

        s3_bucket_block.upload_from_path(
            "hazardous_objects.csv",
            f"{date}_hazardous_objects_by_date/hazardous_objects.csv",
        )

    else:
        print("No hazardous objects today!")
