# FitGPT Two-Layer Evaluation Baseline

## Objective

This exercise adapts the course's two-layer evaluation harness to FitGPT's
five-role orchestration workflow. The first layer checks objective transcript
facts. The second layer uses four isolated Claude judge calls to assess the
quality of the recorded outputs only after the deterministic gate opens.

## Locked holdout set

- File: `docs/holdout-task-set.md`
- Task count: 7
- Lock commit: `e4fbc54d977fb2a195378527f3b1583cb8ac1692`
- SHA-256: `e3aa9cdcec7b643507b7dd6f03ea15d92cfb6ed5fcacc4f56f5b2a8631631f32`

The holdout tasks were committed before the harness was adapted. Their
checksum remained unchanged throughout this exercise, and none of the holdout
tasks was executed. They are reserved for the later calibration lab.

## Course starters and Module 1 rubric

The following read-only course starters were copied before adaptation:

- `/Users/muhammad/LaunchCodeAgenticEngineer/module_3/eval/test_deterministic.py`
- `/Users/muhammad/LaunchCodeAgenticEngineer/module_3/eval/test_rubric_suite.py`
- `/Users/muhammad/LaunchCodeAgenticEngineer/module_3/eval/rubric.json`

The scoring dimensions come from `docs/rubric.md`. Its dimension source is
commit `276feaf242ebd975f59cf9d898ebdc0db9d96fb7`, its scoring source is commit
`fea2c581d9f47f982c813a3212d1cee16dcdd1a4`, and its prior scored uses appear
in `docs/iteration-log.md`.

## Evidence model

The normalized schema records the run and task identifiers, evidence origin,
expected role path, approved and changed paths, protected-state result, exact
human approvals, event sequence, role version, exact handoff text, structured
handoff fields, substantive role output, structured output document, tool
arguments and results, actual-versus-simulated classification, source hashes,
historical attempts, claims, budgets, and limitations.

The evidence trust order is controlled-tool response, Claude stream-json tool
event, Git manifest, normalized field derived from preserved evidence, then
natural-language summary. Unsupported prose is not converted into a tool
event.

## Development baseline

- Run ID: `FITGPT-DEV-BASELINE-001`
- Development task: `COURSE-FITGPT-001`
- Evidence directory:
  `.eval-artifacts/runs/dev/FITGPT-DEV-BASELINE-001/`
- Transcript:
  `.eval-artifacts/runs/dev/FITGPT-DEV-BASELINE-001/transcript.json`
- Equivalent audit evidence:
  `.eval-artifacts/runs/dev/FITGPT-DEV-BASELINE-001/tool-events.jsonl`
- Manifest and checksums: `manifest-before.json`, `manifest-after.json`, and
  `checksums.txt` in the same directory

The baseline was normalized directly from preserved Runs 3, 4, and 5. No role
or controlled tool was replayed. The selected path uses Planner, Implementer,
and Reviewer from Run 3 and Tester plus Project Manager from Run 5. The blocked
Run 3 and Run 4 Tester attempts remain in `historical_attempts`.

The normalized transcript contains 23 events: 5 selected role events, 16 tool
events, and 2 human approvals. Repository manifests before and after
normalization are identical.

## Deterministic results

| Check | Status | Result |
|---|---|---|
| Transcript schema | PASS | Required fields exist and all 23 event sequences are valid. |
| Routing and role order | PASS | Planner → Implementer → Reviewer → Tester → Project Manager appeared exactly once and in order. |
| Tool authorization | PASS | All 16 recorded tool attempts fit the caller's grant. |
| Handoff schema | PASS | Every selected role has required non-empty fields and substantive output. |
| Protected scope | PASS | Only `README.md` and `backend/.env.example` were changed in the preserved workflow; protected manifests match. |
| Human approvals | PASS | `APPROVE_RUN3_PLAN` and `APPROVE_RUN5_FINAL` are unreused, correctly bound, and correctly sequenced. |
| Controlled test evidence | PASS | One actual preserved dummy `test_runner` event targets `backend/tests/test_config_startup.py`; it is explicitly not real pytest. |
| Controlled ticket | PASS | One successful Project Manager event targets only `COURSE-FITGPT-001`. |
| Context isolation | SKIP | The development workflow did not plant a deterministic canary; prose absence is not evidence of isolation. |
| Latency budget | SKIP | A reliable non-overlapping duration for the composite continuation is unavailable. |
| Reported cost budget | SKIP | A reliable non-overlapping aggregate cost is unavailable. |

