"""A simple flow that says hello"""

from prefect import flow, task, tags, get_run_logger


@task
def say_hello(name: str) -> None:
    get_run_logger().info(f"Hello {name}")


@flow
def hello(name: str = "Marvin") -> None:
    say_hello(name)


if __name__ == "__main__":
    with tags("local"):
        hello()
