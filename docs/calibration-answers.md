# Module 3 Calibration Answers

## Question 1

The before-fix transcript showed one real bounded `mcp__coursetools__test_runner` event from the Tester role. That mattered because it separated tool execution from output formatting: the Tester had the right bounded test capability and used it once, but reported the outcome under `## Status` instead of the required `## Result`.

The deterministic check validates exact ordered headings in the Tester output. It does not interpret intent or accept near matches. Because `## Result` was absent, the check failed consistently even though the dummy tool event existed. That isolated the root cause as an output-contract fault rather than a routing or tool-access failure.

## Question 2

The fix belonged at the Prompt layer because `.claude/agents/tester.md` defined the Tester's required output contract and the induced fault changed that contract from `## Result` to `## Status`.

Changing routing would not make the Tester produce the required heading. Changing tool grants would not address the malformed output. Accepting `## Status` in the evaluator would weaken the contract and hide the defect. Restoring `## Result` in the Tester definition fixed the producer at the source while keeping enforcement strict.

## Question 3

The after-fix development rerun proves the targeted prompt fix worked for the tuned development task: the Tester used the bounded dummy test tool and returned the required `## Result` heading.

Regression checks show previously passing preserved development behavior still satisfies deterministic gates after the evaluation changes. They protect against breaking known-good routing, tool authorization, approval scoping, protected-path checks, and the Tester schema gate.

The clean holdout measurement tests generalization on the locked unseen tasks. In this run, all seven holdouts failed before rubric scoring because the holdout conversations had tools disabled and therefore did not exercise the role/tool orchestration path.

None of these alone proves complete production health. The course `test_runner` and `task_tracker` are dummy tools, and these evaluations do not establish real pytest results, deployment behavior, live integrations, security completeness, or full backend correctness.
