import importlib.util
import sys
from pathlib import Path


def _load_script():
    script = Path(__file__).resolve().parents[1] / "scripts" / "check-config-docs-consistency.py"
    spec = importlib.util.spec_from_file_location("check_config_docs_consistency", script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_script()


def test_real_database_url_config_docs_consistency_passes():
    result = checker.check_database_url_consistency(Path("."))
    assert result["status"] == "PASS", result["checks"]
    assert result["model_cost_usd"] == 0
    assert result["checks"]["implementation_requires_database_url_in_production"] is True
    assert result["checks"]["focused_tests_cover_database_url_production_requirement"] is True


def test_missing_env_template_definition_fails(tmp_path):
    for surface in checker.SURFACES.values():
        target = tmp_path / surface
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("DATABASE_URL must be set in production\nfalls back to a local SQLite database\n", encoding="utf-8")
    (tmp_path / "backend/.env.example").write_text("SECRET_KEY=placeholder\n", encoding="utf-8")

    result = checker.check_database_url_consistency(tmp_path)
    assert result["status"] == "FAIL"
    assert result["checks"]["env_template_defines_database_url"] is False


def test_output_contains_only_deterministic_surfaces():
    result = checker.check_database_url_consistency(Path("."))
    assert result["surfaces"] == checker.SURFACES
    assert "agent_opinion" not in result
