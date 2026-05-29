---
item: 47
theme: mcp-servers
title: "Let MCP tools stay deferred; load upfront only what you reach for every turn"
tags: [mcp, context, tool-search, performance]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [44, 48]
things_to_remember:
  - "By default MCP tool definitions are deferred — names load at startup, full schemas load on demand via tool search — keeping context lean"
  - "Don't disable deferral wholesale; loading every tool upfront spends context on schemas you mostly won't use that turn"
  - "Use `alwaysLoad` only for the small set of tools you genuinely need every turn, where on-demand lookup would be pure latency"
  - "Deferral is what lets you keep useful servers connected without paying their full context cost continuously"
agent_steps:
  - "Leave MCP tool deferral on (the default) so tool schemas load on demand rather than all upfront"
  - "Reserve `alwaysLoad: true` for the few tools used on essentially every turn, not for whole servers by default"
  - "If many tools are loading upfront and crowding context, check for `alwaysLoad` flags or a disabled tool-search setting and tighten them"
  - "Treat each upfront-loaded tool as standing context cost and justify it against how often it's actually called"
---

## Why this matters

A server can expose many tools, and each tool's full schema — names, parameters, descriptions — is not free to keep in context. Claude Code's default handles this with *deferral*: at session start only the lightweight tool *names* are loaded, and the full definition for a given tool is fetched on demand, through a tool-search step, when Claude actually needs it. The effect is that you can keep genuinely useful servers connected without their entire tool surface sitting in the context window every turn. Deferral is the mechanism that makes a curated set of servers affordable.

The temptation is to turn deferral off — load everything upfront so nothing has to be looked up. That trades a small, occasional latency (the on-demand fetch) for a large, *continuous* cost (every schema resident in context whether or not it's used this turn). On a session with several servers, that's a lot of window spent describing tools Claude won't touch, which is exactly the context dilution that makes tool selection slower and leaves less room for the actual work. The default is the default because, across most sessions, deferred-and-fetched beats resident-and-idle.

The escape hatch should be narrow, not wholesale. A handful of tools really are called nearly every turn — and for those, the on-demand lookup is pure repeated latency with no upside. Marking *those specific tools* (or the rare server whose tools are all hot) to always load is reasonable; it pays a known, small context cost for tools you'd fetch constantly anyway. What's not reasonable is exempting everything from deferral by reflex. The discipline mirrors the restraint Item: just as you connect only the servers you use, you keep resident only the tools you reach for every turn, and let everything else load when — and only when — it's actually needed.

## What to avoid

Disabling tool search / deferral globally so every connected tool's schema loads upfront, spending context continuously on tools you rarely call. Slapping `alwaysLoad` on whole servers as a default rather than reserving it for genuinely hot tools. Treating the small on-demand fetch latency as a problem worth solving by loading everything. Connecting many servers *and* forcing them all resident — the two mistakes compound into a context window that's mostly tool definitions.

## What to do instead

Leave deferral on. Let tool names load at startup and full schemas load on demand — that's the configuration that keeps context lean while still giving Claude access to everything connected. Reserve `alwaysLoad` for the few tools you call on essentially every turn, where repeated lookup would just be latency. If you notice context crowded with tool definitions, look for `alwaysLoad` flags or a disabled tool-search setting and tighten them. Justify every upfront-loaded tool the way you'd justify a connected server: against how often it's actually used.

## Example

The default — deferred, lean by design — needs no configuration; tool names load at startup and schemas are fetched when Claude reaches for a tool.

The narrow, justified exemption — one tool that's called every turn:

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

Use this only when `remote-api`'s tools are genuinely hot — fetched so often that on-demand lookup is pure repeated latency. The cost is real: every tool from that server is now resident in context for the whole session.

Contrast the anti-pattern — forcing *everything* resident:

```text
8 servers connected, all with alwaysLoad (or tool search disabled)
  → every tool's full schema sits in context every turn
  → most are never called this session
  → tool selection is slower, and the window is crowded with
    descriptions instead of available for the actual task
```

The lean default plus a couple of justified `alwaysLoad` tools beats the everything-resident setup in almost every session. Keep deferred what you don't reach for constantly, and the context you save goes back into the work.
