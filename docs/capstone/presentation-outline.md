# Presentation Outline

## Slide 1 - AURA Forge

Message: Governed adaptive engineering for FitGPT.

Visual: Title plus one-line thesis.

Evidence: `README.md`.

Speaker notes: Introduce AURA Forge as an engineering system, not a consumer feature.

## Slide 2 - Problem: Fixed Autonomy Is Wasteful or Risky

Message: One route for every change either over-serves low-risk work or under-governs sensitive work.

Visual: Fixed-route chain.

Evidence: `docs/capstone/control-baseline-results.md`.

Speaker notes: Explain the PRE-AURA route.

## Slide 3 - Baseline Architecture

Message: The control route uses full governance for LOW, MEDIUM, and HIGH.

Visual: Planner -> approval -> Implementer -> Reviewer -> Tester -> approval -> Project Manager.

Evidence: `docs/capstone/pre-aura-control-harness.md`.

Speaker notes: Baseline was safe but not adaptive.

## Slide 4 - Risk Classifier and Adaptive Routes

Message: Deterministic risk classification selects the minimum justified route.

Visual: LOW/MEDIUM/HIGH route comparison.

Evidence: `eval/risk_classifier.py`, `eval/adaptive_router.py`.

Speaker notes: Router was frozen before measuring AURA.

## Slide 5 - Experimental Design

Message: Three representative scenarios compared fixed route vs AURA route.

Visual: Scenario table.

Evidence: `docs/capstone/representative-scenarios.md`.

Speaker notes: Emphasize measured-only claims.

## Slide 6 - Measured Results

Message: AURA improved quality while reducing cost and governance overhead where risk allowed it.

Visual: Before/after chart from `docs/capstone/control-vs-aura-impact.md`.

Evidence: `docs/capstone/control-vs-aura-impact.md`.

Speaker notes: LOW big reduction, MEDIUM moderate reduction, HIGH governance preserved.

## Slide 7 - Governance and CI

Message: Safety is enforced by MCP policy and real GitHub CI.

Visual: CI governance flow.

Evidence: `docs/capstone/governance-ci-results.md`, `docs/capstone/governance-overreach-demo.md`.

Speaker notes: Show overreach denial and terminal CI run.

## Slide 8 - Change Passport and Right-Tool Conversion

Message: Evidence is machine-readable, and stable factual work moved from agent to deterministic code.

Visual: Passport evidence flow.

Evidence: `docs/capstone/evidence/change-passport-AF-HIGH-001.json`, `docs/capstone/deterministic-conversion.md`.

Speaker notes: Explain why not everything should be agentic.

## Slide 9 - Iteration and Failure Story

Message: The system improved through preserved failures, diagnosis, and repair.

Visual: Failure -> diagnosis -> fix -> green CI timeline.

Evidence: `docs/capstone/iteration-narrative.md`.

Speaker notes: Include failed CI run `31512923419` and repair `92d60c4`.

## Slide 10 - Takeaways and Limitations

Message: Adaptive autonomy works in the measured capstone scenarios, but this is not a production deployment.

Visual: Final metrics and safety boundary.

Evidence: `docs/capstone/final-evidence-snapshot.md`.

Speaker notes: End with measured-only claims and human-only submission tasks.
