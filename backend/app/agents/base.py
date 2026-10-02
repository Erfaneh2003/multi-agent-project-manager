from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import perf_counter


@dataclass(frozen=True, slots=True)
class AgentExecution:
    agent_name: str
    duration_ms: float
    model_name: str
    is_mock: bool


class AgentError(RuntimeError):
    """Raised when an agent cannot produce a validated result."""


class BaseAgent[InputT, OutputT](ABC):
    name: str
    system_prompt: str

    def run(self, input_data: InputT) -> tuple[OutputT, AgentExecution]:
        started = perf_counter()
        try:
            output = self.execute(input_data)
        except Exception as error:
            raise AgentError(f"{self.name} failed: {error}") from error
        metadata = AgentExecution(
            agent_name=self.name,
            duration_ms=round((perf_counter() - started) * 1000, 3),
            model_name=self.model_name,
            is_mock=self.is_mock,
        )
        return output, metadata

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_mock(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def execute(self, input_data: InputT) -> OutputT:
        raise NotImplementedError
