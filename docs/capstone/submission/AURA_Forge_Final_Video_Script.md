# AURA Forge Final Video Script

Target length: 6-8 minutes.

## 0:00-0:30 - Presentation opening

Window/file: `docs/capstone/submission/AURA_Forge_Final_Presentation.pptx`, slide 1.

Say: "This is AURA Forge, my LaunchCode Agentic Engineering capstone. The project is not a FitGPT consumer feature. FitGPT is the real codebase I used to test governed adaptive engineering."

Expected result: audience understands the thesis.

Backup: `docs/capstone/stakeholder-one-pager.md`.

## 0:30-1:20 - Problem and architecture

Window/file: PowerPoint slides 2-4.

Say: "The old route gave every change the same expensive workflow. AURA Forge classifies risk first, then chooses the route, tool grants, gates, and approvals."

Expected result: architecture and route matrix are visible.

Backup: `docs/capstone/final-architecture.md` and `docs/capstone/adaptive-routing.md`.

## 1:20-2:15 - Experimental design and measured results

Window/file: PowerPoint slides 5-6.

Say: "I measured the fixed control route first, froze the router, then measured AURA on the same three representative scenarios."

Expected result: show 19.22% cost reduction, 33.33% fewer model roles, 50% fewer human checkpoints, and 44/48 to 48/48 quality.

Backup: `docs/capstone/control-vs-aura-impact.md`.

## 2:15-3:15 - Governance denial demo

Window/file: terminal in repo plus PowerPoint slide 7.

Command:

```bash
./scripts/capstone-demo.sh denial
```

Say: "This is the governance proof. An implementer attempted to use the Project-Manager-only task tracker. The authorization layer denied it, no external state changed, and model cost was zero."

Expected result: terminal prints denial ID `GO-20260811-001`, role `implementer`, attempted tool `task_tracker`, decision `DENIED`, and the sanitized denial text.

Backup: `docs/capstone/governance-overreach-demo.md` and `docs/capstone/submission/assets/governance-denial.png`.

## 3:15-4:10 - Repository and deterministic evidence

Window/file: terminal in repo.

Command:

```bash
./scripts/capstone-demo.sh routes
./scripts/capstone-demo.sh classifier
```

Say: "The routes are deterministic. LOW removes unnecessary human checkpoints, MEDIUM keeps testing and final approval, and HIGH keeps the full governance route."

Expected result: terminal prints the LOW, MEDIUM, and HIGH route summaries and classifier examples.

Backup: `docs/capstone/risk-classifier.md` and `docs/capstone/adaptive-routing.md`.

## 4:10-5:05 - GitHub Actions evidence

Window/file: browser at `https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31520499134` or PowerPoint slide 8.

Say: "The verified submission-package CI run passed permanent gates: change classification, policy tests, evaluation gate, pipeline integrity, and audit trail. Advisory review skipped safely because the AI secret was unavailable."

Expected result: verified submission-package CI run `31520499134` is visible or summarized.

Backup: `docs/capstone/governance-ci-results.md` and `docs/capstone/submission/assets/github-ci-summary.png`.

## 5:05-6:00 - Change Passport

Window/file: `docs/capstone/evidence/change-passport-AF-HIGH-001.json` and PowerPoint slide 9.

Command:

```bash
./scripts/capstone-demo.sh passport
```

Say: "The Change Passport is the readiness artifact. It aggregates risk tier, route, approvals, tests, policy, CI, and evidence hashes."

Expected result: terminal prints AF-HIGH-001 readiness, route, policy tests, and human checkpoints.

Backup: `docs/capstone/submission/assets/change-passport-summary.png`.

## 6:00-7:15 - Close with limitations and impact

Window/file: PowerPoint slide 10.

Say: "The result is measured, but bounded. I am not claiming company-wide savings or production deployment. The evidence supports the adaptive-autonomy thesis for the three representative scenarios."

Expected result: audience sees measured impact, limitations, and final takeaway.

Backup: `docs/capstone/control-vs-aura-impact.md`.
