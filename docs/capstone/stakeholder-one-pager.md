# AURA Forge Stakeholder One-Pager

## Problem

FitGPT is a real full-stack application, so engineering changes vary widely in risk. A fixed AI workflow treats a small documentation update too much like a governance-sensitive code change. That wastes agent time and human approval effort on low-risk work, while still needing strong controls for high-risk work.

## What AURA Forge Does

AURA Forge is a governed engineering workflow around FitGPT. It classifies a change as LOW, MEDIUM, or HIGH risk using deterministic rules, then routes it through the minimum justified mix of agents, deterministic checks, policy gates, and human approvals.

It does not ask how many AI agents can automate a software change. It decides how much autonomy the change deserves and proves the agents stayed inside policy.

## Why It Matters

The goal is faster routine engineering without weakening governance. Low-risk changes should not need a full multi-agent approval chain. Sensitive changes should keep the full controls.

## Measured Results

Measured across three representative scenarios only:

| Scenario | Quality | Cost change | Model-role change | Human-checkpoint change |
|---|---:|---:|---:|---:|
| LOW | `14/16 -> 16/16` | `-44.32%` | `-60%` | `-100%` |
| MEDIUM | `15/16 -> 16/16` | `-19.71%` | `-40%` | `-50%` |
| HIGH | `15/16 -> 16/16` | `-5.89%` | unchanged | unchanged |
| Aggregate | `44/48 -> 48/48` | `-19.22%` | `-33.33%` | `-50%` |

## Safety and Governance

AURA Forge includes least-privilege MCP tool boundaries, a real overreach denial, policy tests, pipeline-integrity checks, audit artifacts, and a Change Passport. The final GitHub CI run passed permanent policy, evaluation, integrity, and audit gates.

## Tradeoffs

AURA Forge does not eliminate governance for sensitive work. HIGH intentionally keeps the full route, so cost reduction is small. That is the point: autonomy is reduced only where risk allows it.

## Recommendation / Next Step

Use AURA Forge as the course-proven paved road for future FitGPT engineering experiments in the isolated course repository. Do not deploy it to production until a separate production-readiness review exists.
