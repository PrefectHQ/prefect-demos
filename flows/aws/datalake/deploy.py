import os

from prefect import deploy
from prefect.deployments import DeploymentImage
from prefect.events import DeploymentEventTrigger

from prefect.deployments.runner import DeploymentImage 
from prefect.client.schemas.schedules import CronSchedule

from datalake_listener import datalake_listener
from datalake_s3_nasa import fetch_neo_by_date

ecr_repo = os.getenv("ECR_REPO")
image_tag = os.getenv("GITHUB_SHA")

fetch_neo_by_date.deploy(
    name="s3_nasa_fetch",
    schedule=CronSchedule(cron="0 10 * * *"),
    image=DeploymentImage(
        name=f"{ecr_repo}/datalake-demo",
        tag=image_tag,
        dockerfile="Dockerfile",
    ),
    work_pool_name="Demo-ECS"
)

datalake_listener.deploy(
    name="datalake_listener",
    triggers=[
        DeploymentEventTrigger(
            # several DeploymentTrigger fields have defaults and are omitted
            name = "S3 Object Created",
            match = {"prefect.resource.id": "aws.s3.*"},
            expect = ["com.amazonaws.s3.Object Created"],
            parameters = {"bucket": "{{ event.payload.data.bucket.name }}", "key": "{{ event.payload.data.object.key }}"},
        )
    ],
    build=False,
    image=f"{ecr_repo}/datalake-demo:{image_tag}",
    work_pool_name="Demo-ECS"
)
