import pandas as pd
from prefect.blocks.core import Block
from sqlalchemy import create_engine
import time


class SnowflakeConnection(Block):

    """
    Interact with a Snowflake schema using Pandas.
    Requires pandas and snowflake-sqlalchemy packages to be installed.

    Args:
        Number of Rows: number of rows to return from the query

    Example:
        Load stored block:
        ```python
        from snowflake.blocks import SnowflakeConnection
        block = SnowflakeConnection.load("BLOCK_NAME")
        ```
    """  # noqa

    _block_type_name = "Snowflake Connection"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/2DxzAeTM9eHLDcRQx1FR34/f858a501cdff918d398b39365ec2150f/snowflake.png?h=250"  # noqa
    _block_schema_capabilities = ["load_raw_data", "read_sql"]

    def read_sql(self, table_or_query: str) -> pd.DataFrame:
        time.sleep(1)
        cities = pd.DataFrame(
            {"location": ["Houston", "Austin", "Dallas", "San Antonio"]}
        )
        return cities

    def load_raw_data(self, dataframe: pd.DataFrame, table_name: str) -> None:
        time.sleep(1)
        cities = pd.DataFrame(
            {"location": ["Houston", "Austin", "Dallas", "San Antonio"]}
        )
        return cities
