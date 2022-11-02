from prefect.filesystems import S3

s3_block = S3.load("s3-dev")
print(s3_block)
