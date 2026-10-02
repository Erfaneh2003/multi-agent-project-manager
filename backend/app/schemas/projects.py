from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=20_000)


class ProjectRead(ProjectCreate):
    id: UUID
    status: str

    model_config = {"from_attributes": True}
