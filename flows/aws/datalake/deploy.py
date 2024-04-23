import os

from prefect import deploy
from prefect.deployments import DeploymentImage
from prefect.events import DeploymentEventTrigger

from prefect.deployments.runner import DeploymentImage
from prefect.client.schemas.schedules import CronSchedule

from datalake_listener import datalake_listener
from datalake_s3_nasa import fetch_neo_by_date

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
    schedule=CronSchedule(cron="0 10 * * *"),
)

ecr_repo = os.getenv("ECR_REPO")
image_tag = os.getenv("GITHUB_SHA")


deploy(
    datalake_listener_deployment,
    fetch_neo_by_date_deployment,
    image=DeploymentImage(
        name=f"{ecr_repo}/datalake-demo",
        tag=image_tag,
        dockerfile="Dockerfile",
    ),
    work_pool_name="Demo-ECS",
)
