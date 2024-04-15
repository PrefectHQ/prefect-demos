from prefect.input import RunInput
from prefect import get_run_logger
from prefect.blocks.system import JSON
from prefect import task, flow, get_run_logger, pause_flow_run
from pydantic import Field
from prefect.artifacts import create_table_artifact
import requests
import marvin_extension as ai_functions
from prefect_snowflake.database import SnowflakeConnector


URL = "https://randomuser.me/api/"

DEFAULT_FEATURES_TO_DROP = [
    "name",
    "location",
    "email",
    "login",
    "dob",
    "registered",
    "phone",
    "cell",
    "id",
    "picture",
    "nat",
]


class CreateArtifactOrSnowflake(RunInput):
    create_artifact: bool = Field(description="Would you like to approve?")


class CleanedInput(RunInput):
    features_to_keep: list[str]


class UserInput(RunInput):
    number_of_users: int


@task(name="Fetching URL", retries=1, retry_delay_seconds=5, retry_jitter_factor=0.1)
def fetch(url: str):
    logger = get_run_logger()
    response = requests.get(url)
    raw_data = response.json()
    logger.info(f"Raw response: {raw_data}")
    return raw_data


@task(name="Cleaning Data")
def clean(raw_data: dict, features_to_keep: list[str]):
    results = raw_data.get("results")[0]
    return list(map(results.get, features_to_keep))


# HIL: user input for which features to drop initially
@flow(name="User Input Remove Features")
def user_input_remove_features(url: str):
    raw_data = fetch(url)

    features = "\n".join(raw_data.get("results")[0].keys())

    description_md = (
        "## Features available:"
        f"\n```json{features}\n```\n"
        "Please confirm the features you would like to keep in the dataset"
    )

    user_input = pause_flow_run(
        wait_for_input=CleanedInput.with_initial_data(
            description=description_md, features_to_keep=DEFAULT_FEATURES_TO_DROP
        )
    )
    return user_input.features_to_keep


@flow(name="Create Artifact")
def create_artifact():

    features = JSON.load("all-users-json").value
    description_md = (
        "### Features available:\n"
        f"```{features}```\n"
        "### Would you like to create an artifact?"
    )

    logger = get_run_logger()
    create_artifact_input = pause_flow_run(
        wait_for_input=CreateArtifactOrSnowflake.with_initial_data(
            description=description_md, create_artifact=False
        )
    )
    if create_artifact_input.create_artifact == True:
        logger.info("Report approved! Creating artifact...")
        create_table_artifact(
            key="table-of-users", table=JSON.load("all-users-json").value
        )
    else:
        raise Exception("User did not approve")


@flow(name="Create Names")
def create_names():
    logger = get_run_logger()
    df = []
    description_md = """
    How many users would you like to create?
    """
    user_input = pause_flow_run(
        wait_for_input=UserInput.with_initial_data(
            description=description_md, number_of_users=2
        )
    )
    num_of_rows = user_input.number_of_users
    copy = num_of_rows
    features_to_keep = user_input_remove_features(URL)
    logger.info(f"Features to keep: {features_to_keep}")
    while num_of_rows != 0:
        raw_data = fetch(URL)
        df.append(clean(raw_data, features_to_keep))
        num_of_rows -= 1
    logger.info(f"created {copy} users: {df}")
    JSON(value=df).save("all-users-json", overwrite=True)
    return df


@flow(name="Upload to Snowflake")
def upload_to_snowflake(results):
    description_md = (
        "### Features available:\n"
        f"```{results}```\n"
        "### Would you like to upload to snowflake?"
    )

    logger = get_run_logger()
    create_artifact_input = pause_flow_run(
        wait_for_input=CreateArtifactOrSnowflake.with_initial_data(
            description=description_md, create_artifact=False
        )
    )
    if create_artifact_input.create_artifact == True:
        logger.info("Uploading to snowflake...")
        with SnowflakeConnector.load("snowflake-table") as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS customers (name varchar, address varchar);"
            )
            conn.execute_many(
                "INSERT INTO customers (name, address) VALUES (%(name)s, %(address)s);",
                seq_of_parameters=results,
            )
    else:
        raise Exception("User did not approve")


if __name__ == "__main__":
    list_of_names = create_names()
    create_artifact()
    results = ai_functions.extract_information()
    upload_to_snowflake(results)
