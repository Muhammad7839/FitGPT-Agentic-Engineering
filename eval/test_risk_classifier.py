from risk_classifier import CLASSIFIER_VERSION, classify_change


def assert_tier(paths, expected, metadata=None):
    result = classify_change(paths, metadata=metadata)
    assert result.tier == expected
    assert result.classifier_version == CLASSIFIER_VERSION
    assert result.triggered_rules
    return result


def test_low_feature_documentation_file():
    result = assert_tier(["docs/features/accessibility.md"], "LOW")
    assert "LOW_NON_EXECUTABLE_CONTENT" in result.triggered_rules


def test_low_non_governance_readme_style_change():
    assert_tier(["README.md"], "LOW")


def test_medium_bounded_js_react_utility_change():
    result = assert_tier(["web/src/utils/feedbackPrompts.js"], "MEDIUM")
    assert "MEDIUM_EXECUTABLE_OR_TEST_PATH" in result.triggered_rules


def test_medium_application_unit_test_change():
    assert_tier(["web/src/utils/feedbackPrompts.test.js"], "MEDIUM")


def test_high_github_workflow():
    assert_tier([".github/workflows/ci.yml"], "HIGH")


def test_high_governance_policy():
    assert_tier(["docs/governance-policy.md"], "HIGH")


def test_high_mcp_allow_list():
    assert_tier(["mcp-servers/storage/allow-list.json"], "HIGH")


def test_high_mcp_server_contract():
    assert_tier(["mcp/coursetools_server.py"], "HIGH")


def test_high_agent_permissions():
    assert_tier([".claude/agents/implementer.md"], "HIGH")


def test_high_docker_sandbox_security():
    assert_tier(["Dockerfile"], "HIGH")
    assert_tier([".agentic/container/run-agent.sh"], "HIGH")


def test_high_auth_security_sensitive_path():
    assert_tier(["backend/app/auth/session.py"], "HIGH")
    assert_tier(["backend/app/security/passwords.py"], "HIGH")


def test_high_db_migration_schema():
    assert_tier(["migrations/versions/001_add_users.py"], "HIGH")
    assert_tier(["backend/schema.sql"], "HIGH")


def test_high_policy_evaluation_enforcement():
    assert_tier(["eval/test_policy.py"], "HIGH")


def test_mixed_low_and_high_paths_is_high():
    assert_tier(["docs/features/accessibility.md", "mcp-servers/retrieval/allow-list.json"], "HIGH")


def test_mixed_medium_and_high_paths_is_high():
    assert_tier(["web/src/App.jsx", ".github/workflows/deploy.yml"], "HIGH")


def test_mixed_low_and_medium_paths_is_medium():
    assert_tier(["docs/features/accessibility.md", "web/src/utils/feedbackPrompts.js"], "MEDIUM")


def test_empty_path_input_is_conservative_high_not_low():
    result = assert_tier([], "HIGH")
    assert "HIGH_EMPTY_PATH_SET" in result.triggered_rules


def test_unknown_executable_looking_path_is_medium():
    assert_tier(["tools/local_helper.py"], "MEDIUM")


def test_unknown_plain_content_path_is_medium_conservative():
    assert_tier(["notes/operational-checklist.yaml"], "MEDIUM")


def test_path_normalization():
    result = assert_tier(["./web\\src\\utils\\feedbackPrompts.js"], "MEDIUM")
    assert result.normalized_paths == ("web/src/utils/feedbackPrompts.js",)


def test_path_traversal_is_high():
    result = assert_tier(["docs/../.env"], "HIGH")
    assert "HIGH_PATH_TRAVERSAL" in result.triggered_rules


def test_malformed_path_is_high():
    result = assert_tier([""], "HIGH")
    assert "HIGH_EMPTY_PATH_SET" in result.triggered_rules
    assert "HIGH_MALFORMED_PATH" in result.triggered_rules


def test_sensitive_metadata_intent_is_high():
    assert_tier(["docs/features/accessibility.md"], "HIGH", metadata={"request": "document production secret handling"})


def test_locked_representative_scenarios_classify_correctly():
    assert_tier(["docs/features/accessibility.md"], "LOW")
    assert_tier(["web/src/utils/feedbackPrompts.js", "web/src/utils/feedbackPrompts.test.js"], "MEDIUM")
    assert_tier(
        [
            "eval/test_policy.py",
            "mcp-servers/storage/allow-list.json",
            "mcp-servers/retrieval/allow-list.json",
            "docs/governance-policy.md",
        ],
        "HIGH",
    )
