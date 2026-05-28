---
item: 19
theme: subagents
title: "Restrict tools and pick the cheapest model that does the job"
tags: [subagents, tools, model, cost, least-privilege]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [13, 16, 66]
things_to_remember:
  - "Subagents inherit every tool by default — narrow `tools` to what the job actually needs"
  - "Read-only agents should be enforced read-only via the tool list, not by hoping the prompt is followed"
  - "Match `model` to the work: Haiku for search and lookups, Sonnet for most code work, Opus only for genuinely hard reasoning"
  - "`effort` overrides session effort for this agent — useful when one delegated step deserves more depth than the rest of the session"
agent_steps:
  - "When authoring a subagent, list the minimum set of tools in `tools:` — start narrow and add only when something fails"
  - "For research, audit, and 'find where X happens' agents, exclude Write, Edit, and Bash from the tool list"
  - "Set `model: haiku` for codebase search and reading-heavy work; reserve `opus` for reasoning-heavy tasks"
  - "Use `effort` to bump a delegated step without raising effort for the whole session"
ecc_meta:
  target: agents
  action: fix
  check: ".claude/agents/ exists — check for missing tools: field or overly broad tool lists"
---

## Why this matters

A subagent inherits every tool the parent has and runs on the parent's model unless you say otherwise. Both defaults are usually wrong for any specific agent. A "research" subagent with access to `Write` and `Bash` is one bad turn away from editing files it was only supposed to read. An `Explore`-style search running on Opus is paying Opus prices for work Haiku does just as well and faster.

The two tuning levers are independent and both matter. Restricting `tools` is least privilege — the agent literally cannot do things it shouldn't, regardless of what the prompt says. Setting `model` matches cost and latency to task complexity — large-surface read-only work is cheap if you let it be. Together they shape the agent into a specialist instead of a smaller copy of the parent.

A third lever, `effort`, exists for the case where the *agent* should think harder than the rest of the session without raising effort everywhere. Useful for delegated steps with high-leverage decisions — design choices, security review, anything where the cost of a shallow answer is high.

## What to avoid

Inheriting all tools on every subagent because the default is permissive. Running every subagent on Opus because you forgot to set `model`. Trusting prompt instructions like "do not edit any files" instead of removing the Edit tool from the agent's list. Setting `effort: max` on every agent — that drains the budget for the cases where it actually matters.

## What to do instead

Start every custom subagent with the narrowest tool list that lets it do the job, and add only when you see it fail for missing capability. For audits, surveys, and search: read-only tools (Read, Grep, Glob) and Haiku. For multi-step code work that needs Edit and Bash: full tools but a model matched to the difficulty — Sonnet for most, Opus when reasoning depth genuinely earns it. Use `effort` to dial up a single agent without dialing up the session.

When in doubt about whether a tool belongs on an agent, leave it off. Adding it later is one line of YAML; recovering from an agent that wrote to the wrong place is not.

## Example

Read-only, cheap, narrow — the right defaults for a search agent.

```yaml
---
name: ownership-finder
description: Use when you need to find the team or person responsible for a given module. Searches CODEOWNERS, recent commit history, and inline TODO/OWNER comments.
tools: Read, Grep, Glob
model: haiku
---
```

Heavier — appropriate for an agent that actually writes code.

```yaml
---
name: migration-author
description: Use when authoring a new database migration. Writes the migration file, the paired rollback, and runs the local validation script.
tools: Read, Write, Edit, Bash(npm run validate-migration:*)
model: sonnet
effort: high
---
```

Note the scoped Bash permission — the agent can run the migration validator but not arbitrary shell. Least privilege is enforced in the config, not in the prose.
