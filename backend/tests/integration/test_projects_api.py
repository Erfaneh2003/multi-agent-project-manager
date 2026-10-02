from collections.abc import AsyncGenerator
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from app.db.session import get_session
from app.main import app
from app.models import Base
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@pytest.fixture
def client() -> TestClient:
    with TemporaryDirectory() as directory:
        database_path = Path(directory) / "test.db"
        engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
        session_factory = async_sessionmaker(engine, expire_on_commit=False)

        async def setup() -> None:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

        async def override_session() -> AsyncGenerator[AsyncSession, None]:
            async with session_factory() as session:
                yield session

        import asyncio

        asyncio.run(setup())
        app.dependency_overrides[get_session] = override_session
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())


def test_project_crud_persists_data(client: TestClient) -> None:
    created = client.post(
        "/api/v1/projects",
        json={"title": "Stored project", "description": "Project description"},
    )

    assert created.status_code == 201
    project_id = created.json()["id"]
    assert client.get(f"/api/v1/projects/{project_id}").json()["title"] == (
        "Stored project"
    )
    assert len(client.get("/api/v1/projects").json()) == 1
    assert client.delete(f"/api/v1/projects/{project_id}").status_code == 204
    assert client.get(f"/api/v1/projects/{project_id}").status_code == 404


def test_task_crud_is_scoped_to_project(client: TestClient) -> None:
    project = client.post(
        "/api/v1/projects",
        json={"title": "Task project", "description": "Task description"},
    ).json()
    project_id = project["id"]
    created = client.post(
        f"/api/v1/projects/{project_id}/tasks",
        json={
            "title": "Implement API",
            "description": "Implement and test the task endpoint",
            "estimated_days": 3,
            "priority": "high",
        },
    )

    assert created.status_code == 201
    task_id = created.json()["id"]
    assert len(client.get(f"/api/v1/projects/{project_id}/tasks").json()) == 1
    updated = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"status": "in_progress"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"
    assert client.delete(f"/api/v1/tasks/{task_id}").status_code == 204


def test_team_member_lifecycle(client: TestClient) -> None:
    created_team = client.post("/api/v1/teams", json={"name": "Platform team"})

    assert created_team.status_code == 201
    team_id = created_team.json()["id"]
    created_member = client.post(
        f"/api/v1/teams/{team_id}/members",
        json={
            "name": "Ava",
            "experience_level": 7,
            "capacity_days": 20,
        },
    )

    assert created_member.status_code == 201
    member_id = created_member.json()["id"]
    assert len(client.get(f"/api/v1/teams/{team_id}/members").json()) == 1
    updated = client.put(
        f"/api/v1/team-members/{member_id}",
        json={"workload_days": 4},
    )
    assert updated.status_code == 200
    assert updated.json()["workload_days"] == 4
