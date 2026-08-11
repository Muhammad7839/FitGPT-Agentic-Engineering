# AURA Forge Teleprompter

Use this as the single read-aloud script for the final recording. Target length: about 6 to 8 minutes.

## Slide 1

Hi, I’m Muhammad Imran. My capstone is AURA Forge, a governed adaptive engineering workflow for FitGPT.

The main idea is simple: not every software change deserves the same amount of AI autonomy. A small documentation change should not need the same full route as a governance-sensitive change. AURA Forge decides how much autonomy a change deserves, then proves the route stayed inside policy.

## Slide 2

Before AURA, the route was fixed. A change went through Planner, human approval, Implementer, Reviewer, Tester, another human approval, and Project Manager.

That route made sense for high-risk work, but it was too expensive for low-risk work. A documentation-only change got over-served. At the same time, I did not want to remove governance from sensitive work just to show savings.

## Slide 3

AURA Forge starts with deterministic risk classification. The classifier assigns LOW, MEDIUM, or HIGH from repository evidence. It does not call a model.

Then the adaptive router chooses the route. The evidence boundary matters here: every route emits structured evidence, policy results, eval results, approvals when required, and CI signals. The system is designed to avoid unsupported production claims.

## Slide 4

The route changes only when risk justifies it.

LOW gets Implementer, Reviewer, and deterministic gates. MEDIUM gets Implementer, Reviewer, Tester, and final approval. HIGH keeps the full governed route: Planner, plan approval, Implementer, Reviewer, Tester, policy and evaluation gates, final approval, and Project Manager.

The key point is that HIGH is not optimized away. Sensitive work keeps governance.

## Slide 5

I measured three matched scenarios: LOW, MEDIUM, and HIGH.

LOW was a documentation and accessibility scenario. MEDIUM was a bounded executable test change. HIGH was governance and MCP policy-sensitive.

For each one, I measured the fixed control route first, froze the router, and then measured the AURA route. The quality rubric stayed locked at 16 points.

## Slide 6

Here are the measured results.

Across the three representative scenarios, quality improved from 44 out of 48 to 48 out of 48. Successful-route cost dropped 19.22 percent. Model roles dropped 33.33 percent. Human checkpoints dropped 50 percent.

LOW had the clearest gain because it was over-served before. HIGH kept the same number of model roles and human checkpoints because that was the right safety decision.

## Switch to live denial evidence

Now I’m going to show the governance denial.

Run:

```bash
./scripts/capstone-demo.sh denial
```

This is the most important safety moment. An Implementer attempted to use the Project-Manager-only task tracker. The governed authorization layer denied it. External state changed: no. Model cost: zero.

## Slide 7

This slide summarizes that denial. The role was `implementer`, the attempted tool was `task_tracker`, and the decision was `DENIED`.

This matters because the role that changes files should not also mark the work complete. That separation is enforced by the system, not just by a prompt instruction.

## Switch to routes evidence

Run:

```bash
./scripts/capstone-demo.sh routes
```

This shows that the classifier and router are deterministic. LOW, MEDIUM, and HIGH produce the expected route IDs and role summaries.

## Slide 8

The project also uses GitHub Actions as engineering evidence.

Open the verified submission-package CI run:

```text
https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31520499134
```

The important point is not that CI exists. It is that the permanent gates are visible: change classification, policy tests, evaluation, pipeline integrity, audit trail, and advisory graceful skip when the optional AI secret is unavailable.

## Slide 9

Next is the Change Passport.

Run:

```bash
./scripts/capstone-demo.sh passport
```

The Passport gives a reviewer one evidence-backed summary: scenario, readiness, quality, risk tier, route, policy tests, human checkpoints, and source evidence. It is generated from files and machine evidence, not from memory.

I also converted one narrow agentic step to deterministic code. A stable `DATABASE_URL` documentation and config check now runs with zero model cost because that kind of factual check does not need a model.

## Slide 10

The impact is measured, bounded, and honest.

AURA Forge improved quality and reduced overhead for LOW and MEDIUM work, while keeping HIGH governance in place. It does not claim production deployment. It does not claim company-wide savings. It uses three representative scenarios and real course-system evidence.

The final takeaway is: AURA Forge gives each change the minimum autonomy it deserves, then proves the route stayed inside policy.

That is the project.
