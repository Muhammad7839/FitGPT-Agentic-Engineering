# Parallel Agent Session Tasks

## Session A

Branch name: course/parallel-recommendation-tests
Worktree directory: /Users/muhammad/course-worktrees/FitGPT-Agentic-Engineering-parallel-tests
Task: Add focused unit tests for backend/app/recommendation_explanations.py.
Files or folders the agent may write to:
- backend/tests/test_recommendation_explanations.py
Files or folders the agent may read but not write to:
- backend/app/recommendation_explanations.py
- backend/app/models.py
- backend/tests/
- backend/requirements.txt
Commands the agent may run:
- Read-only repository inspection commands
- The single focused pytest command documented in the Session A prompt
Definition of done:
- The new test file covers the public explanation builder’s important observable branches.
- The tests require no external service, network call, production database, or real credential.
- The focused test command passes.
- No production or unrelated file is modified.

## Session B

Branch name: course/parallel-storage-docs
Worktree directory: /Users/muhammad/course-worktrees/FitGPT-Agentic-Engineering-parallel-storage-docs
Task: Create developer documentation for FitGPT’s local and S3/R2 image-storage backends.
Files or folders the agent may write to:
- docs/development/storage-backends.md
Files or folders the agent may read but not write to:
- backend/app/storage.py
- backend/app/config.py
- backend/.env.example
- .env.example
- README.md
- docs/
Commands the agent may run:
- Read-only repository inspection commands
- The documentation-content check documented in the Session B prompt
Definition of done:
- The document accurately explains source-supported local, S3, and R2 storage behavior.
- It identifies configuration names without exposing or inventing secret values.
- It includes concise setup, security, and troubleshooting guidance.
- No application, README, environment-example, or unrelated file is modified.
