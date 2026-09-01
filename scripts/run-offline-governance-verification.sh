#!/usr/bin/env bash
set -euo pipefail

IMAGE="${AGENT_IMAGE:-agentic_engineer_4:latest}"
REPO_ROOT="$(git rev-parse --show-toplevel)"
VERIFY_RUN_ID="${AURA_VERIFY_RUN_ID:-aura-verify-$(date -u +%Y%m%dT%H%M%SZ)-$$}"

if ! [[ "${VERIFY_RUN_ID}" =~ ^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,62}$ ]]; then
  echo "AURA_VERIFY_RUN_ID must be a valid Docker container name up to 63 characters." >&2
  exit 64
fi

if ! docker version >/dev/null 2>&1; then
  echo "Docker is unavailable. Start Docker Desktop and rerun this script." >&2
  exit 69
fi

IMAGE_ID="$(docker image ls --quiet --no-trunc "${IMAGE}" | head -n 1)"
if [[ -z "${IMAGE_ID}" ]] || ! docker image inspect "${IMAGE_ID}" >/dev/null 2>&1; then
  echo "Required image '${IMAGE}' is unavailable. Build it with: docker build -t ${IMAGE} -f Dockerfile ." >&2
  exit 69
fi

docker run --rm \
  --name "${VERIFY_RUN_ID}" \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --entrypoint /usr/local/bin/python \
  --pids-limit 128 \
  --memory 1g \
  --cpus 1 \
  --tmpfs "/tmp:rw,noexec,nosuid,nodev,size=128m" \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e GOVERNANCE_ROOT=/workspace \
  -v "${REPO_ROOT}:/workspace:ro" \
  -w /workspace \
  "${IMAGE_ID}" \
  -m pytest -q -p no:cacheprovider \
    eval/test_policy.py \
    eval/test_mcp_runtime.py \
    eval/test_coursetools_runtime.py \
    eval/test_retrieval_behavior.py \
    eval/test_reliability_controls.py \
    eval/test_sandbox_contract.py
