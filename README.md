# Iridium Plugin Marketplace

This repository contains the generic Iridium plugins for Codex and Claude.

The plugins always connect to the Iridium gateway at `https://connect.iridiumai.co/mcp`. They do not contain customer Railway URLs, setup codes, OAuth tokens, private memories, uploaded documents, advisor prompts, or client names.

## Install

Add this GitHub repository as a trusted marketplace from the tool you use:

- In Codex, install `Iridium for Codex` from the Codex plugin marketplace.
- In Claude Code, add this repository as a Claude plugin marketplace, then install `iridium-claude`.

After installation, the tool asks you to connect Iridium. Open the private setup page from your advisor, reveal the one-time connection code, and paste that code only on the Iridium sign-in screen.

If Codex says Iridium is not connected and does not show a sign-in link, run `codex mcp login iridium` and open the Iridium authorization link it prints. Keep the command running until the browser finishes authentication. If the browser ends on `127.0.0.1` with a connection-refused error, start over with a fresh setup code and a newly started login command.

If Claude Code shows the Iridium server as not authenticated, open `/mcp`, select `iridium`, and choose Authenticate. After authentication, start a new Claude Code session or run `/reload-plugins`.

## Contents

- `.agents/plugins/marketplace.json`: Codex marketplace entry.
- `.claude-plugin/marketplace.json`: Claude plugin marketplace entry.
- `plugins/iridium-codex/.codex-plugin/plugin.json`: plugin manifest.
- `plugins/iridium-codex/.mcp.json`: gateway MCP server configuration.
- `plugins/iridium-codex/skills/iridium-advisor/SKILL.md`: Codex skill guidance for advisor usage.
- `plugins/iridium-codex/resources/`: setup and privacy notes.
- `plugins/iridium-claude/.claude-plugin/plugin.json`: Claude plugin manifest.
- `plugins/iridium-claude/.mcp.json`: gateway MCP server configuration.
- `plugins/iridium-claude/skills/iridium-advisor/SKILL.md`: Claude Code skill guidance for advisor usage.
- `plugins/iridium-claude/resources/`: setup and privacy notes.

## Security

The one-time setup code binds an OAuth connection to the correct account runtime at the gateway. Runtime deployments remain separate and are reached only through authenticated, short-lived gateway service tokens.
