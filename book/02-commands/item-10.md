---
item: 10
theme: commands
title: "Use `/context` and `/usage` as routine telemetry, not as a fire drill"
tags: [commands, context, cost, observability]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [4, 8, 9]
things_to_remember:
  - "Check `/context` early in a long task — see what's filling context before you're forced to `/compact`"
  - "`/usage` shows session cost and plan usage; check before launching another expensive operation"
  - "`/context` flags context-heavy tools, memory bloat, and capacity warnings — read the warnings"
  - "`/insights` surfaces longer-term patterns across sessions when something feels off generally"
agent_steps:
  - "When the user starts a long-running task or context appears to be filling, suggest `/context` so they see what's loaded before it becomes a problem"
  - "Before launching multiple parallel agents or a long-running operation, suggest checking `/usage` to know what budget remains"
  - "If `/context` shows a single tool result dominating, name the call and propose a less verbose alternative (paginate, summarize, narrower glob)"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

`/context` and `/usage` are diagnostic commands most users only learn after they've been bitten — context filled mid-task and forced an awkward `/compact`, or a plan budget got eaten by a session that ran longer than expected. Used proactively, they're routine telemetry that makes the awkward outcomes preventable.

`/context` visualizes current context as a grid: how much is in use, what's filling it (CLAUDE.md, MCP tool results, memory, conversation history), and warnings about specific tools or files that dominate. The grid usually has a single offender — a tool result much larger than the rest, a CLAUDE.md import you forgot, a verbose MCP server. Spotting that early means you adjust before it forces a compact.

`/usage` (aliases `/cost`, `/stats`) shows session cost and plan limits. It's most useful right before you commit to something expensive — spawning multiple subagents, running a long verification, launching an `/ultrareview`. Five seconds of `/usage` prevents the "why did this session eat my whole plan?" moment.

`/insights` is the longer-horizon version: it analyzes recent sessions for patterns, friction points, and where time goes. Useful when something feels generally off but no single session explains it.

## What to avoid

Treating these as debug commands you reach for only when something breaks. Ignoring the warnings in `/context` (they're real signals about specific tools or files). Launching expensive operations without a quick `/usage` check first. Letting context fill silently until `/compact` is forced — `/compact` under pressure produces worse summaries than `/compact` you chose to run with focus instructions.

## What to do instead

Build a quick checkpoint habit at natural pause points: when a task ends, when you're about to switch context, when you're about to spawn agents. A two-second `/context` or `/usage` glance gives you information the rest of the session relies on. When `/context` flags a problem, act on it immediately — name the culprit, swap it for something smaller, or `/compact` deliberately rather than waiting.

## Example

A telemetry check before launching expensive parallel work.

```text
> /context

Context: 42% used
  Conversation: 18%
  Tool results:  16%   ← warning: 9% from a single MCP query
  CLAUDE.md:      4%
  Memory:         3%
  Agents/skills:  1%

> /usage

Session: $1.84  •  Plan: 38% used  •  31 turns
```

```text
> /context

Context: 81% used
  Tool results:  52%   ← warning: large playwright trace
  Conversation: 22%
  …

> /compact keep the bug repro and the fix attempt; drop the playwright traces
```
