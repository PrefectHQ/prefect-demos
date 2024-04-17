from prefect import flow

flow.from_source(
source="https://github.com/Sahiler/interactive-workflow-demo.git",
entrypoint="interactive.py:interactive",
).deploy(
    name="interactive-workflow-demo",
    work_pool_name="managed-execution",
    job_variables={"pip_packages": ["marvin", "prefect-aws"]}
)
