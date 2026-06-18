import json
from pathlib import Path


PLUGIN_ROOT = Path("plugins/iridium-codex")
REPORTING_PLUGIN_ROOT = Path("plugins/iridium-reporting-codex")
CLAUDE_PLUGIN_ROOT = Path("plugins/iridium-claude")


def plugin_text_assets(root: Path) -> str:
    return "\n".join(
        path.read_text()
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".json", ".md"}
    )


def test_codex_marketplace_exposes_codex_plugins():
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


def test_claude_marketplace_exposes_claude_plugin():
    marketplace = json.loads(Path(".claude-plugin/marketplace.json").read_text())

    assert marketplace["name"] == "iridium"
    assert marketplace["owner"]["name"] == "Iridium"
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert set(entries) == {"iridium-claude"}
    assert entries["iridium-claude"]["source"] == "./plugins/iridium-claude"
    assert entries["iridium-claude"]["description"] == (
        "Connect Claude Code to your private Iridium advisor memory."
    )
    assert entries["iridium-claude"]["category"] == "productivity"


def test_published_plugins_point_to_gateway_without_private_data():
    plugin_roots = [PLUGIN_ROOT, REPORTING_PLUGIN_ROOT, CLAUDE_PLUGIN_ROOT]

    assert json.loads((PLUGIN_ROOT / ".mcp.json").read_text())["mcpServers"]["iridium"][
        "url"
    ] == "https://connect.iridiumai.co/mcp"
    assert json.loads((REPORTING_PLUGIN_ROOT / ".mcp.json").read_text())["mcpServers"][
        "iridium_reporting"
    ]["url"] == "https://connect.iridiumai.co/mcp"
    assert json.loads((CLAUDE_PLUGIN_ROOT / ".mcp.json").read_text())["mcpServers"]["iridium"][
        "url"
    ] == "https://connect.iridiumai.co/mcp"

    for plugin_root in plugin_roots:
        all_text = plugin_text_assets(plugin_root)
        assert "connect.iridium.ai" not in all_text
        assert "https://iridium.ai" not in all_text
        assert "Railway" not in all_text
        assert "up.railway.app" not in all_text
        assert "connection code" not in all_text.lower()
        assert "client_secret" not in all_text
