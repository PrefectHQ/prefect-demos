from flows import pipe
from prefect.deployments import Deployment
from prefect.filesystems import S3

s3 = S3.load("s3-dev")

deploy = Deployment.build_from_flow(
    flow=pipe,
    name="S3 Example",
    storage=s3,
)

if __name__ == "__main__":
    deploy.apply()
