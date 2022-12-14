import random
from prefect import flow, task
import pandas as pd
from prefect.blocks.notifications import SlackWebhook

@flow
def flow_a(df):
    print("flow")

    if df.shape[0] < 100:
        print("sending message")

        slack_webhook_block = SlackWebhook.load("staging-general-notifications")
        slack_webhook_block.notify("Not enough rows!")

if __name__ == "__main__":
    df_len = random.choice([10, 120])
    print(df_len)
    df = pd.DataFrame({"A": ["a"] * df_len, "B": ["b"] * df_len})
    flow_a(df)
