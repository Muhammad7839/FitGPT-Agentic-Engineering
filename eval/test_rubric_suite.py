"""Deterministically gated rubric scoring for FitGPT transcripts.

Usage:
    python3 eval/test_rubric_suite.py <transcript.json>
    python3 eval/test_rubric_suite.py --self-test
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from test_deterministic import collect_results, load_json, tally

EVAL_DIR = Path(__file__).resolve().parent
RUBRIC_PATH = EVAL_DIR / "rubric.json"
FIXTURE_PATH = EVAL_DIR / "fixtures" / "valid-development-transcript.json"
JUDGE_KEYS = {
    "dimension",
    "score",
    "passed",
    "justification",
    "evidence",
    "limitations",
}
DISALLOWED_TOOLS = ",".join(
    [
        "Read",
        "Glob",
        "Grep",
        "Bash",
        "Edit",
        "Write",
        "WebFetch",
        "WebSearch",
        "NotebookEdit",
        "Agent",
        "mcp__coursetools__file_read",
        "mcp__coursetools__file_write",
        "mcp__coursetools__codebase_search",
        "mcp__coursetools__shell",
        "mcp__coursetools__test_runner",
        "mcp__coursetools__task_tracker",
        "mcp__coursetools__web_search",
    ]
)


def load_rubric():
    return load_json(RUBRIC_PATH)


def validate_rubric(rubric):
    problems = []
    dimensions = rubric.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        problems.append("dimensions must be a non-empty list")
        dimensions = []
    required = {
        "name",
        "description",
        "levels",
        "pass_threshold",
        "examples",
        "evidence_focus",
        "deterministic_boundary",
    }
    for index, dimension in enumerate(dimensions):
        missing = sorted(required - set(dimension))
        if missing:
            problems.append(f"dimension {index} missing {missing}")
        levels = dimension.get("levels", {})
        if set(levels) != {"1", "2", "3", "4"}:
            problems.append(f"dimension {index} must define levels 1-4")
        if dimension.get("pass_threshold") not in (1, 2, 3, 4):
            problems.append(f"dimension {index} has invalid pass_threshold")
        if not dimension.get("examples"):
            problems.append(f"dimension {index} needs examples")
        if not dimension.get("evidence_focus"):
            problems.append(f"dimension {index} needs evidence_focus")
    maximum = 4 * len(dimensions)
    threshold = rubric.get("overall_pass_threshold")
    if not isinstance(threshold, int) or threshold < len(dimensions) or threshold > maximum:
        problems.append("overall_pass_threshold is invalid")
    if rubric.get("require_each_dimension_threshold") is not True:
        problems.append("each dimension threshold must remain mandatory")
    if problems:
        raise ValueError("; ".join(problems))
    return rubric


def sanitized_evidence(transcript, deterministic_results):
    subagents = []
    for event in transcript.get("events", []):
        if event.get("type") != "subagent" or not event.get("selected_for_path", True):
            continue
        subagents.append(
            {
                "role": event.get("role"),
                "workflow_run": event.get("workflow_run"),
                "verdict": (event.get("output_document") or {}).get("verdict"),
                "substantive_output": event.get("output"),
                "output_document": event.get("output_document"),
            }
        )
    tool_evidence = []
    for event in transcript.get("events", []):
        if event.get("type") != "tool_call":
            continue
        tool_evidence.append(
            {
                "role": event.get("role"),
                "tool": event.get("tool"),
                "args": event.get("args"),
                "result": event.get("result"),
                "success": event.get("success"),
                "actual_event": event.get("actual_event"),
                "fixture_simulation": event.get("fixture_simulation", False),
                "evidence_class": event.get("evidence_class"),
            }
        )
    return {
        "run_kind": transcript.get("run_kind"),
        "fixture": transcript.get("fixture"),
        "evidence_origin": transcript.get("evidence_origin"),
        "task_id": transcript.get("task_id"),
        "task_description": transcript.get("task_description"),
        "expected_path": transcript.get("expected_path"),
        "subagent_outputs": subagents,
        "tool_evidence": tool_evidence,
        "human_approvals": transcript.get("human_approvals"),
        "changed_files": transcript.get("changed_files"),
        "protected_files_unchanged": transcript.get("protected_files_unchanged"),
        "historical_attempts": transcript.get("historical_attempts"),
        "claims": transcript.get("claims"),
        "limitations": transcript.get("limitations"),
        "deterministic_results": [
            {
                "check": item["check"],
                "status": item["status"],
                "message": item["message"],
            }
            for item in deterministic_results
        ],
    }


def build_judge_prompt(transcript, dimension, deterministic_results):
    evidence = sanitized_evidence(transcript, deterministic_results)
    return (
        "You are an isolated agent-as-judge. Score one quality dimension for a "
        "FitGPT orchestration development run. You have no repository, shell, "
        "MCP, test, tracker, file, or web tools. Use only the task, dimension, "
        "levels, and sanitized evidence below. Do not infer missing facts.\n\n"
        "Return strict JSON only, with exactly these fields:\n"
        '{"dimension":"...", "score":1, "passed":false, '
        '"justification":"...", "evidence":["..."], "limitations":["..."]}\n\n'
        f"TASK:\n{json.dumps({'task_id': transcript.get('task_id'), 'description': transcript.get('task_description')}, indent=2)}\n\n"
        f"DIMENSION:\n{json.dumps(dimension, indent=2)}\n\n"
        f"SANITIZED EVIDENCE:\n{json.dumps(evidence, indent=2)}\n"
    )


def parse_judge_reply(reply, dimension):
    try:
        value = json.loads(reply)
    except json.JSONDecodeError as exc:
        raise ValueError(f"judge response is not strict JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("judge response must be one JSON object")
    if set(value) != JUDGE_KEYS:
        raise ValueError(f"judge response keys must be exactly {sorted(JUDGE_KEYS)}")
    if value["dimension"] != dimension["name"]:
        raise ValueError("judge dimension does not match requested dimension")
    if not isinstance(value["score"], int) or not 1 <= value["score"] <= 4:
        raise ValueError("judge score must be an integer from 1 to 4")
    expected_pass = value["score"] >= dimension["pass_threshold"]
    if value["passed"] is not expected_pass:
        raise ValueError("judge passed value contradicts the dimension threshold")
    if not isinstance(value["justification"], str) or not value["justification"].strip():
        raise ValueError("judge justification must be non-empty")
    for field in ("evidence", "limitations"):
        if not isinstance(value[field], list) or not all(
            isinstance(item, str) for item in value[field]
        ):
            raise ValueError(f"judge {field} must be a list of strings")
    return value


def call_judge(prompt, dimension_name):
    with tempfile.TemporaryDirectory(prefix="fitgpt-eval-judge-") as judge_dir:
        empty_mcp = Path(judge_dir) / "empty-mcp.json"
        empty_mcp.write_text('{"mcpServers": {}}\n', encoding="utf-8")
        command = [
            "claude",
            "--print",
            "--output-format",
            "json",
            "--permission-mode",
            "dontAsk",
            "--tools",
            "",
            "--disallowedTools",
            DISALLOWED_TOOLS,
            "--mcp-config",
            str(empty_mcp),
            "--strict-mcp-config",
            "--no-chrome",
            "--setting-sources",
            "user",
            "--no-session-persistence",
        ]
        environment = os.environ.copy()
        environment["MCP_CONNECTION_NONBLOCKING"] = "0"
        completed = subprocess.run(
            command,
            input=prompt,
            cwd=judge_dir,
            capture_output=True,
            text=True,
            timeout=240,
            env=environment,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"judge invocation for {dimension_name} failed: "
                f"{completed.stderr.strip() or completed.stdout.strip()}"
            )
        try:
            envelope = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Claude envelope is not JSON: {exc}") from exc
        if envelope.get("is_error"):
            raise RuntimeError(f"Claude judge returned an error: {envelope.get('result')}")
        reply = envelope.get("result")
        if not isinstance(reply, str):
            raise RuntimeError("Claude envelope has no string result")
        return reply


def deterministic_gate(transcript):
    results = collect_results(transcript)
    counts = tally(results)
    return not counts["FAIL"] and not counts["ERROR"], results, counts


def evaluate(transcript_path):
    rubric = validate_rubric(load_rubric())
    transcript = load_json(transcript_path)
    gate_passed, deterministic_results, deterministic_tally = deterministic_gate(transcript)
    print(
        "DETERMINISTIC_TALLY "
        + " ".join(
            f"{status}={deterministic_tally[status]}"
            for status in ("PASS", "FAIL", "SKIP", "ERROR")
        )
    )
    if not gate_passed:
        for item in deterministic_results:
            if item["status"] in ("FAIL", "ERROR"):
                print(f"[{item['status']}] {item['check']}: {item['message']}")
        print("RUBRIC_GATE=GATED")
        print("JUDGE_CALLS=0")
        return 1

    print("RUBRIC_GATE=OPEN")
    dimension_results = []
    for dimension in rubric["dimensions"]:
        prompt = build_judge_prompt(transcript, dimension, deterministic_results)
        reply = call_judge(prompt, dimension["name"])
        parsed = parse_judge_reply(reply, dimension)
        dimension_results.append(parsed)
        print(
            f"[{'PASS' if parsed['passed'] else 'FAIL'}] {parsed['dimension']}: "
            f"{parsed['score']}/4 - {parsed['justification']}"
        )
        print(f"EVIDENCE {json.dumps(parsed['evidence'], ensure_ascii=False)}")
        print(f"LIMITATIONS {json.dumps(parsed['limitations'], ensure_ascii=False)}")

    total = sum(item["score"] for item in dimension_results)
    each_passed = all(item["passed"] for item in dimension_results)
    aggregate_passed = total >= rubric["overall_pass_threshold"]
    overall = each_passed and aggregate_passed
    print(f"JUDGE_CALLS={len(dimension_results)}")
    print(
        f"AGGREGATE={total}/{rubric['maximum_score']} "
        f"THRESHOLD={rubric['overall_pass_threshold']} "
        f"EACH_DIMENSION_REQUIRED=true"
    )
    print(f"FINAL_VERDICT={'PASS' if overall else 'FAIL'}")
    print(
        "LIMITATION=This rubric result applies only to the evaluated transcript "
        "after deterministic gating; it does not establish full system, security, "
        "deployment, backend, or holdout-task health."
    )
    return 0 if overall else 1


def run_self_tests():
    rubric = validate_rubric(load_rubric())
    fixture = load_json(FIXTURE_PATH)
    gate_passed, _, counts = deterministic_gate(fixture)
    dimension = rubric["dimensions"][0]
    valid = {
        "dimension": dimension["name"],
        "score": 3,
        "passed": True,
        "justification": "Fixture evidence supports the threshold.",
        "evidence": ["fixture"],
        "limitations": ["not a real run"],
    }
    cases = [
        ("rubric schema", len(rubric["dimensions"]) == 4),
        ("deterministic fixture gate", gate_passed and counts["FAIL"] == 0),
        ("strict valid judge JSON", parse_judge_reply(json.dumps(valid), dimension) == valid),
    ]
    try:
        parse_judge_reply(f"\`\`\`json\n{json.dumps(valid)}\n\`\`\`", dimension)
        fenced_rejected = False
    except ValueError:
        fenced_rejected = True
    cases.append(("fenced judge JSON rejected", fenced_rejected))

    missing = dict(valid)
    missing.pop("limitations")
    try:
        parse_judge_reply(json.dumps(missing), dimension)
        missing_rejected = False
    except ValueError:
        missing_rejected = True
    cases.append(("missing judge field rejected", missing_rejected))

    sanitized = sanitized_evidence(fixture, collect_results(fixture))
    cases.append(
        (
            "judge evidence excludes handoffs and source paths",
            '"handoff":' not in json.dumps(sanitized).lower()
            and "sources" not in sanitized,
        )
    )

    for name, passed in cases:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    print(
        f"SELF_TEST_TALLY PASS={sum(passed for _, passed in cases)} "
        f"FAIL={sum(not passed for _, passed in cases)}"
    )
    return 0 if all(passed for _, passed in cases) else 1


def main(argv):
    if argv == ["--self-test"]:
        return run_self_tests()
    if len(argv) != 1:
        print("usage: test_rubric_suite.py <transcript.json>")
        print("       test_rubric_suite.py --self-test")
        return 2
    try:
        return evaluate(argv[0])
    except Exception as exc:
        print(f"RUBRIC_ERROR {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
