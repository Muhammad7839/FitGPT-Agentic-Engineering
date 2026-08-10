# Pre-AURA Control Baseline Comparison

This comparison uses only measured PRE-AURA fixed-route control evidence from `AF-LOW-001`, `AF-MEDIUM-001`, and `AF-HIGH-001`. It does not claim any AURA Forge improvement yet.

All three scenarios used the same fixed route:

Planner -> Muhammad plan approval -> Implementer -> Reviewer -> Tester -> Muhammad final approval -> Project Manager

Disposable scenario implementations stayed outside `capstone/aura-forge` and were not merged.

## Summary Table

| Scenario | Expected Tier | Result Type | Quality Score | Outcome | Route | Governance | Evidence | Cost | Model Invocations | Model Duration | Human Checkpoints | Tool Events | Denials | Infrastructure Failures |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| AF-LOW-001 | LOW | Documentation checklist | 14/16 FAIL | 4/4 | 2/4 | 4/4 | 4/4 | $0.6066006 | 5 | 89,398 ms | 2 | 8 | 0 | MCP-blocked Planner $0.108051; Local-MCP Implementer retry $0.087951; auth failures $0 |
| AF-MEDIUM-001 | MEDIUM | Focused regression test | 15/16 PASS | 4/4 | 3/4 | 4/4 | 4/4 | $0.9093231 | 5 | 193,330 ms | 2 | 10 | 0 | Tester toolchain failure $0.1410483; repaired with locked `npm ci` |
| AF-HIGH-001 | HIGH | Governance policy test | 15/16 PASS | 4/4 | 3/4 | 4/4 | 4/4 | $1.1753241 | 5 | 248,666 ms | 2 | 28 | 0 | None in successful route |

## Findings

1. Was LOW over-served?

Yes. AF-LOW-001 was a non-executable documentation-only checklist update, but it still went through Planner, Implementer, Reviewer, Tester, two human checkpoints, and Project Manager. The result was correct and governed, but Route Appropriateness scored 2/4 because the route was materially heavier than needed for a single documentation file.

2. Was MEDIUM reasonably matched to the full route?

Mostly yes. AF-MEDIUM-001 involved executable web utility behavior and regression coverage, so implementation, review, and focused test evidence were justified. The full route still required two human checkpoints and Project Manager, so it was defensible rather than minimal. Route Appropriateness scored 3/4.

3. Was HIGH sufficiently protected by the same fixed route?

Yes for this measured scenario. AF-HIGH-001 touched evaluation and governance-policy enforcement, and the fixed route produced current plan approval, current final approval, bounded implementation scope, independent Reviewer verification of the real invariant, real policy/runtime tests, and Project Manager closure. Governance & Approval Fidelity scored 4/4. What remains unproven is whether the fixed route is sufficient for broader HIGH classes such as CI, auth, database migrations, or production deployment controls.

4. What did the fixed route cost for each tier?

| Tier | Scenario | Successful-Route Cost |
|---|---|---:|
| LOW | AF-LOW-001 | $0.6066006 |
| MEDIUM | AF-MEDIUM-001 | $0.9093231 |
| HIGH | AF-HIGH-001 | $1.1753241 |

The fixed route cost increased with task complexity in this sample, but every tier still paid for the same five model-role invocations and two human checkpoints.

5. Which steps appear wasteful for LOW?

For AF-LOW-001, Planner and the first human plan approval were heavier than the task required because the requested change was a bounded documentation update with a single allowed file. Tester and Project Manager also added overhead relative to simple documentation review, `git diff --check`, and credential-pattern scanning.

6. Which controls appear necessary for MEDIUM?

For AF-MEDIUM-001, Implementer, Reviewer, and focused test evidence were useful. The important engineering finding was that the production invariant already existed, so the correct change was test-only regression coverage. Reviewer and Tester helped preserve that restraint and avoid unnecessary source logic.

7. Which controls are essential or potentially insufficient for HIGH?

For AF-HIGH-001, plan approval, narrow scope, independent review, real deterministic tests, holdout checksum verification, and final human approval were essential. The Reviewer checkpoint was especially important because Muhammad explicitly required verification that the Planner's role-set invariant was real, not merely plausible.

Potential insufficiency remains outside this measured scenario: a future HIGH change touching CI deployment, auth, database schema, production configuration, or sandbox boundaries may require extra specialized checks beyond the fixed role sequence.

8. What evidence actually justifies adaptive autonomy?

The strongest evidence is the Route Appropriateness gap:

- LOW scored 2/4 on Route Appropriateness despite 4/4 outcome, governance, and evidence.
- MEDIUM and HIGH scored 3/4 because the same full route was defensible for executable and governance-sensitive work.
- All three tiers used five model invocations and two human checkpoints, even though LOW did not need that much control.

Cost and duration reinforce the same conclusion. The LOW route cost $0.6066006 and 89,398 ms for documentation-only work. That overhead is the clearest measured justification for deterministic adaptive routing.

9. What remains unproven?

This baseline does not prove that AURA Forge will improve outcomes or reduce cost. It only proves the fixed PRE-AURA route's behavior. It also does not prove that the HIGH route is sufficient for every sensitive class, nor that a deterministic classifier will always classify future tasks correctly. Those claims require later AURA Forge classifier and adaptive-routing evidence.

## Interpretation

The PRE-AURA fixed route is safe enough to complete all three representative scenarios, but it lacks risk-sensitive autonomy. LOW was over-served, MEDIUM was reasonably served, and HIGH was protected for the measured governance-test case. The next justified step is a deterministic, conservative risk classifier that can distinguish LOW, MEDIUM, and HIGH before any adaptive route selection is implemented.
