# Agent, Skill, and Memory Reflection Evidence

This index surfaces existing run-review-fix-rerun evidence that was previously scattered across long iteration logs. It does not recreate missing history.

## Reflection 1: Automatic Project-Memory Startup

Before:

- Agent: `backend-config-docs-auditor v0.1.0`
- Fresh Run 1: `13/16`, Fail.
- Failure: startup discovery scored `1/4` because memory was not loaded before the first task.

Change:

- Agent updated to `v0.1.1` with a project-scoped `initialPrompt` that verifies repository identity, scans memory before reading it, and loads only indexed active entries.
- Fix commit: `733ceff5bbd7e6cf1e9107cee828df7b7a158731`.

Rerun:

- Fresh Run 2: `15/16`, Pass.
- Startup discovery improved to `4/4`; every binary safety gate passed.

Evidence: `docs/agents/persistent-memory/iteration-log.md`.

## Reflection 2: Focused Test Execution Permission

Before:

- Agent: `focused-test-verifier v0.1.0`.
- Run 1: `12/16`, Fail.
- Failure: Bash existed but was not preauthorized, so the approved pytest command never started.

Change:

- Agent updated to `v0.1.1` to require a narrow Read-and-Bash invocation contract without broadening repository authority.
- Fix commit: `bb04cce29de5d390f07745c892f32c7fdab05cb2`.

Rerun:

- Run 2: `14/16`, Pass.
- The exact command ran once, `7 passed`, permission denials changed from one to zero, cycle time changed from `13.56 s` to `10.88 s`, and displayed cost changed from `$0.1076885` to `$0.0744989`.

Evidence: `docs/agents/focused-test-verifier/iteration-log.md`.

## Reflection 3: Tester Output Contract Calibration

Before:

- Calibration `CAL-20260802-002` produced `PASS=6`, `FAIL=2`, `SKIP=3`, `ERROR=0` after the Tester used `## Status` instead of the required `## Result` and no valid controlled-ticket completion existed.

Change:

- The Tester output contract and deterministic schema coverage were tightened so the exact ordered headings and allowed result value became machine-checkable.

Rerun:

- The after-fix development result produced `PASS=8`, `FAIL=0`, `SKIP=4`, `ERROR=0`.
- The remaining skips are preserved unavailable evidence, not converted to passes.

Evidence: `docs/calibration-log.md`, `docs/calibration-answers.md`, `eval/test_deterministic.py`.

## Memory Review State

The project memory index currently has one active decision with a review date of `2026-10-30`, no archived entries, and no entry currently eligible for stale pruning. The reason no file was pruned is recorded here instead of inventing a stale-entry event.

Memory scope remains repository-specific in `.memory/SCOPE.md`. Secret-shaped memory is scanned before loading, and the historical controlled failure/remediation is preserved in `docs/agents/persistent-memory/iteration-log.md`.
