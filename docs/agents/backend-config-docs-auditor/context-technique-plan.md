# Context-Management Technique Plan

## Explicit Boundary 1: Start of Evidence Discovery

The opening message will establish that setup is complete and Phase 1 is beginning.

It will state the discovery goal, active evidence rules, prohibited actions, and the final deliverable that later phases must support.

Reason:

The first boundary prevents the agent from treating preliminary setup or repository inspection as part of the substantive audit.

## Explicit Boundary 2: Evidence Discovery to Recommendation Draft

This boundary will state that Phase 1 is complete and that Phase 2 may now create recommendations.

It will preserve the verified facts and open questions while introducing the new permission to draft documentation, test, and code recommendations prioritized by production risk.

Reason:

Evidence gathering and recommendation design require different behavior. Separating them reduces the risk that the agent invents recommendations before it has established the current facts.

## Proactive Summary: End of Phase 2

The agent will summarize the session after completing the broad recommendation draft and before receiving the stakeholder requirement change.

The summary must preserve:

- Current goal
- Active constraints
- Decisions
- Stable recommendation IDs
- Current recommendation state
- Supporting evidence
- Open questions
- Next action

Reason:

The recommendation draft is the artifact that Phase 3 must revise. Capturing its exact state before the requirement change makes it possible to determine whether the agent correctly updates or incorrectly preserves superseded recommendations.

## Explicit Boundary 3: Stakeholder Change and Finalization

This boundary will state that Phase 2 is complete and introduce the changed audience, prioritization rule, and allowed recommendation categories.

It will identify:

- Requirements that remain active
- Requirements that are superseded
- Evidence that still matters
- The Phase 2 recommendation draft that must be revisited

Reason:

The requirement change creates the highest context-drift risk in the session. An explicit boundary places the new rules at the top of the current turn and prevents the agent from silently mixing production-risk and onboarding-risk priorities.

## Final Context Check

After the final report, the agent will identify which Phase 2 recommendation IDs were retained, changed, or removed and confirm that no superseded production-code recommendation remains.

Reason:

The final check directly tests whether the agent's locally reasonable final output reflects one coherent current requirement set.

## Compaction

Compaction will not be used unless visible context usage reaches at least 75 percent.

If the session remains below that threshold, the Iteration Log will state that compaction was unnecessary because boundaries and summarization were sufficient.

Reason:

Compaction can discard exact artifact state. This session already has a planned proactive summary, so compaction should remain a fallback rather than the primary technique.
