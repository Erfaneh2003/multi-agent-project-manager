# API

## `GET /health`

Returns `{ "status": "ok", "mode": "mock" }`.

## Project CRUD

- `POST /api/v1/projects`: persist a project in the configured SQLAlchemy database.
- `GET /api/v1/projects`: list projects with `offset` and `limit` pagination.
- `GET /api/v1/projects/{project_id}`: retrieve one project or return `404`.
- `DELETE /api/v1/projects/{project_id}`: delete one project or return `404`.

These endpoints are covered by a SQLite-backed integration test. PostgreSQL remains the intended deployment database.

## Task CRUD

- `POST /api/v1/projects/{project_id}/tasks`: create a task under an existing project.
- `GET /api/v1/projects/{project_id}/tasks`: list project tasks with pagination.
- `GET /api/v1/tasks/{task_id}`: retrieve one task.
- `PUT /api/v1/tasks/{task_id}`: update task fields and controlled status.
- `DELETE /api/v1/tasks/{task_id}`: delete a task.

## Team CRUD

- `POST /api/v1/teams`: create a team.
- `GET /api/v1/teams`: list teams with pagination.
- `POST /api/v1/teams/{team_id}/members`: add a member to an existing team.
- `GET /api/v1/teams/{team_id}/members`: list team members.
- `PUT /api/v1/team-members/{member_id}`: update member profile and workload.

## `POST /api/v1/projects/{project_id}/run-workflow`

Accepts a project input, optional team profiles, a start date, and `approval_status` (`pending` or `approved`). It returns the current workflow stage, structured analysis, allocation proposals, schedule, and non-sensitive execution metadata.

- `pending`: analysis is produced and the workflow stops at human approval.
- `approved`: the allocation and deterministic scheduling stages run.
- `400`: path and body project IDs differ.
- `422`: request contract validation fails.

The endpoint currently executes synchronously for the local MVP and uses the controlled mock agent mode. Background execution tracking and persistent approval records are planned with the database slice.
