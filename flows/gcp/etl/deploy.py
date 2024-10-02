from prefect import flow
from prefect.runner.storage import GitRepository


def deploy():
    repo = GitRepository(
        url="https://github.com/PrefectHQ/prefect-demos.git",
        branch="gcp-etl",
    )

    flow.from_source(
        source=repo,
        entrypoint="flows/gcp/etl/flows/hello.py:hello",
    ).deploy(
        name="hello-cloud-run",
        work_pool_name="cloud-run",
    )

    flow.from_source(
        source=repo,
        entrypoint="flows/gcp/etl/flows/extract.py:extract",
    ).deploy(
        name="extract-cloud-run-tasks",
        work_pool_name="cloud-run",
    )


if __name__ == "__main__":
    deploy()
