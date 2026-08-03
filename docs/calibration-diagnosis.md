# Calibration Diagnosis: Tester Output-Schema Mismatch

## Cycle and development task

- Cycle: `CAL-20260802-002`
- Development task: `COURSE-FITGPT-001`
- Induced-fault commit: `8831e8954f97783adede22d4655b542d7ea274d2`
- Owning component: `.claude/agents/tester.md`

`CAL-20260802-001` remains preserved separately as an invalid execution-setup attempt. It is not used as the official before-fix measurement.

## Visible symptom

The official Tester process invoked the bounded dummy `test_runner` successfully and described the controlled result as `Pass`, but returned it beneath `## Status`. The committed output contract and normalizer require `## Result`, so the normalized Tester verdict was `Unknown` and the deterministic gate stayed closed.

## Runtime and tool evidence

- `coursetools` initialization status: `connected`
- Runtime tools: `mcp__coursetools__file_read`, `mcp__coursetools__test_runner`
- Actual `test_runner` calls: 1
- Actual `file_read` calls: 0
- Actual `task_tracker` calls: 0
- Prohibited-tool calls: 0
- Test target: `backend/tests/test_config_startup.py`
- Tool result class: controlled dummy Pass, not real pytest

The tool event and response are preserved in `.eval-artifacts/calibration/CAL-20260802-002/before-fix/session.jsonl` and `tool-events.jsonl`. Natural-language references to a tool are not counted as events.

## Handoff evidence

The mechanically unchanged handoff contained:

- workflow and issue identity
- Tester role and version
- preserved Reviewer Pass evidence
- approved changed-file list
- exact test target
- acceptance criteria
- explicit prohibitions
- required output-format instruction
- no fabricated approval

No required prerequisite field was missing. The handoff was therefore not the cause of the malformed heading.

## Existing deterministic result

The current suite reported:

```text
PASS=6 FAIL=2 SKIP=3 ERROR=0
```

`controlled_test_evidence` failed because the normalized Tester did not report `Pass`; this is an indirect downstream detection of the output-contract mismatch. The same check also uses a strict literal limitation phrase and reported that phrase absent even though the output clearly stated that the event was a dummy simulation and not a real `pytest` execution. That secondary message is retained as observed behavior and is not being used to weaken the check.

`controlled_ticket` failed because no Project Manager call occurred. That is the expected downstream gate behavior after an unaccepted Tester result, not an independent root cause.

No rubric judge ran because the deterministic gate was closed.

## Structural classification

Structural, deterministic output-schema failure. The defect is the presence and exact level/order of a required Markdown heading, not a qualitative judgment about the prose.

## Root-cause hypothesis

The Tester followed its project-scoped prompt. The induced commit changed the producer's required heading from `## Result` to `## Status`; the produced output reproduced that changed heading exactly. The evaluator continued to enforce the committed `## Result` contract and therefore could not derive an accepted Tester verdict.

## Correct fix layer

Prompt layer.

The narrow repair is to restore `## Result` in `.claude/agents/tester.md` without changing the handoff, role permissions, routing, tool grants, normalizer acceptance rule, development task, or evaluation threshold.

## Why other layers are inappropriate

- Scope: the handoff already contained the required prerequisite evidence. Adding more context would not repair the wrong output heading.
- Routing: the correct Tester role ran at the correct stage.
- Tool: the correct two-tool boundary was exposed, and the exact bounded test event succeeded.
- Evaluator relaxation: accepting `## Status` would weaken the established contract and hide the producer defect.

## Detecting-check requirement

Add a focused deterministic `tester_output_schema` check that verifies the exact ordered core headings and accepts only `Pass`, `Fail`, or `Blocked` beneath `## Result`. It must identify the malformed heading directly rather than relying on the downstream missing-Pass symptom.

## After-fix verification

The targeted Prompt-layer repair restored only `## Result` in `.claude/agents/tester.md`. A fresh after-fix Tester conversation used the same handoff and known-good MCP launch pattern.

Observed after the repair:

- `coursetools`: connected
- runtime tools: `file_read`, `test_runner`
- actual `test_runner` calls: 1
- exact target: `backend/tests/test_config_startup.py`
- Tester heading: `## Result`
- Tester value: `Pass`
- focused `tester_output_schema`: `PASS`
- deterministic tally: `PASS=8 FAIL=0 SKIP=4 ERROR=0`

The four skips are explicit path or measurement limitations: Project Manager was not part of the declared calibration path, no context canary was planted, and composite duration and cost remain unavailable. The preserved full development baseline continued to report `PASS=9 FAIL=0 SKIP=3 ERROR=0` with the new check enabled.

## Rubric infrastructure blocker

The deterministic gate opened, but the rubric suite could not complete. Two rubric-only attempts were made against the same frozen after-fix transcript. In both attempts, the first two dimensions completed, and the third dimension, Evidence Coverage, ended with:

```text
error_max_structured_output_retries
Failed to provide valid structured output after 5 attempts
```

The development task and Tester were not rerun. No repository, MCP, file, shell, tracker, or web tool was available to the rubric judges. The rubric implementation, schema, thresholds, prompts, and model selection were not changed after this failure.

Because no complete four-dimension rubric result exists, regression and locked holdout measurement did not begin.
