from prefect import flow
import os


@flow(log_prints=True)
def my_little_flow():
    print("Hello from dep_a")
    print(os.getenv("MY_VAR"))


if __name__ == "__main__":
    my_little_flow.deploy(
        name="k8s-deployment",
        work_pool_name="my-k8s-pool",
        image="docker.io/taycurran/little-flow:demo4",
        push=False,
        tags=["repro"],
        job_variables={"env": {"MY_VAR": "my_value_b"}},
    )
