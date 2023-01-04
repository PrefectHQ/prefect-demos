from prefect import flow, task
from prefect_dask.task_runners import DaskTaskRunner


@task
def my_task():
    print("Hello World")

my_dask_task_runner = DaskTaskRunner(
    cluster_class="dask_cloudprovider.aws.FargateCluster",
    adapt_kwargs={"maximum": 10}
)

@flow(task_runner=DaskTaskRunner)
def hello_world():
    my_task()
    print("What is your favorite number?")

    return 42


if __name__ == "__main__":
    hello_world()
