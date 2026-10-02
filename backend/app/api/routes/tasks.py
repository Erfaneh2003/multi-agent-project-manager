from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import get_session
from ...repositories.projects import get_project
from ...repositories.tasks import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)
from ...schemas.tasks import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/api/v1", tags=["tasks"])


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_endpoint(
    project_id: UUID,
    payload: TaskCreate,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TaskRead:
    if await get_project(session, project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    task = await create_task(session, project_id, payload)
    return TaskRead.model_validate(task)


@router.get("/projects/{project_id}/tasks", response_model=list[TaskRead])
async def list_tasks_endpoint(
    project_id: UUID,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[TaskRead]:
    if await get_project(session, project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = await list_tasks(session, project_id, offset, limit)
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task_endpoint(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TaskRead:
    task = await get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskRead.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task_endpoint(
    task_id: UUID,
    payload: TaskUpdate,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TaskRead:
    task = await get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = await update_task(session, task, payload)
    return TaskRead.model_validate(updated)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> None:
    task = await get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await delete_task(session, task)