Tally: PASS 8, FAIL 0, SKIP 3, ERROR 0. SKIP is distinct from PASS. The
deterministic gate opened because there was no FAIL or ERROR.

## Rubric results

The rubric runner re-executed the deterministic gate, then used one fresh
Claude call per dimension. Each call ran in a temporary directory with an
empty strict MCP configuration and no repository, shell, file, test, tracker,
or web tools.

| Dimension | Threshold | Score | Judge explanation |
|---|---:|---:|---|
| Test Execution Fidelity | 3/4 | 4/4 | The outputs name the exact target and single bounded tool event, quote its result, and repeatedly distinguish the dummy response from real pytest or system health. |
| Outcome Accuracy | 3/4 | 4/4 | Pass, Blocked, dummy, and controlled outcomes remain distinct, and the prior blocked attempts are preserved rather than converted into success. |
| Evidence Coverage | 3/4 | 4/4 | All five role outputs, tool evidence, approvals, scope, skipped measurements, limitations, and historical failures are organized for review. |
| Readiness Recommendation Quality | 3/4 | 3/4 | Closing the narrow documentation task follows from the evidence and carries scope limits, but those limits are scattered rather than consolidated into one statement naming deployment, security, and holdout generalization. |

Aggregate: 15/16, with a required overall threshold of 12/16 and every
dimension required to score at least 3/4. Judge calls: 4. Final rubric
verdict: PASS.

This result applies only to the evaluated, deterministically valid transcript.
It does not establish complete system, backend, security, deployment, or
holdout-task health.

## Setup fixes and preserved failures

Two evaluation setup issues were corrected without changing a task fact,
deterministic check, threshold, or holdout:

1. The course image's default entrypoint stopped on an unrelated unset Slack
   variable before the evaluator ran. The authorized image was rerun with the
   entrypoint bypassed.
2. The first rubric attempt's first judge returned non-JSON text. The strict
   parser rejected it and accepted no score. The harness was updated to use the
   installed Claude CLI's JSON Schema structured-output option while retaining
   strict key, type, threshold, and malformed-response validation. The parser
   self-test then passed 7/7, and the successful suite used four fresh calls.

There was no valid deterministic failure in the baseline, so no fixture rubric
run was needed. The two earlier blocked Tester attempts are preserved as
historical system evidence. No check was weakened to make the baseline pass.

## Unmeasured risks and limitations

- No context canary was planted, so context isolation is not evaluated.
- Composite latency and cost cannot be added reliably across human continuation
  boundaries.
- No separate server-persisted audit log exists; normalized stream-json events
  are the strongest available tool evidence.
- The final approval exists in the exact Project Manager handoff rather than an
  independently signed audit record.
- `test_runner` and `task_tracker` are controlled dummy tools, not real pytest
  or an external ticket service.
- The baseline does not measure real backend behavior, deployment health,
  security completeness, or generalization to locked tasks.
- One judge noted a minor 5138-versus-5134 byte-count inconsistency in preserved
  Implementer evidence. It did not alter file hashes, scope, or the scored
  outcome, but the discrepancy remains recorded.

## Recommended next step

In the later calibration lab, run the seven locked holdout tasks exactly as
committed, retain all deterministic failures, compare rubric scores with human
review, and adjust only the harness implementation when evidence shows a true
evaluation defect. Do not rewrite holdouts or production behavior to improve
scores.
