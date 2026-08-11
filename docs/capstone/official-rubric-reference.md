# Official Capstone Rubric Reference

Source: Muhammad's saved/uploaded LaunchCode final capstone assignment page, `Agentic Engineer Capstone: Ship Your Agentic Engineering Paved Road`.

Assignment points: `52`

Submission: `an external tool`

Rubric title: `Agentic Engineer Capstone Project`

Provenance note: this rubric was recovered from Muhammad's previously saved/uploaded LaunchCode capstone assignment page. The local `/Users/muhammad/LaunchCodeAgenticEngineer` reference repository contains only Modules 1-3 and was not the source of the final rubric.

## 1. Workflow Scoping

Assessment:
Assesses whether the learner chose a problem with genuine stakes and defined it precisely enough to measure and demo.

4 pts - Exemplary:

- Workflow selection is backed by quantified baseline pain--time spent, error rate, review backlog, or cost--that makes the before-state concrete and checkable.
- The justification explains why a custom agentic pipeline is the right tool rather than a simpler automation or a prebuilt agent.
- Acceptance criteria are tight enough that a grader could evaluate pass/fail on a real run without asking the learner for clarification.

3 pts - Proficient:

- A real or representative engineering workflow is chosen where agents can credibly improve quality, reduce cycle time, or reduce review burden.
- Stakeholder, trigger, inputs, outputs, acceptance criteria, failure modes, and demo requirements are all defined.
- The choice is justified over at least one alternative with a concrete reason such as volume, judgment complexity, or current cost.
- Module 1-4 artifact gaps are identified before work begins.

2 pts - Developing:

- A workflow is identified and a delivery path is chosen.
- Problem definition is underspecified--at least one of stakeholder, trigger, inputs, outputs, or acceptance criteria is missing or unmeasurable.
- The case for why this workflow benefits from a custom agentic pipeline is asserted rather than argued.

1 pt - Beginning:

- No workflow is defined, or the chosen task is trivial and could be handled by a general-purpose agent without customization.
- Stakeholder, trigger, inputs, outputs, and acceptance criteria are absent or too vague to evaluate.

## 2. Sandboxed Environment

Assessment:
Assesses whether the agent runs inside a properly bounded container that protects the host machine, credentials, and parallel sessions.

4 pts - Exemplary:

- Mounts are minimal, network egress is constrained, and credentials are ephemeral or read-only--the container is airtight.
- The README includes a prerequisite check, example commands, and a troubleshooting note.
- Someone could fork, run, and debug without any assistance from the author.

3 pts - Proficient:

- A containerized harness is provided with explicit filesystem, network, and credential boundaries.
- Parallel-session isolation is documented.
- A stranger can fork and run the system in under 15 minutes by following the README.

2 pts - Developing:

- A container exists but at least one boundary is missing or untested.
- Filesystem restrictions are too broad, network egress is unconstrained, or credentials are hardcoded rather than scoped.
- Parallel-session isolation is unverified or undocumented.

1 pt - Beginning:

- No container or explicit boundaries are present; the agent runs directly on the host.
- Credential scoping and parallel-session isolation are absent.

## 3. Quality Spec & Baseline

Assessment:
Assesses whether the learner defined what good output looks like and captured a first-run baseline precise enough to make every later improvement provable.

4 pts - Exemplary:

- Rubric thresholds are tied to specific business outcomes with documented rationale.
- The baseline is precise enough that any future run can be compared without re-interpretation.
- Alternatives considered during rubric design are noted alongside the file--raw material for the capstone ADR.

3 pts - Proficient:

- A complete PRD names triggers, decision events, actions, and acceptance criteria.
- The quality rubric has three to six dimensions with a scoring guide, example cases at each level, and pass thresholds.
- Baseline measurements cover quality, review latency, cycle time, and cost per run.

2 pts - Developing:

- A PRD exists but acceptance criteria are incomplete or unmeasurable.
- The rubric has dimensions but lacks example cases at each scoring level, or pass thresholds are missing.
- Baseline measurements cover fewer than two of quality, speed, and cost.

1 pt - Beginning:

