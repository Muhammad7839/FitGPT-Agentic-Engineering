# Interview Talking Points

## What is AURA Forge?

AURA Forge is a governed engineering workflow around FitGPT. It looks at a proposed repository change, classifies the risk, chooses the right route, and leaves evidence that the route stayed inside policy.

## Why deterministic risk classification?

Risk routing needs to be reproducible. If a change touches `eval/`, MCP boundaries, CI, auth, secrets, or database/schema areas, the system should classify it as HIGH every time. A deterministic classifier makes that easy to test and audit.

## Why not an LLM classifier?

An LLM would add cost and variability to a policy decision. The classification rules are mostly path and metadata facts, so deterministic code is the better tool.

## Why keep HIGH expensive?

HIGH changes touch sensitive engineering controls. The goal is not to make every change cheaper. The goal is to remove overhead only where risk allows it. HIGH keeps Planner, human approvals, Tester, policy gates, and Project Manager because that is the safer route.

## How did you prevent tool overreach?

Roles have narrow tool grants. The real demo shows an `implementer` trying to use `task_tracker`, which is Project-Manager-only. The system denied it, no external state changed, and the denial is documented.

## What failed?

The first GitHub governance CI run failed because the evaluation job did not install `pytest`, and the audit job assumed an artifact that was skipped after the evaluation failure. I fixed the workflow, added focused regression coverage, and preserved the failed run and repaired run as evidence.

## How did CI improve?

CI became more than a test runner. It classifies changes, runs permanent policy tests, runs evaluation gates, checks pipeline integrity, handles optional advisory AI review safely, and builds an audit trail.

## Why Change Passport?

The Change Passport gives a reviewer one machine-checkable summary of risk tier, route, quality score, policy tests, approvals, CI fields, and evidence hashes. It reduces the chance that readiness is just a verbal claim.

## Why convert an agentic step to deterministic code?

One recurring check was stable: whether `DATABASE_URL` behavior was documented consistently across README, env template, implementation, and tests. That does not need a model. The deterministic version has `$0` model cost and is easier to rerun.

## What would you improve next?

I would add stricter sandbox network egress controls, stronger memory pruning evidence, and more representative scenarios before considering any production-adjacent use.

## What are the limitations?

The results are from three representative capstone scenarios, not a production rollout. The sandbox is bounded but not proven airtight on network egress. The final video and LaunchCode submission are human-only.

## What did you personally decide versus what agents executed?

I decided the project scope, the adaptive-autonomy thesis, the safety boundary against production deployment, and the final evidence standard. Agents helped execute bounded implementation, review, test, documentation, presentation packaging, and verification steps under those constraints.
