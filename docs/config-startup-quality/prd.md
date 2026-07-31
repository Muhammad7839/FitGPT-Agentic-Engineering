# PRD: Backend Configuration Startup Test Verification Workflow

## Workflow Description

This workflow runs FitGPT’s focused backend configuration-startup tests inside the sandbox and produces an evidence-based readiness report without changing the repository.

## Trigger

A developer manually invokes Claude Code inside the FitGPT sandbox and provides the approved configuration-test verification prompt while the Target Codebase is available at `/workspace`.

## Decision Events

- If the approved focused test command exits with status 0, the agent classifies the run as passing.
- If the command exits with a nonzero status because one or more tests fail, the agent classifies the run as failing and reports the observed failures.
- If the command cannot begin because of an environment, dependency, or configuration problem, the agent classifies the result as an execution-environment failure.
- If warnings appear, the agent reports them separately even when the tests pass.
- If all focused tests pass with no blocking error, the agent recommends that the tested backend configuration-startup behavior is ready for the next step.
- If tests fail or cannot run, the agent recommends that the tested area is not ready for the next step.
- The agent reports evidence only and does not repair code, install dependencies, retry the command, or broaden the investigation.

## Ordered Actions

1. Read the supplied task prompt.
2. Run the exact approved configuration-startup test command once from `/workspace/backend`.
3. Capture the exit status, test count, pytest duration, failures, errors, and warnings.
4. Classify the result as passed, failed, or execution-environment failure.
5. Produce a structured evidence report.
6. Provide a readiness recommendation consistent with the observed result.
7. Stop without modifying files or running additional commands beyond permitted read-only verification.

## Acceptance Criteria

A run is complete and correct only when all of the following are true:

1. The exact approved test command is executed once.
2. The report identifies the working directory and exact command.
3. The report states the numeric shell exit status.
4. The stated result matches the exit status and pytest output.
5. The report includes the observed test count and pytest duration.
6. The report includes every observed failure, error, and warning, or explicitly states that none were observed.
7. The readiness recommendation follows logically from the evidence.
8. The report clearly limits its conclusion to the focused configuration-startup test file.
9. No tracked or untracked repository file is created, modified, or removed by the agent.
10. The agent does not retry, install dependencies, repair code, run additional tests, push, merge, deploy, or access external services.
11. The agent does not inspect or expose credentials, authentication data, or real environment files.
12. A reviewer can determine the outcome without reading the complete raw terminal log.
