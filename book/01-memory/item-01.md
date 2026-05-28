---
item: 1
theme: memory
title: "Treat CLAUDE.md as a living team artifact, not a one-time setup"
tags: [claude-md, team-practices, maintenance]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: []
things_to_remember:
  - "CLAUDE.md compounds — every recurring correction belongs in it"
  - "Edit it the same week you find the gap; commit the rule alongside the code change that motivated it"
  - "Prune ruthlessly — stale rules cause Claude to follow stale conventions"
  - "Treat `/init` as a starting point, not a finishing point"
agent_steps:
  - "When the user corrects a mistake Claude should have known not to make, propose adding a rule to CLAUDE.md and offer the diff"
  - "Before adding a new rule, check whether a similar rule already exists; update the existing one rather than duplicating"
  - "Phrase new rules concretely — commands, paths, file names — not vague verbs"
  - "When the rule is motivated by a specific code change, suggest committing the CLAUDE.md update in the same commit"
  - "If asked to prune CLAUDE.md, flag rules that conflict, no longer match the codebase, or duplicate other rules"
---

## Why this matters

The default failure mode with CLAUDE.md is the opposite of negligence — it's *completion*. You run `/init`, review the generated file, commit it, and move on. Six months later you're typing the same correction into chat for the fourth time, and the CLAUDE.md still looks the way it did on day one. The file isn't broken; it just stopped being part of the workflow.

CLAUDE.md is most valuable when it accretes. Every recurring correction is a signal that the file has a gap, and every gap closed is a class of mistake Claude will not make again. Teams that treat CLAUDE.md as living knowledge see compounding adherence — the file gets denser with specific, hard-won rules, and Claude gets more reliable on this codebase specifically. Teams that treat it as setup see Claude regress in predictable ways: the same code-review nit, the same naming mistake, the same forgotten test command, session after session.

The framing that helps is: *if you typed a correction into chat that you typed last session, that was a missed CLAUDE.md entry.* The cost of the missed entry isn't the one extra correction — it's every future correction of the same shape, multiplied by every person on the team.

## What to avoid

A CLAUDE.md generated once and never edited. Vague, generic rules ("write clean code", "follow best practices") inherited from a template. Single-author ownership where one person wrote it and no one else feels licensed to change it. Stale rules nobody removed when the convention changed.

## What to do instead

Edit CLAUDE.md the same week you discover a gap, not as a separate hygiene task. After Claude makes a correctable mistake, ask it to update CLAUDE.md so it won't make the mistake again — Claude is unusually good at writing rules for itself when given the example. Commit the rule alongside the code change that motivated it, so reviewers see the context together. Tag `@claude` on coworkers' PRs to suggest CLAUDE.md additions during code review.

Prune as deliberately as you add. An outdated rule is worse than a missing one because Claude will follow it. When a convention changes, the CLAUDE.md edit is part of the change.

## Example

A first-week CLAUDE.md and the same file three months later. The shape of the second one — specific commands, dated decisions, callouts to recent gotchas — is what a lived-in CLAUDE.md looks like.

```markdown
# Project conventions

- Use TypeScript
- Write tests
- Follow good practices
- Keep code clean
```

```markdown
# Project conventions

## Build & test
- `pnpm test` skips DB-backed tests. Run `pnpm test:integration` before pushing anything that touches `src/api/` or `src/db/`.
- `pnpm typecheck` must pass — CI runs it and there is no override.

## Code layout
- API handlers live in `src/api/handlers/<resource>.ts`, one file per resource.
- Shared DB helpers go in `src/db/`, never in handler files.

## Conventions learned the hard way
- Don't roll your own Stripe mocks — use `tests/fixtures/stripe.ts`. (Burned us in #847.)
- Migration files are append-only once merged. Editing a merged migration breaks every other dev's local DB.
- When adding a new env var, update `.env.example` in the same commit, or CI fails.
```
