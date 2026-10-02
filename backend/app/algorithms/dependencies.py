from collections.abc import Iterable, Mapping


class DependencyGraphError(ValueError):
    """Raised when task dependencies do not form a valid directed graph."""


def validate_dependencies(
    task_ids: Iterable[str], dependencies: Mapping[str, Iterable[str]]
) -> None:
    known_ids = set(task_ids)
    for task_id, prerequisites in dependencies.items():
        if task_id not in known_ids:
            raise DependencyGraphError(f"Unknown task in dependency map: {task_id}")
        for prerequisite in prerequisites:
            if prerequisite not in known_ids:
                raise DependencyGraphError(
                    f"Task {task_id} depends on unknown task {prerequisite}"
                )
            if prerequisite == task_id:
                raise DependencyGraphError(f"Task {task_id} cannot depend on itself")


def detect_cycle(
    task_ids: Iterable[str], dependencies: Mapping[str, Iterable[str]]
) -> list[str] | None:
    validate_dependencies(task_ids, dependencies)
    graph = {
        task_id: list(dependencies.get(task_id, ())) for task_id in sorted(task_ids)
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str, path: list[str]) -> list[str] | None:
        if task_id in visiting:
            return path[path.index(task_id) :]
        if task_id in visited:
            return None
        visiting.add(task_id)
        for prerequisite in graph[task_id]:
            cycle = visit(prerequisite, path + [prerequisite])
            if cycle:
                return cycle
        visiting.remove(task_id)
        visited.add(task_id)
        return None

    for task_id in graph:
        cycle = visit(task_id, [task_id])
        if cycle:
            return cycle
    return None


def topological_sort(
    task_ids: Iterable[str], dependencies: Mapping[str, Iterable[str]]
) -> list[str]:
    validate_dependencies(task_ids, dependencies)
    cycle = detect_cycle(task_ids, dependencies)
    if cycle:
        raise DependencyGraphError(f"Dependency cycle detected: {' -> '.join(cycle)}")

    remaining = {task_id: set(dependencies.get(task_id, ())) for task_id in task_ids}
    ordered: list[str] = []
    while remaining:
        ready = sorted(task_id for task_id, deps in remaining.items() if not deps)
        if not ready:
            raise DependencyGraphError("Dependency graph could not be ordered")
        ordered.extend(ready)
        for task_id in ready:
            remaining.pop(task_id)
        for deps in remaining.values():
            deps.difference_update(ready)
    return ordered
