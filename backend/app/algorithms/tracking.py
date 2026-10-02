from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta

from .dependencies import topological_sort


@dataclass(frozen=True, slots=True)
class SchedulableTask:
    task_id: str
    duration_days: int
    priority: int = 0


@dataclass(frozen=True, slots=True)
class ScheduledTask:
    task_id: str
    start: date
    finish: date


def schedule_tasks(
    tasks: list[SchedulableTask],
    dependencies: Mapping[str, list[str]],
    start_date: date,
) -> list[ScheduledTask]:
    task_by_id = {task.task_id: task for task in tasks}
    order = topological_sort(task_by_id, dependencies)
    finish_dates: dict[str, date] = {}
    scheduled: list[ScheduledTask] = []

    for task_id in order:
        task = task_by_id[task_id]
        prerequisite_finish = [
            finish_dates[item] for item in dependencies.get(task_id, [])
        ]
        earliest_start = max(prerequisite_finish, default=start_date)
        finish = earliest_start + timedelta(days=task.duration_days)
        scheduled.append(ScheduledTask(task_id, earliest_start, finish))
        finish_dates[task_id] = finish
    return scheduled
