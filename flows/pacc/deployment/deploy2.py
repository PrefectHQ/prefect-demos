from prefect.deployments import Deployment

from flows import pipe

deploy = Deployment.build_from_flow(
    flow=pipe,
    name="Python Deploy file",
)

if __name__ == "__main__":
    deploy.apply()
