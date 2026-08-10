# AURA Forge PRD

## Product

AURA Forge is Governed Adaptive Engineering for FitGPT.

## Thesis

AURA Forge deterministically determines how much autonomy a routine FitGPT engineering change deserves, routes the change through only the necessary combination of deterministic checks, specialized agents, least-privilege MCP tools, evaluation, and human approvals, and produces machine-verifiable evidence of what happened.

The system does not automate every possible software-engineering activity. It governs a bounded class of routine engineering changes inside the isolated FitGPT Agentic Engineering course repository.

## Stakeholder

The stakeholder is the FitGPT repository maintainer or software engineer responsible for safely reviewing and integrating routine engineering changes.

## Bounded Workflow

The workflow covers routine engineering changes proposed against the isolated FitGPT Agentic Engineering course repository.

## Trigger

A bounded engineering change request is submitted with a clear intended outcome and acceptance criteria.

## Inputs

- Change request.
- Repository state.
- Changed or touched paths where known.
- Existing tests.
- Governance and policy metadata.
- Risk-sensitive path information.

## Decision Events

1. Intake verifies that the request is in scope and not a production or live-user operation.
2. Deterministic risk rules classify the request as `LOW`, `MEDIUM`, or `HIGH`.
3. The selected route is chosen from the risk tier and path metadata.
4. Human approval gates are required when the route calls for implementation approval, final approval, or sensitive-boundary approval.
5. Verification evidence determines whether the change is ready, blocked, or rejected.

## Actions

- Inspect bounded repository context.
- Apply deterministic policy and path rules.
- Select the minimum justified route.
- Run deterministic checks when they are sufficient.
- Delegate to specialized agents only when judgment or implementation is required.
- Use least-privilege MCP grants for the selected role.
- Preserve transcript, tool, timing, test, approval, and policy evidence.
- Produce a final readiness recommendation.

## Outputs

- Risk classification eventually produced by AURA Forge.
- Selected execution route.
- Implementation or deterministic result, as appropriate.
- Test and evaluation evidence.
- Policy and governance outcome.
- Required human approval outcome.
- Final readiness recommendation.
- Later Change Passport.

## Risk Tiers

AURA Forge uses exactly three risk tiers: `LOW`, `MEDIUM`, and `HIGH`.

The classifier is deterministic. It does not use an LLM to decide risk.

Precedence is strict:

1. `HIGH` rules outrank `MEDIUM`.
2. `MEDIUM` rules outrank `LOW`.
3. A request is `LOW` only when no `MEDIUM` or `HIGH` rule matches.

### LOW

`LOW` changes are non-executable, outside governance/security/CI/agent/tool definitions, mechanically checkable, and unlikely to affect runtime behavior.

Examples include useful documentation or onboarding consistency changes in non-governance documents.

### MEDIUM

`MEDIUM` changes are normal application or test implementation changes. They may alter executable code and require engineering judgment, but they do not touch authentication, authorization, database schema or migration behavior, CI, governance policy, MCP permission boundaries, agent permission definitions, sandbox boundaries, or evaluation enforcement logic.

### HIGH

`HIGH` changes touch sensitive areas, including:

- Authentication or authorization.
- Database schema or migration behavior.
- Environment or secret handling.
- `.github/workflows/**`.
- Governance policy.
- MCP allow-lists.
- MCP server contracts.
- Agent permission definitions.
- Sandbox or container security boundaries.
- Evaluation or policy enforcement logic.

`HIGH` changes must not weaken production security.

## Expected Routes

The exact implementation route is deferred to the later AURA Forge classifier and router milestone. The design intent is:

- `LOW`: deterministic checks and lightweight review evidence, with no implementation agent when a mechanical doc-only change is sufficient.
- `MEDIUM`: bounded implementation, focused tests, review, and readiness evidence.
- `HIGH`: bounded implementation plus stricter governance review, policy checks, sensitive-path evidence, and explicit human approval before readiness.

## Measurable Acceptance Criteria

- The request is classified into exactly one of `LOW`, `MEDIUM`, or `HIGH`.
- The selected route follows deterministic precedence and documented path rules.
- The route grants no role more authority than the tier requires.
- All changed paths are recorded.
- Relevant tests and policy checks are recorded with pass, fail, skip, or blocked status.
- Human approvals are recorded only when explicit and current to the run.
- The final result includes a readiness recommendation backed by evidence.
- No production deployment, production data, production secrets, or live-user operation occurs.

## Failure Modes

- Request is out of scope or lacks acceptance criteria.
- Risk tier is ambiguous because path or intent information is incomplete.
- A role attempts a denied tool.
- A human approval is missing, stale, or reused.
- Tests fail or cannot be run in the isolated environment.
- Evidence is incomplete or unsanitized.
- The route changes because of manual judgment instead of deterministic rules.
- The workflow contacts production or requires production secrets.
- The existing pre-AURA workflow cannot execute the representative scenario safely.

## Demo Requirements

- Show one representative scenario per risk tier.
- Show the deterministic risk explanation for each scenario.
- Show the selected route and why it is the minimum justified route.
- Show tests, policy checks, approvals, and final readiness evidence.
- Show that artifacts are sanitized and tied to local repository state.
- Show the before-state baseline or a documented executable-workflow gap before claiming improvement.

## Hard Exclusions

- Production deployment.
- Live-user operations.
- Destructive production testing.
- Unrestricted arbitrary engineering work.
- Changes to the protected original FitGPT repository.
- Access to production databases.
- Use of real user data.
- Use of production secrets.
- Contact with FitGPT production, Render, Vercel, or production data services.

## Current Pre-AURA Workflow Finding

The inspected pre-AURA workflow is a fixed course workflow for controlled issue `COURSE-FITGPT-001`. It routes through Planner, human plan approval, Implementer, Reviewer, Tester, human final approval, and Project Manager. It is not currently a general executable route for arbitrary routine engineering changes.

The current evaluation harness can normalize and score preserved `COURSE-FITGPT-001` evidence. It cannot truthfully score fresh capstone representative scenarios without either a compatible fresh transcript or new adaptation work.

## Why AURA Forge Instead of Simpler Alternatives

### One Generic Coding Agent

A generic coding agent is flexible, but it does not by itself provide controlled routing, least-privilege specialization, evidence discipline, or risk-sensitive human gates. It can implement a change, but it does not make autonomy explicit or prove that a low-risk documentation change received less authority than a high-risk governance change.

### One Fixed Deterministic CI Pipeline

Fixed deterministic automation is excellent for predictable rules, repeatable tests, linting, and policy checks. It cannot perform open-ended planning, implementation, review, or tradeoff analysis where engineering judgment is required. It also cannot decide when human approval is required unless those rules are encoded somewhere else.

### Existing Uniform Multi-Agent Orchestration

The existing uniform route provides specialization and role boundaries, but it spends roughly the same agentic effort and governance path regardless of change risk. The current route is also tied to one controlled documentation issue, which limits reuse for routine engineering changes.

### AURA Forge

AURA Forge uses deterministic rules to choose the minimum justified combination of deterministic automation, agents, and humans. The expected value is not claimed as measured savings yet. The baseline must first show what the pre-AURA workflow can and cannot measure.
