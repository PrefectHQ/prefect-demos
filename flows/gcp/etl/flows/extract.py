"""
Flow for extracting articles from the Dev.to API
API Documentation: https://developers.forem.com/api
"""

from datetime import timedelta

import httpx
from prefect import flow, get_run_logger, tags, task
from prefect.cache_policies import INPUTS, TASK_SOURCE
from prefect.deployments import run_deployment
from prefect_gcp.cloud_storage import GcsBucket

BASE_URL = "https://dev.to/api"

# Bucket must be saved to be used for result storage
BUCKET_NAME = "prefect-cloud-run-worker-storage"
BUCKET = GcsBucket.load(BUCKET_NAME)


@task(
    # Retry in 10, then 30, then 60 seconds
    retries=3,
    retry_delay_seconds=[10, 30, 60],
    # Tag with API route for concurrency limiting
    tags=["dev-to-api/articles"],
)
def list_articles_page(page: int, per_page: int = 10) -> list[dict]:
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
    # Cache results for 1 hour for the given inputs and code
    # Caching will only take effect if stored results are accessible
    cache_policy=INPUTS + TASK_SOURCE,
    cache_expiration=timedelta(hours=1),
)
def list_articles(pages: int) -> list[dict]:
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


@task(
    # Cache results for 1 day for the given inputs and code
    cache_policy=INPUTS + TASK_SOURCE,
    cache_expiration=timedelta(days=1),
    # Avoids downloading already cached articles
    # NOTE: Not sure this actually works
    cache_result_in_memory=False,
    # Configures caching for later non-task access
    # NOTE: The result is stored under a `data` key alongside metadata
    result_storage_key="dev-to-api/articles/{parameters[article_id]}.json",
    result_serializer="json",
    # result_storage=BUCKET,
    # Retry in 10, then 30, then 60 seconds
    retries=3,
    retry_delay_seconds=[10, 30, 60],
    # Tag with API route for concurrency limiting
    tags=["dev-to-api/articles"],
)
def get_article(article_id: int, persist: bool = False) -> dict:
    url = f"{BASE_URL}/articles/{article_id}"
    get_run_logger().info(f"Fetching {url}")
    resp = httpx.get(url)
    resp.raise_for_status()

    # We can persist the data ourselves and just make the result the path
    # This offers additional control over the result format
    if persist:
        path = f"dev-to-api/articles/{article_id}.json"
        BUCKET.write_path(
            path=path,
            content=resp.content,
        )
        return path
    else:
        return resp.json()


@flow
def get_article_flow(
    article_id: int,
    remote_storage: bool,
    refresh_cache: bool,
):
    """Wrap get_article in a flow for deployment"""
    _get_article = get_article.with_options(
        result_storage=BUCKET if remote_storage else None,
        refresh_cache=refresh_cache,
    )
    _get_article(article_id=article_id)


@task
def get_article_run_deployment(
    article_id: int,
    remote_storage: bool,
    refresh_cache: bool,
):
    # Run the flow as a deployment and wait
    run_deployment(
        name="get-article-flow/extract-cloud-run-flow",
        parameters={
            "article_id": article_id,
            "remote_storage": remote_storage,
            "refresh_cache": refresh_cache,
        },
        # Wait indefinitely (default behavior)
        timeout=None,
    )


@flow
def extract(
    remote_storage: bool,
    refresh_cache: bool,
    scale_out: bool,
    pages: int = 20,
):
    """
    Test cached fetching of 200 articles from the Dev.to API

    Local runtimes:
        Local storage first run: ~30s
        Local storage cached run: ~8s
        GCS storage first run: ~1m20s
        GCS storage cached run: ~2m20s
    """
    articles = list_articles(pages)
    tasks = list()

    for article in articles:
        get_run_logger().info(f"[{article['id']}] {article['title']}")
        # Using run_deployment to scale out across Cloud Run jobs
        if scale_out:
            _task = get_article_run_deployment.submit(
                article_id=article["id"],
                remote_storage=remote_storage,
                refresh_cache=refresh_cache,
            )
        # Using Prefect tasks to scale out across threads
        else:
            # Vary the result and caching of the task
            _get_article = get_article.with_options(
                result_storage=BUCKET if remote_storage else None,
                refresh_cache=refresh_cache,
            )
            _get_article.submit(article_id=article["id"])
        tasks.append(_task)

    # Explicitly wait for all tasks to complete
    [_task.wait() for _task in tasks]


if __name__ == "__main__":
    with tags("local"):
        extract(remote_storage=True, refresh_cache=True, scale_out=True)
