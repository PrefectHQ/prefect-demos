"""Implement extract flow using Prefect subflows on independent Cloud Run jobs"""
import httpx
from prefect import flow, get_run_logger, tags, task, unmapped
from prefect.deployments import run_deployment
from prefect.task_runners import ThreadPoolTaskRunner

BASE_URL = "https://dev.to/api"
CONCURRENCY = 10


@task(
    retries=3,
    retry_delay_seconds=[10, 30, 60],
)
def fetch_url(url: str, params: dict | None = None) -> dict:
    """Generic task for fetching a URL"""
    get_run_logger().info(f"Fetching {url}")
    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json()


@flow
def fetch_url_flow(url: str) -> dict:
    """Wrap fetch_url in a flow for deployment"""
    return fetch_url(url=url)


@task
def fetch_url_run_deployment(url: str):
    """Wrap run_deployment in a task for mapping"""
    run_deployment(
        name="fetch-url-flow/cloud-run",
        parameters={"url": url},
        timeout=None,  # Wait indefinitely (default behavior)
    )


@task
def list_articles(pages: int, per_page: int = 10) -> list[str]:
    """List (pages * per_page) article URLs from the Dev.to API"""

    _pages = fetch_url.map(
        unmapped(f"{BASE_URL}/articles"),
        [{"page": page, "per_page": per_page} for page in range(1, pages + 1)],
    )
    pages = [_page.result() for _page in _pages]

    return [
        f"{BASE_URL}/articles/{article['id']}" for page in pages for article in page
    ]


@flow(task_runner=ThreadPoolTaskRunner(max_workers=CONCURRENCY))
def extract(pages: int) -> None:
    """Extract articles from the Dev.to API"""
    article_urls = list_articles(pages)

    _articles = fetch_url_run_deployment.map(article_urls)
    _articles.wait()


if __name__ == "__main__":
    with tags("local"):
        extract(pages=100)
