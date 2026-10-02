from datetime import date

from ..algorithms.dependencies import detect_cycle
from ..algorithms.tracking import SchedulableTask, schedule_tasks
from ..schemas.contracts import ScheduledTask as ScheduledTaskSchema
from ..schemas.contracts import ScheduleResult, TaskDraft
from .base import BaseAgent


class SchedulerInput:
    def __init__(
        self,
        tasks: list[TaskDraft],
        start_date: date,
    ) -> None:
        self.tasks = tasks
        self.start_date = start_date


class SchedulerTrackerAgent(BaseAgent[SchedulerInput, ScheduleResult]):
    name = "scheduler_tracker"
    system_prompt = (
        "Validate the task graph and produce a deterministic schedule. Report graph "
        "errors instead of inventing dates."
    )

    @property
    def model_name(self) -> str:
        return "deterministic-scheduler"

    @property
    def is_mock(self) -> bool:
        return True

    def execute(self, input_data: SchedulerInput) -> ScheduleResult:
        dependencies = {task.task_id: task.dependencies for task in input_data.tasks}
        cycle = detect_cycle([task.task_id for task in input_data.tasks], dependencies)
        if cycle:
            return ScheduleResult(
                tasks=[],
                warnings=[f"Scheduling stopped because of cycle: {' -> '.join(cycle)}"],
            )
        scheduled = schedule_tasks(
            [
                SchedulableTask(task.task_id, task.estimated_days)
                for task in input_data.tasks
            ],
            dependencies,
            input_data.start_date,
        )
        return ScheduleResult(
            tasks=[
                ScheduledTaskSchema(
                    task_id=item.task_id,
                    start=item.start,
                    finish=item.finish,
                )
                for item in scheduled
            ]
        )
