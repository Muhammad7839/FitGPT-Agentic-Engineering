#!/usr/bin/env bash
set -euo pipefail

IMAGE="${AGENT_IMAGE:-agentic_engineer_4:latest}"

if [[ $# -lt 1 ]]; then
  echo "usage: scripts/run-agent.sh <role> [command...]" >&2
  exit 64
fi

ROLE="$1"
shift || true

case "$ROLE" in
  orchestrator)
    WORKSPACE_MODE="rw"
    MEMORY_MODE="omit"
    ;;
  planner|reviewer|tester|project-manager|dependency-auditor)
    WORKSPACE_MODE="ro"
    MEMORY_MODE="omit"
    ;;
  implementer)
    WORKSPACE_MODE="rw"
    MEMORY_MODE="omit"
    ;;
  *)
    echo "Unknown or ungoverned role: $ROLE" >&2
    exit 66
    ;;
esac

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Module 4 image '$IMAGE' is not available locally." >&2
  echo "Restore the exact trusted image before running runtime verification." >&2
  exit 69
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
MOUNTS=(-v "${REPO_ROOT}:/workspace:${WORKSPACE_MODE}")

if [[ "$MEMORY_MODE" == "mount" ]]; then
  MOUNTS+=(-v "fitgpt-governance-memory:/memory")
fi

if [[ $# -gt 0 ]]; then
  COMMAND=("$@")
else
  COMMAND=(bash)
fi

exec docker run --rm \
  -e "AGENT_ROLE=${ROLE}" \
  -e "GOVERNANCE_ROOT=/workspace" \
  "${MOUNTS[@]}" \
  -w /workspace \
  "$IMAGE" \
  "${COMMAND[@]}"
