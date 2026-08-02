"""Normalize preserved FitGPT Run 3/4/5 evidence into one development transcript."""

import hashlib
import json
import re
from pathlib import Path

ROLE_ORDER = ["planner", "implementer", "reviewer", "tester", "project-manager"]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def content_items(record):
    message = record.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content", [])
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [item for item in content if isinstance(item, dict)]


def content_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            item.get("text", str(item))
            if isinstance(item, dict) and item.get("type") == "text"
            else str(item)
            for item in value
        )
    return str(value)


def parse_json_or_text(value):
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return {"value": value}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {"text": value}


def tool_results(records):
    results = {}
    for record in records:
        if record.get("type") != "user":
            continue
        for item in content_items(record):
            if item.get("type") == "tool_result":
                results[item.get("tool_use_id")] = {
                    "content": item.get("content"),
                    "is_error": bool(item.get("is_error")),
                }
    return results


def sanitized_args(args):
    clean = dict(args or {})
    content = clean.pop("content", None)
    if isinstance(content, str):
        clean["content_sha256"] = hashlib.sha256(content.encode("utf-8")).hexdigest()
        clean["content_bytes"] = len(content.encode("utf-8"))
    return clean


def sanitized_result(tool, value):
    parsed = parse_json_or_text(value)
    if tool == "mcp__coursetools__file_read":
        raw = json.dumps(parsed, sort_keys=True, ensure_ascii=False)
        return {
            "result_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "result_bytes": len(raw.encode("utf-8")),
            "summary": "Read content is preserved in the cited source stream and not duplicated.",
        }
    return parsed


def extract_tool_events(records, role, sequence_start, source_path):
    results = tool_results(records)
    events = []
    sequence = sequence_start
    for record in records:
        if record.get("type") != "assistant":
            continue
        for item in content_items(record):
            if item.get("type") != "tool_use":
                continue
            tool_id = item.get("id")
            result_record = results.get(tool_id, {})
            raw_result = result_record.get("content")
            text = content_text(raw_result)
            success = not result_record.get("is_error") and "Authorization error:" not in text
            event = {
                "type": "tool_call",
                "sequence": sequence,
                "role": role,
                "tool": item.get("name"),
                "args": sanitized_args(item.get("input", {})),
                "result": sanitized_result(item.get("name"), raw_result),
                "success": success,
                "actual_event": True,
                "source": {"path": str(source_path), "tool_use_id": tool_id},
            }
            if item.get("name") == "mcp__coursetools__test_runner":
                event["evidence_class"] = "dummy"
            events.append(event)
            sequence += 1
    return events


def agent_invocations(main_records):
    results = tool_results(main_records)
    invocations = {}
    for record in main_records:
        if record.get("type") != "assistant":
            continue
        for item in content_items(record):
            if item.get("type") != "tool_use" or item.get("name") != "Agent":
                continue
            payload = item.get("input", {})
            description = payload.get("description", "")
            role = next((candidate for candidate in ROLE_ORDER if candidate in description.lower()), None)
            if role:
                invocations[role] = {
                    "handoff": payload.get("prompt", ""),
                    "output": content_text(results.get(item.get("id"), {}).get("content")),
                    "tool_use_id": item.get("id"),
                }
    return invocations


def cleaned_paths(text):
    matches = re.findall(r"(?:README\.md|backend/[A-Za-z0-9_./-]+)", text)
    return sorted({item.rstrip(".,;:)") for item in matches})


def lines_matching(text, patterns):
    found = []
    for line in text.splitlines():
        stripped = line.strip(" -*")
        if stripped and any(pattern in stripped.lower() for pattern in patterns):
            found.append(stripped)
    return found


def markdown_headings(text):
    return re.findall(r"^#{1,3}\s+(.+)$", text, flags=re.MULTILINE)


def responsibility(role, handoff):
    task = re.search(r"^Task:\s*(.+)$", handoff, flags=re.MULTILINE)
    if task:
        return task.group(1).strip()
    defaults = {
        "implementer": "Apply only the explicitly approved documentation and template changes.",
        "tester": "Run and interpret only the approved bounded dummy test target.",
        "project-manager": "Update only the controlled dummy issue after every gate and current approval.",
    }
    return defaults.get(
        role,
        f"Perform only the bounded {role} responsibility described in the exact handoff.",
    )