- No PRD, quality rubric, or baseline measurements are provided.
- Success criteria are absent or too vague to score against.

## 4. Agent, Skills & Memory

Assessment:
Assesses whether the learner built a layered memory system and used the self-improving loop to keep it sharp through real session outcomes.

4 pts - Exemplary:

- The self-improving loop is visible in commit history: a run-review-fix-rerun cadence is evident across multiple sessions.
- Memory scoping prevents leakage across sessions.
- Stale entries are pruned with documented reasons.
- Reflection entries show before/after rubric scores confirming that each change held on a rerun.

3 pts - Proficient:

- At least one versioned agent definition and at least two versioned skills live alongside the code.
- Persistent memory layout is documented with a memory-vs-context-vs-prompt decision rationale.
- The reflection log contains at least three entries that each produced a concrete agent, skill, or memory update.

2 pts - Developing:

- At least one agent or skill file exists, but versioning is inconsistent, or the files are not committed alongside the code.
- A memory layout is present, but the allocation across skill, context, and persistent storage is undocumented.
- Reflection log entries exist, but do not describe what changed or why.

1 pt - Beginning:

- No versioned agent definitions or skills are present in the repository.
- Persistent memory is absent or undocumented.

## 5. Orchestration & MCP Tools

Assessment:
Assesses whether the learner designed a well-scoped multi-agent pipeline and stood up MCP-backed tools that are narrow, validated, and ready to govern.

4 pts - Exemplary:

- The blueprint justifies the coordination model with concrete reasoning, and a reader could implement the design from the diagram and map alone without asking clarifying questions.
- Tool grants are deliberately narrow--each subagent accesses only what its role requires.
- The MCP tools are schema-validated, classification-tagged, and citation-bearing, ready for governance enforcement.

3 pts - Proficient:

- An orchestration diagram shows the orchestrator delegating to scoped subagents, including planner, implementer, reviewer, tester, and at least one additional role.
- A routing-and-tool-grant map explains which subagent calls which MCP tools and why.
- At least one MCP-backed persistent storage tool and one vector retrieval tool are configured with schema definitions, classification tags, and citation expectations.
- Human-in-the-loop checkpoints are defined with clear trigger criteria.

2 pts - Developing:

- Multiple agents exist, but the routing-and-tool-grant map is missing or incomplete.
- It is not clear which subagent calls which tools or why the scoping was chosen.
- MCP tools are connected, but at least one of the schema definitions, classification tags, or citation rules is absent.

1 pt - Beginning:

- No orchestration diagram or subagent delegation is present.
- Tool access is global, and no MCP-backed persistent storage or retrieval is configured.

## 6. Evaluation & Calibration

Assessment:
Assesses whether the learner built an evaluation harness that catches real failures and used it to drive documented, evidence-backed improvements.

4 pts - Exemplary:

- The evaluation suite covers normal, edge, and adversarial cases.
- Regression checks confirm that changes did not degrade prior performance.
- Every calibration log entry cites specific holdout scores or failure evidence, so the reasoning behind each decision cannot be revised after the fact.

3 pts - Proficient:

- A holdout-set evaluation harness combines deterministic checks with rubric-based scoring.
- At least three production-representative runs are documented with logs or transcripts.
- Each calibration log entry shows what changed--routing, prompt, subagent scope, or tool grant--and ties that change to a specific eval result or observed failure.

2 pts - Developing:

- An evaluation harness exists, and at least one run is logged.
- Fewer than three representative runs are documented.
- The calibration log records what changed but not why--entries are not connected to specific eval results or observed failures.

1 pt - Beginning:

- No evaluation harness, holdout set, or run evidence is present.
- Results are anecdotal.

## 7. Governance, Security & CI/CD

Assessment:
Assesses whether the learner enforced least-privilege access and eval-gated change control in code, not just in documentation.

4 pts - Exemplary:

- Governance is testable: a policy-bypass or overreach attempt is shown failing in the demo.
- Eval-gated change control is visible in commit history--at least one change was blocked or modified because of a failing eval.
- Escalation and rollback criteria are explicitly defined and connected to quality thresholds.
- Red-team or policy-bypass checks are documented.
- No secrets, PII, or proprietary data appear in any submitted artifact.

