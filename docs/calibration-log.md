# Module 3 Calibration Log

## Repository

- Branch: `module-3-calibration-cycle`
- Final evaluated HEAD before final records commit: `8e2f6a7239ffa369361514fa36ff3464a6378801`
- Locked holdout checksum: `e3aa9cdcec7b643507b7dd6f03ea15d92cfb6ed5fcacc4f56f5b2a8631631f32`
- Original FitGPT repository access: none
- Remote push/contact: none

## Failure Cycle

### Invalid setup attempt

`CAL-20260802-001` is preserved as an invalid setup attempt. It did not isolate the deliberately induced Tester schema mismatch, so it is not counted as the official before-fix measurement.

### Official before-fix run

`CAL-20260802-002/before-fix/` is the official before-fix measurement. The bounded dummy `mcp__coursetools__test_runner` event occurred, proving the Tester could receive and use its bounded test tool. The Tester then returned the result under `## Status` instead of the required `## Result`, leaving the output-contract failure observable.

Before-fix deterministic result after focused schema coverage:

- PASS=7
- FAIL=1
- SKIP=4
- ERROR=0

The failing check was the Tester output-schema check.

### Induced fault

The induced fault changed the Tester output contract in `.claude/agents/tester.md`:

```diff
-## Result
+## Status
```

No routing, tool grant, MCP, production code, production test, or holdout task was changed to induce the fault.

### Deterministic detection

`eval/test_deterministic.py` added exact ordered Tester heading validation. The check requires `## Result` and an allowed value of `Pass`, `Fail`, or `Blocked`. This made the schema mismatch deterministic and independent of judge opinion.

### Prompt-layer fix

The fix restored `## Result` in `.claude/agents/tester.md`. This was the correct layer because the producing agent's output contract was wrong. Routing, grants, or evaluator relaxation would not fix the producer contract.

### After-fix development result

`CAL-20260802-002/after-fix/` preserved the corrected after-fix Tester run.

After-fix deterministic result:

- PASS=8
- FAIL=0
- SKIP=4
- ERROR=0

The corrected Tester process produced one actual dummy `test_runner` event and returned the required `## Result` heading.

## Rubric Verification

Rubric attempts 01 through 06 are preserved and incomplete. They are not combined with the final result.

- Attempts 01 and 02: incomplete rubric infrastructure attempts.
- Attempt 03: authentication failure before model generation.
- Attempt 04: wrapper setup failure because the evidence directory was pre-created.
- Attempt 05: Claude Code internal structured-output validator failed on `Outcome Accuracy`.
- Attempt 06: local JSON validation rejected an over-1200-character justification.

Infrastructure corrections:

- `0cc761d56719ea818d2feb56b201598d74f561e3`: stabilized bounded dimension-specific rubric prompts.
- `1a2a37d083a5daf9ba0ccf3e701ce5014927019b`: removed Claude Code internal structured-output validation and parsed the plain JSON result locally.
- `8e2f6a7239ffa369361514fa36ff3464a6378801`: increased the local justification transport bound from 1200 to 2000 characters while preserving strict local validation.

Final completed rubric attempt:

- Attempt: `rubric-attempt-07`
- Deterministic gate: open
- Test Execution Fidelity: 4/4
- Outcome Accuracy: 4/4
- Evidence Coverage: 4/4
- Readiness Recommendation Quality: 3/4
- Aggregate: 15/16
- Verdict: PASS

## Regression

Regression result: PASS

Evidence used:

- After-fix development transcript: PASS=8 FAIL=0 SKIP=4 ERROR=0
- Preserved successful baseline: PASS=9 FAIL=0 SKIP=3 ERROR=0

Confirmed:

- Tester output-schema check remains passing.
- Routing remains correct in preserved passing transcripts.
- Tool authorization remains correct.
- Approvals remain correctly scoped.
- Protected paths remain unchanged.
- Previously passing baseline behavior remains passing.

Limitation: regression reused preserved transcripts rather than launching new development-agent executions.

## Holdout Measurement

Holdout measurement root: `.eval-artifacts/calibration/CAL-20260802-002/holdout/measurement-final/`

All seven locked tasks ran exactly once as fresh Claude Code conversations. No task was rerun. No tuning occurred between tasks.

Result: FAIL

The holdout runs used tools-disabled conversations to avoid mutating the repository after the final rubric success. Because no repository, Agent, MCP, test, tracker, shell, file, or web tools were exposed, every deterministic gate failed before rubric scoring.

| Task | Result | Deterministic tally | Rubric |
|---|---|---|---|
| HO-01 | FAIL | PASS=4 FAIL=5 SKIP=3 ERROR=0 | Not run, gate closed |
| HO-02 | FAIL | PASS=4 FAIL=2 SKIP=6 ERROR=0 | Not run, gate closed |
| HO-03 | FAIL | PASS=4 FAIL=2 SKIP=6 ERROR=0 | Not run, gate closed |
| HO-04 | FAIL | PASS=4 FAIL=2 SKIP=6 ERROR=0 | Not run, gate closed |
| HO-05 | FAIL | PASS=4 FAIL=4 SKIP=4 ERROR=0 | Not run, gate closed |
| HO-06 | FAIL | PASS=4 FAIL=4 SKIP=4 ERROR=0 | Not run, gate closed |
| HO-07 | FAIL | PASS=4 FAIL=5 SKIP=3 ERROR=0 | Not run, gate closed |

## Remaining Gaps and Near Misses

- The development case passed deterministic and rubric evaluation, but the final holdout measurement did not generalize because the holdout execution setup did not expose the role/tool orchestration path.
- The clean holdout result is therefore a measured failure, not evidence of production readiness.
- `test_runner` and `task_tracker` remain controlled dummy course tools and do not prove real pytest, deployment, integration, external tracker, or production health.
- No complete production health claim is made.