def handoff_fields(role, handoff, workflow_run, extra=None):
    version_match = re.search(
        r"(?:Role version:\s*[^\n]*?v|Agent version:\s*)(\d+\.\d+\.\d+)",
        handoff,
    )
    issue_match = re.search(r"(?:Controlled issue|Issue):\s*([^\n.]+)", handoff)
    criteria = lines_matching(
        handoff,
        ("criterion", "acceptance", "pass only", "required action", "must satisfy", "must match"),
    )
    fields = {
        "workflow_identity": workflow_run,
        "task_or_issue": issue_match.group(1).strip() if issue_match else "COURSE-FITGPT-001",
        "role": role,
        "version": version_match.group(1) if version_match else "1.0.0",
        "single_responsibility": responsibility(role, handoff),
        "allowed_context": cleaned_paths(handoff)
        or ["Only the role-specific evidence explicitly included in the handoff."],
        "acceptance_criteria": criteria
        or ["The exact handoff output and boundary conditions must be satisfied."],
        "prohibitions": lines_matching(handoff, ("do not", "prohibit", "no other tools"))
        or ["Do not exceed the role boundary."],
        "required_output_format": markdown_headings(handoff)
        or ["Return the role-specific structured result."],
    }
    if extra:
        fields.update(extra)
    return fields


def output_document(role, output):
    lower = output.lower()
    if role == "reviewer":
        status = bool(re.search(r"## Verdict\s+Pass", output, re.DOTALL))
    elif role == "tester":
        status = bool(re.search(r"## Result\s+[^A-Za-z]*Pass", output, re.DOTALL))
    elif role == "project-manager":
        status = bool(re.search(r"## New status\s+[^A-Za-z]*Done", output, re.DOTALL))
    else:
        status = bool(output.strip()) and "blocked" not in lower
    return {
        "verdict": "Pass" if status else "Unknown",
        "sections": markdown_headings(output),
        "summary": output.strip().splitlines()[0] if output.strip() else "",
        "verdict_source": "Preserved role output and accepted orchestration gate.",
    }


def stream_init(records):
    return next(
        (
            record
            for record in records
            if record.get("type") == "system" and record.get("subtype") == "init"
        ),
        {},
    )


def stream_result(records):
    return next((record for record in records if record.get("type") == "result"), {})


def source(path, kind):
    path = Path(path)
    return {"kind": kind, "path": str(path), "sha256": sha256(path)}


