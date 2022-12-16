from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket
from prefect.filesystems import GitHub

from dotenv import load_dotenv
import os

# -- env vars --
load_dotenv()
aws_staging_access_key_id = os.environ.get("AWS_STAGING_ACCESS_KEY_ID")
aws_staging_secret_access_key = os.environ.get("AWS_STAGING_SECRET_ACCESS_KEY")

# -- aws --

aws_creds = AwsCredentials(
    aws_access_key_id=aws_staging_access_key_id,
    aws_secret_access_key=aws_staging_secret_access_key)

aws_creds.save('se-aws-creds', overwrite=True)

s3_bucket = S3Bucket(
        bucket_name="se-demo-result-storage",
        aws_credentials=aws_creds,
        basepath="development"
    )
s3_bucket.save('result-storage', overwrite=True)

s3_bucket = S3Bucket(
        bucket_name="se-demo-flow-code-store",
        aws_credentials=aws_creds,
        basepath="development"
    )
s3_bucket.save('flow-code-storage', overwrite=True)

s3_bucket = S3Bucket(
        bucket_name="dbt-tutorial-public",
        aws_credentials=aws_creds,
        endpoint_url="s3://dbt-tutorial-public/"
    )
s3_bucket.save('raw-data-jaffle-shop', overwrite=True)

print('Development Blocks Created or Edited!')