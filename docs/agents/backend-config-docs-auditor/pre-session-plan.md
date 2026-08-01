# Pre-Session Plan: Backend Configuration Documentation Audit

## Real Project Task

Audit FitGPT's committed backend startup and configuration documentation against the current implementation and focused tests. Produce a prioritized report identifying documentation gaps, unsupported claims, and onboarding improvements without changing application code or documentation during the session.

## Agent

The session will use the project-scoped `backend-config-docs-auditor` agent, version `v0.1.0`.

The agent is appropriate because the work requires accumulated evidence from several related files, judgment about discrepancies and priority, and revision of an earlier recommendation set after a stakeholder requirement changes.

## Phase 1: Evidence Discovery

The agent will identify and inspect the committed documentation, configuration implementation, startup behavior, and focused configuration tests.

Rules:

- Read-only investigation
- No recommendations yet
- Implementation and tests are authoritative for runtime behavior
- Documentation claims must be recorded separately
- Facts, inferences, and open questions must remain distinguishable
- Relevant file paths and line evidence should be retained

Expected phase output:

- Evidence table
- Verified current behavior
- Documentation claims
- Mismatches or omissions
- Open questions

## Phase 2: Broad Recommendation Draft

The agent will convert the verified discrepancies into a draft recommendation set.

Rules:

- No files may be changed
- Recommendations may concern documentation, tests, or production code
- Each recommendation must retain a stable ID
- Recommendations must be prioritized by production risk
- Every recommendation must cite evidence
- Unsupported recommendations must be excluded

Expected phase output:

- Draft recommendations with stable IDs
- Category for each recommendation
- Production-risk priority
- Supporting evidence
- Known limitations

## Planned Proactive Summary

At the end of Phase 2, the agent will produce a structured summary before any new requirement is introduced.

The summary must preserve:

- Current goal
- Active requirements
- Decisions
- Recommendation IDs and current draft state
- Evidence that must carry forward
- Unresolved questions
- Next action

The summary will be reviewed and saved as a Markdown session artifact.

## Planned Requirement Change

After the Phase 2 summary, the stakeholder will clarify that the final deliverable is for new-contributor onboarding rather than production remediation.

New requirements:

- Reprioritize recommendations by likely onboarding confusion and reproducibility impact, not production risk
- Exclude production-code change recommendations
- Retain only documentation and test-support recommendations
- Use exact commands or values only when supported by committed evidence
- Explicitly identify important scopes that the audit did not verify

This change supersedes the Phase 2 recommendation categories and prioritization rule but does not invalidate the verified evidence collected earlier.

## Phase 3: Final Onboarding-Focused Report

The agent will revisit the Phase 2 recommendation draft and produce a coherent final report under the changed requirements.

Expected final sections:

1. Scope
2. Evidence reviewed
3. Confirmed current behavior
4. Documentation gaps
5. Prioritized onboarding recommendations
6. Recommendations removed or changed after the stakeholder update
7. Open questions
8. Out of scope
9. Final consistency statement

## Artifact to Revisit

The Phase 2 recommendation draft is the main artifact that must be revisited.

The agent must identify which recommendation IDs were:

- Retained
- Reprioritized
- Rewritten
- Removed

## Evaluation Evidence

The session will be evaluated using:

- Complete interactive transcript
- Agent tool calls
- Phase outputs
- Boundary checks
- Proactive summary
- Final report
- Final context-consistency check
- Repository-integrity evidence
- Accuracy, task-adherence, and coherence rubric scores

## Compaction Decision

Compaction is not planned.

It may be used only if the visible Claude context usage reaches at least 75 percent and the session cannot safely continue after the proactive summary. If used, the timing, reason, and observed effects must be recorded.
