from flows import pipe
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

gh = GitHub.load("gh-test")

deploy = Deployment.build_from_flow(
    flow=pipe,
    name="GH Python Deployment Example",
    storage=gh,
)


if __name__ == "__main__":
    deploy.apply()
