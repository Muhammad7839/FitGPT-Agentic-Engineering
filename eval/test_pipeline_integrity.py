import sys
import importlib.util
from pathlib import Path

import yaml


def _load_script(name):
    script = Path(__file__).resolve().parents[1] / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


integrity = _load_script("check-pipeline-integrity.py")


def test_current_ci_workflow_passes_integrity():
    result = integrity.check_workflow(Path(".github/workflows/ci.yml"))
    assert result["status"] == "PASS", result["failures"]


def test_policy_continue_on_error_is_rejected(tmp_path):
    data = yaml.safe_load(Path(".github/workflows/ci.yml").read_text(encoding="utf-8"))
    data["jobs"]["policy-tests"]["continue-on-error"] = True
    path = tmp_path / "ci.yml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    result = integrity.check_workflow(path)
    assert result["status"] == "FAIL"
    assert "policy-tests must not use continue-on-error" in result["failures"]


def test_audit_trail_removal_is_rejected(tmp_path):
    data = yaml.safe_load(Path(".github/workflows/ci.yml").read_text(encoding="utf-8"))
    data["jobs"].pop("audit-trail")
    path = tmp_path / "ci.yml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    result = integrity.check_workflow(path)
    assert result["status"] == "FAIL"
    assert any("audit-trail" in failure for failure in result["failures"])


def test_global_write_all_permission_is_rejected(tmp_path):
    data = yaml.safe_load(Path(".github/workflows/ci.yml").read_text(encoding="utf-8"))
    data["permissions"] = "write-all"
    path = tmp_path / "ci.yml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    result = integrity.check_workflow(path)
    assert result["status"] == "FAIL"
    assert "workflow uses write-all permissions" in result["failures"]
