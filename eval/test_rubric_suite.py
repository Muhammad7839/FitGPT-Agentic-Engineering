"""Deterministically gated rubric scoring for FitGPT transcripts.

Usage:
    python3 eval/test_rubric_suite.py <transcript.json>
    python3 eval/test_rubric_suite.py --self-test
"""

import json
import hashlib
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
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "dimension": {"type": "string"},
        "score": {"type": "integer", "minimum": 1, "maximum": 4},
        "passed": {"type": "boolean"},
        "justification": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1200,
        },
        "evidence": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {"type": "string", "minLength": 1, "maxLength": 500},
        },
        "limitations": {
            "type": "array",
            "maxItems": 6,
            "items": {"type": "string", "minLength": 1, "maxLength": 500},
        },
    },
    "required": sorted(JUDGE_KEYS),
    "additionalProperties": False,
}
MAX_ROLE_EXCERPT_CHARS = 2400
MAX_GENERAL_ROLE_EXCERPT_CHARS = 1200
MAX_HISTORY_EXCERPT_CHARS = 600
EVIDENCE_DIR_ENV = "FITGPT_RUBRIC_EVIDENCE_DIR"
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


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def bounded_text(value, limit):
    if not isinstance(value, str):
        return value
    record = {
        "sha256": sha256_text(value),
        "characters": len(value),
        "markdown_headings": [
            line.strip()
            for line in value.splitlines()
            if line.lstrip().startswith("#")
        ],
    }
    if len(value) <= limit:
        record["truncated"] = False
        record["text"] = value
        return record
    half = limit // 2
    record["truncated"] = True
    record["head"] = value[:half]
    record["tail"] = value[-half:]
    return record


def bounded_history(attempt):
    result = {}
    for key, value in attempt.items():
        if key in {"output", "model_text"}:
            result[key] = bounded_text(value, MAX_HISTORY_EXCERPT_CHARS)
        else:
            result[key] = value
    return result


def summarize_tool_evidence(tool_evidence):
    counts = {}
    for item in tool_evidence:
        key = (item["role"], item["tool"])
        current = counts.setdefault(
            key, {"calls": 0, "successful": 0, "actual_events": 0}
        )
        current["calls"] += 1
        current["successful"] += item["success"] is True
        current["actual_events"] += item["actual_event"] is True
    return {
        "counts": [
            {"role": role, "tool": tool, **values}
            for (role, tool), values in sorted(counts.items())
        ],
        "non_read_events": [
            item
            for item in tool_evidence
            if not item["tool"].endswith("file_read")
        ],
    }


def dimension_schema(dimension_name):
    schema = json.loads(json.dumps(JUDGE_SCHEMA))
    schema["properties"]["dimension"]["enum"] = [dimension_name]
    return schema


