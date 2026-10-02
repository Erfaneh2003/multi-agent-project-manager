# Requirements Baseline

## Approved Project

- Persian title: مديريت پروژه هاي سازمان با استفاده از معماري چندعاملي
- English title: Intelligent Organizational Project Management Using a Multi-Agent Architecture Based on Large Language Models
- Source: approved undergraduate project proposal, Islamic Azad University, Najafabad, revision 1404.
- Target users: small and medium project-oriented software and knowledge-based teams.

## Problem and Product

The system is a web application that receives project requirements, decomposes them into executable tasks, proposes assignments using team skills and capacity, schedules and tracks work, and produces project reports. It uses a shared project state and a graph-based orchestrator to coordinate specialized agents.

The approved proposal explicitly positions the product as a researchable, extensible architecture rather than a replacement for existing tools. The core contribution is a hybrid agentic-deterministic design: LLMs handle language analysis and qualitative proposals, while deterministic algorithms enforce structural and computational constraints.

## Approved MVP Scope

The following three agents are complete MVP scope:

1. Project Manager Agent: analyze requirements and decompose a project into draft tasks, priorities, estimates, skills, acceptance criteria, dependencies, assumptions, and open questions.
2. Task Allocation Agent: propose task assignments using skill, experience, capacity, workload, availability, priority, and dependency constraints. It must leave tasks unassigned when no valid candidate exists.
3. Scheduler and Tracker Agent: validate dependencies, detect cycles, produce a deterministic schedule, track task states, identify delays and blocked tasks, and calculate the critical path when sufficient data exists.

The following agents are architectural extension points only and must not be presented as implemented unless independently developed and tested:

- Collaboration and Communication Agent
- Quality Assurance Agent
- Resource Management Agent

## Functional Requirements

- Manage projects, teams, members, skills, tasks, dependencies, assignments, comments, reports, agent executions, decisions, approvals, and audit records.
- Store generated tasks as drafts until human approval.
- Use structured Pydantic contracts for agent input and output.
- Use a provider abstraction for OpenAI and controlled mock execution.
- Coordinate the MVP agents through a LangGraph StateGraph and a shared state.
- Implement controlled retries, error capture, execution tracking, resumable workflow state, and human approval for sensitive proposals.
- Validate dependency references, self-dependencies, graph structure, cycles, allocation capacity, and schedule validity with deterministic code.
- Expose versioned FastAPI endpoints and a Streamlit dashboard backed by the API, not fabricated dashboard data.
- Provide scenario-based evaluation for simple, dependent, constrained, conflicting, time-limited, invalid-graph, ambiguous, and invalid-LLM-output cases.

## Non-functional Requirements

- Python 3.12 managed exclusively with uv.
- FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, LangGraph, OpenAI SDK, Streamlit, Plotly, pytest, Ruff, and mypy as appropriate.
- Clean boundaries between domain logic, persistence, API, LLM provider, orchestration, and presentation.
- Deterministic algorithms must be repeatable and testable.
- No secret in source, tests, logs, audit data, Docker images, or documentation.
- Explicit validation and error handling; no direct execution of untrusted LLM output.
- Structured logging and execution metadata without sensitive payloads.
- PostgreSQL is the primary database. Redis is optional and will be added only if a concrete need is demonstrated.
- The system must run in mock mode without an API key, while clearly labeling mock results.

## Proposal Technology Constraints

- Backend: Python, FastAPI, LangGraph, OpenAI SDK.
- Database: PostgreSQL; Redis only if needed.
- Frontend: Streamlit dashboard; React is not required.
- Infrastructure: Git/GitHub, Docker, optional Langfuse observability.
- Required research topics: multi-agent coordination patterns, LLM agent frameworks, structured output, function/tool calling, prompt/context management, and deterministic scheduling logic.

## Explicit Limitations and Assumptions

- Authentication and organization-level authorization are outside the confirmed proposal detail; the MVP will include a documented local-development access boundary and leave production identity integration as a security limitation unless implemented.
- A live OpenAI key is not assumed. All ordinary tests must use a mock provider; live LLM evaluation is optional and must be separately labeled.
- PostgreSQL-backed integration tests require a separate test database or Docker service. Unit tests must remain runnable without PostgreSQL.
- No performance, quality, or commercial claim may be reported without an executed experiment.
- The supplied proposal text is the requirements source available in this workspace; the original binary PDF is not stored locally.

## Acceptance Boundary

A capability is considered implemented only after code exists, focused tests execute successfully, and the relevant documentation describes the actual behavior. Conceptual extension points and unexecuted integrations remain explicitly marked as planned.
