from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AllocationWeights:
    skill_match: float = 0.45
    experience_match: float = 0.2
    available_capacity: float = 0.2
    workload_balance: float = 0.15


@dataclass(frozen=True, slots=True)
class AllocationCandidate:
    member_id: str
    skill_match: float
    experience_match: float
    available_capacity: float
    workload_balance: float

    def score(self, weights: AllocationWeights | None = None) -> float:
        weights = weights or AllocationWeights()
        values = (
            self.skill_match,
            self.experience_match,
            self.available_capacity,
            self.workload_balance,
        )
        weight_values = (
            weights.skill_match,
            weights.experience_match,
            weights.available_capacity,
            weights.workload_balance,
        )
        weighted = sum(
            value * weight for value, weight in zip(values, weight_values, strict=True)
        )
        return round(weighted, 6)


def select_candidate(
    candidates: list[AllocationCandidate],
    weights: AllocationWeights | None = None,
) -> AllocationCandidate | None:
    weights = weights or AllocationWeights()
    feasible = [
        candidate for candidate in candidates if candidate.available_capacity > 0
    ]
    if not feasible:
        return None
    return max(
        feasible,
        key=lambda candidate: (candidate.score(weights), candidate.member_id),
    )
