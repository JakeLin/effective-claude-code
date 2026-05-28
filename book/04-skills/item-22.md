---
item: 22
theme: skills
title: "Treat a skill as a folder, not a markdown file"
tags: [skills, structure, progressive-disclosure]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: []
things_to_remember:
  - "A skill is a folder — `SKILL.md` is the entry point, but supporting files are where the leverage compounds"
  - "Split long reference material into sibling files (`references/api.md`, `examples/`, `gotchas.md`) and point to them from `SKILL.md`"
  - "Ship scripts in the skill folder when a deterministic step is better than asking Claude to reason it out"
  - "`SKILL.md` and the description always load; supporting files load only when Claude reads them — use that for progressive disclosure"
agent_steps:
  - "When authoring a skill, keep `SKILL.md` short and reference long-form material in sibling files rather than inlining it"
  - "Place deterministic helpers (validators, parsers, generators) as scripts in the skill folder and invoke them from `SKILL.md`"
  - "For skills that need user-specific setup, store the configuration in `config.json` in the skill folder and read it at invocation time"
---

## Why this matters

The common misread of skills is that they're "just markdown files." They're not — they're folders, and that distinction is where most of the leverage lives. The `SKILL.md` file is the entry point Claude sees when invoking, but the folder around it can contain reference docs, example code, scripts, configuration files, and data. Claude reads what it needs, when it needs it. The folder is the context-engineering surface.

This matters because skill descriptions and `SKILL.md` content count against the session context budget. The character budget for skill listings is finite (15,000 by default), and skills that try to inline a complete reference manual into `SKILL.md` either run into that limit or push useful content out of context. A skill structured as a folder — short `SKILL.md`, deeper material in sibling files referenced by path — loads only the entry point at session start and the deeper material only when Claude actually needs it. That's progressive disclosure, and it's how skills scale past trivial cases.

The second leverage point is scripts. Claude is great at composing behavior and weaker at reconstructing boilerplate. A skill that ships a `scripts/validate.py` or `scripts/render.sh` lets Claude spend its turns on the parts that actually need reasoning. The script is deterministic; Claude calls it and reasons about the output. The same approach works for templates, schemas, and any reference data the skill keeps consulting — keep them as files Claude can read, not strings Claude has to memorize.

## What to avoid

`SKILL.md` files that grow into thousand-line reference manuals. Skills that paste API tables, framework conventions, or long example code blocks into the main body — that material always loads, even on sessions where the skill never gets invoked. Skills that ask Claude to re-derive boilerplate every time when a shipped script would have produced it deterministically.

## What to do instead

Keep `SKILL.md` short — what the skill is for, when to invoke, the goal and constraints, and pointers to where the long material lives. Put reference content in sibling files (`references/api.md`, `examples/`, `gotchas.md`) and tell Claude in `SKILL.md` that they exist. Put deterministic logic in scripts inside the folder and have Claude invoke them. If the skill needs user-specific setup, store it in `config.json` and read it at invocation time; if the config is missing, prompt the user.

## Example

A flat skill — works but doesn't scale.

```
.claude/skills/billing-lib/
└── SKILL.md          # 800 lines of frontmatter, API reference,
                      #   example queries, gotchas, schema dump
```

A folder-shaped skill — same content, but Claude loads only what it needs.

```
.claude/skills/billing-lib/
├── SKILL.md                    # ~80 lines: when to invoke, goal,
│                               #   pointers to references/scripts
├── references/
│   ├── api.md                  # Function signatures, parameters
│   ├── schema.md               # Table layouts
│   └── gotchas.md              # Non-obvious failure modes
├── examples/
│   ├── revenue-by-cohort.sql
│   └── refunds-last-30d.sql
└── scripts/
    └── validate-query.py       # Deterministic linter for queries
```

The `SKILL.md` itself ends up looking like a table of contents:

```markdown
---
name: billing-lib
description: Use when working with the billing data warehouse. Knows the schema, the canonical queries, and the gotchas that bite first-timers.
---

# Billing Lib

For schema lookups, read `references/schema.md`.
For canonical query patterns, see `examples/*.sql`.
For known footguns (timezone columns, soft-deleted rows, etc.),
always check `references/gotchas.md` before writing a new query.
Before executing any query, run `scripts/validate-query.py` against it.
```

Same surface area; far less always-on context cost.