def sanitized_evidence(transcript, deterministic_results, dimension_name=None):
    role_excerpt_limit = (
        MAX_ROLE_EXCERPT_CHARS
        if dimension_name == "Test Execution Fidelity"
        else MAX_GENERAL_ROLE_EXCERPT_CHARS
    )
    subagents = []
    for event in transcript.get("events", []):
        if event.get("type") != "subagent" or not event.get("selected_for_path", True):
            continue
        subagents.append(
            {
                "role": event.get("role"),
                "workflow_run": event.get("workflow_run"),
                "verdict": (event.get("output_document") or {}).get("verdict"),
                "substantive_output": bounded_text(
                    event.get("output"), role_excerpt_limit
                ),
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
    evidence = {
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
        "historical_attempts": [
            bounded_history(attempt)
            for attempt in transcript.get("historical_attempts") or []
        ],
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
    if dimension_name == "Test Execution Fidelity":
        evidence["subagent_outputs"] = [
            item for item in subagents if item["role"] == "tester"
        ]
        evidence["tool_evidence"] = [
            item for item in tool_evidence if item["tool"].endswith("test_runner")
        ]
        evidence.pop("historical_attempts", None)
    elif dimension_name in {"Outcome Accuracy", "Evidence Coverage"}:
        evidence["tool_evidence"] = summarize_tool_evidence(tool_evidence)
    elif dimension_name == "Readiness Recommendation Quality":
        evidence["tool_evidence"] = summarize_tool_evidence(
            [
                item
                for item in tool_evidence
                if item["tool"].endswith(("test_runner", "task_tracker"))
            ]
        )
        evidence.pop("historical_attempts", None)
    return evidence


def build_judge_prompt(transcript, dimension, deterministic_results):
    evidence = sanitized_evidence(
        transcript, deterministic_results, dimension["name"]
    )
    return (
        "You are an isolated agent-as-judge. Score one quality dimension for a "
        "FitGPT orchestration development run. You have no repository, shell, "
        "MCP, test, tracker, file, or web tools. Use only the task, dimension, "
        "levels, and sanitized evidence below. Do not infer missing facts.\n\n"
        "Return exactly one JSON object and no other text. Do not use Markdown "
        "fences. Use exactly these fields:\n"
        '{"dimension":"...", "score":1, "passed":false, '
        '"justification":"...", "evidence":["..."], "limitations":["..."]}\n\n'
        "Mechanical response limits:\n"
        "- dimension: copy the requested dimension name exactly\n"
        "- score: integer 1 through 4\n"
        "- passed: true exactly when score meets the supplied threshold\n"
        "- justification: one non-empty string, at most 1200 characters\n"
        "- evidence: 1 through 8 non-empty strings, each at most 500 characters\n"
        "- limitations: 0 through 6 non-empty strings, each at most 500 characters\n\n"
        "Bounded excerpts include SHA-256 hashes, character counts, and heading "
        "inventories. A truncated excerpt is evidence only for the text shown; "
        "do not infer omitted content.\n\n"
        f"TASK:\n{json.dumps({'task_id': transcript.get('task_id'), 'description': transcript.get('task_description')}, indent=2)}\n\n"
        f"DIMENSION:\n{json.dumps(dimension, indent=2)}\n\n"
        "SANITIZED EVIDENCE:\n"
        f"{json.dumps(evidence, ensure_ascii=False, separators=(',', ':'))}\n"
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
    if type(value["score"]) is not int or not 1 <= value["score"] <= 4:
        raise ValueError("judge score must be an integer from 1 to 4")
    if type(value["passed"]) is not bool:
        raise ValueError("judge passed must be a boolean")
    expected_pass = value["score"] >= dimension["pass_threshold"]
    if value["passed"] is not expected_pass:
        raise ValueError("judge passed value contradicts the dimension threshold")
    if (
        not isinstance(value["justification"], str)
        or not value["justification"].strip()
        or len(value["justification"]) > 1200
    ):
        raise ValueError("judge justification must be non-empty")
    if not isinstance(value["evidence"], list):
        raise ValueError("judge evidence must be a list")
    if not isinstance(value["limitations"], list):
        raise ValueError("judge limitations must be a list")
    if not 1 <= len(value["evidence"]) <= 8:
        raise ValueError("judge evidence must contain 1 through 8 items")
    if len(value["limitations"]) > 6:
        raise ValueError("judge limitations must contain at most 6 items")
    for field in ("evidence", "limitations"):
        if not isinstance(value[field], list) or not all(
            isinstance(item, str) and item.strip() and len(item) <= 500
            for item in value[field]
        ):
            raise ValueError(f"judge {field} must be a bounded list of strings")
    return value


def extract_judge_reply(envelope):
    structured = envelope.get("structured_output")
    if isinstance(structured, dict):
        return json.dumps(structured)
    reply = envelope.get("result")
    if not isinstance(reply, str):
        raise RuntimeError("Claude envelope has no structured output or string result")
    return reply


def write_json(path, value):
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def call_judge(prompt, dimension_name, evidence_dir=None):
    with tempfile.TemporaryDirectory(prefix="fitgpt-eval-judge-") as judge_dir:
        empty_mcp = Path(judge_dir) / "empty-mcp.json"
        empty_mcp.write_text('{"mcpServers": {}}\n', encoding="utf-8")
        schema = dimension_schema(dimension_name)
        command = [
            "claude",
            "--print",
            "--output-format",
            "json",
            "--json-schema",
            json.dumps(schema, separators=(",", ":")),
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
        dimension_dir = None
        if evidence_dir is not None:
            dimension_dir = evidence_dir / dimension_name.lower().replace(" ", "-")
            dimension_dir.mkdir(parents=True, exist_ok=False)
            (dimension_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
            write_json(
                dimension_dir / "request-metadata.json",
                {
                    "dimension": dimension_name,
                    "prompt_sha256": sha256_text(prompt),
                    "prompt_characters": len(prompt),
                    "prompt_bytes": len(prompt.encode("utf-8")),
                    "schema_sha256": sha256_text(
                        json.dumps(schema, separators=(",", ":"))
                    ),
                    "schema": schema,
                    "model_selection": "unchanged default; no --model flag",
                    "available_tools": [],
                    "mcp_servers": {},
                    "command": [
                        "<claude>",
                        "--print",
                        "--output-format",
                        "json",
                        "--json-schema",
                        "<dimension-schema>",
                        "--permission-mode",
                        "dontAsk",
                        "--tools",
                        "",
                        "--disallowedTools",
                        "<complete-disallowed-list>",
                        "--mcp-config",
                        "<temporary-empty-mcp.json>",
                        "--strict-mcp-config",
                        "--no-chrome",
                        "--setting-sources",
                        "user",
                        "--no-session-persistence",
                    ],
                },
            )
        completed = subprocess.run(
            command,
            input=prompt,
            cwd=judge_dir,
            capture_output=True,
            text=True,
            timeout=240,
            env=environment,
        )
        if dimension_dir is not None:
            (dimension_dir / "stdout.txt").write_text(
                completed.stdout, encoding="utf-8"
            )
            (dimension_dir / "stderr.txt").write_text(
                completed.stderr, encoding="utf-8"
            )
            (dimension_dir / "exit-code.txt").write_text(
                f"{completed.returncode}\n", encoding="utf-8"
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
        if dimension_dir is not None:
            write_json(dimension_dir / "response-envelope.json", envelope)
        return extract_judge_reply(envelope)


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
    evidence_dir = None
    if os.environ.get(EVIDENCE_DIR_ENV):
        evidence_dir = Path(os.environ[EVIDENCE_DIR_ENV]).resolve()
        evidence_dir.mkdir(parents=True, exist_ok=False)
    dimension_results = []
    for dimension in rubric["dimensions"]:
        prompt = build_judge_prompt(transcript, dimension, deterministic_results)
        reply = call_judge(prompt, dimension["name"], evidence_dir)
        parsed = parse_judge_reply(reply, dimension)
        dimension_results.append(parsed)
        if evidence_dir is not None:
            dimension_dir = evidence_dir / dimension["name"].lower().replace(" ", "-")
            write_json(dimension_dir / "parsed-result.json", parsed)
            write_json(
                dimension_dir / "validation-result.json",
                {"valid": True, "parser": "parse_judge_reply"},
            )
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
    if evidence_dir is not None:
        write_json(
            evidence_dir / "aggregate-result.json",
            {
                "judge_calls": len(dimension_results),
                "dimension_results": dimension_results,
                "score": total,
                "maximum_score": rubric["maximum_score"],
                "threshold": rubric["overall_pass_threshold"],
                "each_dimension_required": True,
                "passed": overall,
            },
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
        (
            "structured Claude envelope",
            extract_judge_reply({"structured_output": valid}) == json.dumps(valid),
        ),
        (
            "dimension schema matches parser keys",
            set(dimension_schema(dimension["name"])["properties"]) == JUDGE_KEYS
            and set(dimension_schema(dimension["name"])["required"]) == JUDGE_KEYS
            and dimension_schema(dimension["name"])["additionalProperties"] is False,
        ),
    ]
    try:
        parse_judge_reply("{not json", dimension)
        malformed_rejected = False
    except ValueError:
        malformed_rejected = True
    cases.append(("malformed judge JSON rejected", malformed_rejected))
    try:
        parse_judge_reply(f"```json\n{json.dumps(valid)}\n```", dimension)
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

    incorrect_type = dict(valid)
    incorrect_type["score"] = "3"
    try:
        parse_judge_reply(json.dumps(incorrect_type), dimension)
        incorrect_type_rejected = False
    except ValueError:
        incorrect_type_rejected = True
    cases.append(("incorrect judge field type rejected", incorrect_type_rejected))

    sanitized = sanitized_evidence(
        fixture, collect_results(fixture), "Evidence Coverage"
    )
    cases.append(
        (
            "judge evidence excludes handoffs and source paths",
            '"handoff":' not in json.dumps(sanitized).lower()
            and "sources" not in sanitized,
        )
    )
    bounded = all(
        output["substantive_output"]["characters"]
        <= MAX_GENERAL_ROLE_EXCERPT_CHARS
        or output["substantive_output"]["truncated"]
        for output in sanitized["subagent_outputs"]
    )
    cases.append(("dimension evidence uses bounded role text", bounded))

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
