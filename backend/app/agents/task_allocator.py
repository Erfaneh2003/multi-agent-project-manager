from ..algorithms.allocation import AllocationCandidate, select_candidate
from ..schemas.contracts import AllocationProposal, TaskDraft, TeamMemberProfile
from .base import BaseAgent


class AllocationInput:
    def __init__(
        self, tasks: list[TaskDraft], members: list[TeamMemberProfile]
    ) -> None:
        self.tasks = tasks
        self.members = members


class TaskAllocationAgent(BaseAgent[AllocationInput, list[AllocationProposal]]):
    name = "task_allocator"
    system_prompt = (
        "Propose assignments using only the supplied team data. Never exceed capacity "
        "and leave tasks unassigned when no feasible member exists."
    )

    @property
    def model_name(self) -> str:
        return "controlled-mock"

    @property
    def is_mock(self) -> bool:
        return True

    def execute(self, input_data: AllocationInput) -> list[AllocationProposal]:
        proposals: list[AllocationProposal] = []
        for task in input_data.tasks:
            candidates = []
            for member in input_data.members:
                skill_match = (
                    len(set(task.required_skills) & member.skills)
                    / len(task.required_skills)
                    if task.required_skills
                    else 1.0
                )
                candidates.append(
                    AllocationCandidate(
                        member_id=member.member_id,
                        skill_match=skill_match,
                        experience_match=min(member.experience_level / 10, 1.0),
                        available_capacity=max(
                            0.0,
                            min(
                                1.0,
                                (member.capacity_days - member.workload_days)
                                / max(task.estimated_days, 1),
                            ),
                        ),
                        workload_balance=max(
                            0.0,
                            1.0 - member.workload_days / max(member.capacity_days, 1),
                        ),
                    )
                )
            selected = select_candidate(candidates)
            proposals.append(
                AllocationProposal(
                    task_id=task.task_id,
                    member_id=selected.member_id if selected else None,
                    score=selected.score() if selected else 0.0,
                    reason=(
                        "Selected by deterministic skill and capacity score."
                        if selected
                        else "No available team member satisfies capacity constraints."
                    ),
                )
            )
        return proposals
