from flows import pipe
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import RRuleSchedule

rr = RRuleSchedule(rrule="FREQ=HOURLY;UNTIL=20300102T040000Z", timezone="Asia/Kolkata")
deployment = Deployment.build_from_flow(
    flow=pipe,
    name="RRule Scheduled Deployment",
    schedule=rr,
)

if __name__ == "__main__":
    deployment.apply()
