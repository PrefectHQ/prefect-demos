# prefect-demos
Welcome to our repository dedicated to showcasing a variety of Prefect demos. 

Here, you'll find an extensive collection of practical examples and workflows designed to demonstrate the versatility and power of Prefect as a modern data workflow automation tool. Whether you're new to Prefect or an experienced user seeking to enhance your workflow designs, this repository offers valuable insights and easy-to-follow examples. Dive into our demos to explore how Prefect seamlessly orchestrates complex data processes, ensuring efficient and reliable execution of your data tasks. 

Get inspired, learn best practices, and discover innovative ways to leverage Prefect in your data projects!

# Flows
We have broken down our flows into digestible one-off examples that can be easily plugged into your current implementation

### AWS
- [wave_data.py](flows/aws/wave_data.py)

    *Fetches wave height data via API, writes it to a file, reshapes it using pandas for analysis, and demonstrates Prefect's task caching and result storage capabilities using an AWS S3 bucket.*

- [weather.py](flows/aws/weather.py)

    *Showcases error handling, task retries, conditional flows, result caching, notification alerts, and integration with AWS S3 for result storage*

#### Datalake Usage
- [datalake_listener.py](flows/aws/datalake/datalake_listener.py)

    *Processes Near Earth Object (NEO) data from an AWS S3 bucket, filters for potentially hazardous objects, flattens the data structure, and then uploads the results back to S3 in CSV format*

- [datalake_s3_nasa.py](flows/aws/datalake/datalake_s3_nasa.py)

    *Retrieves Near Earth Object (NEO) data from NASA's API for a given timeframe, caches the request to avoid unnecessary API calls, and then uploads the data to an AWS S3 bucket*

- [deploy.py](flows/aws/datalake/deploy.py)

    *Automates the deployment of two Prefect workflows for data processing: `datalake_listener`, which triggers on AWS S3 object creation, and `fetch_neo_by_date`, which fetches Near Earth Object data daily, using a Docker image from an ECR repository for execution on an ECS push work pool*

### Dask
- [partition_example.py](flows/simple_flows/partition_examples.py)

    *Demostrates flexibility in deployment strategies with parallel and asynchronous data ingestion tasks for customers, payments, and orders within specified date ranges, utilizing Prefect with optional Dask for parallel execution

### Databricks
- [consumer_flow.py](flows/simple_flows/consumer_flow.py)
    
    *Dynamically scales Databricks resources based on the count of unprocessed blocks, utilizing random values to simulate resource and workload metrics, and executing shell commands as part of the scaling process*

### DBT
- [dbt_snowflake_flow.py](flows/dbt/dbt_snowflake_flow.py)

    *Integrates Airbyte sync for data extraction, DBT Cloud for transformation jobs, Great Expectations for data quality checks, and Snowflake queries, with Slack notifications for task failures.*


### Misc Flows
- [hello.py](flows/simple_flows/hello.py)
    
    *Logs a hello, demonstrates task creation, logging, and optional tagging within a minimalist setup.*

- [classic_flow.py](flows/simple_flows/classic_flow.py)

    *Concurrently fetch and report current temperatures for predefined cities, leveraging task caching and S3 for result persistence.*


# Utilities
Utilize utilities for any additional workflows necessary to keep Prefect owned objects up to date





