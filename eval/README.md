# FitGPT Two-Layer Evaluation Harness

This harness evaluates normalized orchestration evidence for the already-used
development task COURSE-FITGPT-001. The locked tasks in
docs/holdout-task-set.md are calibration inputs for a later exercise and must
not be run or edited here.

## Public seams

    python3 eval/test_deterministic.py <transcript.json>
    python3 eval/test_rubric_suite.py <transcript.json>

The rubric command always executes the deterministic gate first. Any
deterministic FAIL or ERROR prevents judge calls.

Self-tests:

    python3 eval/test_deterministic.py --self-test
    python3 eval/test_rubric_suite.py --self-test

Normalize the preserved development workflow with eval/run_baseline.py and the
preserved Run 3, Run 4, and Run 5 evidence roots. Generated evidence is stored
under .eval-artifacts/runs/dev/<run-id>/ and is ignored by Git.

The sanitized fixture under eval/fixtures/ tests harness structure and never
claims real tool execution.

## Evidence trust order

1. MCP responses and Claude stream-json tool events
2. Git manifests and checksums
3. Normalized fields derived directly from preserved evidence
4. Natural-language summaries

Unsupported prose is never converted into a tool event.

## Evidence-gap report

Available evidence records task and run identifiers, role order and versions,
exact handoffs, substantive role outputs, structured headings, tool names,
arguments and responses, both human approvals, changed paths, protected-state
verification, per-process runtime metadata, reported per-process cost, ticket
identity, and controlled dummy-tool responses.

The completed lineage spans Runs 3-5 rather than one uninterrupted process.
Run 3 and Run 4 Tester failures remain historical attempts; the selected path
uses Planner, Implementer, and Reviewer from Run 3 and Tester plus Project
Manager from Run 5.

The following gaps are not filled by inference:

1. No separate server-persisted audit database exists. The normalized
   tool-events.jsonl comes directly from preserved Claude stream-json.
2. Final Run 5 approval is preserved in the exact Project Manager handoff, not
   an independently signed approval record.
3. Human waiting and continuation boundaries prevent a reliable
   non-overlapping aggregate duration and cost. Provisional ceilings are 1,800
   seconds and $1.50, derived from prior Module 1 and Module 3 evidence, but
   composite baseline values remain SKIP.
4. No context canary was planted, so context-isolation evaluation is SKIP.
5. test_runner is not real pytest, and task_tracker is not an external service.

## Module 1 rubric source

The judgment layer uses docs/rubric.md, created by commits
276feaf242ebd975f59cf9d898ebdc0db9d96fb7 and
fea2c581d9f47f982c813a3212d1cee16dcdd1a4. Three scored uses are preserved in
docs/iteration-log.md.

Its dimensions remain Test Execution Fidelity, Outcome Accuracy, Evidence
Coverage, and Readiness Recommendation Quality. Deterministic checks establish
event facts; judges score only output fidelity, semantic accuracy, evidence
quality, and recommendation calibration.
