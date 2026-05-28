---
item: 18
theme: subagents
title: "Write the `description` field so Claude routes work to the right agent"
tags: [subagents, description, routing, auto-invocation]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [16]
things_to_remember:
  - "`description` is what the harness reads to decide which agent fits a task — write it as routing copy, not a label"
  - "Name the triggers explicitly: 'Use when X', 'Use PROACTIVELY when Y' — vague descriptions get bypassed"
  - "Auto-invocation only fires when the description's triggers are unambiguous and the keyword `PROACTIVELY` is present"
  - "If you find yourself manually invoking your own subagent by name, the description is too weak"
agent_steps:
  - "Write `description` as routing copy: name the triggering situation, what the agent does, and what it returns — not a bare label"
  - "State triggers explicitly with 'Use when X'; add the keyword `PROACTIVELY` only when Claude should reach for the agent unprompted"
  - "Add a scope-narrowing clause ('Do NOT use for ...') when the agent must stay in its lane"
  - "Update the description in the same edit whenever you change the agent's responsibilities"
  - "If you catch yourself invoking your own subagent by name, rewrite the description — it's too weak to route on"
ecc_meta:
  target: agents
  action: fix
  check: ".claude/agents/ exists — review description fields for vague or missing routing triggers"
---

## Why this matters

`description` is not documentation. It's the field the harness reads when Claude is deciding whether to delegate a piece of work to your subagent. If it says "An agent for handling database stuff," Claude will not route to it — there's no signal about *when* this agent applies versus the dozen other things that mention databases. The agent will sit unused, and the team will conclude subagents don't help, when actually the routing rule was unwritable.

A description that works treats itself like a router rule. It names the triggering situations explicitly: "Use this agent when reviewing a migration PR." "Use PROACTIVELY when running database migrations against production schemas." The presence of concrete triggers — and the keyword `PROACTIVELY` for cases where Claude should reach for the agent without being asked — is the difference between an agent that gets invoked and one that gathers dust.

The same applies to the inverse case. A description that's too broad ("Use for any code question") will get routed to when it shouldn't, swallowing tasks the built-ins would handle better. It's the same discipline as writing a good function signature: state precisely when this thing should be called and what it returns.

## What to avoid

`description: "Database helper agent"` — Claude has no way to know when to pick it. `description: "Handles all backend code"` — too broad; will get invoked for things it isn't tuned for. Descriptions that read like an internal note ("Our team's preferred migration auditor") rather than routing criteria.

## What to do instead

Write the description so a stranger reading just that line knows exactly when this agent is the right choice. Include the trigger context, what the agent does, and — if relevant — what it returns. Use `PROACTIVELY` only when you genuinely want Claude to reach for the agent without being asked; overusing it makes Claude over-delegate.

When you change an agent's responsibilities, update the description in the same edit. Stale routing copy is how you end up with agents being invoked for tasks they're no longer designed to handle.

## Example

Weak — Claude will not route here.

```yaml
---
name: migration-auditor
description: Audits migrations.
---
```

Strong — names the trigger, the action, and the return.

```yaml
---
name: migration-auditor
description: Use this agent PROACTIVELY when reviewing or authoring a database migration PR. It checks for missing indexes, backfill safety on tables over 1M rows, and paired rollback steps, and returns a pass/fail report with line-specific findings.
---
```

A second example showing scope-narrowing language so the agent stays in its lane:

```yaml
---
name: rpc-contract-checker
description: Use when changes touch files under `src/rpc/` or any `.proto` file. Verifies that wire-compatible changes (added fields, deprecated enums) follow the team's compatibility rules. Do NOT use for non-RPC code review.
---
```

The "do NOT use for" clause prevents the agent being pulled into tasks it isn't designed for.
