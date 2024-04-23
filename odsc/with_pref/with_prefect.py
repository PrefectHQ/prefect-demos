from prefect import task, flow
from datetime import date, timedelta
import pandas as pd
from io import StringIO
from pydantic import BaseModel
from data_ingestion import ingest_raw_customers
from snowflake_blocks import SnowflakeConnection
from prefect.tasks import task_input_hash, exponential_backoff
import time
from prefect_aws.s3 import S3Bucket
from prefect.deployments import DeploymentImage


@task(retries=10, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def list_s3_objects(s3_block_raw_data: S3Bucket):
    objs = [
        "jaffle_shop_customers.csv",
        "jaffle_shop_orders.csv",
        "jaffle_shop_locations.csv",
    ]
    time.sleep(2)
    return objs


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=30))
def read_csv_to_df(s3_block_raw_data: S3Bucket, object_key):
    csv = s3_block_raw_data.read_path(object_key)
    df = pd.read_csv(StringIO(csv.decode("utf-8")))
    df_json = df.to_json()
    time.sleep(2)
    return df_json


@task
def find_nulls_in_df(df):
    null_counts = df.isna().sum()
    time.sleep(2)
    return null_counts


@task
def imputation_task(null_count, df):
    imputed_df = df.fillna("Jane")
    time.sleep(2)
    return imputed_df


@task
def historical_raw_integration(historical_df, raw_df):
    block_name = "historical-data"

    connector = SnowflakeConnection.load(block_name, validate=False)
    new_rows = connector.read_sql("SELECT * FROM geo_data")
    # integrated = pd.concat([raw_df, historical_df])

    # Assert Column Format Matches Historical Data
    # assert integrated.shape[1] == historical_df.shape[1]

    time.sleep(2)

    return new_rows


@task
def get_geographical_data(block_name: str) -> None:
    # block_name = "historical-data"
    connector = SnowflakeConnection.load(block_name, validate=False)
    new_rows = connector.read_sql("SELECT * FROM geo_data")
    time.sleep(2)

    return new_rows


@task
def combine_geo_hist_data(geo_df, hist_df):
    print("Geographical data combined with historical data")
    combined = pd.DataFrame(pd.DataFrame({"test": [1, 2, 3]}))
    time.sleep(3)
    return combined


@task
def column_detection(imputed_df):
    imputed_df.columns = ["ID", "FIRST_NAME", "LAST_NAME"]
    time.sleep(2)
    return imputed_df


@task
def upload_combined_data(final_df):
    print("Uploading")
    time.sleep(4)
    return "Good"


# my pydantic class
class RiskProfile(BaseModel):
    nulls: bool = False
    api_failure: bool = False
    integration_failure: bool = False


default_risk_profile = RiskProfile(
    nulls=False, api_failure=False, integration_failure=False
)


@flow()
def load_in_historical_data():
    # Load in Block to Instantiate Block Object
    s3_block_historical_data = S3Bucket.load("raw-data-jaffle-shop")

    for i in range(3):
        s3_objs = list_s3_objects.submit(s3_block_historical_data)

    historical_dfs = {
        "jaffle_shop_customer": pd.DataFrame(
            {
                "ID": [1, 2, 3],
                "FIRST_NAME": ["John", "Jane", "Jim"],
                "LAST_NAME": ["Doe", "Smith", "Johnson"],
            }
        ),
        "jaffle_shop_orders": pd.DataFrame(
            {
                "ID": [1, 2, 3],
                "ORDER": ["Pizza", "Burger", "Fries"],
                "PRICE": [10, 5, 3],
            }
        ),
        "jaffle_shop_locations": pd.DataFrame(
            {
                "ID": [1, 2, 3],
                "CITY": ["Houston", "Austin", "Dallas"],
                "STATE": ["TX", "TX", "TX"],
            }
        ),
    }

    return historical_dfs


from prefect import flow

@flow
def data_cleaning_flow(
    start_date: date = date(2020, 2, 1),
    end_date: date = date.today(),
    risk_profile: RiskProfile = default_risk_profile,
):
    raw_customer_data = ingest_raw_customers.submit(risk_profile)

    null_counts = find_nulls_in_df.submit(raw_customer_data)

    if null_counts.result().sum() > 0:
        new_customer_data = imputation_task.submit(null_counts, raw_customer_data)
    else:
        new_customer_data = raw_customer_data

    # Combine with historical data
    historical_dfs = load_in_historical_data()

    combined = historical_raw_integration.submit(
        historical_dfs["jaffle_shop_customer"],
        new_customer_data,
        return_state=True,
        wait_for=historical_dfs,
    )

    cities = get_geographical_data.submit("geo-data-warehouse")

    geo_hist = combine_geo_hist_data.submit(cities, historical_dfs, wait_for=[combined])

    if combined.is_failed():
        new_raw = column_detection.submit(new_customer_data)

        # Retry Combined Task with Fixed Raw File
        combined = historical_raw_integration.submit(
            historical_dfs["jaffle_shop_customer"], new_raw, return_state=True
        )

    combined_data = upload_combined_data.submit(geo_hist)

    return combined_data


if __name__ == "__main__":
    # data_cleaning_flow()

    data_cleaning_flow.deploy(
        name="ecs-deployment-odsc",
        work_pool_name="Demo-ECS",
        image=DeploymentImage(
            name="455346737763.dkr.ecr.us-east-2.amazonaws.com/data-cleaning-odsc:demo-odsc-1", platform="linux/amd64",),
        tags=["data-cleaning", "odsc"],
        interval=240
    )
