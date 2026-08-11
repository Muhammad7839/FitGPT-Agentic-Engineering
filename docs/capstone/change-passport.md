# Change Passport

The Change Passport is an evidence aggregator, not a new decision-making subsystem.

It reads machine-produced artifacts and actual human-approval records, then emits a versioned JSON summary for a completed change. A field is included only when a real producer exists. CI-specific fields are omitted until real GitHub Actions evidence exists.

## Current Schema

Schema version: `change-passport-v1`

Supported fields include:

- scenario ID and final readiness result;
- classifier version, risk tier, triggered rules, and normalized paths;
- router version, route ID, ordered roles actually used, and human checkpoint count;
- deterministic gates and test results when produced;
- actual human approval events when a recorded approval artifact exists;
- tool-event count and authorization-denial count;
- measured cost and timing read from run artifacts;
- evidence references and SHA-256 hashes.

## Evidence Discipline

The generator follows this rule:

`NO PASSPORT FIELD EXISTS UNLESS IT IS AUTOMATICALLY DERIVED FROM REAL MACHINE EVIDENCE OR AN ACTUAL HUMAN-APPROVAL RECORD.`

Unavailable optional fields are omitted. The generator does not add placeholder CI claims before a real CI run exists.

## Generated Local Passports

Local ignored artifacts were generated for:

- `AF-LOW-001`
- `AF-MEDIUM-001`
- `AF-HIGH-001`

Location:

`.eval-artifacts/capstone/change-passports/`

The generated passports are intentionally local evidence artifacts. This tracked document describes the design; the ignored JSON files can be regenerated from the preserved local run evidence.

## Validation

Deterministic tests verify that:

- real evidence produces expected fields;
- unavailable CI evidence is not fabricated;
- missing required producers fail validation;
- classifier and router versions trace to evidence;
- actual approvals trace to approval artifacts when present;
- measured costs are read from evidence;
- evidence references resolve and hashes match;
- path traversal references are rejected;
- output is deterministic for the same evidence set.
