# Module 2 Lab Final Calibration Selection

## Selected Live Agent

`backend-config-docs-auditor v0.1.2`

## Reason for Selection

The lab used one fixed task, one committed rubric, and fresh read-only sessions to compare five agent versions.

| Run | Version | Score | Result |
|---|---|---:|---|
| Run 1 | v0.1.2 | 13/16 | Pass |
| Run 2 | v0.1.3 | 9/16 | Fail |
| Run 3 | v0.1.4 | 7/16 | Fail |
| Run 4 | v0.1.5 | 11/16 | Fail |
| Run 5 | v0.1.6 | 11/16 | Fail |

v0.1.2 was the only version to meet every numeric threshold and every binary gate.

Later versions were not discarded. Their exact definitions and reports remain archived because they produced important evidence:

- v0.1.3 improved evidence closure but produced an incomplete report.
- v0.1.4 added output-completion controls but stopped even earlier.
- v0.1.5 restored structural completion but retained evidence inaccuracies.
- v0.1.6 improved source accounting and validation criteria but still produced contradictory or unsupported patch wording.

The final selection therefore uses the best demonstrated version rather than assuming the highest version number is the most reliable.

## Preserved Evidence

- Fixed plan and rubric
- Archived agent definitions v0.1.2 through v0.1.6
- Complete reports from Runs 1 through 5
- Complete Iteration Log entries
- External PTY evidence paths and checksums
- Starting tag `lesson-4-lab-start`

## Remaining Improvement Opportunity

A future iteration should use a deterministic output validator or structured schema that checks:

- required headings and recommendation fields
- source-inventory closure
- contradictory proposed wording
- exact validation acceptance criteria
- unsupported runtime claims

That mechanism should be tested separately before replacing the selected v0.1.2 agent.

## Safety and Repository State

All calibration runs were read-only. No application code, tests, production configuration, or persistent memory changed. No secret was exposed, nothing was pushed, and the original FitGPT repository was never accessed.
