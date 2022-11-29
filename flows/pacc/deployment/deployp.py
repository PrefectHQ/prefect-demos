from prefect.deployments import Deployment
from weatherflow import fetch_weather

deploy = Deployment.build_from_flow(
    flow=fetch_weather,
    name="Python deploy file with params",
    parameters={"lat": 22, "lon": 50},
)

if __name__ == "__main__":
    deploy.apply()
