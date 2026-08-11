# ADR 0004: Adaptive Risk Routing

## Context

The PRE-AURA route sent LOW, MEDIUM, and HIGH through the same full route. AURA introduced deterministic `aura-risk-v1` and `aura-router-v1`, frozen at `c844db1b457712d4c68c9353c49e8bd9fd2121a1`.

## Decision

Use deterministic path/metadata classification and fixed route plans per tier. Do not tune the router during measurement.

## Rejected Alternatives

- Model-decided risk routing. Rejected because routing must be reproducible and auditable.
- Always using the full route. Rejected because LOW measured as materially over-served.
- Always minimizing cost. Rejected because HIGH must preserve strong governance.

## Evidence

- LOW: model roles reduced from `5` to `2`, human checkpoints from `2` to `0`, quality improved from `14/16` to `16/16`.
- MEDIUM: model roles reduced from `5` to `3`, human checkpoints from `2` to `1`.
- HIGH: retained `5` model roles and `2` human checkpoints.

## Consequences

The route is risk-sensitive without being ad hoc.

## Open Risks

Future HIGH categories such as deployment, auth, database migration, or production configuration may need extra deterministic gates beyond the measured scenario.
