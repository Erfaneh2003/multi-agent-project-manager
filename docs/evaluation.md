# Evaluation Plan

The proposal requires reproducible scenarios for simple projects, dependent tasks, resource constraints, allocation conflicts, time constraints, invalid graphs, ambiguous requirements, and invalid LLM output.

## Current Executed Result

The local deterministic and workflow test suite was executed with the controlled mock provider: 10 tests passed. This is a software correctness result, not a claim about LLM quality or production performance.

## Metrics

- Dependency validation accuracy: valid or invalid graph decisions divided by labeled graph cases.
- Assignment validity: feasible proposals divided by all assigned proposals.
- Skill matching: assigned required skills divided by required skills.
- Schedule validity: scheduled tasks respecting all prerequisites divided by scheduled tasks.
- Structured output validity: schema-valid outputs divided by provider outputs.
- Workflow success rate: completed workflows divided by started workflows.
- Response time: wall-clock duration captured in `AgentExecution`.
- Token consumption and cost: recorded only when a live provider supplies usage data.

Live-model metrics and mock metrics must remain separate. No quality or cost figure is reported until that experiment is executed and its inputs are stored.
