---
item: 16
theme: subagents
title: "Default to built-in agents before writing your own"
tags: [subagents, built-in, defaults]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [14, 15]
things_to_remember:
  - "Start with the bundled subagents — most real delegations are covered by `Explore`, `Plan`, or `general-purpose`"
  - "`Explore` is read-only and runs on Haiku — fast, cheap, and incapable of accidental writes"
  - "`Plan` is for design work before code: codebase reading plus implementation strategy, no edits"
  - "Write a custom subagent only when the built-ins miss — usually domain tools, MCP scope, or a recurring instruction pattern"
agent_steps:
  - "Before authoring a `.claude/agents/<name>.md`, check whether `Explore`, `Plan`, `general-purpose`, `statusline-setup`, or `claude-code-guide` already fits"
  - "For codebase search and 'where is X used' questions, prefer `Explore` over `general-purpose`"
  - "For 'design how to implement Y' questions before any code is written, prefer `Plan`"
  - "Author a custom subagent only when the built-in either lacks the tools, the MCP servers, or the recurring instructions you'd otherwise repeat in every prompt"
ecc_meta:
  target: conversation
  action: suggest
  check: ".claude/agents/ exists with custom agents — review whether any duplicate built-in Explore, Plan, or general-purpose"
---

## Why this matters

At the Claude Code version verified for this Item, the bundled subagents handle most reasons people delegate. `general-purpose` is the catch-all — full tool list, full model, fine for arbitrary multi-step work. `Explore` is the one most people underuse: read-only, Haiku-backed, optimized for finding things in a codebase and answering "where" questions. `Plan` is read-only too, but oriented at designing an approach before any code gets written. Other bundled agents, such as `statusline-setup` and `claude-code-guide`, cover narrow but real cases. Re-check the current list after Claude Code upgrades; the principle is to exhaust the built-ins before authoring a custom agent.

The temptation is to jump to a custom subagent because "we always do X this way." Custom subagents are real overhead: a markdown file to maintain, a `description` that has to be tuned so the router picks it up, a set of tool restrictions that need to stay current, and a place where instructions can drift out of sync with project conventions. None of that earns its keep if `Explore` would have done the job.

The decision rule is narrow. A custom subagent is justified when one of three is true: it needs project-specific tools or MCP servers the built-ins don't have; it needs to run against a specific scope (a particular directory, a particular branch) with rules the built-ins don't enforce; or it embodies a recurring instruction pattern long enough that writing it into the agent file beats restating it in every prompt. Otherwise, reach for what ships.

## What to avoid

Writing a `code-searcher` subagent that duplicates `Explore`. Writing a `read-only-explorer` that duplicates `Plan`. Authoring custom subagents for one-off use — if you'll invoke it once, the prompt was the agent. Custom subagents that exist mostly to encode "be careful and read files before editing" — that belongs in CLAUDE.md, not a separate process.

## What to do instead

Start every delegation with a built-in. For research and codebase search, `Explore`. For design work that precedes implementation, `Plan`. For arbitrary multi-step work, `general-purpose`. Only when a built-in clearly misses — a project-specific MCP server, a repeated multi-paragraph briefing, a permissioned scope — promote it to a custom subagent in `.claude/agents/`.

When you do write a custom one, use `/agents` to scaffold it. The interactive UI sets the frontmatter fields correctly and prevents the silent-failure mode where a typo in the YAML makes the agent unloadable.

## Example

Reaching for `Explore` before reaching for something custom.

```text
> where do we still construct a `LegacyClient` directly?

Agent(subagent_type="Explore",
      description="Find LegacyClient direct construction",
      prompt="List every site that constructs `LegacyClient` directly
              (not via the factory). Report file:line and the
              surrounding 2 lines of context. Quick search.")
```

A custom subagent only when a built-in genuinely misses.

```yaml
---
name: migration-auditor
description: Use PROACTIVELY when reviewing a database migration PR. Checks for missing indexes, backfill safety on large tables, and rollback steps.
tools: Read, Grep, Bash(psql:*)
model: sonnet
---

You audit database migration PRs against this team's checklist:
1. NOT NULL adds on tables over 1M rows must use a backfill + swap.
2. Every new index must specify CONCURRENTLY.
3. Every migration file must have a paired rollback.
...
```

The custom agent earns its place because the checklist is long, recurring, and specific to this team — restating it in every prompt would be worse than authoring it once.
