"""
Flow for extracting articles from the Dev.to API
API Documentation: https://developers.forem.com/api
"""

from datetime import timedelta

import httpx
from prefect import flow, get_run_logger, task
from prefect.cache_policies import INPUTS, TASK_SOURCE

BASE_URL = "https://dev.to/api"


@task(
    # Retry in 10, then 30, then 60 seconds
    retries=3,
    retry_delay_seconds=[10, 30, 60],
    # Tag with API route for concurrency limiting
    tags=["dev-to-api/articles"],
)
def list_articles_page(page, per_page: int = 10):
    resp = httpx.get(
        url=f"{BASE_URL}/articles",
        params={
            "page": page,
            "per_page": per_page,
        },
    )
    resp.raise_for_status()
    return resp.json()


@task(
    # Cache results for 10 minutes for the given inputs and code
    # Caching will only take effect if stored results are accessible
    cache_policy=INPUTS + TASK_SOURCE,
    cache_expiration=timedelta(minutes=10),
)
def list_articles(pages: int = 20):
    # Submit all tasks at once for concurrent execution
    # Alternatively use native Python async concurrency
    tasks = [list_articles_page.submit(page) for page in range(1, pages + 1)]

    # Gather the results and return
    # Yielding interferes with caching
    articles = list()
    for _task in tasks:
        # Wait for each task's result to be ready
        articles.extend(_task.result())
    return articles


@flow
def extract():
    articles = list_articles()
    for article in articles:
        get_run_logger().info(article["title"])


if __name__ == "__main__":
    extract()
