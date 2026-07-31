# FitGPT Agent Sandbox Setup

## 1. Purpose

This sandbox completes LaunchCode Module 1, Lesson 1, Exercise 2 for the FitGPT Target Codebase. It preserves the course agent environment, adds the existing FitGPT backend dependencies, and limits repository access to an isolated exercise worktree.

No application code, API, schema, production service, original repository, or production credential was changed.

## 2. Target Codebase and scope

The selected Target Codebase is:

```text
/Users/muhammad/course-worktrees/FitGPT-Agentic-Engineering-exercise-1-2
```

It is mounted as:

```text
/Users/muhammad/course-worktrees/FitGPT-Agentic-Engineering-exercise-1-2 -> /workspace
```

The exercise branch is `course/exercise-1-2-sandbox`, based exactly on commit `c5a7ce37805ef58602b5d25b5aabf0b20b55f1bc` before the exercise commit.

The complete repository is mounted because its FastAPI backend, React frontend, Android/Kotlin Gradle application, shared documentation, and Git metadata belong to one Target Codebase. The sandbox is backend-focused and does not install web dependencies or the Android toolchain.

## 3. Final verified image and runtime

The final image is `fitgpt-agent-sandbox:baseline`.

```text
Image ID: sha256:1b88165a88a5d9786c38255e318b299bfa7c4a128ffe05233232c317a6ed08e3
Created: 2026-07-31T14:54:01.049569385Z
Architecture: arm64
Operating system: linux
Inspect size: 671213714 bytes
Docker images display size: 2.69GB
Working directory: /workspace
Entrypoint: ["docker-entrypoint.sh"]
Node: 22.23.2
npm: 10.9.8
Claude Code: 2.1.220
OpenCode: 1.18.10
Python: 3.12.13
pip: 25.0.1
pytest: 9.0.3
ngrok: 3.39.10
Java: intentionally absent
```

Node and npm are copied from a `node:22-slim` build stage into the final `python:3.12-slim` image. Claude Code and OpenCode are pinned to `2.1.220` and `1.18.10`. The earlier unsupported-engine warning was eliminated; the final build output contained no `EBADENGINE` or `Unsupported engine` warning.

FitGPT web CI may still use Node 20, so the Node 22 agent runtime and web CI runtime differ intentionally. Node 22 is required because Claude Code 2.1.220 declares Node 22 or newer.

## 4. Course Dockerfile and support files

The root Dockerfile is adapted from:

```text
/Users/muhammad/LaunchCodeAgenticEngineer/module_1/Dockerfile
```

Only the support files referenced by that course Dockerfile were copied to `.agentic/container/`:

```text
.agentic/container/docker-entrypoint.sh
.agentic/container/requirements.txt
.agentic/container/settings.json
.agentic/container/statusline.sh
```

All four files remained byte-for-byte identical to their LaunchCode Module 1 sources. The original LaunchCode repository was not modified.

## 5. Docker build

The final build command, run from the exercise worktree root, was:

```bash
docker build --pull=false --progress=plain \
  -t fitgpt-agent-sandbox:baseline .
```

Verified final build output included:

```text
exporting manifest sha256:1b51262584461af88840a6ed7f992c3acff1aea556bca8e1b4d9617f7614b846
exporting config sha256:384f6a08e9cde6898c84eef94558ff0f663497a3108333aaeaec7fa39683c930
naming to docker.io/library/fitgpt-agent-sandbox:baseline done
unpacking to docker.io/library/fitgpt-agent-sandbox:baseline done
exit code: 0
```

The build context transferred 356 bytes after `.dockerignore` filtering. Image history contained 31 entries. Credential-like material was absent from the inspected history and image configuration.

## 6. Docker run commands

A future interactive course container can be started from the worktree with:

```bash
docker run -it --rm \
  -v "${PWD}:/workspace" \
  -v "claude-auth:/claude-auth" \
  fitgpt-agent-sandbox:baseline
```

