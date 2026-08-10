# AURA Forge Adaptive Routing

Version: `aura-router-v1`

## Purpose

AURA Forge adaptive routing selects the minimum justified execution route after the deterministic `aura-risk-v1` classifier assigns a change to `LOW`, `MEDIUM`, or `HIGH`.

The router is deterministic and model-free. It does not invoke agents, edit files, run tests, grant tools at runtime, approve work, or tune routes during measurement.

## Pre-AURA Fixed Route vs AURA Route Matrix

| Tier | Pre-AURA Fixed Route | AURA Route | Route ID | Model Roles | Human Gates | Project Manager |
|---|---|---|---|---:|---:|---|
| LOW | Planner -> Implementer -> Reviewer -> Tester -> Project Manager | Implementer -> Reviewer -> deterministic verification -> terminal readiness | `aura-low-v1` | 2 | 0 | No |
| MEDIUM | Planner -> Implementer -> Reviewer -> Tester -> Project Manager | Implementer -> Reviewer -> Tester -> Muhammad final approval -> terminal readiness | `aura-medium-v1` | 3 | 1 | No |
| HIGH | Planner -> Implementer -> Reviewer -> Tester -> Project Manager | Planner -> Muhammad plan approval -> Implementer -> Reviewer -> Tester -> deterministic policy/eval gates -> Muhammad final approval -> Project Manager | `aura-high-v1` | 5 | 2 | Yes |

The pre-AURA control route remains available for historical comparison and is not modified by the adaptive router.

## Route Matrix

| Tier | Purpose | Roles | Human Checkpoints | Deterministic Gates |
|---|---|---|---|---|
| LOW | Right-size non-executable, mechanically verifiable changes | Implementer, Reviewer | 0 | approved path scope, `git diff --check`, credential-pattern scan, scenario-specific checks, no executable or HIGH-sensitive paths |
| MEDIUM | Bounded executable or test work requiring implementation, review, and real test evidence | Implementer, Reviewer, Tester | 1 final readiness approval after Tester | approved path scope, `git diff --check`, credential-pattern scan, focused test evidence, no HIGH-sensitive paths |
| HIGH | Security, governance, CI, MCP, schema, credential, or policy-sensitive work | Planner, Implementer, Reviewer, Tester, Project Manager | 2: plan and final | approved path scope, `git diff --check`, credential-pattern scan, policy/eval gates, no permission widening |

## Tool Profiles

| Tier | Role | Intended Grants | Denied Boundaries |
|---|---|---|---|
| LOW | Implementer | bounded file reads, bounded writes only to scenario-approved LOW-safe paths | Planner, Tester model, Project Manager, task tracker, general shell, permission mutation |
| LOW | Reviewer | bounded read-only review | writes, task tracker, general shell, permission mutation |
| MEDIUM | Implementer | bounded reads and writes to approved MEDIUM paths | Planner, Project Manager, task tracker, permission mutation, production access |
| MEDIUM | Reviewer | bounded read-only review | writes, task tracker, general shell, permission mutation |
| MEDIUM | Tester | bounded focused test execution | writes, Project Manager, task tracker, production access |
| HIGH | Planner, Implementer, Reviewer, Tester, Project Manager | established governed role/tool map from the course governance policy | unrestricted shell, production access, and unapproved permission widening |

LOW and MEDIUM intentionally exclude the Project Manager tracker. HIGH keeps the established governed grants rather than introducing an unrestricted profile.

## Fail-Closed Behavior

The router fails closed when:

- the classifier tier is unknown or malformed;
- route metadata is malformed;
- scenario/path evidence is inconsistent;
- implementation expands into a higher-risk path than the frozen route.

The required output for a mid-run expansion is `ESCALATION REQUIRED`, including the original tier, newly observed evidence, and required higher tier. A measured run must not silently self-upgrade or tune the route.

## Why Each Tier Gets This Autonomy

LOW gets the smallest route because the locked LOW scenario is non-executable documentation. It still gets an Implementer because the document must actually be changed, and it still gets an independent Reviewer because semantic documentation claims can be wrong even when formatting checks pass.

MEDIUM drops Planner and Project Manager because the scenario already supplies bounded acceptance criteria and no tracker update is required. It keeps Implementer, Reviewer, Tester, and final human readiness approval because executable behavior and regression coverage require more judgment than documentation-only work.

HIGH remains fully governed because it touches policy, evaluation, MCP, CI, schema, credential, or security-sensitive surfaces. It keeps plan approval, final approval, deterministic policy/eval gates, and Project Manager closure. HIGH is not expected to become cheaper merely to show savings.

## Measurement Boundary

This document records structural route expectations only. It does not claim measured AURA savings. Measured results belong in `docs/capstone/aura-results.md` and the final control-vs-AURA comparison after post-AURA runs complete.
