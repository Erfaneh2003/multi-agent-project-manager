from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(StrEnum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"


class ProjectInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=20, max_length=20_000)
    goals: list[str] = Field(default_factory=list, max_length=20)
    constraints: list[str] = Field(default_factory=list, max_length=20)
    expected_days: int | None = Field(default=None, gt=0, le=3650)


class TaskDraft(BaseModel):
    task_id: str = Field(pattern=r"^[a-z][a-z0-9_-]{1,63}$")
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=5000)
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_days: int = Field(gt=0, le=365)
    required_skills: list[str] = Field(default_factory=list, max_length=20)
    acceptance_criteria: list[str] = Field(default_factory=list, max_length=20)
    dependencies: list[str] = Field(default_factory=list, max_length=50)
    status: TaskStatus = TaskStatus.BACKLOG


class ProjectAnalysis(BaseModel):
    summary: str = Field(min_length=1, max_length=5000)
    functional_requirements: list[str] = Field(default_factory=list, max_length=100)
    non_functional_requirements: list[str] = Field(default_factory=list, max_length=100)
    tasks: list[TaskDraft] = Field(min_length=1, max_length=200)
    assumptions: list[str] = Field(default_factory=list, max_length=50)
    open_questions: list[str] = Field(default_factory=list, max_length=50)

    @model_validator(mode="after")
    def validate_task_dependencies(self) -> "ProjectAnalysis":
        task_ids = {task.task_id for task in self.tasks}
        if len(task_ids) != len(self.tasks):
            raise ValueError("Task identifiers must be unique")
        invalid = {
            dependency
            for task in self.tasks
            for dependency in task.dependencies
            if dependency not in task_ids or dependency == task.task_id
        }
        if invalid:
            raise ValueError(f"Invalid task dependencies: {sorted(invalid)}")
        return self


class TeamMemberProfile(BaseModel):
    member_id: str = Field(min_length=1, max_length=100)
    skills: set[str] = Field(default_factory=set)
    experience_level: int = Field(ge=0, le=10)
    capacity_days: int = Field(ge=0, le=3650)
    workload_days: int = Field(ge=0, le=3650)
    available: bool = True


class AllocationProposal(BaseModel):
    task_id: str
    member_id: str | None = None
    score: float = Field(ge=0, le=1)
    reason: str = Field(min_length=1, max_length=1000)
    requires_approval: bool = True


class ScheduledTask(BaseModel):
    task_id: str
    start: date
    finish: date
    blocked: bool = False


class ScheduleResult(BaseModel):
    tasks: list[ScheduledTask]
    critical_tasks: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
