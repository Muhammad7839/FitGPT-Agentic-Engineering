# Governance Risk Analysis

This document records the real FitGPT orchestration risks used to design the Module 4 governance baseline. It is newly designed for this target repository; it was not ported from Module 4 template files.

## Risk Patterns

### Unauthorized tracker access

- Observed near-miss: `docs/routing-and-tool-grant-map.md` records that Failed Run 2 showed prompt-only Orchestrator separation was insufficient because the Orchestrator attempted `task_tracker` before the later process-level denial pattern.
- Risk statement: A coordinating or implementation role with tracker access can mutate workflow state before independent review, testing, and human approval.
- Affected role: orchestrator, implementer, reviewer, tester, dependency-auditor.
- Boundary: deny tracker-equivalent state updates except for project-manager after final approval.
- Policy denial or checkpoint: non-project-manager roles are denied issue-update and external-state operations; project-manager requires final human approval.

### Unsupported Tester success

- Observed near-miss: `docs/calibration-log.md` records that the before-fix Tester used the bounded dummy `test_runner` but reported the result under `## Status` instead of required `## Result`.
- Risk statement: A role can have the right tool event and still produce an invalid or unsupported outcome if the output contract is not enforced.
- Affected role: tester, orchestrator.
- Boundary: deterministic output-schema enforcement and Tester handoff prerequisites.
- Policy denial or checkpoint: tester cannot repair, retry broadly, or update external state; it may only run the focused bounded test representation and must return the required structure.

### Missing handoff prerequisites

- Observed near-miss: `docs/calibration-log.md` preserves blocked attempts where incomplete Tester evidence did not satisfy the accepted before-fix measurement.
- Risk statement: Missing prerequisite evidence can be replaced by plausible prose unless handoff gates remain explicit and role-specific.
- Affected role: orchestrator, tester, reviewer.
- Boundary: role-specific handoffs, approval checkpoints, and deterministic transcript gates.
- Policy denial or checkpoint: tester requires Reviewer pass evidence, changed-file list, exact target, and acceptance criteria before acting.

### Excessive or missing tool exposure

- Observed near-miss: `docs/calibration-log.md` records that the holdout measurement failed because tools were disabled and the role/tool orchestration path was not exercised.
- Risk statement: Tool exposure drift in either direction can invalidate evaluation: overexposure permits unsafe actions, while underexposure prevents the governed workflow from running.
- Affected role: all governed roles.
- Boundary: explicit policy-to-runtime allow-lists and static policy tests.
- Policy denial or checkpoint: every grant must be explicit, and runtime evidence must not be claimed until the required image-dependent checks run.

### Protected-path modification risk

- Observed near-miss: `docs/holdout-task-set.md` includes protected-path modification as a locked risk for documentation work, especially HO-05.
- Risk statement: A documentation or advisory workflow can drift into production code or production test changes to make the task appear complete.
- Affected role: implementer, reviewer, tester, dependency-auditor.
- Boundary: writable-path allow-lists, read-only containers for advisory roles, and protected checksum comparisons.
- Policy denial or checkpoint: advisory roles use read-only workspaces; implementer remains bounded by explicit approved writable paths.

## Least-Privilege Defaults

When no recorded near-miss applies directly, the policy uses least privilege:

- Advisory roles receive read-only workspaces and no memory mount.
- State-changing storage operations are denied unless they are part of the role's job.
- Retrieval is limited by a data classification ceiling.
- Skills are denied unless they directly support the role's responsibility.
- Unknown roles are denied by default.
