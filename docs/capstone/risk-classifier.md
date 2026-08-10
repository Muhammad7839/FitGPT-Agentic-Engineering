# AURA Forge Risk Classifier

Version: `aura-risk-v1`

## Purpose

The AURA Forge risk classifier deterministically assigns a bounded repository change to exactly one tier: `LOW`, `MEDIUM`, or `HIGH`.

The classifier only decides risk. It does not select routes, invoke agents, grant tools, request approvals, or implement adaptive routing.

## Design Rules

- Deterministic and model-free.
- Exactly three tiers: `LOW`, `MEDIUM`, `HIGH`.
- Strict precedence: `HIGH` first, then `MEDIUM`, then `LOW`.
- Conservative defaults for missing, malformed, traversal, or unknown executable-looking paths.
- Sensitive path always outranks diff size.

## Rule Table

| Precedence | Tier | Trigger |
|---:|---|---|
| 1 | HIGH | Empty path input, malformed path input, absolute path input, or path traversal attempt |
| 1 | HIGH | `.github/workflows/**` |
| 1 | HIGH | Governance policy or governance risk documents |
| 1 | HIGH | `mcp/**` or `mcp-servers/**` |
| 1 | HIGH | `.claude/agents/**` |
| 1 | HIGH | Docker, compose, or `.agentic/container/**` sandbox/container boundary |
| 1 | HIGH | Auth, authorization, security, secret, environment, database schema, or migration path |
| 1 | HIGH | `eval/**` policy, runtime, rubric, harness, or evaluation enforcement path |
| 1 | HIGH | Metadata text mentions production, secrets, credentials, auth, database, or migrations |
| 2 | MEDIUM | Executable application, test, or tooling path such as `backend/**`, `web/src/**`, `web/tests/**`, `scripts/**`, or `tests/**` |
| 2 | MEDIUM | Executable-looking suffix such as `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.sh`, or `.sql` when no HIGH rule matches |
| 2 | MEDIUM | Unknown path that is not clearly non-executable documentation |
| 3 | LOW | All changed paths are non-executable content such as `.md`, `.txt`, or `.rst` outside HIGH-sensitive and executable surfaces |

## Why No LLM

Risk classification is governance logic. It must be inspectable, repeatable, and testable without model variance. A model can explain or review a result later, but it must not decide the tier.

## Why No Weighted Score

A weighted score can hide a sensitive path behind a small diff or benign-looking request. AURA Forge uses precedence instead: any HIGH trigger immediately classifies the change as HIGH.

## Examples

| Paths | Tier | Reason |
|---|---|---|
| `docs/features/accessibility.md` | LOW | Non-executable feature documentation |
| `web/src/utils/feedbackPrompts.js` | MEDIUM | Executable web utility code |
| `web/src/utils/feedbackPrompts.test.js` | MEDIUM | Application test code |
| `eval/test_policy.py` | HIGH | Evaluation and policy enforcement |
| `mcp-servers/storage/allow-list.json` | HIGH | MCP permission boundary |
| `.github/workflows/ci.yml` | HIGH | CI control surface |
| `docs/features/accessibility.md` plus `mcp/coursetools_server.py` | HIGH | HIGH outranks LOW |

## Locked Scenario Results

| Scenario | Paths | Expected | Classifier Result |
|---|---|---|---|
| AF-LOW-001 | `docs/features/accessibility.md` | LOW | LOW |
| AF-MEDIUM-001 | `web/src/utils/feedbackPrompts.js`, `web/src/utils/feedbackPrompts.test.js` | MEDIUM | MEDIUM |
| AF-HIGH-001 | `eval/test_policy.py`, `mcp-servers/storage/allow-list.json`, `mcp-servers/retrieval/allow-list.json`, `docs/governance-policy.md` | HIGH | HIGH |

These are representative capstone scenarios, not the locked Module 3 holdout conversations.

## Known Limitations

- The classifier does not inspect diff content, only paths and simple metadata markers.
- Unknown non-documentation paths classify as MEDIUM unless a HIGH rule matches.
- Empty path input classifies as HIGH because it is unsafe to default missing evidence to LOW.
- This milestone does not wire adaptive routing.

## Future Connection To Adaptive Routing

Later AURA Forge routing can use this deterministic tier result to select the minimum justified route. That routing layer must remain separate and must preserve evidence for the classifier result, selected route, tool grants, tests, and human approvals.
