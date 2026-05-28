---
item: 12
theme: commands
title: "Verify changes against the running app with `/run` and `/verify`, not just tests"
tags: [commands, verification, testing, bundled-skills]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [8, 53]
things_to_remember:
  - "Tests verify code; `/verify` and `/run` verify behavior against the running app"
  - "`/run` launches and drives your app so you can see a change working in the real environment"
  - "`/run-skill-generator` records a per-project recipe so subsequent runs don't re-discover setup"
  - "Run `/run-skill-generator` once per project, again when the launch process changes"
agent_steps:
  - "After implementing a user-facing feature, propose `/verify` to confirm it works in the real app — even if tests pass"
  - "On first use in a project that needs more than a vanilla launch (DB, env vars, build step), propose `/run-skill-generator` to capture the recipe"
  - "If `/run` or `/verify` fails because setup steps are missing, suggest re-running `/run-skill-generator` to update the recipe rather than patching manually"
  - "Skip /run and /verify when the change is purely internal (refactor, comments, formatting) and behavior cannot have shifted"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

Tests passing is not the same as the feature working. Tests cover what someone wrote tests for; the feature includes everything else — UI affordances, real-world data, integration with running services, what the user actually sees. A change that passes its unit tests can still ship a broken button, a wrong message, an empty state Claude didn't notice. The expensive lesson is that "all green" gives false confidence about whether the change does what it should.

The bundled run/verify skills bridge that gap. `/verify` builds and runs the app to confirm a code change does what it's supposed to, observed against actual behavior rather than test outcomes. `/run` launches the app and lets Claude drive it — clicking through, calling the endpoint, watching the log. `/run-skill-generator` is the setup step: it records what it takes to get the app running in your project (install commands, env vars, launch script) as a per-project skill, so the next `/verify` doesn't have to rediscover everything.

The reason `/run-skill-generator` matters: `/run` and `/verify` infer their launch from package.json, README, or Makefile when they can, and that inference gets unreliable as projects gain real-world complexity (databases, env files, graphical sessions, multi-step builds). Running the generator once captures what worked and commits it, so every future run is reproducible.

## What to avoid

Reporting a feature complete because tests passed without ever running the app. Spending a long time hand-debugging why `/run` won't launch when the right fix is to run `/run-skill-generator`. Skipping the generator on the assumption "the app launches with `pnpm dev`, surely Claude can figure it out" — it usually can, until it can't, and then debugging the launch chews the same budget you tried to save.

## What to do instead

After implementing anything user-facing, `/verify` it before marking the work done. For first-time setup in a real project, run `/run-skill-generator` so the recipe lives in the repo and works for everyone. When the build, launch, or env requirements change, run the generator again to update.

Reserve the skip for cases where behavior demonstrably hasn't changed: internal refactors that preserve interface, comment edits, formatting passes. Anything that could plausibly shift behavior deserves a quick `/verify`.

## Example

First-time project setup, then routine use.

```text
> /run-skill-generator

[Claude works through getting the app running from a clean clone — installs
deps, finds the env file, runs the migration, launches the dev server,
confirms it's reachable. Commits the recipe to .claude/skills/run-myapp/.]
```

```text
> [after implementing a new "share" button]
> /verify the share button copies the post URL to the clipboard

[Claude follows the captured recipe to launch the app, clicks the share
button, inspects clipboard contents, reports back.]
```

When the launch process changes:

```text
> [we just added a redis dependency for the worker]
> /run-skill-generator

[recipe updated to start redis before the dev server]
```
