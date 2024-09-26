from prefect import flow
from prefect.runner.storage import GitRepository


def deploy():
    flow.from_source(
        source=GitRepository(
            url="https://github.com/PrefectHQ/prefect-demos.git",
            branch="gcp-etl",
        ),
        entrypoint="flows/gcp/etl/hello.py:hello",
    ).deploy(
        name="hello-cloud-run",
        work_pool_name="cloud-run",
    )


if __name__ == "__main__":
    deploy()
