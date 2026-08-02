"""Create a sanitized development baseline from preserved orchestration evidence."""

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from normalize_transcript import normalize


def run(command):
    return subprocess.run(command, text=True, capture_output=True, check=True).stdout


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def repository_manifest(repo):
    raw = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo,
        capture_output=True,
        check=True,
    ).stdout
    hashes = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        rel = item.decode("utf-8")
        hashes[rel] = file_sha(repo / rel)
    status = run(["git", "-C", str(repo), "status", "--short", "--untracked-files=all"])
    head = run(["git", "-C", str(repo), "rev-parse", "HEAD"]).strip()
    return {
        "head": head,
        "status_short": status.splitlines(),
        "tracked_sha256": hashes,
    }


def write_json(path, value):
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run3-root", required=True)
    parser.add_argument("--run4-root", required=True)
    parser.add_argument("--run5-root", required=True)
    parser.add_argument("--artifacts-root", default=".eval-artifacts/runs/dev")
    args = parser.parse_args(argv)

    repo = Path.cwd().resolve()
    output = (repo / args.artifacts_root / args.run_id).resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing baseline: {output}")
    output.mkdir(parents=True)

    before = repository_manifest(repo)
    write_json(output / "manifest-before.json", before)

    transcript = normalize(args.run3_root, args.run4_root, args.run5_root)
    transcript["run_id"] = args.run_id
    transcript["generated_at_utc"] = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    )
    transcript["baseline_repository_head"] = before["head"]
    write_json(output / "transcript.json", transcript)

    with (output / "tool-events.jsonl").open("w", encoding="utf-8") as handle:
        for event in transcript["events"]:
            if event.get("type") == "tool_call":
                handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    after = repository_manifest(repo)
    write_json(output / "manifest-after.json", after)
    unchanged = before == after

    summary = f"""# FitGPT Development Baseline Evidence

Run ID: {args.run_id}

Task: COURSE-FITGPT-001

Evidence origin: preserved Run 3, Run 4, and Run 5 artifacts were normalized.
No role was replayed, no holdout task was executed, and no tracker was called.

Repository manifest unchanged during normalization: {"yes" if unchanged else "no"}

Selected path: Planner -> Implementer -> Reviewer -> Tester -> Project Manager

Historical failures preserved: {len(transcript["historical_attempts"])}

Tool events preserved in normalized form: {sum(1 for event in transcript["events"] if event.get("type") == "tool_call")}

Separate server audit log: unavailable. tool-events.jsonl is the equivalent
derived directly from preserved Claude stream-json events.

Limitations:

"""
    summary += "\n".join(f"- {item}" for item in transcript["limitations"]) + "\n"
    (output / "run-summary.md").write_text(summary, encoding="utf-8")

    files = sorted(path for path in output.iterdir() if path.name != "checksums.txt")
    checksums = "\n".join(f"{file_sha(path)}  {path.name}" for path in files) + "\n"
    (output / "checksums.txt").write_text(checksums, encoding="utf-8")

    if not unchanged:
        raise SystemExit("repository manifest changed during baseline normalization")
    print(output)


if __name__ == "__main__":
    main()
