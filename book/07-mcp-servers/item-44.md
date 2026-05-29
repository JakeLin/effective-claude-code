---
item: 44
theme: mcp-servers
title: "Install fewer servers than you think you need"
tags: [mcp, restraint, context, curation]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [43, 47, 48]
things_to_remember:
  - "Every connected server costs context, attention, and trust surface — more servers does not mean more capability, it means more overhead"
  - "Most people who install many servers end up using a handful; install for what you actually do, not what you might someday do"
  - "A bloated tool list makes Claude slower to pick the right tool and dilutes the ones that matter"
  - "Periodically prune servers you stopped using — an idle server is pure cost with no benefit"
agent_steps:
  - "Connect only the servers the current work actually needs; do not pre-install servers speculatively"
  - "When tempted to add a server, confirm there's a concrete, recurring task that needs it"
  - "Review connected servers periodically and remove any not used in recent work"
  - "Prefer a few well-chosen servers over a large catalog — the marginal server usually adds cost without adding value"
---

## Why this matters

The instinct with MCP is to collect servers — there's one for every system, they're easy to add, and more tools feels like more power. It isn't. A widely-repeated experience from practitioners captures it: *"Went overboard with 15 MCP servers thinking more = better. Ended up using only 4 daily."* The other eleven weren't helping; they were sitting in the session as overhead. Every connected server costs three things whether or not you use it — context, attention, and trust surface — and those costs are real even when the benefit is zero.

The context cost is mechanical. Each server contributes tool definitions, and the listing of available tools is something Claude carries each turn. A sprawling catalog crowds the context window with capabilities you're not using and makes the model slower and less accurate at picking the *right* tool from the pile. The signal you want — the four servers you actually reach for — gets diluted by the eleven you don't. Fewer, well-chosen servers leave more room for the actual conversation and make tool selection sharper.

The attention and trust costs compound it. Every server is code you've chosen to run and an output channel you've chosen to trust (a theme the security Items in this chapter return to). An idle server you installed "just in case" gives you nothing back for that standing exposure. The discipline is the same one good engineers apply to dependencies: add when there's a concrete, recurring need; prune when the need passes. The marginal server almost always adds cost without adding value, so the default answer to "should I install this one too?" should lean toward no.

## What to avoid

Pre-installing servers speculatively — "I might need a browser one, a database one, a docs one, a diagramming one…" — before any concrete task calls for them. Equating a large server catalog with greater capability. Leaving servers connected long after the work that needed them is done. Adding a server because it exists and looks interesting, rather than because a recurring task requires it.

## What to do instead

Install for what you actually do. When you're tempted to add a server, name the concrete, recurring task that needs it; if you can't, don't add it yet. Keep the connected set small and let it track your real work. Review it periodically and remove servers you haven't used recently — an idle server is pure cost. Treat a few well-chosen servers as the goal, not a comprehensive catalog, because the catalog you don't use is the overhead you pay for nothing.

## Example

The pattern almost everyone reports, made concrete:

```text
Installed (the "more = better" phase):
  context7, playwright, chrome, deepwiki, excalidraw,
  postgres, github, slack, jira, sentry, figma,
  notion, linear, aws, gdrive          (15 servers)

Actually used day to day:
  context7    — live library docs
  playwright  — UI testing
  github      — issues and PRs
  postgres    — local DB queries     (4 servers)
```

The other eleven sat in every session contributing tool definitions, attention drain, and trust surface, and returning nothing. The fix isn't clever — it's deletion: connect the four you use, drop the rest, and add a server back only when a real task demands it. A lean set keeps Claude fast at choosing tools and keeps your context spent on work instead of on a catalog you're not touching.
