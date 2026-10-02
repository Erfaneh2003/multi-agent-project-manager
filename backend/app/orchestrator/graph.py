from dataclasses import asdict
from datetime import date
from typing import Any, Literal

from langgraph.graph import END, START, StateGraph

from ..agents.project_manager import ProjectManagerAgent
from ..agents.scheduler_tracker import SchedulerInput, SchedulerTrackerAgent
from ..agents.task_allocator import AllocationInput, TaskAllocationAgent
from ..schemas.contracts import TeamMemberProfile
from .state import WorkflowState


def validate_input(state: WorkflowState) -> WorkflowState:
    state["current_stage"] = "validated"
    state.setdefault("agent_errors", [])
    state.setdefault("agent_outputs", {})
    return state


def run_project_manager(state: WorkflowState) -> WorkflowState:
    output, metadata = ProjectManagerAgent().run(state["project_input"])
    state["analysis"] = output
    state["agent_outputs"]["project_manager"] = output.model_dump()
    state["execution_metadata"]["project_manager"] = asdict(metadata)
    state["current_stage"] = "draft_ready"
    return state


def route_after_approval(state: WorkflowState) -> Literal["allocate", "await_approval"]:
    if state.get("approval_status") == "approved":
        return "allocate"
    return "await_approval"


def await_approval(state: WorkflowState) -> WorkflowState:
    state["current_stage"] = "awaiting_human_approval"
    return state


def run_allocation(state: WorkflowState) -> WorkflowState:
    members = [
        TeamMemberProfile.model_validate(item) for item in state.get("team_members", [])
    ]
    output, metadata = TaskAllocationAgent().run(
        AllocationInput(tasks=state["analysis"].tasks, members=members)
    )
    state["allocation_proposals"] = output
    state["agent_outputs"]["task_allocator"] = [item.model_dump() for item in output]
    state["execution_metadata"]["task_allocator"] = asdict(metadata)
    state["current_stage"] = "allocation_ready"
    return state


def run_scheduler(state: WorkflowState) -> WorkflowState:
    output, metadata = SchedulerTrackerAgent().run(
        SchedulerInput(
            tasks=state["analysis"].tasks,
            start_date=state.get("start_date", date.today()),
        )
    )
    state["schedule"] = output
    state["agent_outputs"]["scheduler_tracker"] = output.model_dump()
    state["execution_metadata"]["scheduler_tracker"] = asdict(metadata)
    state["current_stage"] = "completed"
    return state


def build_workflow() -> Any:
    graph = StateGraph(WorkflowState)
    graph.add_node("validate_input", validate_input)
    graph.add_node("project_manager", run_project_manager)
    graph.add_node("await_approval", await_approval)
    graph.add_node("allocate", run_allocation)
    graph.add_node("schedule", run_scheduler)
    graph.add_edge(START, "validate_input")
    graph.add_edge("validate_input", "project_manager")
    graph.add_conditional_edges(
        "project_manager",
        route_after_approval,
        {"allocate": "allocate", "await_approval": "await_approval"},
    )
    graph.add_edge("await_approval", END)
    graph.add_edge("allocate", "schedule")
    graph.add_edge("schedule", END)
    return graph.compile()
