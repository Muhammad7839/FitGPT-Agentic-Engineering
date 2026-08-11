# Final Architecture

## System Architecture

```mermaid
flowchart LR
    A["Change request"] --> B["Scope and safety precheck"]
    B --> C["Deterministic risk classifier<br/>aura-risk-v1"]
    C --> D["Adaptive router<br/>aura-router-v1"]
    D --> E["LOW route<br/>minimal agents + deterministic checks"]
    D --> F["MEDIUM route<br/>Implementer -> Reviewer -> Tester -> final approval"]
    D --> G["HIGH route<br/>Planner -> approval -> Implementer -> Reviewer -> Tester -> approval -> Project Manager"]
    E --> H["Policy / eval evidence"]
    F --> H
    G --> H
    H --> I["Change Passport + audit trail"]
```

## LOW / MEDIUM / HIGH Route Comparison

```mermaid
flowchart TB
    L["LOW<br/>docs/non-executable"] --> L1["2 model roles"]
    L1 --> L2["0 human checkpoints"]
    L2 --> L3["16/16 PASS"]

    M["MEDIUM<br/>bounded executable/test"] --> M1["3 model roles"]
    M1 --> M2["1 human checkpoint"]
    M2 --> M3["16/16 PASS"]

    H["HIGH<br/>governance/eval/tool-sensitive"] --> H1["5 model roles"]
    H1 --> H2["2 human checkpoints"]
    H2 --> H3["16/16 PASS"]
```

## Evidence Flow / Change Passport

```mermaid
flowchart LR
    A["Classifier output"] --> P["Change Passport builder"]
    B["Router output"] --> P
    C["Role sequence and metrics"] --> P
    D["Human approvals"] --> P
    E["Policy/eval results"] --> P
    F["GitHub CI artifacts"] --> P
    P --> G["Versioned JSON passport"]
    G --> H["Grader evidence<br/>docs/capstone/evidence/change-passport-AF-HIGH-001.json"]
```

## CI Governance Flow

```mermaid
flowchart TB
    A["Push to capstone/aura-forge"] --> B["change-classifier"]
    B --> C["policy-tests<br/>blocking"]
    B --> D["advisory-review<br/>non-blocking"]
    C --> E["evaluation-gate<br/>conditional deterministic eval"]
    E --> F["pipeline-integrity<br/>blocking, if always"]
    D --> G["audit-trail<br/>if always"]
    F --> G
    G --> H["Sanitized artifacts"]
```

## What Is Not In The Architecture

- No Render deployment.
- No Vercel deployment.
- No production database write.
- No FitGPT production mutation.
- No real user data.