3 pts - Proficient:

- A role-to-tool access matrix establishes least-privilege defaults and documents justification to widen.
- Policies are enforced in configuration through MCP allow-lists, skill activation rules, CI/CD checks, or container permissions rather than only in a document.
- Prompt, skill, tool-contract, and policy changes must pass the relevant eval or policy test before merging.
- The audit log contains real entries capturing agent actions, tool calls, policy decisions, human approvals, failures, retries, and rollbacks.
- Secrets handling and data classification are demonstrated.

2 pts - Developing:

- A governance document and a CI/CD pipeline both exist, but neither is enforced in code.
- The role-to-tool access matrix is not reflected in the MCP allow-lists or container permissions.
- Prompt or policy changes can merge without passing an eval or policy test.
- The audit log template contains no entries from real runs.

1 pt - Beginning:

- No governance policy, role-to-tool access matrix, audit logging, or CI/CD integration is present.
- Permissions are undifferentiated, and secrets may be exposed.

## 8. Right-Tool Decisions & ADRs

Assessment:
Assesses whether the learner made and documented deliberate engineering judgments about when to use an agent, deterministic code, or a human--and can defend those choices with evidence.

4 pts - Exemplary:

- Conversion evidence is quantitative and compelling--measured latency cuts or cost reductions justify the decision.
- The agent-vs-deterministic-vs-human matrix is clear enough that a new team member could apply the same logic to future steps without guidance.
- At least one rejected alternative in every ADR cites concrete evidence from logs, evals, cost data, or calibration results.
- The records read as real engineering reasoning made at decision time rather than retroactive documentation.

3 pts - Proficient:

- Every major workflow step is classified as agentic, deterministic, or human-reviewed with a stated rationale.
- At least one stable agentic step is converted to deterministic code with before/after evidence covering latency, cost, predictability, and audit clarity.
- ADRs cover rubric design, memory layout, MCP boundaries, subagent scoping and routing, governance policy, and the agent-to-deterministic conversion.
- Each ADR includes context, decision, rejected alternatives, evidence, consequences, and open risks.

2 pts - Developing:

- Steps are labeled as agent, deterministic, or human, but the rationale is superficial.
- Labels are applied without explaining the trade-offs.
- ADRs exist for some decisions, but at least one required area is missing.
- The records that do exist do not cite rejected alternatives with evidence.

1 pt - Beginning:

- All steps are agentic regardless of suitability, or no rationale is provided for any step.
- No Architecture Decision Records are included.

## 9. Production Integration & Tool-Evolution Drill

Assessment:
Assesses whether the learner ran a complete, production-like pipeline with real controls and used the self-improving loop to document a real regression and fix.

4 pts - Exemplary:

- The tool-evolution drill demonstrates the self-improving loop catching a real regression--the eval harness flagged a problem that was not caught manually.
- The monitoring and incident runbook are specific enough to act on without guesswork.
- The system degrades gracefully under failure conditions.
- Escalation and rollback paths are tested rather than only documented.

3 pts - Proficient:

- The complete agent, deterministic, and human workflow runs end-to-end on real, sanitized, public, or representative data.
- Reliability controls and cost controls are present.
- The tool-evolution drill documents the change attempted, what broke, what improved, what the eval harness detected, what was fixed, and the final result.

2 pts - Developing:

- An end-to-end run is attempted, but reliability controls (timeouts, retries, fallbacks) or cost controls (per-call and per-workflow budgets) are missing.
- A tool-evolution drill is attempted, but the documentation is incomplete--what broke, what improved, or what the eval harness detected is not clearly recorded.

1 pt - Beginning:

- The pipeline is not run end-to-end; only isolated components are demonstrated.
- No reliability or cost controls are present, and the tool-evolution drill is absent.

## 10. Iteration Narrative & Impact

Assessment:
Assesses whether the learner can show the system measurably improved through evidence-driven iteration, not just that it eventually worked.

4 pts - Exemplary:

