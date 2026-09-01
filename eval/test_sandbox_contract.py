"""Static contract checks for the offline grader verification container."""

from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run-offline-governance-verification.sh"


def test_offline_verification_has_fail_closed_container_boundaries():
    text = SCRIPT.read_text(encoding="utf-8")

    for required in (
        "--network none",
        "--read-only",
        "--cap-drop ALL",
        "no-new-privileges",
        "--entrypoint /usr/local/bin/python",
        '--tmpfs "/tmp:rw,noexec,nosuid,nodev,size=128m"',
        '-v "${REPO_ROOT}:/workspace:ro"',
    ):
        assert required in text

    assert "claude-auth" not in text


def test_parallel_runs_receive_an_explicit_unique_container_name():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "AURA_VERIFY_RUN_ID" in text
    assert '--name "${VERIFY_RUN_ID}"' in text
    assert "$$" in text


def test_offline_verifier_resolves_the_image_to_an_immutable_id():
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'docker image ls --quiet --no-trunc "${IMAGE}"' in text
    assert '"${IMAGE_ID}"' in text
