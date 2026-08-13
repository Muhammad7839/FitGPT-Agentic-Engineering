# AURA Forge Speaker Notes

Historical note: these notes were created for the earlier Codex-generated deck. The final Gamma recording should use `docs/capstone/submission/AURA_Forge_TELEPROMPTER.md`.

Target duration: 6-8 minutes.

## Slide 1: AURA Forge

Goal: Open with the project thesis.

What to say: This project is AURA Forge. It is not a FitGPT feature demo. FitGPT is the real codebase I used to test an agentic engineering system that decides how much autonomy a change deserves.

What to point at: Point to the thesis box on the right.

Transition: Next, explain why the old fixed route was the problem.

Sources:
- `docs/capstone/stakeholder-one-pager.md`
- `docs/capstone/final-rubric-audit.md`

## Slide 2: Fixed autonomy made simple changes too expensive

Goal: Show why fixed autonomy is wrong.

What to say: Before AURA, representative changes went through the same full path: Planner, human approval, Implementer, Reviewer, Tester, another human approval, and Project Manager. That was defensible for high risk, but too heavy for low risk.

What to point at: Point across the fixed route, then contrast LOW and HIGH.

Transition: Now show how AURA makes the route deterministic and risk-based.

Sources:
- `docs/capstone/control-baseline-comparison.md`
- `docs/routing-and-tool-grant-map.md`

## Slide 3: AURA Forge routes each change by risk

Goal: Explain the architecture clearly.

What to say: AURA separates risk classification from execution. The classifier is deterministic and model-free. The router uses that result to choose roles, tools, gates, and approvals.

What to point at: Point from Change through Change Passport.

Transition: Next, compare the three actual routes.

Sources:
- `docs/capstone/final-architecture.md`
- `docs/capstone/risk-classifier.md`
- `docs/capstone/adaptive-routing.md`

## Slide 4: LOW gets speed; HIGH keeps governance

Goal: Make adaptive autonomy concrete.

What to say: LOW kept an implementer, an independent reviewer, and deterministic gates. MEDIUM kept implementer, reviewer, tester, and one final approval. HIGH kept the full governed route.

What to point at: Point to each route row, especially the HIGH row.

Transition: Next, explain how the evidence was measured.

Sources:
- `docs/capstone/adaptive-routing.md`
- `docs/capstone/aura-results.md`

## Slide 5: The experiment compared matched scenarios

Goal: Establish credibility of the experiment.

What to say: I used three representative scenarios: a LOW documentation change, a MEDIUM executable/test change, and a HIGH governance-sensitive change. I measured the fixed control route first, froze the router, then measured AURA.

What to point at: Point to the three scenario boxes and the matched-rules line.

Transition: Now show the measured results.

Sources:
- `docs/capstone/representative-scenarios.md`
- `docs/capstone/quality-rubric.md`
- `docs/capstone/control-vs-aura-impact.md`

## Slide 6: Measured results: less overhead, stronger quality

Goal: Present the measured result without overclaiming.

What to say: Across the three representative scenarios, AURA improved quality from 44 out of 48 to 48 out of 48. Successful-route cost dropped 19.22 percent, model roles dropped 33.33 percent, and human checkpoints dropped 50 percent.

What to point at: Point at LOW first because it shows the largest reduction, then call out HIGH retaining governance.

Transition: Next, show that governance was not only documented; it stopped overreach.

Sources:
- `docs/capstone/control-vs-aura-impact.md`
- `docs/capstone/aura-results.md`

## Slide 7: Governance stopped a real overreach attempt

Goal: Make the safety story visible.

What to say: This is the most important demo moment. An implementer attempted to use the Project-Manager-only task tracker. The real governed authorization layer denied it. No external state changed, and the model cost was zero.

What to point at: Point to DENIED, then read the sanitized denial sentence.

Transition: Next, connect this local governance boundary to CI gates.

Sources:
- `docs/capstone/governance-overreach-demo.md`
- `docs/capstone/governance-ci-local-verification.md`

## Slide 8: CI made the engineering gates visible

Goal: Show that the project is eval-gated.

What to say: The repository did not stop at local files. The verified submission-package CI run passed GitHub Actions. The advisory review also behaved safely: when the AI secret was unavailable, it skipped gracefully instead of failing open.

What to point at: Point to verified CI run 31531270032 and the green job list.

Transition: Next, show how all of this evidence is packaged.

Sources:
- `docs/capstone/governance-ci-results.md`
- `docs/capstone/final-evidence-snapshot.md`

## Slide 9: The Change Passport turns evidence into readiness

Goal: Explain the Change Passport and right-tool lesson.

What to say: The Change Passport pulls together risk tier, route, roles, tests, approvals, policy, CI, and readiness. I also found that some work should not be agentic at all. A narrow config/docs check became deterministic code with zero model cost.

What to point at: Point to the Passport fields, then the evidence-flow asset.

Transition: Close by stating the bounded impact and remaining human tasks.

Sources:
- `docs/capstone/change-passport.md`
- `docs/capstone/evidence/change-passport-AF-HIGH-001.json`
- `docs/capstone/deterministic-conversion.md`

## Slide 10: Impact is measured, bounded, and honest

Goal: Close with the honest takeaway.

What to say: The measured evidence supports the thesis, but only for these three representative scenarios. The important result is not just lower cost. It is matching autonomy to risk and proving the system stayed governed.

What to point at: Point to measured impact, limitations, and final takeaway.

Transition: End the recording and move to submission links/checklist.

Sources:
- `docs/capstone/control-vs-aura-impact.md`
- `docs/capstone/final-rubric-audit.md`
