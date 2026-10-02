from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, UUIDTimestampMixin


class Team(UUIDTimestampMixin, Base):
    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    members: Mapped[list["TeamMember"]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )


class TeamMember(UUIDTimestampMixin, Base):
    __tablename__ = "team_members"

    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    experience_level: Mapped[int] = mapped_column(default=0, nullable=False)
    capacity_days: Mapped[int] = mapped_column(default=0, nullable=False)
    workload_days: Mapped[int] = mapped_column(default=0, nullable=False)
    team: Mapped[Team] = relationship(back_populates="members")
