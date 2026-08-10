# AURA Forge Baseline Method

## Before State

The before state is the existing pre-AURA engineering workflow before deterministic risk classification and adaptive routing.

## Current Executable Baseline Finding

Inspection found a real governed workflow, but it is not a general executable baseline path for the three capstone scenarios.

The existing workflow is fixed to controlled issue `COURSE-FITGPT-001` and the route:

Planner -> Human plan approval -> Implementer -> Reviewer -> Tester -> Human final approval -> Project Manager

The executable and evaluation artifacts are also fixed to the old backend onboarding documentation task:

- writable paths: `README.md`, `backend/.env.example`
- test target: `backend/tests/test_config_startup.py`
- issue: `COURSE-FITGPT-001`
- preserved normalized evidence under `.eval-artifacts/runs/dev/FITGPT-DEV-BASELINE-001/`
- deterministic and rubric evaluation entry points under `eval/`

That route does not currently accept arbitrary scenario definitions, risk tiers, or touched paths. Running the three representative scenarios through it would require new orchestration adaptation, which this milestone explicitly forbids.

Therefore, if no additional executable path is introduced in a later milestone, the pre-AURA baseline result for the three scenarios must be recorded as an executable-workflow gap, not as measured agent quality.

## Baseline Run Rule

For every executable baseline scenario, run the existing pre-AURA workflow once in a disposable local worktree. Do not tune between scenarios. Do not retry silently.

If an infrastructure, authentication, or workflow-fit failure prevents a meaningful run, preserve that evidence and classify the failure correctly.

## Metrics

### 1. Outcome Quality

Score the run with `docs/capstone/quality-rubric.md`.

Record:

- each dimension score;
- aggregate score out of `16`;
- pass or fail;
- evidence cited for each score.

### 2. Cycle Time

Start:

Initial workflow invocation.

End:

Final readiness result or terminal blocked result.

Record timestamps in UTC and elapsed seconds.

### 3. Review Latency

Start:

Implementation or handoff ready for Reviewer.

End:

Reviewer result produced.

Record `not available` if the run does not reach Reviewer.

### 4. Model Usage

Record:

- number of model or agent invocations;
- tokens if the runtime exposes reliable token counts.

If token counts are absent or not reliably tied to the run, record `not reliably measurable`.

### 5. Cost Per Run

Use real recorded model/provider cost if available.

If exact cost cannot be measured from real evidence, record `not reliably measurable` and explain why. Do not invent prices or estimated dollar values.

### 6. Human Checkpoints

Count explicit approvals and interventions.

Record whether each approval is current to the run, reused, missing, or not reached.

### 7. Tool Activity

Record:

- total relevant tool events;
- tool authorization denials;
- role associated with each relevant event;
- whether an event is actual, simulated, or unavailable.

### 8. Retries and Failures

Distinguish:

- engineered-system failure;
- infrastructure or model failure.

Do not count a blocked authentication or tool-exposure failure as an implementation-quality failure.

### 9. Route

Record the actual pre-AURA route taken.

Do not manually vary the route based on `LOW`, `MEDIUM`, or `HIGH` labels. The purpose is to observe the uniform pre-AURA behavior or its inability to run the scenario.

## Reproducibility Requirements

For each scenario preserve sanitized evidence under:

`.eval-artifacts/capstone/baseline/<scenario-id>/`

Each directory may contain:

- scenario definition or reference;
- normalized transcript, if a meaningful run exists;
- timing metrics;
- deterministic or evaluation output;
- rubric result;
- run metadata;
- failure classification where applicable.

Do not store secrets, authentication material, production data, or raw credentials.

## Required Result Summary

`docs/capstone/baseline-results.md` must summarize all three scenarios in one table with:

- scenario;
- expected tier;
- actual pre-AURA route;
- quality score;
- cycle time;
- review latency;
- agent/model invocations;
- cost if reliably measured;
- human checkpoints;
- notable failures;
- key observation.

The interpretation must answer only from measured evidence or preserved gap evidence:

1. Does the pre-AURA workflow treat all three scenarios similarly?
2. Does `LOW` appear over-served by the current agentic route?
3. Does `HIGH` receive enough additional governance/human treatment?
4. Which measured metric gives the strongest justification for adaptive routing?
5. What cannot yet be concluded?
