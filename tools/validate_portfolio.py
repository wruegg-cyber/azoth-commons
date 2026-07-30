"""Validate the public AZOTH project portfolio using only the standard library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PORTFOLIO = ROOT / "PROJECT_PORTFOLIO.json"
REQUIRED_PROJECT_FIELDS = {
    "id",
    "name",
    "priority",
    "status",
    "repository",
    "depends_on",
    "resume_anchor",
    "next_gate",
    "hive_role",
}


def load_portfolio(path: Path = DEFAULT_PORTFOLIO) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    projects = data.get("projects", [])
    repositories = data.get("repositories", [])
    project_ids = [project.get("id") for project in projects]
    repository_ids = {repository.get("id") for repository in repositories}

    if len(project_ids) != len(set(project_ids)):
        errors.append("project ids must be unique")
    if len(repository_ids) != len(repositories):
        errors.append("repository ids must be unique")

    expected = data.get("counts", {})
    if expected.get("primary_project_lanes") != len(projects):
        errors.append("primary_project_lanes count does not match projects")
    if expected.get("repositories") != len(repositories):
        errors.append("repositories count does not match repositories")
    if expected.get("candidate_libraries") != len(data.get("candidate_libraries", [])):
        errors.append("candidate_libraries count does not match candidate_libraries")

    by_id = {project.get("id"): project for project in projects}
    for project in projects:
        project_id = project.get("id", "<missing>")
        missing = REQUIRED_PROJECT_FIELDS - set(project)
        if missing:
            errors.append(f"{project_id}: missing fields {sorted(missing)}")
        if project.get("repository") not in repository_ids:
            errors.append(f"{project_id}: unknown repository {project.get('repository')!r}")
        if project.get("priority") not in (0, 1, 2, 3):
            errors.append(f"{project_id}: priority must be 0, 1, 2, or 3")
        for dependency in project.get("depends_on", []):
            if dependency == project_id:
                errors.append(f"{project_id}: cannot depend on itself")
            elif dependency not in by_id:
                errors.append(f"{project_id}: unknown dependency {dependency!r}")
            elif by_id[dependency].get("priority", 99) > project.get("priority", -1):
                errors.append(
                    f"{project_id}: dependency {dependency!r} has a later priority"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(project_id: str, trail: tuple[str, ...]) -> None:
        if project_id in visiting:
            errors.append("dependency cycle: " + " -> ".join((*trail, project_id)))
            return
        if project_id in visited or project_id not in by_id:
            return
        visiting.add(project_id)
        for dependency in by_id[project_id].get("depends_on", []):
            visit(dependency, (*trail, project_id))
        visiting.remove(project_id)
        visited.add(project_id)

    for project_id in project_ids:
        if project_id:
            visit(project_id, ())

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PORTFOLIO)
    args = parser.parse_args()
    data = load_portfolio(args.path)
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "portfolio valid: "
        f"{len(data['projects'])} projects, "
        f"{len(data['repositories'])} repositories, "
        f"{len(data['candidate_libraries'])} candidate libraries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

