from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket

from dotenv import load_dotenv
import os

# -- env vars --
load_dotenv()
aws_staging_access_key_id = os.environ.get("AWS_STAGING_ACCESS_KEY_ID")
aws_staging_secret_access_key = os.environ.get("AWS_STAGING_SECRET_ACCESS_KEY")

# -- aws --

# TODO: Fix these

aws_creds = AwsCredentials(
    aws_access_key_id=aws_staging_access_key_id,
    aws_secret_access_key=aws_staging_secret_access_key)

aws_creds.save('se-aws-creds', overwrite=True)

s3_bucket = S3Bucket(
        bucket_name="se-demo-result-storage",
        aws_credentials=aws_creds,
        basepath="staging"
    )
s3_bucket.save('flow-cache', overwrite=True)

print('Staging Blocks Created or Edited!')
