# AURA Forge Portfolio Summary

## Two-line summary

AURA Forge is a governed adaptive engineering workflow for FitGPT that decides how much autonomy each software change deserves. It combines deterministic risk classification, scoped agent roles, policy gates, CI evidence, and a Change Passport so routine changes move faster without weakening governance.

## Problem

FitGPT is a real full-stack application, so not every engineering change should follow the same AI workflow. A small documentation change was being treated too much like a policy-sensitive change, while high-risk changes still needed strong controls.

## Architecture

AURA Forge uses a deterministic classifier to assign `LOW`, `MEDIUM`, or `HIGH` risk. A frozen router then chooses the role path:

- `LOW`: Implementer, Reviewer, deterministic checks.
- `MEDIUM`: Implementer, Reviewer, Tester, final human approval.
- `HIGH`: Planner, plan approval, Implementer, Reviewer, Tester, policy/eval gates, final approval, Project Manager.

## Strongest measured results

Measured across three representative capstone scenarios:

- Quality improved from `44/48` to `48/48`.
- Successful-route cost dropped `19.22%`.
- Model roles dropped `33.33%`.
- Human checkpoints dropped `50%`.
- LOW had the largest gain: cost dropped `44.32%`, model roles dropped `60%`, and human checkpoints dropped `100%`.

## Technologies and techniques

Python, pytest, deterministic classifiers, adaptive routing, MCP-style role authorization, GitHub Actions, CI integrity checks, evidence aggregation, JSON artifacts, policy tests, and PowerPoint/PDF presentation packaging.

## Governance

The project includes a real overreach denial: an `implementer` role attempted a Project-Manager-only `task_tracker` action and was denied by the governed authorization layer. The system also uses deterministic policy tests, audit artifacts, secret scans, and CI gates.

## What Muhammad learned

The strongest agentic system is not always the one with the most agents. The better engineering decision is to use deterministic code when facts are stable, agents when judgment is needed, and humans when accountability or approval cannot be delegated.
