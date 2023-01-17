from re import L
from prefect import flow, task, unmapped
from prefect_aws.s3 import S3Bucket
from datetime import date, timedelta
from prefect.orion.schemas.states import Completed, Failed
from prefect.task_runners import ConcurrentTaskRunner
from prefect.blocks.notifications import SlackWebhook
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect import tags
import os
import random
import pandas as pd
from io import StringIO
from pydantic import BaseModel
from data_ingestion import ingest_raw_customers
import time

# subflows
# looping
# if statement
# run_deployment
# query snowflake (1 simple pre-built task)
# cyclical logic
# retries

# cashing
# Use time.sleep() in a caching task

@task
def list_s3_objects(s3_block_raw_data: S3Bucket):
    obj_dict = s3_block_raw_data.list_objects()
    objs = [obj_dict[i]["Key"] for i in range(len(obj_dict))]

    return objs

@task
def read_csv_to_df(s3_block_raw_data: S3Bucket, object_key):

    csv = s3_block_raw_data.read_path(object_key)
    df = pd.read_csv(StringIO(csv.decode("utf-8")))

    return df

@task
def find_nulls_in_df(df):
    null_counts = df.isna().sum()
    return null_counts

@task
def imputation_task(null_count, df):
    imputed_df = df.fillna('Jane')
    return imputed_df 

@task
def historical_raw_integration(historical_df, raw_df):
    integrated = pd.concat([raw_df, historical_df])

    # Assert Column Format Matches Historical Data
    assert integrated.shape[1] == historical_df.shape[1]

    return integrated

@task
def column_detection(imputed_df):
    imputed_df.columns = ['ID', 'FIRST_NAME', 'LAST_NAME']
    return imputed_df

@task
def upload_combined_data(final_df):
    print('Uploading')
    return 'Good'

# my pydantic class
class RiskProfile(BaseModel):
    nulls: bool = False
    api_failure: bool = False
    integration_failure: bool = False

default_risk_profile = RiskProfile(
    nulls=False, 
    api_failure=False,
    integration_failure=False
    )

@flow
def load_in_historical_data():
    # Load in Block to Instantiate Block Object
    s3_block_historical_data = S3Bucket.load("raw-data-jaffle-shop")

    # First Task
    s3_objs = list_s3_objects(s3_block_historical_data)

    # Submitting Task 
    historical_dfs = {}
    for i in range(len(s3_objs) - 1):
        historical_dfs.update({
            s3_objs[i].rstrip('.csv'): 
            read_csv_to_df.submit(s3_block_historical_data, s3_objs[i])
            })
    
    return historical_dfs


@flow(task_runner=ConcurrentTaskRunner())
def main_flow(
        start_date: date = date(2020, 2, 1),
        end_date: date = date.today(),
        risk_profile: RiskProfile = default_risk_profile
):

    raw_customer_data = ingest_raw_customers(risk_profile)

    null_counts = find_nulls_in_df(raw_customer_data)

    if null_counts.sum() > 0:
        new_customer_data = imputation_task(null_counts, raw_customer_data)
    else:
        new_customer_data = raw_customer_data
    
    # Combine with historical data
    historical_dfs = load_in_historical_data()

    combined = historical_raw_integration(
        historical_dfs['jaffle_shop_customer'], 
        new_customer_data, 
        return_state=True)

    if combined.is_failed():
        print('hiiii tay')
        new_raw = column_detection(new_customer_data)
    
        # Retry Combined Task with Fixed Raw File
        combined = historical_raw_integration(
            historical_dfs['jaffle_shop_customer'], 
            new_raw, 
            return_state=True)

    upload_combined_data(combined)

    print(combined.result().tail())

    print("Done!")


    
    

    

 

#     ['jaffle_shop_customer', 'jaffle_shop_order', 'stripe_payment']

#     #   Customer
# ---  ------      --------------  ----- 
#  0   ID          100 non-null    int64 
#  1   FIRST_NAME  100 non-null    object
#  2   LAST_NAME   100 non-null    object

#     #   Orders
# ---  ------      --------------  ----- 
#  0   ID          99 non-null     int64 
#  1   USER_ID     99 non-null     int64 
#  2   ORDER_DATE  99 non-null     object
#  3   STATUS      99 non-null     object

#     #   Payments   
# ---  ------         --------------  ----- 
#  0   ID             120 non-null    int64 
#  1   ORDERID        120 non-null    int64 
#  2   PAYMENTMETHOD  120 non-null    object
#  3   STATUS         120 non-null    object
#  4   AMOUNT         120 non-null    int64 
#  5   CREATED        120 non-null    object

 #   Column      Non-Null Count  Dtype 

if __name__ == "__main__":
    main_flow()
