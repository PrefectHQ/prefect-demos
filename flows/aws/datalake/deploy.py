import os

from datalake_listener import datalake_listener
from datalake_s3_nasa import fetch_neo_by_date
from prefect import deploy
from prefect.client.schemas.schedules import CronSchedule
from prefect.deployments import DeploymentImage
from prefect.events import DeploymentEventTrigger

ecr_repo = os.getenv("IMG_REPO")
image_tag = os.getenv("GITHUB_SHA")
work_pool_name = os.getenv("WORK_POOL_NAME")
schedules_active = os.getenv("SCHEDULES_ACTIVE")

datalake_listener_deployment = datalake_listener.to_deployment(
    name="datalake_listener",
    triggers=[
        DeploymentEventTrigger(
            # several DeploymentTrigger fields have defaults and are omitted
            name="S3 Object Created",
            match={"prefect.resource.id": "aws.s3.*"},
            expect=["com.amazonaws.s3.Object Created"],
            parameters={
                "bucket": "{{ event.payload.data.bucket.name }}",
                "key": "{{ event.payload.data.object.key }}",
            },
        )
    ],
)

fetch_neo_by_date_deployment = fetch_neo_by_date.to_deployment(
    name="s3_nasa_fetch",
    schedules=[
        {
            "schedule": CronSchedule(cron="0 10 * * *"),
            "active": schedules_active,
        }
    ],
)

deploy(
    datalake_listener_deployment,
    fetch_neo_by_date_deployment,
    image=DeploymentImage(
        name=f"{ecr_repo}/datalake-demo",
        tag=image_tag,
        dockerfile="Dockerfile",
    ),
    work_pool_name=work_pool_name,
)
