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

| Scenario | Quality | Model cost | Measured model time | Human checkpoints |
|---|---:|---:|---:|---:|
| LOW | `14/16 -> 16/16` | `$0.6066006 -> $0.3377550`, saving `$0.2688456` | `89.398s -> 45.969s`, saving `43.429s` | `2 -> 0` |
| MEDIUM | `15/16 -> 16/16` | `$0.9093231 -> $0.7300815`, saving `$0.1792416` | `193.330s -> 109.502s`, saving `83.828s` | `2 -> 1` |
| HIGH | `15/16 -> 16/16` | `$1.1753241 -> $1.1061042`, saving `$0.0692199` | `248.666s -> 158.510s`, saving `90.156s` | `2 -> 2` |
| Aggregate | `44/48 -> 48/48` | `$2.6912478 -> $2.1739407`, saving `$0.5173071` | `531.394s -> 313.981s`, saving `217.413s` or about `3m 37s` | `6 -> 3` |

Measured model time is a cycle-time proxy because complete human waiting time was not captured consistently across all six runs. Human checkpoint savings are counts only; no hourly labor-dollar claim is made because approval duration was not measured.

## Safety and Governance

AURA Forge includes least-privilege MCP tool boundaries, governed semantic retrieval with citations, deterministic timeout/retry/budget decisions, a real overreach denial, policy tests, pipeline-integrity checks, audit artifacts, and a Change Passport. The last recorded GitHub CI run passed permanent policy, evaluation, integrity, and audit gates; the current unpushed revision still requires a fresh CI run.

## Tradeoffs

AURA Forge does not eliminate governance for sensitive work. HIGH intentionally keeps the full route, so cost reduction is small. That is the point: autonomy is reduced only where risk allows it.

## Recommendation / Next Step

Use AURA Forge as the course-proven paved road for future FitGPT engineering experiments in the isolated course repository. Do not deploy it to production until a separate production-readiness review exists.
