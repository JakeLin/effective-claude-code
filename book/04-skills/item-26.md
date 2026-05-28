---
item: 26
theme: skills
title: "Default to a skill before reaching for an agent or a command"
tags: [skills, agents, commands, choosing]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [8, 14, 15, 16]
things_to_remember:
  - "Resolution preference is skill → agent → command — Claude reaches for the lightest fit first"
  - "Skills run inline (no extra context window) and auto-invoke from `description` — usually the right default"
  - "Promote to an agent when the work needs context isolation, persistent memory, or a different permission mode"
  - "Promote to a command when the workflow must be user-initiated and never auto-fire"
agent_steps:
  - "When authoring a new extension, start with a skill; only promote to an agent or command if the skill form misses a requirement"
  - "Promote to an agent when the work would pollute the main context (large-surface research, autonomous multi-step exploration) or needs a permission mode like `acceptEdits`/`plan`"
  - "Promote to a command when the workflow must only run on explicit user invocation (no auto-discovery, no preload)"
  - "Resist the temptation to write three siblings (skill + agent + command) for the same task — pick the one that fits and ship it"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

Skills, subagents, and commands overlap enough that "which one should this be?" comes up every time you author an extension. The defaults matter because the three mechanisms have different costs and different invocation surfaces. A skill is inline (shares the main context window), auto-invocable via its description, and lightweight — Claude reaches for it without a separate process. A subagent runs in an isolated context with its own model, tools, and permission mode — more powerful, but heavier per invocation. A command is user-initiated only — the slash menu fires it, never the model.

When more than one of these would technically work, Claude prefers the lightest: skill before agent before command. That ordering is also what you want most of the time. A skill auto-invokes on intent match, costs only its description in resident context, and is fully sufficient for anything that doesn't need a separate context window or a different permission posture.

Promotion to agent earns its keep when context isolation is the point — large-surface research that would pollute the main thread, autonomous multi-step work that benefits from its own reasoning context, or anything that needs persistent memory, a permission mode like `acceptEdits` or `plan`, or its own MCP server scope. Promotion to a command is right when the workflow must never auto-fire — user-initiated entry points to orchestrations, things you only want triggered when the user types the slash.

The failure mode is going straight to agent or command for tasks where a skill would have done the job. An agent for every recurring helper produces a fleet of subagents that each cost a turn to invoke and reconcile. A command for every helper turns the slash menu into clutter no one remembers. Default to a skill; promote only when the skill form clearly misses.

## What to avoid

Writing a custom agent for every recurring task. Writing a command for things Claude should reach for on its own. Authoring all three siblings (skill + agent + command) for the same job, because the team couldn't decide — that triples the maintenance and confuses the routing.

## What to do instead

Start every new extension as a skill. Ship it. If, in practice, you find the skill form is missing something concrete — context isolation, a different permission mode, persistent memory, an entry point that must require explicit user invocation — promote it. Otherwise, leave it alone.

When in doubt: skill if Claude should reach for it; agent if the work needs a separate brain; command if only the user should ever trigger it.

## Example

A "find ownership" task. Three siblings — overkill.

```
.claude/skills/find-ownership/SKILL.md       # auto-invocable
.claude/agents/ownership-finder.md           # subagent for the same thing
.claude/commands/ownership.md                # /ownership for the same thing
```

The same task, picked correctly — a skill is sufficient.

```yaml
---
name: find-ownership
description: Use when the user asks who owns a file, module, or feature. Searches CODEOWNERS, recent commits, and OWNER comments. Returns team/person and reasoning.
allowed-tools: Read, Grep, Glob
model: haiku
---
```

When promotion is right — a "babysit PRs" workflow that must run autonomously with its own context, tool scope, and a watchful loop:

```yaml
---
name: pr-babysitter
description: Use PROACTIVELY when monitoring an open PR for CI failures and review comments. Investigates each event, pushes fixes for tractable failures, escalates ambiguous ones.
tools: Read, Edit, Bash, Agent(Explore)
model: sonnet
permissionMode: acceptEdits
memory: project
---
```

The PR babysitter needs an isolated context (events arrive over time), a permission mode (`acceptEdits` so the loop doesn't stall), and its own memory. A skill couldn't carry that. An agent can.
