---
item: 27
theme: skills
title: "Preload skills into the subagents that need them; fork to a subagent only when context isolation is the point"
tags: [skills, subagents, composition, fork]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [15, 16, 19]
things_to_remember:
  - "`skills:` on an agent preloads full skill content at startup — bake domain knowledge into a specialized agent"
  - "`context: fork` on a skill runs the skill in an isolated subagent context — use when the skill's intermediate work shouldn't pollute the main thread"
  - "Preload is for knowledge an agent always needs; fork is for runtime context isolation"
  - "Don't fork by default — inline skills are cheaper and keep results in the main reasoning context"
agent_steps:
  - "When a custom subagent has a recurring knowledge dependency, list the skill under `skills:` in the agent's frontmatter so it loads at agent startup"
  - "Use `context: fork` on a skill when its work would dump significant tool output into the main thread (large research, doc reading)"
  - "When forking, set `agent: Explore` or `agent: Plan` for read-only forks — they skip CLAUDE.md to keep context small"
  - "Audit `context: fork` usage: if the skill's result is short and the parent immediately reasons about it, the fork is probably wasted overhead"
---

## Why this matters

Skills and subagents compose in two different ways, and the difference matters because they solve different problems. The `skills:` field on a subagent preloads full skill content into that agent's context at startup — the agent is born already knowing the domain. The `context: fork` field on a skill flips it around: the skill itself runs in a fresh subagent context, with its body becoming the subagent's prompt. Same components, different direction of composition.

Preloading is the right pattern when you have a specialized agent that *always* needs a given body of knowledge to do its job. A `migration-author` agent that should know the team's migration checklist on every invocation, a `frontend-reviewer` agent that should always have the design conventions in context. Putting the skill name in `skills:` injects the full content at agent startup so the agent doesn't have to remember to read it.

Forking is the right pattern when a skill's *work* would otherwise pollute the main thread — large-surface research, reading many files, generating long intermediate output that the main thread doesn't need after the skill returns. The fork is a context firewall (same principle as Item 15) applied at the skill level: the skill does its work in a child, returns a short result, and the noise stays out of the parent. Choosing `agent: Explore` or `agent: Plan` for the fork is the cheap option — those subagents skip CLAUDE.md to keep the forked context small.

The mistake is reaching for fork by default. A skill that runs inline shares the main context window — its result is already in the parent's reasoning context, no reconciliation needed. Forking adds overhead (a separate subagent process, the briefing cost, the return summarization step). It earns its keep only when the inline version would meaningfully bloat the main thread. For most skills — short bodies, small returns — inline is the right choice.

## What to avoid

Setting `context: fork` on every skill because "isolated is better." Listing every skill in an agent's `skills:` field whether the agent needs them or not (each preload counts against the agent's context budget from turn zero). Authoring a skill that's purely a thin wrapper around forking to a subagent — the subagent could have been the unit of composition in the first place.

## What to do instead

For custom subagents, list under `skills:` only the skills the agent genuinely needs every time. Skills that the agent might invoke situationally don't need preloading — Claude can reach for them via the normal Skill tool.

For skills, default to inline. Reach for `context: fork` when the skill does large-surface work whose intermediate output the parent shouldn't see. When forking, prefer `agent: Explore` for read-only research and `agent: Plan` for design work, since those skip CLAUDE.md and keep the forked context lean.

## Example

Preload — agent always needs this knowledge.

```yaml
---
name: migration-author
description: Use when the user is writing a database migration. Generates the migration, the rollback, and runs the team's safety checklist.
tools: Read, Write, Edit, Bash(npm run validate-migration:*)
model: sonnet
skills:
  - migration-checklist
  - schema-conventions
---

You author database migrations for this codebase. Follow the
preloaded checklist and conventions. ...
```

The two skills load at agent startup; the agent never has to re-fetch them.

Fork — skill does heavy work; isolate it.

```yaml
---
name: dependency-audit
description: Use when the user asks whether a dependency upgrade is safe. Reads every call site, checks for breaking changes in the changelog, returns a yes/no with reasoning.
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, WebFetch
---

You are auditing a proposed dependency upgrade. ...
```

The skill reads many call sites and may fetch changelogs — the kind of work whose intermediate state shouldn't live in the main thread. Forking to `Explore` keeps the parent's context clean and the audit's reasoning isolated.

Inline (default) — skill does small work; share the main context.

```yaml
---
name: find-ownership
description: Use when the user asks who owns a file or module.
allowed-tools: Read, Grep, Glob
---

...
```

Result is short and the parent will reason about it immediately — no fork needed.
