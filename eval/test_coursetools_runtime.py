"""Runtime regression checks for the course-only coursetools MCP server."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_coursetools_server_imports_and_registers_expected_functions():
    module = import_module(ROOT / "mcp" / "coursetools_server.py", "coursetools_server_under_test")

    assert module.SERVER_NAME == "coursetools"
    for name in (
        "file_read",
        "file_write",
        "codebase_search",
        "shell",
        "test_runner",
        "task_tracker",
        "web_search",
    ):
        assert callable(getattr(module, name))
