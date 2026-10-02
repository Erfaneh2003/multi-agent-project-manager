from datetime import date

from app.orchestrator.graph import build_workflow
from app.schemas.contracts import ProjectInput


def base_state(approval_status: str) -> dict:
    return {
        "project_id": "demo-project",
        "project_input": ProjectInput(
            title="Internal planning tool",
            description=(
                "A tool for planning software project work and tracking progress."
            ),
            goals=["Track work"],
        ),
        "team_members": [],
        "approval_status": approval_status,
        "start_date": date(2026, 1, 1),
        "execution_metadata": {},
    }


def test_workflow_stops_for_human_approval() -> None:
    result = build_workflow().invoke(base_state("pending"))

    assert result["current_stage"] == "awaiting_human_approval"
    assert "analysis" in result
    assert "allocation_proposals" not in result


def test_approved_workflow_runs_all_mvp_agents() -> None:
    result = build_workflow().invoke(base_state("approved"))

    assert result["current_stage"] == "completed"
    assert len(result["allocation_proposals"]) == 1
    assert len(result["schedule"].tasks) == 1
