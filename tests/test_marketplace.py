import json
from pathlib import Path


PLUGIN_ROOT = Path("plugins/iridium-codex")
REPORTING_PLUGIN_ROOT = Path("plugins/iridium-reporting-codex")
CLAUDE_PLUGIN_ROOT = Path("plugins/iridium-claude")
CLAUDE_REPORTING_PLUGIN_ROOT = Path("plugins/iridium-reporting-claude")

ADVISOR_MCP_CONTRACT_TERMS = (
    "get_advisor_identity",
    "accepted_names",
    "user-facing advisor name may change",
    "source of truth",
    "recall_client_memory_tool",
    "search_session_activity_tool",
    "fetch_client_memory_tool",
    "answer_evidence_items",
    "support_evidence_items",
    "client_planning_guidance.search_loop_contract",
    "retrieval_profile.exact_handles",
    "retrieval_profile.excluded_entities",
    "Do not use fact_recall with include_session_evidence",
)


def plugin_text_assets(root: Path) -> str:
    text_suffixes = {".json", ".md"}
    return "\n".join(
        path.read_text() for path in root.rglob("*") if path.is_file() and path.suffix in text_suffixes
    )


def test_iridium_codex_marketplace_exposes_advisor_and_reporting_plugins():
    marketplace = json.loads(Path(".agents/plugins/marketplace.json").read_text())

    assert marketplace["name"] == "iridium"
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert set(entries) == {"iridium-codex", "iridium-reporting-codex"}
    assert entries["iridium-codex"]["source"] == {
        "source": "local",
        "path": "./plugins/iridium-codex",
    }
    assert entries["iridium-reporting-codex"]["source"] == {
        "source": "local",
        "path": "./plugins/iridium-reporting-codex",
    }
    assert entries["iridium-codex"]["policy"] == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }
    assert entries["iridium-reporting-codex"]["policy"] == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }


def test_iridium_claude_marketplace_exposes_advisor_and_reporting_plugins():
    marketplace = json.loads(Path(".claude-plugin/marketplace.json").read_text())

    assert marketplace["name"] == "iridium-claude"
    assert marketplace["owner"]["name"] == "Iridium"
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert set(entries) == {"iridium-claude", "iridium-reporting-claude"}
    assert entries["iridium-claude"]["source"] == "./plugins/iridium-claude"
    assert entries["iridium-claude"]["description"] == (
        "Connect Claude Code to your private Iridium advisor memory."
    )
    assert entries["iridium-claude"]["category"] == "productivity"
    assert entries["iridium-reporting-claude"]["source"] == (
        "./plugins/iridium-reporting-claude"
    )
    assert entries["iridium-reporting-claude"]["description"] == (
        "Connect Claude Code to Iridium business reporting for an account."
    )
    assert entries["iridium-reporting-claude"]["category"] == "productivity"


def test_iridium_codex_plugin_contains_no_private_or_deployment_data():
    manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text())
    mcp = json.loads((PLUGIN_ROOT / ".mcp.json").read_text())
    skill = (PLUGIN_ROOT / "skills/iridium-advisor/SKILL.md").read_text()
    all_text = plugin_text_assets(PLUGIN_ROOT)

    assert manifest["name"] == "iridium-codex"
    assert manifest["version"] == "1.0.10"
    assert manifest["repository"] == "https://github.com/Jdashford/iridium-codex-plugin"
    assert manifest["mcpServers"] == "./.mcp.json"
    assert manifest["skills"] == "./skills/"
    assert "mcp_servers" not in mcp
    assert mcp["mcpServers"]["iridium"]["url"] == "https://connect.iridiumai.co/mcp"
    assert "connect.iridium.ai" not in all_text
    assert "https://iridium.ai" not in all_text
    assert "ask_advisor" in skill
    assert "client_planning_guidance.recommended_tool_calls" in skill
    assert "recommended_follow_ups" in skill
    assert "query_instruction" in skill
    assert "slot_label" in skill
    assert "target_entities" in skill
    assert "answer_precision_instruction" in skill
    assert "answer_constraints" in skill
    for term in ADVISOR_MCP_CONTRACT_TERMS:
        assert term in skill
    assert "recall_client_memory_tool" in skill
    assert "task `recent_documents`" in skill
    assert "list_recent_client_documents_tool" in skill
    assert "document metadata questions" in skill
    assert "Do not start with `ask_advisor`" in skill
    assert "If neither document metadata tool is exposed" in skill
    assert "task `recent_documents` and the requested limit" in skill
    assert "Do not rely on server inference from raw text" in skill
    assert "ask_advisor is not available" in skill
    assert "tool discovery" in skill
    assert "tool_search" in skill
    assert "before starting OAuth login" in skill
    assert "codex mcp login iridium" in skill
    assert "https://connect.iridiumai.co/oauth/authorize?" in skill
    assert "Do not block inside an interactive login loop" in skill
    assert "report the local Codex error plainly and stop" in skill
    assert "127.0.0.1 refused" in skill
    assert "fresh setup code" in skill
    assert "new Codex thread" in skill
    assert "hot-load" in skill
    assert "Do not use other Iridium, memory-system" in skill
    assert "Railway" not in all_text
    assert "up.railway.app" not in all_text
    assert "connection code" not in all_text.lower()
    assert "secret" not in all_text.lower()


