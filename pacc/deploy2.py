from flows import pipe
from prefect.deployments import Deployment

deploy = Deployment.build_from_flow(
    flow=pipe,
    name="Python Deploy file",
)

if __name__ == "__main__":
    deploy.apply()
