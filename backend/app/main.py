from datetime import date
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .api.routes.projects import router as projects_router
from .api.routes.tasks import router as tasks_router
from .api.routes.teams import router as teams_router
from .orchestrator.graph import build_workflow
from .schemas.contracts import ProjectInput, TeamMemberProfile


class WorkflowRequest(BaseModel):
    project_id: str = Field(min_length=1, max_length=100)
    project: ProjectInput
    team_members: list[TeamMemberProfile] = Field(default_factory=list, max_length=500)
    approval_status: str = Field(default="pending", pattern="^(pending|approved)$")
    start_date: date = date.today()


class WorkflowResponse(BaseModel):
    project_id: str
    current_stage: str
    analysis: dict[str, Any] | None = None
    allocation_proposals: list[dict[str, Any]] = Field(default_factory=list)
    schedule: dict[str, Any] | None = None
    execution_metadata: dict[str, Any] = Field(default_factory=dict)


app = FastAPI(
    title="Intelligent Organizational Project Management",
    version="0.1.0",
    description="Research MVP for hybrid multi-agent project management.",
)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(teams_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "mock"}


@app.post("/api/v1/projects/{project_id}/run-workflow", response_model=WorkflowResponse)
def run_workflow(project_id: str, request: WorkflowRequest) -> WorkflowResponse:
    if project_id != request.project_id:
        raise HTTPException(
            status_code=400,
            detail="Path project_id must match request project_id",
        )
    result = build_workflow().invoke(
        {
            "project_id": project_id,
            "project_input": request.project,
            "team_members": [member.model_dump() for member in request.team_members],
            "approval_status": request.approval_status,
            "start_date": request.start_date,
            "execution_metadata": {},
        }
    )
    analysis = result.get("analysis")
    schedule = result.get("schedule")
    return WorkflowResponse(
        project_id=project_id,
        current_stage=result["current_stage"],
        analysis=analysis.model_dump() if analysis else None,
        allocation_proposals=[
            item.model_dump() for item in result.get("allocation_proposals", [])
        ],
        schedule=schedule.model_dump() if schedule else None,
        execution_metadata=result.get("execution_metadata", {}),
    )
