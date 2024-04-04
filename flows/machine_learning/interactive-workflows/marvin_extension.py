import marvin
from prefect.blocks.system import Secret
from prefect import flow, task, get_run_logger, pause_flow_run
from prefect.input import RunInput
from prefect.blocks.system import JSON

DEFAULT_EXTRACT_QUERY = (
    "Group by location and count the number of users in each location." # Create a table of a users name, location, coordinates, and continent the user is located
)


class InputQuery(RunInput):
    input_instructions: str


@flow(name="Extract User Insights")
def extract_information():
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
    result = marvin.extract(
        JSON.load("all-users-json"),
        target=str,
        instructions=user_input.input_instructions,
    )
    logger.info(f"Query results: {result}")
    return result
