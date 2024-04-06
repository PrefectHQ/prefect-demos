from prefect import flow
from re import L
from prefect import flow, task, unmapped
from prefect_aws.s3 import S3Bucket
from datetime import date, timedelta
from prefect.blocks.notifications import SlackWebhook
from datetime import timedelta
import pandas as pd
from io import StringIO
from pydantic import BaseModel
from data_ingestion import ingest_raw_customers
from snowflake_bocks import SnowflakeConnection
from prefect.tasks import task_input_hash, exponential_backoff
import time
from prefect_aws.s3 import S3Bucket
from prefect_kubernetes.jobs import KubernetesJob, KubernetesJobRun
from r_k8s_job import r_script_kubernetes_job, v1_job_model


@task(retries=10, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def list_s3_objects(s3_block_raw_data: S3Bucket):
    obj_dict = s3_block_raw_data.list_objects()
    objs = [obj_dict[i]["Key"] for i in range(len(obj_dict))]
    time.sleep(2)
    return objs


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=30))
def read_csv_to_df(s3_block_raw_data: S3Bucket, object_key):
    csv = s3_block_raw_data.read_path(object_key)
    df = pd.read_csv(StringIO(csv.decode("utf-8")))
    time.sleep(2)
    return df


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
    integrated = pd.concat([raw_df, historical_df])

    # Assert Column Format Matches Historical Data
    assert integrated.shape[1] == historical_df.shape[1]
    time.sleep(2)

    return integrated


@task(retries=3)
def get_geographical_data(block_name: str) -> None:
    connector = SnowflakeConnection.load(block_name, validate=False)
    new_rows = connector.read_sql("SELECT * FROM geo_data")
    time.sleep(2)


@task
def combine_geo_hist_data(geo_df, hist_df):
    print("Geographical data combined with historical data")
    combined = pd.DataFrame({"geo": geo_df, "hist": hist_df})
    time.sleep(3)
    return combined


@task(retries=3)
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


@flow
def load_in_historical_data():
    # Load in Block to Instantiate Block Object
    s3_block_historical_data = S3Bucket.load("raw-data-jaffle-shop")

    # First Task to list S3 objects
    s3_objs = list_s3_objects(s3_block_historical_data)

    # Initialize an empty dictionary to store DataFrames
    historical_dfs = {}

    # Loop through the object keys returned by list_s3_objects
    for obj in s3_objs[:-1]:  # Assuming you want to skip the last object for some reason
        # Submit the read_csv_to_df task for execution and immediately wait for its result
        df_future = read_csv_to_df.submit(s3_block_historical_data, obj)
        df = df_future.result()  # Wait for the future to resolve and get the DataFrame

        # Update the historical_dfs dictionary with the new DataFrame
        # Use the S3 object key without the '.csv' extension as the dictionary key
        key_without_csv = obj.rstrip(".csv")
        historical_dfs[key_without_csv] = df

    return historical_dfs



@flow(log_prints=True, result_storage=S3Bucket.load("result-storage"))
def data_cleaning_flow(
    start_date: date = date(2024, 2, 1),
    end_date: date = date.today(),
    risk_profile: RiskProfile = default_risk_profile,
):
    raw_customer_data = ingest_raw_customers.submit(risk_profile)

    null_counts = find_nulls_in_df.submit(raw_customer_data)

    if null_counts.result().sum() > 0:
        new_customer_data = imputation_task.submit(
            null_counts, 
            raw_customer_data
            )
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

    # Launch the Kubernetes job
    job_run = KubernetesJobRun(
        kubernetes_job=r_script_kubernetes_job, v1_job_model=v1_job_model
    )

    print(start_date, end_date)

    print("Done!")


if __name__ == "__main__":
    data_cleaning_flow()

    # data_cleaning_flow.deploy(
    #     name="k8s-deployment",
    #     work_pool_name="my-k8s-pool",
    #     image="docker.io/taycurran/data-cleaning2:demo2",
    #     push=False,
    #     tags=["data-cleaning", "proj-caraga"],
    #     cron="0 6,7,8,9,10 * * *",
    # )

    # data_cleaning_flow.deploy(
    #     name="triggered-deployment",
    #     work_pool_name="my-k8s-pool",
    #     image="docker.io/taycurran/data-cleaning:demo",
    #     push=False,
    #     triggers=[
    #         {
    #             "match_related": {"prefect.resource.name": "active-batch-webhook"},
    #             "expect": {"webhook.called"},
    #             "parameters": {
    #                 "start_date": "{{event.payload.start_date}}",
    #             },
    #         }
    #     ],
    # )
