# Controlled Tool-Evolution Fault Injection

Drill ID: `controlled-fault-001`

This was an intentional capstone drill, not an accidental discovery.

## Attempted Change

Commit `7c666e5` intentionally added:

```yaml
continue-on-error: true
```

to the permanent `policy-tests` job in `.github/workflows/ci.yml`.

## Why It Was Plausible

The workflow already uses `continue-on-error: true` for the advisory AI review job. A legitimate-seeming but unsafe tool evolution is to copy that non-blocking behavior to another job to reduce friction.

## Exact Breakage

The permanent policy gate became non-blocking. That weakens the core governance guarantee that policy and MCP runtime failures must fail CI.

## Gate That Caught It

`scripts/check-pipeline-integrity.py`

Failure evidence:

```json
{
  "failures": [
    "policy-tests must not use continue-on-error"
  ],
  "schema_version": "pipeline-integrity-v1",
  "status": "FAIL",
  "workflow": ".github/workflows/ci.yml"
}
```

Local evidence:

- `.eval-artifacts/capstone/tool-evolution-drill/controlled-fault-001/pipeline-integrity-failure.json`
- `.eval-artifacts/capstone/tool-evolution-drill/controlled-fault-001/pipeline-integrity-failure-exit-code.txt`

## Diagnosis

The integrity checker correctly distinguishes advisory review from permanent gates. Advisory review may be non-blocking; `policy-tests` must not be.

## Fix

Remove `continue-on-error: true` from `policy-tests` and rerun the same integrity gate.

## Final Result

The repaired workflow passes the integrity checker again. The local history intentionally preserves:

1. the fault commit;
2. the failing gate evidence;
3. the fixing commit.

The broken state was never pushed.
