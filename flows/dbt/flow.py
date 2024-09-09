import tempfile
from enum import Enum
from typing import Optional

from prefect import flow, get_run_logger, task
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_github import GitHubCredentials, GitHubRepository


class DbtJob(Enum):
    BUILD = "build"
    TEST = "test"


class DbtTarget(Enum):
    DEV = "dev"
    PROD = "prod"
    CI = "ci"


@task
def clone_dbt_repo(
    project_dir: str,
    dbt_repo_url: str,
    dbt_repo_branch: str,
    dbt_repo_credentials: str = None,
) -> None:
    """Download dbt repository to a temporary directory"""
    credentials = (
        GitHubCredentials.load(dbt_repo_credentials) if dbt_repo_credentials else None
    )

    repository = GitHubRepository(
        repository_url=dbt_repo_url, credentials=credentials, reference=dbt_repo_branch
    )
    repository.get_directory(local_path=project_dir)


@task
def dbt_deps(project_dir: str, profiles_dir: str) -> None:
    """Install any required DBT dependencies"""
    trigger_dbt_cli_command(
        command="dbt deps", project_dir=project_dir, profiles_dir=profiles_dir
    )


@task
def dbt_build(
    profiles_dir: str,
    project_dir: str,
    target: str = "dev",
    select: Optional[str] = None,
) -> None:
    """Run a dbt build job"""
    extra_command_args = ["-t", target]
    if select:
        extra_command_args.extend(["-s", select])
    trigger_dbt_cli_command(
        command="dbt build",
        profiles_dir=profiles_dir,
        project_dir=project_dir,
        return_state=True,
        create_summary_artifact=True,
        summary_artifact_key=f"dbt-build-{target}-summary",
        extra_command_args=extra_command_args,
    )


@task
def dbt_test(
    profiles_dir: str,
    project_dir: str,
    target: str = "dev",
    select: Optional[str] = None,
) -> None:
    """Run a dbt test job"""
    extra_command_args = ["-t", target]
    if select:
        extra_command_args.extend(["-s", select])
    trigger_dbt_cli_command(
        command="dbt test",
        profiles_dir=profiles_dir,
        project_dir=project_dir,
        return_state=True,
        create_summary_artifact=True,
        summary_artifact_key=f"dbt-test-{target}-summary",
        extra_command_args=extra_command_args,
    )


@flow
def dbt_runner(
    dbt_repo_url: str,
    dbt_repo_branch: str = "main",
    dbt_repo_credentials: Optional[str] = None,
    dbt_job: DbtJob = DbtJob.BUILD,
    target: DbtTarget = DbtTarget.DEV,
    select: Optional[str] = None,
) -> None:
    """Clone a dbt repository and run a dbt job"""
    with tempfile.TemporaryDirectory() as project_dir:
        clone_dbt_repo(
            project_dir=project_dir,
            dbt_repo_url=dbt_repo_url,
            dbt_repo_branch=dbt_repo_branch,
            dbt_repo_credentials=dbt_repo_credentials,
        )
        get_run_logger().warning(f"Cloned dbt repo to {project_dir}")

        profiles_dir = project_dir

        dbt_deps(project_dir=project_dir, profiles_dir=profiles_dir)

        if dbt_job == DbtJob.BUILD:
            dbt_build(
                target=target.value,
                select=select,
                profiles_dir=profiles_dir,
                project_dir=project_dir,
            )
        elif dbt_job == DbtJob.TEST:
            dbt_test(
                target=target.value,
                select=select,
                profiles_dir=profiles_dir,
                project_dir=project_dir,
            )


if __name__ == "__main__":
    dbt_runner(
        dbt_repo_url="https://github.com/dbt-labs/jaffle_shop_duckdb.git",
        dbt_repo_branch="duckdb",
        dbt_job=DbtJob.BUILD,
        target=DbtTarget.DEV,
    )