No interactive Claude session was launched during this exercise.

The final non-interactive smoke container used the worktree read-write because Claude needed to create `agent-summary.md`, mounted authentication only for that run, and used temporary runtime directories:

```bash
docker run --rm \
  -v "${PWD}:/workspace" \
  -v "claude-auth:/claude-auth" \
  --tmpfs /workspace/backend/uploads:rw,nosuid,nodev,noexec,size=64m,mode=0700 \
  --tmpfs /workspace/backend/.pytest_cache:rw,nosuid,nodev,noexec,size=16m,mode=0700 \
  fitgpt-agent-sandbox:baseline \
  claude \
  --print \
  --output-format text \
  --no-session-persistence \
  --permission-mode dontAsk \
  --max-budget-usd 1.00 \
  --tools "Read,Glob,Grep,Bash,Write" \
  --allowedTools "Read" "Glob" "Grep" "Write" "Bash" \
  --no-chrome \
  --disallowedTools "WebFetch" "WebSearch" "mcp__*" \
  --verbose \
  "$CLAUDE_PROMPT"
```

Docker's normal bridge network was used only because the Claude model call required networking. Host networking was not used.

## 7. Filesystem boundary

The Claude container mounted only the selected worktree at `/workspace` and the Docker-managed authentication volume at `/claude-auth`. The home directory, original FitGPT clone, SSH directory, Desktop, Downloads, and unrelated repositories were not mounted.

The repository mount contained `.git`, confirming that `/workspace` was the selected Git worktree. Boundary verification reported:

```text
/workspace
workspace Git metadata detected
prohibited host paths absent
```

No smoke-test repository or deliverable file was written outside the selected worktree mount. Coordinator evidence logs were captured separately outside the worktree and were not created by Claude repository tools.

## 8. Authentication policy

The existing Docker-managed `claude-auth` volume was mounted only for the model-backed Claude smoke test. It was not mounted during filesystem, persistence, offline-network, import, or direct pytest checks.

Claude Code used configured authentication normally. Neither Codex nor Claude inspected, printed, or exposed the authentication-volume contents, authorization codes, tokens, or credential values. The volume was not copied into the image or repository. This policy does not claim that `/root/.claude` was technically inaccessible to the CLI.

## 9. Network policy

Non-Claude verification containers used `--network none`. The corrected direct validation also ran successfully with `--network none`, demonstrating that the approved backend test did not require network access.

The separate offline HTTPS boundary check reported:

```text
external HTTPS blocked under --network none
exit code: 0
```

The Claude run used Docker's ordinary bridge network only for its required model connection. The prompt and tool restrictions prohibited Groq, OpenWeather, Gmail, Google OAuth, Render, Vercel, production databases, WebFetch, WebSearch, browsers, plugins, subagents, MCP tools, and other unrelated external access. No unrelated access was observed.

Bridge networking was not kernel-level destination isolation and did not technically enforce an Anthropic-only egress allowlist.

## 10. Persistent and ephemeral storage

The bind-mounted exercise worktree is persistent. The intended smoke-test output, `agent-summary.md`, persisted on the host after the container exited.

The authentication volume is persistent but was mounted only for the Claude run. Container-local `/tmp`, the SQLite test database, upload scratch space, pytest cache, logs, and other runtime state were intended to remain ephemeral.

The read-only validation approach mounted the repository as `/workspace:ro` and overlaid these writable runtime paths:

```text
tmpfs -> /workspace/backend/uploads
tmpfs -> /workspace/backend/.pytest_cache
```

The tmpfs preflight confirmed:

```text
repository source is read-only
uploads tmpfs is writable
pytest cache tmpfs is writable
exit code: 0
```

The marker files created in those mounts disappeared when the disposable preflight container exited.

## 11. Environment-variable policy

Real `.env` files were excluded from the Docker build context and were never passed to the container. `.env.example` files remained available for source inspection.

The validation used only these sandbox values:

