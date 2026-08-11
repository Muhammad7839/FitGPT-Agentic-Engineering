#!/usr/bin/env python3
"""Create a sanitized advisory-review artifact.

The capstone workflow treats AI review as advisory and non-blocking. When no
review secret is available, this script records an explicit skip instead of
fabricating AI output.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def build_advisory(output_dir: Path) -> dict[str, object]:
    secret_available = bool(os.environ.get("AURA_ADVISORY_AI_KEY"))
    status = "SKIPPED" if not secret_available else "SKIPPED"
    reason = (
        "AI SECRET UNAVAILABLE"
        if not secret_available
        else "AI SECRET PRESENT BUT LOCAL ADVISORY CLIENT IS NOT CONFIGURED IN THIS CAPSTONE"
    )
    artifact = {
        "schema_version": "advisory-review-v1",
        "status": status,
        "reason": reason,
        "blocking": False,
        "human_review_required": True,
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "advisory-review.json").write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "advisory-review.md").write_text(
        f"# Advisory Review\n\nStatus: {status} -- {reason}\n\nThis advisory job is non-blocking and does not fabricate AI output.\n",
        encoding="utf-8",
    )
    return artifact


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/advisory-review")
    args = parser.parse_args(argv)
    artifact = build_advisory(Path(args.output_dir))
    print(json.dumps(artifact, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
