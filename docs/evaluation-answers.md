# Evaluation Exercise Answers

## Question 1

I represented requirements as deterministic checks when the transcript makes
them objectively true or false.

The routing check compares `expected_path` with the selected role events and
their sequence. The authorization check compares every recorded tool call with
the committed role grant map and separately enforces the Tester, Implementer,
Orchestrator, and Project Manager boundaries. The handoff check requires the
shared schema fields plus Reviewer evidence for Tester and Reviewer, Tester,
and current approval evidence for Project Manager. The protected-scope check
compares changed files with approved writable paths, rejects sensitive or
application/test paths, and requires the protected-state flag. The approval
check verifies that the plan approval precedes Implementer, the final approval
precedes Project Manager, each approval belongs to the correct workflow run,
and neither is reused. The controlled-test check requires one actual preserved
Tester tool event for the exact approved target and requires the output to call
the result dummy rather than real pytest. The ticket check accepts only one
successful Project Manager call for `COURSE-FITGPT-001` and rejects alternate
or `test` tickets. The schema check also validates required transcript fields
and event ordering.

These are pass-or-fail requirements because they do not depend on writing
style or reviewer preference. A role either occurred in the required position
or it did not. A tool was either authorized or it was not. An approval either
preceded a gated action in the current run or it did not. A protected path or
alternate ticket either appears in the recorded evidence or it does not.

Context isolation, latency, and cost are also deterministic in principle, but
the baseline lacks the evidence needed to decide them. The harness therefore
returns SKIP instead of treating missing evidence as a Pass.

## Question 2

The rubric evaluates qualities that cannot be settled by the presence of an
event or field alone.

Test Execution Fidelity asks whether the role outputs explain the bounded test
faithfully and make the dummy limitation clear. Outcome Accuracy asks whether
the narrative keeps Pass, Blocked, denied, simulated, and real outcomes
semantically consistent. Evidence Coverage asks whether the important role,
tool, approval, scope, failure, and limitation evidence is organized well
enough for a reviewer to use. Readiness Recommendation Quality asks whether the
recommended next action is proportionate to the evidence and clearly separates
measured workflow readiness from unmeasured risks.

Judgment is appropriate for those questions because two transcripts can
contain the same required events while differing substantially in clarity,
groundedness, review usefulness, and calibration. The 3/4 readiness score shows
that distinction: the deterministic evidence was valid, but the limits were
spread across outputs instead of being synthesized into one concise readiness
statement.

Important gaps remain outside both layers. This baseline does not test real
backend behavior, real pytest health, deployed Android/web integration,
security completeness, or generalization to the locked holdout tasks. It also
cannot determine context isolation without a planted canary, and it cannot
reliably measure aggregate time or cost across the composite human-continuation
boundaries.

## Question 3

If every rubric dimension receives a high score, I can reasonably conclude
only that a run with no deterministic FAIL or ERROR produced outputs that met
the defined thresholds for test-execution fidelity, outcome accuracy, evidence
coverage, and readiness-recommendation quality. For this baseline, 15/16 means
the recorded development workflow is a strong, reviewable baseline for the
narrow `COURSE-FITGPT-001` documentation task.

It would be unsafe to conclude that FitGPT has complete system health, has no
security defects, behaves correctly in areas the harness does not measure,
generalizes to the seven locked holdout tasks, or is ready for deployment. It
would also be unsafe to treat the dummy `test_runner` response as real pytest
or backend health, or the controlled `task_tracker` response as proof that an
external issue service changed. High rubric scores describe the evaluated
evidence and dimensions; they do not turn missing evidence into coverage.
