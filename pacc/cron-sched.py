from flows import pipe
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule

cr = CronSchedule(cron="3 3 3 3 2", timezone="America/Chicago")

deployment = Deployment.build_from_flow(
    flow=pipe,
    name="Cron Scheduled Deployment",
    schedule=cr,
)

if __name__ == "__main__":
    deployment.apply()
