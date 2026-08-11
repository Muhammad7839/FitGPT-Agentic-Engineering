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
- GitHub Actions CI fields only when explicit run metadata and artifact producers are supplied.

## Evidence Discipline

The generator follows this rule:

`NO PASSPORT FIELD EXISTS UNLESS IT IS AUTOMATICALLY DERIVED FROM REAL MACHINE EVIDENCE OR AN ACTUAL HUMAN-APPROVAL RECORD.`

Unavailable optional fields are omitted. The generator does not add placeholder CI claims before a real CI run exists.

## GitHub CI Evidence

After the first green capstone GitHub Actions run, a CI-backed terminal Passport was generated locally for `AF-HIGH-001`.

Real CI producer:

- workflow run: `31513173735`
- commit: `92d60c438039b65e6229eefd7abc607c73393a0f`
- policy status: `success`
- evaluation status: `success`
- pipeline-integrity status: `success`
- audit-trail status: `success`
- advisory status: `SKIPPED` because `AURA_ADVISORY_AI_KEY` was unavailable

Local ignored output:

`.eval-artifacts/capstone/change-passports/AF-HIGH-001-with-ci.json`

The GitHub CI fields are derived from downloaded run metadata and artifacts under:

`.eval-artifacts/capstone/github-ci/31513173735/`

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
- CI fields are included only when real CI metadata and artifact producers are provided.
