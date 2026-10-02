from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.team import Team, TeamMember
from ..schemas.teams import TeamCreate, TeamMemberCreate, TeamMemberUpdate


async def create_team(session: AsyncSession, data: TeamCreate) -> Team:
    team = Team(name=data.name)
    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team


async def list_teams(session: AsyncSession, offset: int, limit: int) -> list[Team]:
    result = await session.scalars(
        select(Team).order_by(Team.created_at.desc()).offset(offset).limit(limit)
    )
    return list(result)


async def get_team(session: AsyncSession, team_id: UUID) -> Team | None:
    return await session.get(Team, team_id)


async def create_member(
    session: AsyncSession, team_id: UUID, data: TeamMemberCreate
) -> TeamMember:
    member = TeamMember(team_id=team_id, **data.model_dump())
    session.add(member)
    await session.commit()
    await session.refresh(member)
    return member


async def list_members(session: AsyncSession, team_id: UUID) -> list[TeamMember]:
    result = await session.scalars(
        select(TeamMember)
        .where(TeamMember.team_id == team_id)
        .order_by(TeamMember.created_at.asc())
    )
    return list(result)


async def get_member(session: AsyncSession, member_id: UUID) -> TeamMember | None:
    return await session.get(TeamMember, member_id)


async def update_member(
    session: AsyncSession, member: TeamMember, data: TeamMemberUpdate
) -> TeamMember:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    await session.commit()
    await session.refresh(member)
    return member
