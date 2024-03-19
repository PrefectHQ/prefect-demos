# prefect-demos
Welcome to our repository dedicated to showcasing a variety of Prefect demos. 

Here, you'll find an extensive collection of practical examples and workflows designed to demonstrate the versatility and power of Prefect as a modern data workflow automation tool. Whether you're new to Prefect or an experienced user seeking to enhance your workflow designs, this repository offers valuable insights and easy-to-follow examples. Dive into our demos to explore how Prefect seamlessly orchestrates complex data processes, ensuring efficient and reliable execution of your data tasks. 

Get inspired, learn best practices, and discover innovative ways to leverage Prefect in your data projects!

# Simple flows
- [hello.py](flows/simple_flows/hello.py)
    
    *Logs a hello, demonstrates task creation, logging, and optional tagging within a minimalist setup.*

- [weather.py](flows/simple_flows/weather.py)

    *Showcases error handling, task retries, conditional flows, result caching, notification alerts, and integration with AWS S3 for result storage*

- [classic_flow.py](flows/simple_flows/classic_flow.py)

    *Concurrently fetch and report current temperatures for predefined cities, leveraging task caching and S3 for result persistence.*

# Specialty flows
- [consumer_flow.py](flows/specialty_flows/consumer_flow.py)
- [dbt_snowflake_flow.py](flows/specialty_flows/dbt_snowflake_flow.py)
- [partition_example.py](flows/specialty_flows/dbt_snowflake_flow.py)
- [wave_data.py](flows/specialty_flows/dbt_snowflake_flow.py)






