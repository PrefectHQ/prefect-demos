# prefect-demos
Welcome to our repository dedicated to showcasing a variety of Prefect demos. 

These demos are meant to be end-to-end examples showcasing how multiple features within prefect can be utilized to accommodate different use cases demonstrating the versatility and power of Prefect as a workflow application tool. These demos focus specifically on the code and any prefect features necessary to create these examples, any external configurations necessary are assumed to have been completed separately. Dive into our demos to explore how Prefect seamlessly orchestrates complex data processes, ensuring efficient and reliable execution of your data tasks. 

Get inspired, learn best practices, and discover innovative ways to leverage Prefect in your data projects!

# Flows
Demos separated by project.

#### Datalake Usage
- [datalake_listener.py](flows/aws/datalake/datalake_listener.py)

    *Processes Near Earth Object (NEO) data from an AWS S3 bucket, filters for potentially hazardous objects, flattens the data structure, and then uploads the results back to S3 in CSV format*

- [datalake_s3_nasa.py](flows/aws/datalake/datalake_s3_nasa.py)

    *Retrieves Near Earth Object (NEO) data from NASA's API for a given timeframe, caches the request to avoid unnecessary API calls, and then uploads the data to an AWS S3 bucket*

- [deploy.py](flows/aws/datalake/deploy.py)

    *Automates the deployment of two Prefect workflows for data processing: `datalake_listener`, which triggers on AWS S3 object creation, and `fetch_neo_by_date`, which fetches Near Earth Object data daily, using a Docker image from an ECR repository for execution on an ECS push work pool*







