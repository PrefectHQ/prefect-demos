from prefect import flow
import os


@flow(log_prints=True)
def my_flow_b():
    print("Hello from dep_a")
    print(os.getenv("MY_VAR"))

if __name__ == "__main__":
    my_flow_b()