from prefect import deploy
from prefect.deployments import DeploymentImage
from prefect.events.schemas import DeploymentTrigger

from datalake_listener import datalake_listener

datalake_listener_deployment = datalake_listener.to_deployment(
    name="datalake_listener",
    triggers=[
        DeploymentTrigger(
            # several DeploymentTrigger fields have defaults and are omitted
            name = "S3 Object Created",
            match = {"prefect.resource.id": "aws.s3.*"},
            expect = ["com.amazonaws.s3.Object Created"],
            parameters = {"bucket": "{{ event.payload.data.bucket.name }}", "key": "{{ event.payload.data.object.key }}"},
        )
    ],
)

deploy(
    datalake_listener_deployment,
    work_pool_name="<some-work-pool>",
    image=DeploymentImage(
        name="<some-stuff-here>/datalake-listener",
        tag="latest",
        dockerfile="Dockerfile",
    )
)