from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, UUIDTimestampMixin


class Project(UUIDTimestampMixin, Base):
    __tablename__ = "projects"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Task(UUIDTimestampMixin, Base):
    __tablename__ = "tasks"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="backlog", nullable=False)
    priority: Mapped[str] = mapped_column(String(30), default="medium", nullable=False)
    estimated_days: Mapped[int] = mapped_column(nullable=False)
    project: Mapped[Project] = relationship(back_populates="tasks")
