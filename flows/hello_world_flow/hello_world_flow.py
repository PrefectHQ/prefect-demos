from prefect import flow, task


@task
def my_task():
    print("Hello World")


@flow
def hello_world():
    my_task()
    print("What is your favorite number my friendly friends?")

    return 42


if __name__ == "__main__":
    hello_world()
