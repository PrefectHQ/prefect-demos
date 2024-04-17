import marvin
from prefect import flow, get_run_logger, pause_flow_run
from prefect.blocks.system import JSON, Secret
from prefect.input import RunInput
from prefect_aws.s3 import S3Bucket
from pydantic import BaseModel, constr, Field

from prefect.variables import Variable


DEFAULT_EXTRACT_QUERY = "Group by location and count the number of users in each location."  # Create a table of a users name, location, coordinates, and continent the user is located
GENERATE_SUGGESTED_FILE_NAME = "10-letter phrase that describes the user's query: "
# "Please provide a single word for a file name that describes the user's query: "


class userApprovalAndFileName(RunInput):
    file_name: constr(pattern=r"^[a-zA-Z]+$", max_length=10)
    approve: bool = Field(description="Would you like to approve?")


class InputQuery(RunInput):
    input_instructions: str


class generatedFileName(BaseModel):
    fixed_length_string: constr(pattern=r"^[a-zA-Z]+$", min_length=10, max_length=10)


@flow(name="Extract User Insights")
def extract_information():
    secret_block = Secret.load("openai-creds-interactive-workflows")
    marvin.settings.openai.api_key = secret_block.get()

    features = JSON.load("all-users-json").value
    description_md = (
        "### Features available:\n"
        f"```{features}```\n"
        "### Please provide a query to extract user insights.\n"
    )

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
        JSON.load("all-users-json").value,
        target=str,
        instructions=user_input.input_instructions,
    )
    Variable.set(name="user_query", value=user_input.input_instructions, overwrite=True)

    logger.info(f"Query results: {result}")
    return result


@flow(name="Upload to S3", log_prints=True)
def upload_to_s3(results):
    logger = get_run_logger()
    logger.info(f"Uploading to S3: {results}")

    description_md = (
        "## Query results:\n"
        f"```{results}```\n"
        "## Would you like to upload the results to s3?\n"
        "### Please provide a file name based on the query from results.\n"
        "### A suggestion is provided:"
    )
    user_query = Variable.get("user_query")

    instructions = f"{GENERATE_SUGGESTED_FILE_NAME} + {user_query.value}"
    print(instructions)
    marvin_annotated_file_name = marvin.extract(
        results,
        target=generatedFileName,
        instructions=instructions,
    )

    output_file_name = marvin_annotated_file_name[0].fixed_length_string

    Variable.set(name=output_file_name, value=output_file_name, overwrite=True)

    print(f"marvin_annotated_file_name: {marvin_annotated_file_name}")
    print(f"marvin_annotated_file_name.fixed_length_string: {output_file_name}")
    logger = get_run_logger()
    upload_to_s3_input = pause_flow_run(
        wait_for_input=userApprovalAndFileName.with_initial_data(
            description=description_md, file_name=output_file_name, approve=False
        )
    )

    if upload_to_s3_input.approve:
        s3_bucket_block = S3Bucket.load("interactive-workflow-output")

        logger.info("Report approved! Uploading to s3...")
        with open(f"./{output_file_name}.txt", "w") as outfile:
            outfile.write(str(results))
        pass

        s3_bucket_block.upload_from_path(
            f"./{output_file_name}.txt", f"{output_file_name}.txt"
        )
    else:
        raise Exception("User did not approve")

    return results
