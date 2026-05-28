---
item: 28
theme: skills
title: "Scope each skill where it applies — project, personal, plugin, nested"
tags: [skills, scope, monorepo, plugins, distribution]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [5, 6]
things_to_remember:
  - "Project skills (`.claude/skills/`) are team-shared and version with the repo; personal skills (`~/.claude/skills/`) are yours across projects"
  - "In monorepos, nested `.claude/skills/` under a package load automatically when Claude works in that package's files"
  - "Plugin skills are namespaced (`plugin:skill-name`) — use when distributing across many repos or teams"
  - "Skill descriptions always count against the context budget — don't ship a skill globally if it's only useful in one place"
agent_steps:
  - "Place team-shared skills in `.claude/skills/<name>/` at the repo root and commit them; place your personal skills in `~/.claude/skills/<name>/`"
  - "In a monorepo, put package-specific skills under `packages/<pkg>/.claude/skills/` so they load only when working inside that package"
  - "When the same skill would be useful across many repos under your control, package it as a plugin and distribute via marketplace"
  - "Audit skills periodically: any skill no team member invokes after a month is probably scoped wrong or under-described"
---

## Why this matters

Where a skill lives controls who sees it, when it loads, and how much context budget it consumes. Skill descriptions are always-on — they sit in the session listing whether the skill ever fires or not. A skill scoped too broadly costs every session a little context for the few sessions where it's actually relevant. A skill scoped too narrowly forces people to redefine it everywhere. The four scopes — project, personal, plugin, nested — each fit a different sharing and locality profile.

Project skills (`.claude/skills/<name>/`) version with the repo and ship to every teammate working in it. This is where team conventions live: the migration checklist, the API endpoint style, the local CLI wrappers. Personal skills (`~/.claude/skills/<name>/`) follow you across projects and stay out of the team's repo. This is where personal preferences and cross-cutting helpers live — the `grill-me` skill you use to start every feature, the prompt-format tweaks you like, anything you don't want to impose on others.

In monorepos, the nested-discovery mechanism is the lever that keeps context lean. Skills under `packages/<pkg>/.claude/skills/` are not loaded at session start; they get discovered automatically when Claude touches a file in that package's tree. A frontend developer working in `packages/frontend/` gets the React conventions; a backend developer in `packages/backend/` doesn't pay the context cost for them. This matters more than people expect — in a large monorepo with package-specific conventions across many teams, scoping nested is the difference between a tractable context and one always near the budget limit.

Plugins are the right scope when a skill needs to ship across repos or organizations. Plugin skills are namespaced (`plugin-name:skill-name`), so they don't collide with project skills, and distribution flows through a marketplace rather than copy-paste between repos. The trade-off is operational: you're now maintaining a plugin and a release cadence, not editing a file in `.claude/skills/`.

## What to avoid

Putting every skill at project scope because it's the easiest location — every team member then pays the description budget for skills only one person uses. Putting personal preferences in `.claude/skills/` and committing them — that imposes your workflow on the team. Putting package-specific skills at the repo root in a monorepo — they load on sessions where they're irrelevant. Building a plugin for a skill only your team uses — the maintenance overhead exceeds the value.

## What to do instead

Match scope to actual reach:

- **Team-shared, this repo only** → `.claude/skills/<name>/` (project, committed)
- **You, across all your projects** → `~/.claude/skills/<name>/` (personal, not committed)
- **Package-specific in a monorepo** → `packages/<pkg>/.claude/skills/<name>/` (nested, committed)
- **Across many repos or teams** → plugin (namespaced, distributed via marketplace)

Watch the character budget. Run `/context` periodically — if the skill listing is being truncated, you have too many always-on skills. Move what you can to nested or personal scope.

## Example

A monorepo with mixed scopes:

```
/myrepo/
├── .claude/skills/
│   ├── commit-style/SKILL.md         # team-wide, committed
│   └── pr-template/SKILL.md          # team-wide, committed
├── packages/
│   ├── frontend/
│   │   └── .claude/skills/
│   │       ├── react-patterns/SKILL.md   # loads only in packages/frontend/
│   │       └── tailwind-conventions/SKILL.md
│   ├── backend/
│   │   └── .claude/skills/
│   │       └── api-endpoint-style/SKILL.md  # loads only in packages/backend/
│   └── shared/
└── ...

~/.claude/skills/
├── grill-me/SKILL.md                 # your personal interview skill
└── concise-plans/SKILL.md            # your prompt-format preferences
```

A session started at the root sees `commit-style` and `pr-template`. The frontend skills load only when Claude touches files under `packages/frontend/`. The personal skills load on every session you run, in any repo, and never enter the team's repo.

For skills that should reach many repos at once — say, a "deploy with rollback" workflow used by every service team — promote them to a plugin:

```yaml
---
name: deploy-with-rollback
description: Use when deploying a service to staging or prod. Runs the deploy, watches metrics for 5 minutes, rolls back on regression.
disable-model-invocation: true
---
```

Distributed via `/plugin install company-infra`, invoked as `/company-infra:deploy-with-rollback`. The namespace prevents collisions with anything teams have locally.
