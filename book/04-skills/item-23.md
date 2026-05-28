---
item: 23
theme: skills
title: "Write `description` for the router; use `disable-model-invocation` when auto-invocation is wrong"
tags: [skills, description, routing, auto-invocation]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [18]
things_to_remember:
  - "`description` is the routing rule — it tells Claude *when* to invoke, not *what* the skill is"
  - "Name the trigger explicitly: 'Use when X', 'Use when the user asks for Y' — vague descriptions never fire"
  - "Set `disable-model-invocation: true` for destructive or expensive skills you want users to invoke deliberately"
  - "Set `user-invocable: false` for background knowledge that should never appear in the `/` menu"
agent_steps:
  - "When authoring a skill, write the `description` as a trigger criterion ('Use when…'), not a label"
  - "For destructive skills (deploys, drops, force-pushes), set `disable-model-invocation: true` so they only fire on explicit user invocation"
  - "For skills that exist purely as background knowledge for Claude, set `user-invocable: false` to hide them from the `/` menu"
  - "Audit existing skills: if Claude never auto-invokes one, rewrite the description as a trigger criterion before assuming the skill is broken"
---

## Why this matters

A skill's `description` is the line Claude reads when deciding "is there a skill for this request?" It's not documentation; it's a routing rule. The harness builds a listing of every available skill with its description at session start, and that listing is what gets scanned against each new user intent. If the description reads like a label — "Billing query helper" — there's no signal about when this skill applies versus the dozen other things that mention queries. The skill sits in the listing, costs context, and never fires.

A description that works names the triggering situation. "Use when the user asks to write a SQL query against the billing warehouse." "Use when generating or modifying a database migration." The verb forms matter: imperative, situation-specific, ideally pointing to user phrasings or task shapes. Treat it like the docstring you'd write so a teammate could tell, from one line, whether to reach for this skill or a different one.

The auto-invocation surface has two safety valves. `disable-model-invocation: true` means Claude cannot invoke the skill on its own — only `/skill-name` will fire it. Use this for skills that do something destructive or expensive: deployments, table drops, force-pushes, long-running data jobs. The wrong skill auto-firing on a near-miss intent is much more dangerous when the skill writes to production than when it reads a schema. `user-invocable: false` is the inverse: the skill stays available to Claude (for auto-invocation or as background knowledge) but is hidden from the `/` menu. Use it for skills that aren't meant to be triggered by a user typing slash at all — internal scaffolding, knowledge bases, things Claude reaches for but the user shouldn't.

## What to avoid

`description: "Database helper"` — Claude has no way to know when to pick it. `description: "Skill for managing migrations"` — no trigger, no situation. Leaving `disable-model-invocation` off on a skill that runs `terraform apply` against prod. Hiding skills with `user-invocable: false` when the user actually needs to invoke them, then wondering why the slash menu is empty.

## What to do instead

Write descriptions that read like router rules. "Use when X happens" or "Use when the user asks for Y." Include the user phrasings or task shapes that should trigger it. Audit skills that you authored months ago but never see auto-invoke — the description is almost always the bug.

Reserve `disable-model-invocation: true` for skills where the cost of a wrong auto-invocation is real. Reserve `user-invocable: false` for skills that exist only as background knowledge or only as targets of other skills/agents.

## Example

Weak — Claude won't route.

```yaml
---
name: db-migration
description: Database migration utilities.
---
```

Strong — names the trigger.

```yaml
---
name: db-migration
description: Use when the user is writing, reviewing, or running a database migration. Generates the migration file, the paired rollback, and validates schema safety against the team's checklist (NOT NULL adds, missing indexes, large-table backfills).
---
```

Destructive skill that should never auto-fire:

```yaml
---
name: deploy-prod
description: Use when the user explicitly asks to deploy to production. Runs the deploy pipeline, watches metrics for 5 minutes, and rolls back on regression.
disable-model-invocation: true
---
```

Background-knowledge skill that shouldn't clutter the `/` menu:

```yaml
---
name: internal-billing-schema
description: Use when constructing queries or migrations that touch billing tables. Provides the schema, the soft-delete conventions, and the timezone gotchas.
user-invocable: false
---
```

The two toggles are independent. Together they cover the full matrix: anyone-can-invoke, user-only, Claude-only, neither (which is just dead config).
