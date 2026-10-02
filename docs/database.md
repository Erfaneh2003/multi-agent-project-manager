# Database Status

PostgreSQL is the intended primary database and Docker Compose provisions it with a health check and persistent volume. SQLAlchemy models currently cover projects, tasks, teams, and team members. An initial Alembic migration has been executed successfully through upgrade, current, and downgrade against a local SQLite validation database.

The persistence phase still needs the remaining entities (users, skills, dependencies, assignments, comments, agent executions, decisions, reports, approvals, and audit logs), repositories, service transaction boundaries, and isolated PostgreSQL integration tests. Until those tests pass, full production persistence is an explicit remaining item rather than a claimed feature.
