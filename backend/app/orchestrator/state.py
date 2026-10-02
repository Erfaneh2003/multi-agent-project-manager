from datetime import date
from typing import Any, TypedDict

from ..schemas.contracts import (
    AllocationProposal,
    ProjectAnalysis,
    ProjectInput,
    ScheduleResult,
)


class WorkflowState(TypedDict, total=False):
    project_id: str
    project_input: ProjectInput
    analysis: ProjectAnalysis
    allocation_proposals: list[AllocationProposal]
    schedule: ScheduleResult
    team_members: list[dict[str, Any]]
    approval_status: str
    current_stage: str
    agent_outputs: dict[str, object]
    agent_errors: list[str]
    execution_metadata: dict[str, object]
    start_date: date
