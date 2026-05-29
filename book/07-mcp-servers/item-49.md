---
item: 49
theme: mcp-servers
title: "Govern MCP access with permission rules and managed allowlists"
tags: [mcp, permissions, governance, enterprise, security]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [38, 39, 40, 48]
things_to_remember:
  - "MCP tools use the `mcp__<server>__<tool>` naming convention, so the same allow/ask/deny permission rules govern them"
  - "Scope MCP permissions per server and per tool — allow the safe read-only tools, leave or deny the ones that act"
  - "Control which project servers connect with `enableAllProjectMcpServers`, `enabledMcpjsonServers`, and `disabledMcpjsonServers`"
  - "For organizations, managed settings (`allowedMcpServers`, `deniedMcpServers`, `allowManagedMcpServersOnly`) enforce which servers are usable at all"
agent_steps:
  - "Write MCP permission rules with the `mcp__server__tool` pattern: allow safe tools (e.g., `mcp__context7__*`), deny or leave-to-prompt the ones that take action"
  - "Avoid a blanket `mcp__*` allow when any connected server can take consequential action; scope per server instead"
  - "Use enabledMcpjsonServers / disabledMcpjsonServers to control which project-scoped servers auto-connect rather than enabling all blindly"
  - "In managed environments, set allowedMcpServers / deniedMcpServers (and allowManagedMcpServersOnly to lock the set) to enforce org policy"
---

## Why this matters

The distrust from the previous Item only matters if it's enforceable, and MCP plugs directly into the permission system to make it so. MCP tools are named `mcp__<server>__<tool>` — a stable, structured convention — which means the same `allow` / `ask` / `deny` machinery that governs Bash and file tools governs MCP tools too. Everything from the permissions chapter applies: deny wins over allow across every layer, rules are scoped specifiers, and a curated allowlist removes friction on the safe operations while leaving the consequential ones to prompt. MCP isn't a separate trust domain; it's the same one, addressed with the same rules.

That structure invites the same discipline as any allowlist: scope per server and per tool rather than reaching for a blanket grant. A read-only docs server is safe to allow wholesale — `mcp__context7__*` costs you nothing in risk. A server that can write to a database, send messages, or take other real-world actions is not; allowing all of its tools is the MCP equivalent of `Bash(*)`. The fine-grained naming lets you allow the snapshot-and-read tools while leaving the act-on-the-world tools to prompt, or denying a server you connected but don't trust to run unattended. A broad `mcp__*` allow across a mix of servers throws that precision away exactly where the acting tools make it most dangerous.

Above individual permission rules sit two more controls. Which project-scoped servers connect at all is governed by `enableAllProjectMcpServers`, `enabledMcpjsonServers`, and `disabledMcpjsonServers` — the difference between blindly trusting every server a repo declares and approving a named set. And for organizations, managed settings raise this to enforceable policy: `allowedMcpServers` and `deniedMcpServers` define which servers may be used regardless of what a user or repo configures, and `allowManagedMcpServersOnly` locks the set so only org-sanctioned servers connect. These are the same idea at three altitudes — per-tool rules, per-project server gating, and org-wide policy — each making the trust decision concrete instead of implicit.

## What to avoid

A blanket `mcp__*` allow when some connected server can take consequential action — it auto-approves the dangerous tools along with the safe ones. Setting `enableAllProjectMcpServers` to auto-connect every server a repo declares without reviewing them. Relying only on the intent to "be careful" with an untrusted server instead of encoding a `deny` rule. In an org, leaving server choice entirely to users when policy requires a sanctioned set.

## What to do instead

Govern MCP with the permission system, scoped. Allow the safe, read-only tools by server (`mcp__docs-server__*`), and leave or explicitly deny the tools that act. Skip the blanket `mcp__*` grant wherever a connected server can do something consequential. Gate which project servers connect with `enabledMcpjsonServers` / `disabledMcpjsonServers` rather than enabling all of them blindly. And in managed environments, enforce the sanctioned set with `allowedMcpServers`, `deniedMcpServers`, and `allowManagedMcpServersOnly`, so org policy holds regardless of local config.

## Example

Per-tool permission rules — allow the safe, gate the rest:

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__*",
      "mcp__playwright__browser_snapshot"
    ],
    "deny": [
      "mcp__untrusted-server__*"
    ]
  }
}
```

The read-only docs server is allowed wholesale; only `browser_snapshot` is pre-approved on the browser server, so its navigating and acting tools still prompt; the server you don't trust is denied outright. Note what's absent — a blanket `mcp__*` — because that would auto-approve every acting tool too.

Project-server gating — connect a named set, not everything:

```json
{
  "enabledMcpjsonServers": ["context7", "playwright"],
  "disabledMcpjsonServers": ["experimental-server"]
}
```

Org-wide enforcement via managed settings — policy that local config can't override:

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverUrl": "https://mcp.company.com/*" }
  ],
  "deniedMcpServers": [{ "serverName": "dangerous-server" }],
  "allowManagedMcpServersOnly": true
}
```

With `allowManagedMcpServersOnly`, only the sanctioned servers connect no matter what a user or repo declares. The three layers — per-tool rules, per-project gating, managed policy — turn the "treat servers as untrusted" principle into boundaries the harness actually enforces, which is the point: a trust decision you can't enforce is just a hope.
