from prefect import task
import random
from faker import Faker
import pandas as pd



@task
def ingest_raw_customers(risk_profile):

    fake = Faker()
    row_count = 300

    output = [
        {
            "ID": random.randint(1, row_count),
            "FIRST_NAME": fake.first_name(),
            "LAST_NAME": fake.last_name(),
        }
        for x in range(round(row_count*0.5))
    ]

    if risk_profile.nulls:

      null_injection = [
          {
              "ID": random.randint(1, row_count),
              "FIRST_NAME": None,
              "LAST_NAME": fake.last_name(),
          }
          for x in range(round(row_count*0.5))
      ]
      null_row = {'ID': row_count + 1, 'FIRST_NAME': None, 'LAST_NAME': 'Smith'}
      
      output += null_injection + [null_row]

    df = pd.DataFrame(output)
    df = df.drop_duplicates(subset=["ID"])
    df = df.sort_values('ID')
    df = df.reset_index(drop=True)
    
    if risk_profile.integration_failure:
        df.columns = ['InCorrect', 'Column', 'Titles']

    print(df.tail())

    return df



if __name__ == "__main__":

    from pydantic import BaseModel
    class RiskProfile(BaseModel):
        nulls: bool
        api_failure: bool
        integration_failure: bool

    default_risk_profile = RiskProfile(
        nulls=True, 
        api_failure=False,
        integration_failure=True
        )

    ingest_raw_customers.fn(default_risk_profile)