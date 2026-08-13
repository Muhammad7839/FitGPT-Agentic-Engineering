# AURA Forge Teleprompter

Use this as the single read-aloud script for the final Gamma deck recording. Target length: about 6 to 8 minutes.

## Slide 1: AURA Forge

Hi, I am Muhammad Imran. My capstone is AURA Forge, a governed adaptive engineering workflow for FitGPT.

The core idea is simple: fixed autonomy makes small changes too expensive, but removing governance from sensitive work is unsafe.

AURA Forge solves that by routing each change by risk, then preserving evidence that the route stayed inside policy.

The best agentic engineering system is not the one that uses the most agents. It is the one that knows when not to use them.

## Slide 2: Fixed autonomy made simple changes too expensive

Before AURA, every change followed the same PRE-AURA route:

Planner to Human Plan Approval to Implementer to Reviewer to Tester to Human Final Approval to Project Manager.

That seven-stage route makes sense for high-risk work. The problem is that low-risk work, like documentation-only cleanup, still paid the full coordination cost.

I did not want to prove savings by weakening governance. The goal was to keep strong controls where they matter and remove unnecessary overhead where they do not.

## Slide 3: AURA Forge routes each change by risk

AURA Forge starts with a deterministic classifier. It reads repository evidence and assigns LOW, MEDIUM, or HIGH risk without calling a model.

Then the adaptive router chooses the route. The route controls which roles participate, which policy gates run, which approvals are required, and which evidence gets captured.

The important boundary is that this is not a production deployment claim. It is a course-system engineering workflow with preserved evidence, policy checks, evals, and CI.

## Slide 4: LOW gets speed. HIGH keeps governance.

The route changes only when risk justifies it.

LOW gets speed: fewer roles and no human checkpoints for simple, bounded work.

MEDIUM keeps review, testing, and one final approval.

HIGH keeps the full governed path: planning, human plan approval, implementation, review, testing, final human approval, and project-manager closure.

The safety point is that HIGH is not optimized away. Sensitive work keeps governance.

## Slide 5: The experiment compared matched scenarios

The experiment used three matched scenarios: LOW, MEDIUM, and HIGH.

LOW represented documentation and accessibility work. MEDIUM represented a bounded executable test change. HIGH represented governance and MCP policy-sensitive work.

For each one, I measured the fixed control route first, froze the AURA router, then measured the AURA route against the same 16-point quality rubric.

That kept the comparison bounded and checkable.

## Slide 6: Less overhead. Stronger quality.

Across the three representative scenarios, AURA Forge reduced successful-route cost by 19.22 percent.

It used 33.33 percent fewer model roles and 50 percent fewer human checkpoints.

Quality improved from 44 out of 48 to 48 out of 48.

LOW had the biggest cost drop, from $0.6066006 to $0.3377550. MEDIUM dropped from $0.9093231 to $0.7300815. HIGH stayed close, from $1.1753241 to $1.1061042, because HIGH kept full governance.

## Slide 7: Governance stopped a real overreach attempt

Now I am going to show the governance denial.

Run:

```bash
./scripts/capstone-demo.sh denial
```

Expected result: the role is `implementer`, the attempted tool is `task_tracker`, and the decision is `DENIED`.

This matters because the role that changes files should not also mark the work complete. The system enforced that boundary through policy, not just through prompt wording.

External state changed: no. Model cost: zero.

## Slide 8: CI made the engineering gates visible

GitHub Actions made the engineering gates visible.

Open this verified CI run:

```text
https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31531270032
```

The important story is failure to diagnosis to repair to rerun. The final verified run, `31531270032`, is green.

The visible gates include classifier behavior, adaptive routing, policy tests, evaluation checks, pipeline integrity, and advisory AI graceful skip when optional credentials are unavailable.

## Slide 9: Change Passport proves readiness

Next is the Change Passport.

Run:

```bash
./scripts/capstone-demo.sh passport
```

Or open:

```text
docs/capstone/evidence/change-passport-AF-HIGH-001.json
```

The Passport gives a reviewer one evidence-backed readiness record: scenario, route, risk tier, quality, policy results, human checkpoints, and source evidence.

This slide also shows the right-tool decision. A stable `DATABASE_URL` documentation/config check was converted to deterministic code. It now runs with zero model cost and about 0.156 milliseconds of local runtime because that factual consistency check does not need a model.

## Slide 10: Impact is measured, bounded, and honest

The impact is measured, bounded, and honest.

AURA Forge reduced overhead for LOW and MEDIUM work while preserving HIGH governance. It improved measured quality in the three-scenario comparison.

It does not claim production deployment. It does not claim real-user production data. It does not make an organization-wide projection. Advisory AI was safely skipped when optional credentials were unavailable.

AURA Forge gives each change the minimum autonomy it deserves, then proves the route stayed inside policy.

That is the project.
