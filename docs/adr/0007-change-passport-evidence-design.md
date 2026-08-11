# ADR 0007: Change Passport Evidence Design

## Context

The capstone produced real classifier, router, role, test, approval, and metrics artifacts. A terminal summary alone was not enough to make the evidence portable and machine-checkable.

## Decision

Implement Change Passport as an evidence aggregator. A field exists only when automatically derived from machine evidence or an actual human-approval record.

## Rejected Alternatives

- Manually filled passport fields. Rejected because they would create unverifiable claims.
- Adding CI fields before GitHub Actions runs. Rejected because local CI structure is not real GitHub status evidence.
- Making Passport a new router. Rejected because classification and routing already have deterministic producers.

## Evidence

- Commit `13edafc` added `scripts/build-change-passport.py` and tests.
- Generated local passports for LOW, MEDIUM, and HIGH read final metrics, quality scores, classifier/router evidence, approval artifacts where present, and evidence hashes.

## Consequences

Passport output is deterministic and traceable to files.

## Open Risks

CI fields must be added only after real GitHub Actions producers exist.