def test_iridium_claude_plugin_is_native_and_contains_no_private_or_deployment_data():
    manifest = json.loads((CLAUDE_PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text())
    mcp = json.loads((CLAUDE_PLUGIN_ROOT / ".mcp.json").read_text())
    skill = (CLAUDE_PLUGIN_ROOT / "skills/iridium-advisor/SKILL.md").read_text()
    setup = (CLAUDE_PLUGIN_ROOT / "resources/setup.md").read_text()
    privacy = (CLAUDE_PLUGIN_ROOT / "resources/privacy.md").read_text()
    all_text = plugin_text_assets(CLAUDE_PLUGIN_ROOT)

    assert manifest["name"] == "iridium-claude"
    assert manifest["version"] == "1.0.1"
    assert manifest["repository"] == "https://github.com/Jdashford/iridium-claude-plugin"
    assert manifest["skills"] == "./skills/"
    assert manifest["mcpServers"] == "./.mcp.json"
    assert mcp["mcpServers"]["iridium"]["type"] == "http"
    assert mcp["mcpServers"]["iridium"]["url"] == "https://connect.iridiumai.co/mcp"
    assert "ask_advisor" in skill
    assert "Claude Code" in skill
    assert "/mcp" in setup
    assert "one-time setup code" in setup
    assert "Select `iridium`" in setup
    assert "Choose **Authenticate**" in setup
    assert "Paste the setup code only into the Iridium sign-in page" in setup
    assert "Do not paste it into Claude Code chat" in setup
    assert "contains no private memories" in privacy
    assert "connect.iridium.ai" not in all_text
    assert "https://iridium.ai" not in all_text
    assert "Railway" not in all_text
    assert "up.railway.app" not in all_text
    assert "sha256:" not in all_text
    assert "agent_client_id" not in all_text
    assert "setup_link_id" not in all_text
    assert "client_secret" not in all_text
    assert "recall_client_memory_tool" in skill
    assert "task `recent_documents`" in skill
    assert "list_recent_client_documents_tool" in skill
    assert "If neither document metadata tool is exposed" in skill
    assert "task `recent_documents` and the requested limit" in skill
    assert "Do not rely on server inference from raw text" in skill


def test_iridium_reporting_claude_plugin_has_separate_identity_and_no_private_data():
    manifest = json.loads((CLAUDE_REPORTING_PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text())
    mcp = json.loads((CLAUDE_REPORTING_PLUGIN_ROOT / ".mcp.json").read_text())
    skill = (CLAUDE_REPORTING_PLUGIN_ROOT / "skills/iridium-reporting/SKILL.md").read_text()
    setup = (CLAUDE_REPORTING_PLUGIN_ROOT / "resources/setup.md").read_text()
    privacy = (CLAUDE_REPORTING_PLUGIN_ROOT / "resources/privacy.md").read_text()
    all_text = plugin_text_assets(CLAUDE_REPORTING_PLUGIN_ROOT)

    assert manifest["name"] == "iridium-reporting-claude"
    assert manifest["version"] == "1.0.0"
    assert manifest["repository"] == "https://github.com/Jdashford/iridium-claude-plugin"
    assert manifest["skills"] == "./skills/"
    assert manifest["mcpServers"] == "./.mcp.json"
    assert mcp["mcpServers"]["iridium_reporting"]["type"] == "http"
    assert mcp["mcpServers"]["iridium_reporting"]["url"] == "https://connect.iridiumai.co/mcp"
    assert "resolve_reporting_scope" in skill
    assert "ask_business_report" in skill
    assert "prepare_business_report_context" in skill
    assert "Claude Code" in skill
    assert "open `/mcp`, select the `iridium_reporting` server" in skill
    assert "ask_advisor" not in skill
    assert "Iridium Reporting for Claude" in setup
    assert "Select `iridium_reporting`" in setup
    assert "Choose **Authenticate**" in setup
    assert "Paste the setup code only into the Iridium sign-in page" in setup
    assert "Do not paste it into Claude Code chat" in setup
    assert "contains no private account data" in privacy
    assert "connect.iridium.ai" not in all_text
    assert "https://iridium.ai" not in all_text
    assert "Railway" not in all_text
    assert "up.railway.app" not in all_text
    assert "sha256:" not in all_text
    assert "agent_client_id" not in all_text
    assert "setup_link_id" not in all_text
    assert "client_secret" not in all_text


def test_iridium_reporting_codex_plugin_has_separate_identity_and_no_private_data():
    manifest = json.loads((REPORTING_PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text())
    mcp = json.loads((REPORTING_PLUGIN_ROOT / ".mcp.json").read_text())
    skill = (REPORTING_PLUGIN_ROOT / "skills/iridium-reporting/SKILL.md").read_text()
    all_text = plugin_text_assets(REPORTING_PLUGIN_ROOT)

    assert manifest["name"] == "iridium-reporting-codex"
    assert manifest["version"] == "1.0.1"
    assert manifest["repository"] == "https://github.com/Jdashford/iridium-codex-plugin"
    assert manifest["interface"]["displayName"] == "Iridium Reporting for Codex"
    assert manifest["mcpServers"] == "./.mcp.json"
    assert manifest["skills"] == "./skills/"
    assert mcp["mcpServers"]["iridium_reporting"]["url"] == "https://connect.iridiumai.co/mcp"
    assert "resolve_reporting_scope" in skill
    assert "ask_business_report" in skill
    assert "prepare_business_report_context" in skill
    assert "tool discovery" in skill
    assert "tool_search" in skill
    assert "before starting OAuth login" in skill
    assert "codex mcp login iridium_reporting" in skill
    assert "ask_advisor" not in skill
    assert "Railway" not in all_text
    assert "up.railway.app" not in all_text
    assert "connection code" not in all_text.lower()
    assert "secret" not in all_text.lower()