```text
ENVIRONMENT=test
SECRET_KEY=sandbox-test-only
DATABASE_URL=sqlite:////tmp/fitgpt_test.db
TEST_DATABASE_URL=sqlite:////tmp/fitgpt_test.db
STORAGE_BACKEND=local
```

Groq, OpenWeather, Google, Gmail, Sentry, and other external-service variables were explicitly empty. The SQLite database path remained under the disposable container's `/tmp`.

## 12. Included and omitted dependencies

The copied course `requirements.txt` preserves the Module 1 Python agent environment. The adapted Dockerfile additionally installs the Target Codebase's existing `backend/requirements.txt`, which includes the backend dependencies and pytest used by the approved validation.

Node and npm remain available for web manifest inspection. The image does not install `web/node_modules`, a JDK, the Android SDK, Android emulator tooling, PostgreSQL, or production services. Web builds and Android execution remain outside this backend-focused baseline.

## 13. Initial validation-harness correction

The initial Node 22 validation mounted the full workspace read-only without a writable upload directory. FitGPT startup stopped before test collection. The corrected invocation retained read-only source access while providing ephemeral tmpfs mounts for runtime uploads and pytest cache.

The initial exit code `4` was a container-mount harness issue, not a failed test or application assertion. It was corrected only after explicit authorization.

## 14. Approved validation command

The coordinator executed the corrected validation once. Claude executed the same approved validation once during its single smoke-test invocation. Neither was rerun afterward.

```bash
cd /workspace/backend && \
ENVIRONMENT=test \
SECRET_KEY=sandbox-test-only \
DATABASE_URL=sqlite:////tmp/fitgpt_test.db \
TEST_DATABASE_URL=sqlite:////tmp/fitgpt_test.db \
STORAGE_BACKEND=local \
OPENWEATHER_API_KEY= \
GROQ_API_KEY= \
GOOGLE_CLIENT_ID= \
GOOGLE_WEB_CLIENT_ID= \
GMAIL_ADDRESS= \
GMAIL_APP_PASSWORD= \
SENTRY_DSN= \
pytest -q tests/test_config_startup.py
```

The corrected direct container invocation was:

```bash
docker run --rm --network none \
  -v "${PWD}:/workspace:ro" \
  --tmpfs /workspace/backend/uploads:rw,nosuid,nodev,noexec,size=64m,mode=0700 \
  --tmpfs /workspace/backend/.pytest_cache:rw,nosuid,nodev,noexec,size=16m,mode=0700 \
  --entrypoint /bin/bash \
  fitgpt-agent-sandbox:baseline \
  -lc '
    cd /workspace/backend &&
    ENVIRONMENT=test \
    SECRET_KEY=sandbox-test-only \
    DATABASE_URL=sqlite:////tmp/fitgpt_test.db \
    TEST_DATABASE_URL=sqlite:////tmp/fitgpt_test.db \
    STORAGE_BACKEND=local \
    OPENWEATHER_API_KEY= \
    GROQ_API_KEY= \
    GOOGLE_CLIENT_ID= \
    GOOGLE_WEB_CLIENT_ID= \
    GMAIL_ADDRESS= \
    GMAIL_APP_PASSWORD= \
    SENTRY_DSN= \
    pytest -q tests/test_config_startup.py
  '
```

## 15. Corrected direct-validation output

```text
.......                                                                  [100%]
=============================== warnings summary ===============================
../../usr/local/lib/python3.12/site-packages/_pytest/cacheprovider.py:475
  /usr/local/lib/python3.12/site-packages/_pytest/cacheprovider.py:475: PytestCacheWarning: could not create cache path /workspace/.pytest_cache/v/cache/nodeids: [Errno 30] Read-only file system: '/workspace/pytest-cache-files-l9nld72i'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
7 passed, 1 warning in 0.30s
exit code: 0
```

