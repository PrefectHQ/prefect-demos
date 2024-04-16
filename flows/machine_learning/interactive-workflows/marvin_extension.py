import marvin
from prefect.blocks.system import Secret
from prefect import flow, task, get_run_logger, pause_flow_run
from prefect.input import RunInput
from prefect.blocks.system import JSON
from pydantic import BaseModel, Field
from typing import List


DEFAULT_EXTRACT_QUERY = (
    "Create a json with name and address as two keys" # Create a table of a users name, location, coordinates, and continent the user is located
) # Group by location and count the number of users in each location.

class ParsedOutput(BaseModel):
    listOfKeys: List[str] = Field(default_factory=list)
    key_value: List[List[str]] = Field(default_factory=list)


class InputQuery(RunInput):
    input_instructions: str


@flow(name="Extract User Insights")
def extract_information_to_json():
    secret_block = Secret.load("openai-creds-interactive-workflows")
    marvin.settings.openai.api_key = secret_block.get()

    description_md = f"""
    The most recent user information: {JSON.load("all-users-json")}
    What would you like to gain insights on?
    """
    logger = get_run_logger()
    user_input = pause_flow_run(
        wait_for_input=InputQuery.with_initial_data(
            description=description_md,
            input_instructions=DEFAULT_EXTRACT_QUERY,  
        )
    )

    logger = get_run_logger()

    logger.info(
        f"""
    Extracting user insights... \n
    User input: {user_input.input_instructions}
    """
    )
    result_json = marvin.extract(
        JSON.load("all-users-json"),
        target=list,
        instructions=user_input.input_instructions + " in JSON format",
    )
    logger.info(f"Query results: {result_json}")
    return result_json
