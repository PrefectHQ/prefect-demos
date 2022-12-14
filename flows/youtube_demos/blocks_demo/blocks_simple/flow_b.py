import random
from prefect import flow, task
import pandas as pd
from prefect.blocks.notifications import SlackWebhook

@flow
def flow_b(df):
    print("flow")

    if df.columns[0] != "A":
        print("sending message")

        slack_webhook_block = SlackWebhook.load("staging-general-notifications")
        slack_webhook_block.notify("First Column Header is Wrong!")

if __name__ == "__main__":
    first_col = random.choice(["A", "C"])
    print(first_col)
    df = pd.DataFrame({first_col: ["a"] * 20, "B": ["b"] * 20})
    flow_b(df)