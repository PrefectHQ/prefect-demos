# Datalake Workflow Automation

## Overview

This project automates the ingestion and processing of Near Earth Objects (NEO) data from NASA's API into an AWS S3 datalake using Prefect for orchestration. It comprises two main components: a data fetcher that retrieves and stores NEO data in S3, and a listener that processes this data upon arrival.

## Components

- **deploy.py**: Orchestrates the deployment of Prefect flows to AWS
- **requirements.txt**: Lists the project's Python dependencies
- **Dockerfile**: Specifies the Docker container configuration for running the application
- **datalake_s3_nasa.py**: Defines the flow to fetch NEO data from NASA's API and store it in S3
- **datalake_listener.py**: Implements the flow to process new NEO data files added to S3

## Setup

1. Installation setup

    a. Clone this repository:

    ```bash
    git clone https://github.com/PrefectHQ/prefect-demos.git
    cd prefect-demos/flows/aws/datalake
    ```

    b. Set up a virtual environment (optional but recommended)

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    c. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
2. Ensure AWS CLI is configured with the necessary access rights
3. Install Docker and ensure it's running
4. Set the necessary environment variables, including `ECR_REPO` for the AWS ECR repository
5. Run `python deploy.py` to deploy the Prefect flows to AWS

## Dependencies

- Prefect: For workflow orchestration
- AWS SDK: For interactions with AWS services
- HTTPX & Pendulum: For making API requests and handling dates

## Deployment

Deployments are handled via the `deploy.py` script, which sets up the flows and configurations needed for execution in AWS. Ensure that you have the necessary AWS permissions and configurations in place.