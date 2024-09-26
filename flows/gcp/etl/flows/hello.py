from prefect import flow, get_run_logger, tags


@flow
def hello(name: str = "Marvin"):
    get_run_logger().info(f"Hello {name}!")


if __name__ == "__main__":
    with tags("local"):
        hello()
