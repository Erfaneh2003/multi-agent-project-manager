from datetime import date

import pytest
from app.algorithms.allocation import AllocationCandidate, select_candidate
from app.algorithms.dependencies import (
    DependencyGraphError,
    detect_cycle,
    topological_sort,
)
from app.algorithms.tracking import SchedulableTask, schedule_tasks


def test_topological_sort_is_stable_and_respects_dependencies() -> None:
    dependencies = {"build": ["design"], "test": ["build"], "design": []}

    assert topological_sort(["test", "design", "build"], dependencies) == [
        "design",
        "build",
        "test",
    ]


def test_cycle_detection_returns_cycle_path() -> None:
    cycle = detect_cycle(["a", "b", "c"], {"a": ["c"], "b": ["a"], "c": ["b"]})

    assert cycle == ["a", "c", "b", "a"]


def test_invalid_dependency_is_rejected() -> None:
    with pytest.raises(DependencyGraphError, match="unknown task"):
        topological_sort(["a"], {"a": ["missing"]})


def test_allocation_ignores_infeasible_candidates() -> None:
    selected = select_candidate(
        [
            AllocationCandidate("m1", 1.0, 1.0, 0.0, 1.0),
            AllocationCandidate("m2", 0.8, 0.8, 0.5, 0.8),
        ]
    )

    assert selected is not None
    assert selected.member_id == "m2"


def test_schedule_starts_dependents_after_prerequisites() -> None:
    result = schedule_tasks(
        [
            SchedulableTask("design", 2),
            SchedulableTask("build", 3),
            SchedulableTask("test", 1),
        ],
        {"build": ["design"], "test": ["build"]},
        date(2026, 1, 1),
    )

    assert [(task.task_id, task.start, task.finish) for task in result] == [
        ("design", date(2026, 1, 1), date(2026, 1, 3)),
        ("build", date(2026, 1, 3), date(2026, 1, 6)),
        ("test", date(2026, 1, 6), date(2026, 1, 7)),
    ]
