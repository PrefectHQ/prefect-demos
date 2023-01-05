from re import L
from prefect import task, flow
from prefect_aws.s3 import S3Bucket
from prefect.orion.schemas.states import Completed, Failed
from prefect.blocks.notifications import SlackWebhook
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect import tags
import os
import random
import pandas as pd
from io import StringIO


@task
def read_in_raw_data():

    s3_raw_data_bucket = S3Bucket.load("raw-data-jaffle-shop")
    csv_contents = s3_raw_data_bucket.read_path("jaffle_shop_customers.csv")
    df = pd.read_csv(StringIO(csv_contents.decode("utf-8")))

    return df

def get_row_count(df):
    print(df.shape[0])

@flow(retries=2, retry_delay_seconds=30)
def main_flow(
        start_date: date = date(2020, 2, 1),
        end_date: date = date.today(),
):
    read_in_raw_data()


if __name__ == "__main__":
    main_flow()