def normalize(run3_root, run4_root, run5_root):
    run3_root = Path(run3_root)
    run4_root = Path(run4_root)
    run5_root = Path(run5_root)
    main_path = run3_root / "orchestrator-stage/final-jsonl/main.jsonl"
    main_records = read_jsonl(main_path)
    invocations = agent_invocations(main_records)

    role_streams = {}
    meta_dir = run3_root / "orchestrator-stage/final-jsonl/subagents"
    for meta_path in sorted(meta_dir.glob("*.meta.json")):
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        role_streams[metadata["agentType"]] = meta_path.with_name(
            meta_path.name.replace(".meta.json", ".jsonl")
        )

    events = []
    sources = [source(main_path, "Claude main stream-json")]
    stage_sequences = {"planner": 10, "implementer": 30, "reviewer": 40}

    for step, role in enumerate(("planner", "implementer", "reviewer"), start=1):
        invocation = invocations[role]
        stream_path = role_streams[role]
        events.append(
            {
                "type": "subagent",
                "sequence": stage_sequences[role],
                "step": step,
                "role": role,
                "version": "1.0.0",
                "workflow_run": "Run 3",
                "selected_for_path": True,
                "handoff": invocation["handoff"],
                "handoff_fields": handoff_fields(role, invocation["handoff"], "Run 3"),
                "output": invocation["output"],
                "output_document": output_document(role, invocation["output"]),
                "source": {"path": str(main_path), "tool_use_id": invocation["tool_use_id"]},
            }
        )
        events.extend(
            extract_tool_events(
                read_jsonl(stream_path),
                role,
                stage_sequences[role] + 1,
                stream_path,
            )
        )
        sources.append(source(stream_path, f"{role} subagent stream-json"))

    approvals = []
    for record in main_records:
        message = record.get("message")
        if (
            record.get("type") == "user"
            and isinstance(message, dict)
            and isinstance(message.get("content"), str)
            and message["content"].strip() == "APPROVE_RUN3_PLAN"
        ):
            approvals.append(message["content"].strip())
    if approvals != ["APPROVE_RUN3_PLAN"]:
        raise ValueError("exact Run 3 plan approval was not found once")
    plan_approval = {
        "kind": "plan",
        "token": "APPROVE_RUN3_PLAN",
        "workflow_run": "Run 3",
        "sequence": 20,
        "reused": False,
        "source": str(main_path),
    }
    events.append(
        {"type": "human_approval", **{key: value for key, value in plan_approval.items() if key != "source"}}
    )

    reviewer_path = run5_root / "outputs/run3-reviewer-pass.txt"
    reviewer_evidence = reviewer_path.read_text(encoding="utf-8")

    tester_handoff_path = run5_root / "tester-stage/handoff.md"
    tester_session_path = run5_root / "tester-stage/session.jsonl"
    tester_handoff = tester_handoff_path.read_text(encoding="utf-8")
    tester_records = read_jsonl(tester_session_path)
    tester_output = stream_result(tester_records).get("result", "")
    events.append(
        {
            "type": "subagent",
            "sequence": 50,
            "step": 4,
            "role": "tester",
            "version": "1.0.0",
            "workflow_run": "Run 5",
            "selected_for_path": True,
            "handoff": tester_handoff,
            "handoff_fields": handoff_fields(
                "tester",
                tester_handoff,
                "Run 5",
                {
                    "reviewer_evidence": reviewer_evidence,
                    "approved_changed_files": ["README.md", "backend/.env.example"],
                },
            ),
            "output": tester_output,
            "output_document": output_document("tester", tester_output),
            "runtime_tools": stream_init(tester_records).get("tools", []),
            "source": {"path": str(tester_session_path)},
        }
    )
    events.extend(extract_tool_events(tester_records, "tester", 51, tester_session_path))

    pm_handoff_path = run5_root / "project-manager-stage/handoff.md"
    pm_session_path = run5_root / "project-manager-stage/session.jsonl"
    pm_handoff = pm_handoff_path.read_text(encoding="utf-8")
    pm_records = read_jsonl(pm_session_path)
    pm_output = stream_result(pm_records).get("result", "")
    approval_match = re.search(r"Explicit current approval:\s*(APPROVE_RUN5_FINAL)", pm_handoff)
    if not approval_match:
        raise ValueError("exact Run 5 final approval was not found")
    final_approval = {
        "kind": "final",
        "token": approval_match.group(1),
        "workflow_run": "Run 5",
        "sequence": 60,
        "reused": False,
        "source": str(pm_handoff_path),
    }
    events.append(
        {"type": "human_approval", **{key: value for key, value in final_approval.items() if key != "source"}}
    )
    events.append(
        {
            "type": "subagent",
            "sequence": 70,
            "step": 5,
            "role": "project-manager",
            "version": "1.0.0",
            "workflow_run": "Run 5",
            "selected_for_path": True,
            "handoff": pm_handoff,
            "handoff_fields": handoff_fields(
                "project-manager",
                pm_handoff,
                "Run 5",
                {
                    "reviewer_evidence": f"Exact Reviewer Pass SHA-256 {sha256(reviewer_path)}",
                    "tester_evidence": tester_output,
                    "current_human_approval": approval_match.group(1),
                },
            ),
            "output": pm_output,
            "output_document": output_document("project-manager", pm_output),
            "runtime_tools": stream_init(pm_records).get("tools", []),
            "source": {"path": str(pm_session_path)},
        }
    )
    events.extend(extract_tool_events(pm_records, "project-manager", 71, pm_session_path))

    run3_tester = invocations.get("tester", {})
    historical = [
        {
            "workflow_run": "Run 3",
            "role": "tester",
            "outcome": "Blocked",
            "reason": "Required Reviewer evidence, changed-file list, and acceptance criteria were absent.",
            "tool_call_count": 0,
            "output": run3_tester.get("output", ""),
            "source": str(main_path),
        }
    ]
    run4_session = run4_root / "tester-stage/session.jsonl"
    run4_records = read_jsonl(run4_session)
    historical.append(
        {
            "workflow_run": "Run 4",
            "role": "tester",
            "outcome": "Blocked",
            "reason": "coursetools was pending, init.tools was empty, and no actual tool-use event existed.",
            "tool_call_count": sum(
                1
                for record in run4_records
                for item in content_items(record)
                if item.get("type") == "tool_use"
            ),
            "model_text": stream_result(run4_records).get("result", ""),
            "source": str(run4_session),
        }
    )

    verification_path = run5_root / "final-checkpoint/exercise-verification.txt"
    protected_unchanged = (
        "Prohibited path changes in Run 5: none"
        in verification_path.read_text(encoding="utf-8")
    )
    if not protected_unchanged:
        raise ValueError("Run 5 protected-path verification is missing")

    sources.extend(
        [
            source(reviewer_path, "exact Reviewer Pass"),
            source(tester_handoff_path, "Tester handoff"),
            source(tester_session_path, "Tester stream-json"),
            source(pm_handoff_path, "Project Manager handoff"),
            source(pm_session_path, "Project Manager stream-json"),
            source(run4_session, "preserved blocked Run 4 stream-json"),
            source(verification_path, "final workflow verification"),
        ]
    )
    events.sort(key=lambda item: item["sequence"])

    return {
        "schema_version": "1.0.0",
        "run_id": "FITGPT-DEV-BASELINE-R3-R5",
        "run_kind": "development",
        "fixture": False,
        "evidence_origin": "Normalized directly from preserved Run 3, Run 4, and Run 5 evidence; no role or tool was replayed.",
        "task_id": "COURSE-FITGPT-001",
        "task_description": "Clarify local SQLite fallback and production DATABASE_URL requirements in contributor documentation.",
        "expected_path": ROLE_ORDER,
        "approved_writable_paths": ["README.md", "backend/.env.example"],
        "changed_files": ["README.md", "backend/.env.example"],
        "protected_files_unchanged": protected_unchanged,
        "required_test_target": "backend/tests/test_config_startup.py",
        "allowed_ticket_id": "COURSE-FITGPT-001",
        "duration_seconds": None,
        "reported_cost_usd": None,
        "budgets": {
            "duration_seconds": 1800,
            "reported_cost_usd": 1.5,
            "basis": "Provisional ceilings derive from preserved Module 1 and Module 3 evidence. The composite continuation has no reliable non-overlapping aggregate, so both checks remain SKIP.",
        },
        "claims": {
            "real_pytest": False,
            "full_system_health": False,
            "real_external_tracker": False,
        },
        "context_canary": None,
        "human_approvals": [plan_approval, final_approval],
        "events": events,
        "historical_attempts": historical,
        "sources": sources,
        "limitations": [
            "The baseline combines accepted stages from Runs 3 and 5; blocked Run 3 and Run 4 Tester attempts remain historical evidence.",
            "The final approval is preserved in the exact Project Manager handoff rather than an independently signed audit record.",
            "No server-persisted audit log exists; stream-json tool events are the strongest tool-call evidence.",
            "No deterministic context canary was planted in this development workflow.",
            "There is no reliable non-overlapping aggregate duration or reported cost for the composite continuation.",
            "test_runner and task_tracker are controlled dummy tools, not real pytest or an external issue service.",
        ],
    }


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--run3-root", required=True)
    parser.add_argument("--run4-root", required=True)
    parser.add_argument("--run5-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    normalized = normalize(args.run3_root, args.run4_root, args.run5_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
