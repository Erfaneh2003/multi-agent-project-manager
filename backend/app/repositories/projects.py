from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.project import Project
from ..schemas.projects import ProjectCreate


async def create_project(session: AsyncSession, data: ProjectCreate) -> Project:
    project = Project(title=data.title, description=data.description)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def list_projects(
    session: AsyncSession, offset: int, limit: int
) -> list[Project]:
    result = await session.scalars(
        select(Project).order_by(Project.created_at.desc()).offset(offset).limit(limit)
    )
    return list(result)


async def get_project(session: AsyncSession, project_id: UUID) -> Project | None:
    return await session.get(Project, project_id)


async def delete_project(session: AsyncSession, project: Project) -> None:
    await session.delete(project)
    await session.commit()
