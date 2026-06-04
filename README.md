# Iridium for Codex

This repository contains the generic Iridium plugin for Codex.

The plugin always connects Codex to the Iridium gateway at `https://connect.iridiumai.co/mcp`. It does not contain customer Railway URLs, setup codes, OAuth tokens, private memories, uploaded documents, advisor prompts, or client names.

## Install

Add this GitHub repository as a trusted Codex plugin marketplace, then install `Iridium for Codex`.

After installation, Codex asks you to connect Iridium. Open the private setup page from your advisor, reveal the one-time connection code, and paste that code only on the Iridium sign-in screen.

If Codex says Iridium is not connected and does not show a sign-in link, run `codex mcp login iridium` and open the Iridium authorization link it prints. Keep the command running until the browser finishes authentication. If the browser ends on `127.0.0.1` with a connection-refused error, start over with a fresh setup code and a newly started login command.

## Contents

- `.agents/plugins/marketplace.json`: Codex marketplace entry.
- `plugins/iridium-codex/.codex-plugin/plugin.json`: plugin manifest.
- `plugins/iridium-codex/.mcp.json`: gateway MCP server configuration.
- `plugins/iridium-codex/skills/iridium-advisor/SKILL.md`: Codex skill guidance for advisor usage.
- `plugins/iridium-codex/resources/`: setup and privacy notes.

## Security

The one-time setup code binds a Codex OAuth connection to the correct account runtime at the gateway. Runtime deployments remain separate and are reached only through authenticated, short-lived gateway service tokens.
