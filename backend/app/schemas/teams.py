from uuid import UUID

from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class TeamRead(TeamCreate):
    id: UUID

    model_config = {"from_attributes": True}


class TeamMemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    experience_level: int = Field(default=0, ge=0, le=10)
    capacity_days: int = Field(default=0, ge=0, le=3650)


class TeamMemberUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    experience_level: int | None = Field(default=None, ge=0, le=10)
    capacity_days: int | None = Field(default=None, ge=0, le=3650)
    workload_days: int | None = Field(default=None, ge=0, le=3650)


class TeamMemberRead(TeamMemberCreate):
    id: UUID
    team_id: UUID
    workload_days: int

    model_config = {"from_attributes": True}
