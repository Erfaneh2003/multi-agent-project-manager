# Intelligent Organizational Project Management

This repository implements the first executable MVP of the approved undergraduate project proposal: a hybrid multi-agent project-management system for small and medium software teams.

## MVP Scope

The current slice contains three tested agents: Project Manager, Task Allocation, and Scheduler & Tracker. LangGraph coordinates them through typed shared state. LLM-style analysis is isolated behind agent contracts; dependency validation, allocation feasibility, and scheduling are deterministic. Human approval is an actual workflow gate.

The current provider is a clearly labeled controlled mock. PostgreSQL and Docker configuration are included, while persistent repositories and migrations remain an explicit next phase.

## Setup with uv

```powershell
uv sync --locked
uv run pytest -q
uv run ruff check .
uv run mypy backend/app
```

## Run

```powershell
uv run uvicorn app.main:app --app-dir backend --reload
uv run streamlit run frontend/app.py
```

The API is documented at `http://localhost:8000/docs`. Copy `.env.example` to `.env` only when local configuration is needed. Never commit `.env` or an API key.

## Docker

```powershell
docker compose up --build
```

## Documentation

- [Requirements baseline](docs/requirements.md)
- [Implementation roadmap](docs/roadmap.md)
- [Architecture](docs/architecture.md)
- [Algorithms](docs/algorithms.md)
- [API](docs/api.md)
- [Database status](docs/database.md)
- [Evaluation](docs/evaluation.md)
- [User guide](docs/user_guide.md)

## Verification

The current local suite has 10 passing tests covering deterministic algorithms, schema validation, the StateGraph approval gate, and FastAPI workflow endpoints. These results do not claim live LLM quality, PostgreSQL persistence, or production security.
