# Deterministic Algorithms

## Dependency Graph

Each task maps to prerequisite task IDs. Validation rejects unknown tasks and self-dependencies. DFS returns a concrete cycle path; topological sorting repeatedly selects sorted ready IDs, making equal-order cases reproducible.

## Allocation Score

For a candidate member, the score is:

$$S = 0.45M_s + 0.20M_e + 0.20C + 0.15B$$

where `M_s` is required-skill overlap, `M_e` is normalized experience, `C` is normalized remaining capacity, and `B` is workload balance. Candidates with no remaining capacity are infeasible. Ties are resolved by member ID.

## Scheduling

Tasks are emitted in stable topological order. A task starts at the requested project start date or after the latest prerequisite finish. Finish is start plus the deterministic duration in days. Cyclic graphs stop with a warning.

## Limitations

The current scheduler is dependency-aware but not yet a full resource-constrained parallel scheduler. Critical Path Method and persistent workload aggregation remain next implementation slices and are not presented as implemented.
