from prefect import flow


@flow
def hello():
    print("Hi there!")


if __name__ == "__main__":
    hello()
