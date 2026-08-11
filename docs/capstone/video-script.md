# Video Script

Target length: 5-7 minutes.

## 0:00-0:30

"My capstone is called AURA Forge. It is a governed adaptive engineering workflow around FitGPT. I am not trying to add another consumer feature to FitGPT here. I am solving an engineering problem: how much autonomy should an AI workflow get for a specific software change?"

## 0:30-1:10

"The fixed baseline route sent every representative change through the same heavy workflow: Planner, human approval, Implementer, Reviewer, Tester, another human approval, and Project Manager. That is safe, but it is not always efficient. A small documentation change does not need the same route as a governance or MCP policy change."

## 1:10-1:55

"AURA Forge starts with deterministic risk classification. It classifies a change as LOW, MEDIUM, or HIGH. Then a frozen router selects the route. LOW receives the lightest justified route, MEDIUM keeps implementation, review, and test evidence, and HIGH keeps full governance."

## 1:55-2:45

"For LOW, the fixed baseline scored 14 out of 16 and cost 0.6066006 dollars. AURA scored 16 out of 16 and cost 0.3377550 dollars. That is a 44.32 percent cost reduction, 60 percent fewer model roles, and no human checkpoints for a low-risk documentation change."

## 2:45-3:25

"For MEDIUM, AURA still kept engineering rigor. It used Implementer, Reviewer, Tester, and final human approval. Quality improved from 15 to 16 out of 16, cost dropped 19.71 percent, model roles dropped 40 percent, and human checkpoints dropped 50 percent."

## 3:25-4:00

"For HIGH, the system deliberately preserved governance. It kept the full route and both human checkpoints because the change touched sensitive evaluation and MCP-governance areas. Cost only dropped 5.89 percent, but quality improved from 15 to 16 out of 16."

## 4:00-4:45

"The safety story is not just documentation. I ran a real governance overreach demo. An implementer role attempted to use the Project-Manager-only task tracker. The governed MCP authorization layer denied it. That denial is recorded as GO-20260811-001."

## 4:45-5:30

"The project also has real GitHub Actions governance CI. The first run failed because the evaluation job was missing pytest. I preserved the failed run, repaired the workflow, and the terminal run passed policy, evaluation, pipeline integrity, advisory skip, and audit trail."

## 5:30-6:10

"The Change Passport pulls the important evidence into one machine-readable artifact: classifier, route, roles used, approvals, tests, costs, timing, and GitHub CI status. I also converted one stable documentation/configuration check from an agentic auditor task into deterministic code, because not every task should be agentic."

## 6:10-6:45

"The measured aggregate result across three representative scenarios was quality improving from 44 out of 48 to 48 out of 48, successful-route cost dropping 19.22 percent, model roles dropping 33.33 percent, and human checkpoints dropping 50 percent. These are measured only across the three capstone scenarios. I am not claiming production-wide savings."

## 6:45-7:00

"The main takeaway is that good agentic engineering is not maximum automation. It is choosing the right amount of autonomy, proving the route stayed inside policy, and leaving evidence that a reviewer can actually trust."
