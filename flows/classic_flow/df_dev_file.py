from re import L
from prefect import flow, task, unmapped
from prefect_aws.s3 import S3Bucket
from datetime import date, timedelta
from prefect.orion.schemas.states import Completed, Failed
from prefect.blocks.notifications import SlackWebhook
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect import tags
import os
import random
import pandas as pd
from io import StringIO

# subflows
# looping
# if statement
# run_deployment
# query snowflake (1 simple pre-built task)

def list_s3_objects(s3_block_raw_data: S3Bucket):
    obj_dict = s3_block_raw_data.list_objects()
    objs = [obj_dict[i]["Key"] for i in range(len(obj_dict))]

    return objs

def read_csv_to_df(s3_block_raw_data: S3Bucket, object_key):

    csv = s3_block_raw_data.read_path(object_key)
    df = pd.read_csv(StringIO(csv.decode("utf-8")))

    return df

def main_flow(
        start_date: date = date(2020, 2, 1),
        end_date: date = date.today(),
        risk_level: int = 0
):
    # Load in Block to Instantiate Block Object
    s3_block_raw_data = S3Bucket.load("raw-data-jaffle-shop")

    # First Task
    s3_objs = list_s3_objects(s3_block_raw_data)

    dfs = {}
    for i in range(len(s3_objs)):
        dfs.update({s3_objs[i].rstrip('.csv'): read_csv_to_df(s3_block_raw_data, s3_objs[i])})

    ['jaffle_shop_customer', 'jaffle_shop_order', 'stripe_payment']

    breakpoint()

    print(dfs)

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

if __name__ == "__main__":
    main_flow()