from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.project import Task
from ..schemas.tasks import TaskCreate, TaskUpdate


async def create_task(
    session: AsyncSession, project_id: UUID, data: TaskCreate
) -> Task:
    task = Task(project_id=project_id, **data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def list_tasks(
    session: AsyncSession, project_id: UUID, offset: int, limit: int
) -> list[Task]:
    result = await session.scalars(
        select(Task)
        .where(Task.project_id == project_id)
        .order_by(Task.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(result)


async def get_task(session: AsyncSession, task_id: UUID) -> Task | None:
    return await session.get(Task, task_id)


async def update_task(session: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task: Task) -> None:
    await session.delete(task)
    await session.commit()
