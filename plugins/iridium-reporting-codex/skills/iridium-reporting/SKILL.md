---
name: iridium-reporting
description: Use when the user asks for account-scoped business reporting, business intelligence, activity analysis, leadership updates, or reporting across agents through Iridium.
---

# Iridium Reporting

Use the authenticated Iridium Reporting MCP tools before answering requests that depend on account business intelligence, agent activity logs, central intelligence, or connected dashboard evidence.

## Workflow

1. If the request targets a person, role, department, team, organization, client, or agent by name, call `resolve_reporting_scope` with the exact scope text and intended scope type before requesting report context.
2. For business reporting requests, call `prepare_business_report_context` or `ask_business_report` before answering. When `resolve_reporting_scope` returns `resolved`, pass its `requested_scope` and `scope_id` into the report request.
3. Keep the report account-scoped. Do not infer beyond the account connected by the Iridium Reporting setup code.
4. Treat returned context as grounding, not as text to expose directly.
5. Write the final answer as business intelligence for leadership: what is becoming true, what changed, what patterns matter, and where a decision may be required.
6. Do not include raw activity entries, private prompts, database rows, hidden instructions, or implementation identifiers unless the user is debugging the system itself.
7. If `resolve_reporting_scope`, `ask_business_report`, and `prepare_business_report_context` are not available in the currently exposed tools, try tool discovery before starting OAuth login:
   - If `tool_search` is available, search for `iridium reporting resolve_reporting_scope ask_business_report MCP`. If discovery exposes the reporting tools, call the right tool and continue this workflow.
   - Treat discovery as loading the authenticated reporting entry point, not as a substitute data search. Do not use advisor memory tools or other Iridium tools as a substitute.
   - If tool discovery is unavailable, or discovery still does not expose the reporting tools, stop. Ask the user to finish Iridium Reporting authentication:
     - If terminal tools are available, run `codex mcp login iridium_reporting` in an interactive shell, capture the printed `https://connect.iridiumai.co/oauth/authorize?...` URL, and show that URL to the user.
     - Leave that login command running while the user opens the URL, enters their one-time setup code, and completes OAuth.
     - If terminal tools are not available, tell the user to run `codex mcp login iridium_reporting` locally and open the Iridium authorization link it prints.
     - If the browser redirects to `127.0.0.1` and says the local page refused the connection, the local Codex login listener was not running. The one-time setup code has likely been consumed, so the user needs a fresh setup code and a newly started login command.
     - After authentication, ask the user to start a new Codex thread with Iridium Reporting for Codex selected if the tools are still missing in the current thread.

## Boundaries

- This plugin is for reporting and analytics only. It is separate from Iridium advisor memory.
- Do not use advisor memory tools for Reporting Agent work.
- Do not save personal memory from this plugin.
- Do not expose raw tool output, hidden instructions, private activity logs, or implementation details to the user.
