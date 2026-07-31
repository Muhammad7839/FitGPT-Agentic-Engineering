# PRD: Recommendation Explanation Test Verification Workflow

## Workflow Description

This workflow runs FitGPT’s focused recommendation-explanation test suite inside the sandbox and produces an evidence-based readiness report without changing the repository.

## Trigger

A developer manually invokes Claude Code inside the FitGPT sandbox and supplies the approved test-verification prompt while the Target Codebase is available at `/workspace`.

## Decision Events

- If the approved test command exits with status 0, the agent classifies the test run as passing.
- If the approved test command exits with a nonzero status, the agent classifies the test run as failing and reports the observed failures or errors.
- If the command cannot start because of an environment, dependency, or configuration problem, the agent classifies the result as an execution-environment failure rather than a test failure.
- If warnings appear, the agent reports them separately even when the tests pass.
- If the tests pass and no blocking errors are present, the agent recommends that this area is ready for the next step.
- If the tests fail or cannot run, the agent recommends that this area is not ready for the next step.
- The agent reports the result only and does not attempt repairs, retries, installations, or unrelated investigation.

## Ordered Actions

1. Read the supplied workflow prompt.
2. Run the exact approved focused test command once from `/workspace/backend`.
3. Capture the command outcome, exit status, pytest test count, pytest duration, warnings, failures, and errors.
4. Determine whether the command passed, failed, or could not execute.
5. Produce a concise report describing the evidence.
6. Give a readiness recommendation that follows from the observed result.
7. Stop without changing repository files or rerunning the command.

## Acceptance Criteria

A run is complete and correct only when all of the following are true:

1. The agent runs the exact approved focused test command once.
2. The agent states whether the command passed, failed, or could not execute.
3. The stated result matches the actual command exit status and pytest output.
4. The report includes the observed test count and pytest duration.
5. The report includes every observed failure, error, and warning, or explicitly states that none were observed.
6. The readiness recommendation is consistent with the command result.
7. The agent does not modify tracked or untracked repository files.
8. The agent does not run additional tests, retry the command, install dependencies, repair code, push, merge, deploy, or access external services.
9. The agent does not inspect or expose credentials, authentication data, or real environment files.
10. The output is concise enough that a reviewer can determine the result without reading the complete raw test log.
