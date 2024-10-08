from pathlib import Path

from dbt_common.events.base_types import EventMsg

from dbt.cli.main import dbtRunner, dbtRunnerResult
from dbt.contracts.graph.manifest import Manifest


def invoke(
    runner: dbtRunner, command: list[str], profiles_dir: Path, project_dir: Path
) -> dbtRunnerResult:
    """Handler for dealing with exceptions"""
    res = runner.invoke(
        command + ["--profiles-dir", profiles_dir, "--project-dir", project_dir]
    )
    if not res.success:
        raise res.exception
    return res.result


def parse_manifest(profiles_dir: Path, project_dir: Path) -> tuple[Manifest, dict]:
    """Parse a dbt manifest"""
    runner = dbtRunner()
    manifest: Manifest = invoke(runner, ["parse"], profiles_dir, project_dir)
    graph = dict()

    for node in manifest.nodes.values():
        if node.resource_type in ["model"]:
            graph[node.unique_id] = node.depends_on.nodes

    return manifest, graph


def handle_event(event: EventMsg):
    """Handle an event"""
    # if event.info.name in ["NodeCompiling", "NodeExecuting", "NodeStart", "NodeFinished"]:
    if event.info.name.startswith("Node"):
        print(
            f"{event.info.name} - {event.data.node_info.resource_type} - {event.data.node_info.unique_id}"
        )


def build(profiles_dir: Path, project_dir: Path):
    manifest, graph = parse_manifest(profiles_dir, project_dir)
    runner = dbtRunner(manifest=manifest, callbacks=[handle_event])
    invoke(runner, ["build"], profiles_dir, project_dir)


if __name__ == "__main__":
    build("./jaffle_shop_duckdb", "./jaffle_shop_duckdb")
