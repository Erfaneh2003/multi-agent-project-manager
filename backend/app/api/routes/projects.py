from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import get_session
from ...repositories.projects import (
    create_project,
    delete_project,
    get_project,
    list_projects,
)
from ...schemas.projects import ProjectCreate, ProjectRead

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project_endpoint(
    payload: ProjectCreate,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ProjectRead:
    project = await create_project(session, payload)
    return ProjectRead.model_validate(project)


@router.get("", response_model=list[ProjectRead])
async def list_projects_endpoint(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[ProjectRead]:
    projects = await list_projects(session, offset, limit)
    return [ProjectRead.model_validate(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project_endpoint(
    project_id: UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ProjectRead:
    project = await get_project(session, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_endpoint(
    project_id: UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> None:
    project = await get_project(session, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    await delete_project(session, project)
