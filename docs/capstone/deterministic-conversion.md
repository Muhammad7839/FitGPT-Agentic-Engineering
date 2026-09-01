# Agent-To-Deterministic Conversion

## Conversion Plan

Original agentic step:

`backend-config-docs-auditor` performed read-only comparisons across backend configuration implementation, tests, documentation, and templates.

Converted narrow behavior:

Verify the factual `DATABASE_URL` representation across:

- `README.md`
- `backend/.env.example`
- `backend/app/config.py`
- `backend/tests/test_config_startup.py`

Why this became deterministic:

The selected behavior is not judgment-heavy. It asks whether known strings and production/local fallback claims are present in known source surfaces. The historical auditor evidence showed that the agentic audit repeatedly spent model effort checking this stable fact pattern.

Judgment that remains agentic:

Prioritizing broader documentation recommendations, weighing onboarding severity, and deciding how to rewrite prose remain reviewer/auditor work. The deterministic replacement only checks a stable factual invariant.

## Measurement Method

Fresh agentic benchmark:

The capstone uses the historical Module 2 `backend-config-docs-auditor` evidence as the agentic comparison because it already measured the exact source-comparison behavior on this repository. The most relevant preserved run is Run 5:

- Report: `docs/agents/backend-config-docs-auditor/lab/runs/run-005-report.md`
- Summary evidence: `docs/agents/backend-config-docs-auditor/lab/iteration-log.md`
- Report commit: `0591f12ecb4078591c7447e61904c01b930774ae`

Historical agentic result:

Run 5 inspected README, `.env.example`, implementation, focused tests, and deployment configuration together for `DATABASE_URL`. It improved evidence precision but still had factual weaknesses, including incomplete handling of the `ALLOW_SQLITE_IN_PRODUCTION` override and exact-source precision errors.

The preserved Run 5 record reports a total cycle of `354 seconds` and a UI-displayed model cost of `$0.91`. These values cover the complete agentic audit, not only the narrow `DATABASE_URL` comparison, so they are an upper-bound context rather than an isolated apples-to-apples benchmark.

Deterministic replacement:

`scripts/check-config-docs-consistency.py`

The utility reads the same known surfaces and emits JSON with:

- status;
- checked fact;
- per-surface booleans;
- runtime duration;
- model cost `$0`.

## Result

The preserved deterministic result completed in `0.156 ms` and cost `$0`.

It produces the relevant factual conclusion without a model: `DATABASE_URL` is represented in README, env template, implementation, and focused production tests, including the local SQLite fallback and production requirement.

Local evidence:

- `.eval-artifacts/capstone/deterministic-conversion/config-docs-consistency.json`

## Comparison

| Dimension | Agentic Auditor | Deterministic Utility |
|---|---|---|
| Scope | Multi-source judgment and recommendations | One stable factual invariant |
| Cost | `$0.91` UI-displayed for complete historical Run 5; exact narrow-subtask cost unavailable | `$0` |
| Latency | `354 s` for complete historical Run 5; exact narrow-subtask latency unavailable | `0.156 ms` preserved local result |
| Output | Narrative report with recommendations | Machine-readable JSON |
| Auditability | Requires transcript/report review | Direct boolean checks |
| Best use | Ambiguous documentation audits | Repeated factual guardrail |

## Success Criteria

- Same relevant factual conclusion as the source-comparison portion of the agentic audit.
- No model call.
- Deterministic JSON output.
- Focused tests cover pass/fail behavior.
- Broader judgment-heavy audit remains out of scope.

## Quantified Interpretation

For the complete historical-run upper bound, the observed cost difference is `$0.91 - $0 = $0.91`, or a `100%` model-cost reduction for the deterministic execution.

Converting `0.156 ms` to seconds gives `0.000156 s`. The upper-bound timing comparison is `(354 - 0.000156) / 354 × 100 = 99.99996%` faster, rounded. This percentage must not be read as an isolated subtask benchmark because the `354 s` source includes the whole agentic audit.
