from flows3 import pipe3
from prefect.infrastructure import Process
from prefect.deployments import Deployment

infra = Process.load("dev")

deploy = Deployment.build_from_flow(flow=pipe3, name="process", infrastructure=infra)

if __name__ == "__main__":
    deploy.apply()
