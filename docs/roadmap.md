# Implementation Roadmap

This roadmap follows the approved proposal and keeps the three-agent MVP as the delivery boundary.

## Phase 1: Baseline and Environment

- [x] Inspect the empty workspace and confirm no prior source or Git history.
- [x] Extract the proposal baseline into `docs/requirements.md`.
- [x] Initialize the local Git repository.
- [ ] Install and validate uv-managed Python 3.12.
- [ ] Create the project configuration, lockfile, ignore rules, and environment template.
- [ ] Add a minimal FastAPI health service and a focused smoke test.

## Phase 2: Architecture and Foundation

- [ ] Define domain contracts, enums, error types, and settings.
- [ ] Define SQLAlchemy models and Alembic migration strategy.
- [ ] Define repositories and application services behind interfaces.
- [ ] Document component, state, database, and approval flows.

## Phase 3: Deterministic Algorithms

- [ ] Dependency validation and cycle detection.
- [ ] Stable topological sort.
- [ ] Workload and allocation scoring.
- [ ] Capacity-aware deterministic scheduling.
- [ ] Critical path calculation.
- [ ] Unit tests for every algorithm and invalid input.

## Phase 4: MVP Agents and LLM Boundary

- [ ] Base agent contract with validation, logging, timing, errors, and usage metadata.
- [ ] Provider abstraction with controlled mock and OpenAI implementation.
- [ ] Project Manager Agent with structured draft output.
- [ ] Task Allocation Agent using deterministic feasibility and scoring.
- [ ] Scheduler and Tracker Agent using deterministic graph and scheduling logic.
- [ ] Independent agent tests, including invalid structured output.

## Phase 5: Orchestration and Human Approval

- [ ] Typed shared state.
- [ ] LangGraph nodes and conditional transitions.
- [ ] Retry and failure routing.
- [ ] Checkpoint/resume strategy.
- [ ] Persistent human approvals and controlled continuation/rejection.
- [ ] Workflow integration tests with the mock provider.

## Phase 6: API and Persistence

- [ ] Project, task, team, allocation, scheduling, agent, approval, and report endpoints.
- [ ] Pagination, filtering, validation, transaction boundaries, and safe error responses.
- [ ] Async execution tracking for workflow runs.
- [ ] PostgreSQL integration tests and migration checks.

## Phase 7: Streamlit Application

- [ ] API client and connection/error states.
- [ ] Dashboard and project/task/team views.
- [ ] Agent execution and human approval views.
- [ ] Scheduling, critical path, and report views.
- [ ] Persian/RTL-friendly labels where practical, without inventing data.

## Phase 8: Evaluation, Operations, and Documentation

- [ ] Eight proposal scenarios and reproducible metric definitions.
- [ ] Record only executed mock/live results.
- [ ] Dockerfile and Compose with PostgreSQL health checks.
- [ ] GitHub Actions with uv lock validation, Ruff, mypy, and tests.
- [ ] README and technical/user documentation.
- [ ] Final validation, Git status review, and Persian delivery report.

## Phase Gates

Each phase ends with a focused executable check. A later phase does not claim completion of an earlier phase's behavior without a passing check. Public GitHub publication and any live LLM usage remain approval-gated actions.