The seven tests passed. Pytest attempted to create a root-level cache under the read-only workspace, producing one cache warning. The warning did not affect the validation result.

Future validation hardening should set `PYTHONDONTWRITEBYTECODE=1` and run `pytest -p no:cacheprovider`. This is a documentation-only recommendation; the accepted tests were not rerun.

## 16. Exact Claude smoke-test prompt

```text
Perform one narrowly scoped sandbox smoke test.

Inspect repository files only under /workspace. Do not inspect /claude-auth, /root/.claude, credentials, authentication data, or any path outside /workspace.

Do not use WebFetch, WebSearch, MCP tools, browsers, plugins, subagents, or external APIs. Do not contact Groq, OpenWeather, Gmail, Google OAuth, Render, Vercel, production databases, or any service other than the Claude model connection required for this run.

Do not install dependencies. Do not modify application code. Do not create or edit any file except /workspace/agent-summary.md. Do not commit, push, change branches, or alter Git configuration.

Limit repository inspection to confirming the top-level backend, web, and Android app areas. Do not perform broader architecture analysis.

Run this approved validation command exactly once and never retry it, even if it fails:

cd /workspace/backend && ENVIRONMENT=test SECRET_KEY=sandbox-test-only DATABASE_URL=sqlite:////tmp/fitgpt_test.db TEST_DATABASE_URL=sqlite:////tmp/fitgpt_test.db STORAGE_BACKEND=local OPENWEATHER_API_KEY= GROQ_API_KEY= GOOGLE_CLIENT_ID= GOOGLE_WEB_CLIENT_ID= GMAIL_ADDRESS= GMAIL_APP_PASSWORD= SENTRY_DSN= pytest -q tests/test_config_startup.py

Then create /workspace/agent-summary.md containing only the top-level structure, exact validation command, exit code and result, observed sandbox boundaries, and setup limitations. Describe backend/ as the FastAPI backend, web/ as the React frontend, and app/ as the Android/Kotlin Gradle application. Do not use the phrase not actively developed.

Use accurate authentication wording: Claude Code used configured authentication normally. Claude did not inspect, print, or report authentication contents. State that prompt and tool restrictions prohibited unrelated external-service access and that no unrelated access was observed. Do not claim kernel-level domain isolation during this bridge-network run.

If authentication, permissions, tools, or the budget prevent completion, do not retry and do not create other files. Report the blocker in terminal output.
```

## 17. Claude invocation flags

The installed `claude --help` confirmed these requested flags:

```text
--print
--output-format text
--no-session-persistence
--permission-mode dontAsk
--max-budget-usd 1.00
--tools Read,Glob,Grep,Bash,Write
--allowedTools Read Glob Grep Write Bash
--no-chrome
--disallowedTools WebFetch WebSearch mcp__*
--verbose
```

Claude Code 2.1.220 did not expose `--max-turns`, so that unsupported flag was omitted. No fallback model, continuation, resume, background mode, subagent, interactive login, or dangerous permission bypass was used. The smoke test ran exactly once and was not retried.

## 18. Claude output

Sanitized stdout:

```text
The smoke test is complete. The validation command exited 0 with 7 tests passing, and `/workspace/agent-summary.md` has been created documenting the structure, command, result, sandbox boundaries, and authentication wording as specified. No blockers were encountered.
```

```text
exit code: 0
validation recorded in agent-summary.md: 7 passed in 0.30s
```

The verbose stderr log was empty. No OAuth URL, authorization code, token, credential, authentication-volume content, or unnecessary debug output was stored in the worktree or displayed.

## 19. Checksum and persistence evidence

The pre-run manifest included every regular file under the worktree except `.git`:

```text
Pre-run regular files: 453
Immediate post-run regular files: 483

Generated during the run:
- agent-summary.md
- 4 pytest-cache files
- 25 Python bytecode files

After cleanup:
Post-clean regular files: 454
Only remaining checksum difference: agent-summary.md
```