- The iteration narrative reads as a coherent engineering story: baseline problem, first run, what failed, what changed and why, improved result--each step backed by logs, eval scores, or calibration entries.
- The impact report distinguishes measured gains from projected gains with specific and defensible assumptions.
- The self-improving loop ran across the full course, not just in the final drill, and this is visible in the commit history and calibration log.

3 pts - Proficient:

- Post-capstone results are compared against the Module 1 baseline across quality, review latency, defect rate, cycle time, and cost per run, with proxy metrics explained where direct measurement is impossible.
- The submission shows at least two improvement cycles--a change made because of eval or run evidence, and a rerun confirming the change held.
- Results are packaged into a stakeholder-ready impact report.

2 pts - Developing:

- Before/after metrics are presented but the baseline is vague or the delta analysis is incomplete.
- The iteration narrative describes changes without connecting them to eval evidence, making it impossible to tell what drove each improvement.

1 pt - Beginning:

- No baseline comparison or post-capstone metrics are provided.
- There is no evidence that the system improved between the first run and the final submission.

## 11. Stakeholder Communication

Assessment:
Assesses whether the learner can translate the same engineering work into language and form that serve both a technical reviewer and a non-engineer decision-maker.

4 pts - Exemplary:

- The one-pager is portfolio-ready: a hiring manager or engineering director could read it in two minutes and understand both the problem solved and the value created.
- The video is compelling, on-time, and shows governance stopping an over-reaching agent so the safety story is visible rather than claimed.
- A technical reviewer can evaluate the full submission in five minutes and probe any engineering decision in 30.

3 pts - Proficient:

- The stakeholder one-pager translates the system into terms a non-engineer can act on: hours saved, defects avoided, dollars recovered, risks managed, and next steps.
- The walkthrough video runs five-to-ten minutes and is understandable to a technical reviewer while making the value clear to a semi-technical manager.
- All submitted artifacts are sanitized--no secrets, PII, proprietary data, internal URLs, or customer data are present.

2 pts - Developing:

- A stakeholder one-pager exists but stays at the level of features and outputs.
- It does not translate results into hours saved, defects avoided, or dollars recovered.
- The walkthrough video covers the technical demo but does not connect engineering decisions to business outcomes.

1 pt - Beginning:

- The stakeholder one-pager is missing or is a copy of the technical write-up with no translation for a non-engineer audience.
- The walkthrough video does not make the value of the system clear to a semi-technical viewer.

## 12. Clarity & Flow

Assessment:
Assesses whether the overall presentation tells a coherent story from baseline problem through to measured impact.

4 pts - Exemplary:

- The presentation frames the project around a compelling engineering problem from the first minute and builds a narrative arc that makes the value feel earned rather than reported.
- Transitions between technical and stakeholder sections are seamless.

3 pts - Proficient:

- The presentation follows a clear sequence: problem and baseline, architecture, live run, governance, evaluation, right-tool decisions, impact, and operations.
- Both a technical reviewer and a semi-technical manager can follow their relevant section from start to finish.

2 pts - Developing:

- The presentation covers problem, solution, and result but fails to connect them in a logical narrative.
- The flow feels disjointed and transitions between technical and stakeholder sections are abrupt.

1 pt - Beginning:

- The presentation is disorganized and difficult to follow.
- The purpose of the project is unclear.

## 13. Design

Assessment:
Assesses whether the visual presentation supports the content and reflects the professionalism expected of a portfolio piece.

4 pts - Exemplary:

- The design actively enhances the message.
- Visual hierarchy guides the audience to critical information.
- Complex ideas such as orchestration flows, governance matrices, and before/after metrics are made intuitive through thoughtful visual choices.

3 pts - Proficient:

- The layout is clean and consistent.
- Architecture diagrams, decision matrices, and impact charts are legible at presentation size.
- The design supports the information without distracting the audience.

2 pts - Developing:

- The presentation is functional but plain.
- Minor inconsistencies or unclear diagrams detract from the message without obscuring it entirely.

1 pt - Beginning:

- The presentation is visually messy with frequent errors.
- Diagrams are unreadable and the overall impression is unprofessional.
