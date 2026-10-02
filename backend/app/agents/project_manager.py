from ..algorithms.dependencies import validate_dependencies
from ..schemas.contracts import ProjectAnalysis, ProjectInput, TaskDraft
from .base import BaseAgent


class ProjectManagerAgent(BaseAgent[ProjectInput, ProjectAnalysis]):
    name = "project_manager"
    system_prompt = (
        "Analyze project requirements. Return only validated structured data. "
        "Report uncertainty as open questions and never invent missing facts."
    )

    @property
    def model_name(self) -> str:
        return "controlled-mock"

    @property
    def is_mock(self) -> bool:
        return True

    def execute(self, input_data: ProjectInput) -> ProjectAnalysis:
        task = TaskDraft(
            task_id="requirements-analysis",
            title="Analyze project requirements",
            description=input_data.description,
            estimated_days=max(1, min(5, (len(input_data.description) // 500) + 1)),
            required_skills=["requirements-analysis"],
            acceptance_criteria=["Requirements are reviewed and documented"],
        )
        validate_dependencies([task.task_id], {task.task_id: task.dependencies})
        return ProjectAnalysis(
            summary=f"Structured analysis of {input_data.title}",
            functional_requirements=input_data.goals,
            non_functional_requirements=input_data.constraints,
            tasks=[task],
            assumptions=[
                "The supplied project description is the available source of truth."
            ],
            open_questions=["Which stakeholders must approve the task draft?"],
        )
