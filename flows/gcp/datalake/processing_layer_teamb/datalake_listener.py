import csv
import json

from prefect import deploy, flow, task
from prefect_gcp import GcsBucket
from prefect.assets import materialize, Asset

from prefect.events import DeploymentEventTrigger
from prefect.runner.storage import GitRepository



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

@materialize(Asset(key="gcs://PROCESSED_DATA/hazardous_objects.csv"))
def upload_csv(gcs_bucket_block: GcsBucket, date, flattened_objs):
    writer = csv.DictWriter(
            open("hazardous_objects.csv", "w"), flattened_objs[0].keys()
        )
    writer.writeheader()
    writer.writerows(flattened_objs)

    gcs_bucket_block.upload_from_path(
        "hazardous_objects.csv",
        f"PROCESSED_DATA/{date}_hazardous_objects/hazardous_objects.csv",
    )


@flow
def datalake_listener(bucket: str, key: str):
    gcs_bucket_block: GcsBucket = GcsBucket.load("shared-team-bucket")

    near_earth_objects_by_date = json.loads(gcs_bucket_block.read_path(key))

    file_name = key.split("/")[-1]

    date = file_name[:10]
    near_eath_objects = near_earth_objects_by_date["near_earth_objects"][date]

    hazardous_objects = [
        obj for obj in near_eath_objects if obj["is_potentially_hazardous_asteroid"]
    ]

    flattened_objs = [flatten_near_earth_object(obj) for obj in hazardous_objects]

    if hazardous_objects:
        upload_csv(
            gcs_bucket_block=gcs_bucket_block,
            date=date,
            flattened_objs=flattened_objs
        )

    else:
        print("No hazardous objects today!")


if __name__ == "__main__":
    # datalake_listener(key="RAW_DATA/2025-09-25-neo_result.json")
    datalake_listener_deployment = datalake_listener.from_source(
        source=GitRepository(
            url="https://github.com/PrefectHQ/prefect-demos.git",
            branch="prefect-3-update-gcp-ex"
        ),
        entrypoint="flows/gcp/datalake/processing_layer_teamb/datalake_listener.py:datalake_listener"
    ).to_deployment(
    name="datalake_listener",
    triggers=[
        DeploymentEventTrigger(
            # several DeploymentTrigger fields have defaults and are omitted
            name="GCS Object Created",
            match={"prefect.resource.id": "gcs.cloud.event.*", "key": "RAW_DATA/*"},
            expect=["gcs.object.created"],
            parameters={
                "bucket": "{{ event.resource.gcs_bucket }}",
                "key": "{{ event.resource.key }}",
            },
        )
    ],
    )

    deploy(
        datalake_listener_deployment,
        work_pool_name="mm2-project1",
        image="us-central1-docker.pkg.dev/prefect-sbx-sales-engineering/masonm2-supporttesting/mason_gcs_default:09262025.2",
        build=False,
        push=False
    )
