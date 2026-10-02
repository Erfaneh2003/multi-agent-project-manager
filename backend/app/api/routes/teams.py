from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import get_session
from ...repositories.teams import (
    create_member,
    create_team,
    get_member,
    get_team,
    list_members,
    list_teams,
    update_member,
)
from ...schemas.teams import (
    TeamCreate,
    TeamMemberCreate,
    TeamMemberRead,
    TeamMemberUpdate,
    TeamRead,
)

router = APIRouter(prefix="/api/v1", tags=["teams"])


@router.post("/teams", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team_endpoint(
    payload: TeamCreate,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TeamRead:
    return TeamRead.model_validate(await create_team(session, payload))


@router.get("/teams", response_model=list[TeamRead])
async def list_teams_endpoint(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[TeamRead]:
    teams = await list_teams(session, offset, limit)
    return [TeamRead.model_validate(team) for team in teams]


@router.post(
    "/teams/{team_id}/members",
    response_model=TeamMemberRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_member_endpoint(
    team_id: UUID,
    payload: TeamMemberCreate,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TeamMemberRead:
    if await get_team(session, team_id) is None:
        raise HTTPException(status_code=404, detail="Team not found")
    member = await create_member(session, team_id, payload)
    return TeamMemberRead.model_validate(member)


@router.get("/teams/{team_id}/members", response_model=list[TeamMemberRead])
async def list_members_endpoint(
    team_id: UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[TeamMemberRead]:
    if await get_team(session, team_id) is None:
        raise HTTPException(status_code=404, detail="Team not found")
    members = await list_members(session, team_id)
    return [TeamMemberRead.model_validate(member) for member in members]


@router.put("/team-members/{member_id}", response_model=TeamMemberRead)
async def update_member_endpoint(
    member_id: UUID,
    payload: TeamMemberUpdate,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TeamMemberRead:
    member = await get_member(session, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Team member not found")
    updated = await update_member(session, member, payload)
    return TeamMemberRead.model_validate(updated)