Pytest and Python created ordinary ignored runtime artifacts inside `/workspace` while the approved test ran. They were not application edits. Post-run verification captured them as evidence and removed them. No tracked file changed, no application file changed, and no smoke-test output file was written outside the selected worktree. The intended output, `agent-summary.md`, persisted.

## 20. Secret and credential protections

The `.dockerignore` excludes Git metadata, real environment files, virtual environments, caches, dependencies, build outputs, databases, credential filenames, private keys, signing files, and OS or IDE metadata.

Image history and configuration scans found no credential-like material. The final deliverables contain no real environment file, production secret, OAuth credential, token, signing file, database, authentication material, or copied repository data beyond the explicitly selected support and dependency manifests.

## 21. Known limitations

1. Claude Code 2.1.220 does not expose `--max-turns`; the `$1.00` maximum budget and one-invocation rule bounded the run.
2. Docker bridge networking cannot enforce an Anthropic-only destination allowlist.
3. Some course and backend dependency declarations use version ranges rather than hashes, so later rebuilds may resolve newer packages.
4. The image is backend-focused. Web dependencies, Java, the Android SDK, Android execution, PostgreSQL, and production services are intentionally omitted.
5. FitGPT web CI may use Node 20 while the agent image intentionally uses Node 22 for Claude Code compatibility.
6. Render's declared Python 3.10.13 differs from the image and Python 3.12 CI runtime.
7. Without the documented hardening flags, pytest and Python may create ignored cache or bytecode files when `/workspace` is writable.

## 22. Cleanup and rebuild instructions

All verification containers used `--rm`, so no exercise container remains. Temporary upload directories, pytest caches, Python bytecode, markers, test databases, and logs were removed from the worktree. The exercise image and worktree remain available.

Rebuild after an intentional Dockerfile or dependency change with:

```bash
docker build --pull=false --progress=plain \
  -t fitgpt-agent-sandbox:baseline .
```

If future validation uses a writable workspace, prevent routine cache files with:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q tests/test_config_startup.py
```

Do not remove the worktree, branch, image, or authentication volume until no longer needed. No cleanup command that deletes those resources was run during this exercise.

## 23. Security decisions

### Question 1: Why did you mount only this folder?

The isolated worktree contains the complete Target Codebase needed for the backend, web, and Android source inspection. Mounting only that folder prevents unrelated home, SSH, cloud, Desktop, Downloads, original-clone, and repository paths from entering the container's host-file boundary.

### Question 2: What did you choose to keep ephemeral?

Container-local `/tmp`, the SQLite test database, upload scratch space, pytest cache, Python bytecode, logs, downloads, and other runtime state were kept ephemeral or removed after evidence capture. The validation upload directory and requested pytest-cache directory used tmpfs overlays.

### Question 3: What did you choose to persist?

The exercise worktree persists the reviewed Dockerfile, documentation, course support files, and `agent-summary.md`. The existing Docker-managed `claude-auth` volume persists authentication and is mounted only during Claude runs.

### Question 4: What dependencies did you include?

The sandbox includes the course Dockerfile's agent environment and exact support files plus FitGPT's existing `backend/requirements.txt`. Node 22 and npm remain available for agent and web-manifest inspection. Web dependencies, Java, the Android SDK, PostgreSQL, and production services were intentionally omitted.

### Question 5: What did the smoke test prove?

The smoke test proved Claude could inspect the selected repository areas, run the approved backend validation successfully, and persist the requested summary. Post-run verification also showed that pytest and Python generated only ignored runtime cache files, which were removed, while no tracked or application file changed.

### Question 6: What risks remain?

Claude had ordinary bridge-network egress and write access to `/workspace` during the model-backed smoke test. Prompt and tool restrictions reduce but do not technically eliminate unrelated egress or file-write risk. Dependency ranges are not fully reproducible, the authentication volume remains sensitive, the agent and web CI Node runtimes intentionally differ, and the image does not include the web or Android execution toolchains.
