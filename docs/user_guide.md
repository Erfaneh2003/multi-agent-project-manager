# User Guide

1. Copy `.env.example` to `.env` only when local configuration is needed. A live OpenAI key is not required for mock mode.
2. Start the API with `uv run uvicorn app.main:app --app-dir backend --reload`.
3. Open the FastAPI documentation at `http://localhost:8000/docs`.
4. Start the dashboard with `uv run streamlit run frontend/app.py`.
5. Submit a project with approval set to `pending` to inspect the draft and stop for review.
6. Re-run with `approved` only after reviewing the draft. The API then returns allocation proposals and a deterministic schedule.

The current dashboard is a research MVP. Persistent project editing, approval history, reports, and PostgreSQL repositories are planned for the next implementation phase.
