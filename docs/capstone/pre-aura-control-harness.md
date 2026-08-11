# Pre-AURA Fixed-Route Control Harness

## Purpose

The pre-AURA control harness is an experimental baseline instrument. It lets the existing fixed legacy route accept a bounded scenario definition instead of being hard-coded to `COURSE-FITGPT-001`.

It is not AURA Forge routing. It does not classify risk, adapt the route, implement the Change Passport, or change CI/CD.

## Fixed Route

Every scenario receives the same route:

Planner -> human plan approval -> Implementer -> Reviewer -> Tester -> human final approval -> Project Manager

The route is invariant to `LOW`, `MEDIUM`, or `HIGH` metadata. Risk labels may be stored as measurement metadata, but they are not runtime decision inputs.

## Input Contract

The input contains only the fields needed for a bounded engineering task:

- `scenario_id`
- `request`
- `acceptance_criteria`
- `worktree`
- `relevant_paths`
- optional `risk_label` for measurement metadata only

The worktree must be under a disposable sibling control worktree named `aura-forge-control`.

The primary capstone worktree is rejected as a scenario execution target.

## Output Contract

The control contract preserves:

- fixed role order;
- plan and final human checkpoints;
- tool grants;
- scenario request;
- acceptance criteria;
- allowed scenario worktree;
- relevant bounded paths;
- measurement metadata;
- explicit statement that risk metadata was not used for routing.

Live runs must preserve:

- role events;
- tool events;
- approval events;
- timestamps;
- final status;
- test evidence;
- authorization denials;
- infrastructure failures;
- transcript or evidence location.

If exact model usage or cost is available from the actual runtime, preserve it. If not reliably available, record `not reliably measurable`.

## Existing Mechanism Classification

Generic already:

- role order;
- two human checkpoints;
- least-privilege course-tool grants;
- handoff templates;
- transcript event concepts;
- deterministic policy tests;
- fixed container role launcher.

Hard-coded to `COURSE-FITGPT-001`:

- agent prompt descriptions;
- controlled issue identity;
- approved writable paths in the old workflow;
- focused test target;
- Project Manager ticket target;
- preserved transcript normalization for the old run.

Simulated or dummy infrastructure:

- `mcp/coursetools_server.py` is a course-only MCP server;
- `mcp__coursetools__test_runner` returns a bounded dummy test result;
- `mcp__coursetools__task_tracker` simulates ticket update behavior;
- old transcript evidence contains preserved and normalized events rather than a generic live runner.

Real executable runtime:

- Docker-based role container launcher;
- MCP server import and allow-list enforcement;
- Python deterministic tests;
- read-only workspace enforcement;
- local Git worktree isolation.

## Minimal Generalization

The implementation adds `eval/pre_aura_control.py`, which validates scenario input and emits the invariant fixed-route contract. It does not run agents by itself and does not change tool grants.

The key regression property is:

`Control route is invariant to risk label.`
