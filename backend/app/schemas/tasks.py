from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

TaskStatus = Literal[
    "backlog",
    "todo",
    "in_progress",
    "blocked",
    "in_review",
    "done",
    "cancelled",
]
TaskPriority = Literal["low", "medium", "high", "critical"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=20_000)
    estimated_days: int = Field(gt=0, le=365)
    priority: TaskPriority = "medium"


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=20_000)
    estimated_days: int | None = Field(default=None, gt=0, le=365)
    priority: TaskPriority | None = None
    status: TaskStatus | None = None


class TaskRead(TaskCreate):
    id: UUID
    project_id: UUID
    status: TaskStatus

    model_config = {"from_attributes": True}
