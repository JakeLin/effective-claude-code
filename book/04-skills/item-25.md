---
item: 25
theme: skills
title: "Give a skill goals and constraints, not prescribed steps"
tags: [skills, prompting, reuse]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [17]
things_to_remember:
  - "Skills are reused in contexts you didn't anticipate — prescriptions break when the situation deviates"
  - "State the goal, the constraints, and the success criteria; let Claude pick the steps"
  - "If a step really must run in a specific order, make it a script — don't railroad it in prose"
  - "When in doubt, ask: would a competent teammate handle this if I gave them only this skill body? If yes, ship it; if no, you're under-specifying the *what*, not the *how*"
agent_steps:
  - "When writing a skill body, lead with the goal and the constraints, not the sequence of actions"
  - "Replace 'first do X, then Y, then Z' patterns with 'achieve X subject to constraints A, B, C'"
  - "If a strict order is genuinely required (e.g., migrations must run before code deploy), enforce it via a script or a hook rather than via prose"
  - "Audit existing skills for over-prescription: where they read like a recipe rather than a brief"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

A skill that prescribes exact steps fails the moment the situation deviates from what the author imagined. And situations always deviate. The user's task is slightly different, the codebase has shifted, a file isn't where the recipe said it would be — and the skill either produces wrong output (Claude follows the prescription literally) or gets ignored (Claude notices the mismatch and improvises without the skill). Either way, the skill stops earning its keep.

Skills are different from individual prompts in this respect. A prompt is one-shot: write what you want, get the result. A skill is reused across sessions, projects, and intents you didn't predict. The discipline that scales is to state the *goal* and the *constraints*, then trust Claude to pick the steps. "Generate a migration that adds a NOT NULL column to a table over 1M rows, subject to: backfill in a separate transaction; CONCURRENTLY for any new index; paired rollback file" describes the outcome and the rules. "First run pg_dump, then write to migrations/, then run validate.py, then commit" prescribes a sequence that fails the first time the situation isn't exactly that.

The carve-out is when an ordering is genuinely load-bearing — migrations must apply before the code that depends on them; tests must pass before push. For those, encode the ordering in a script or a hook, not in skill prose. A script that runs the steps in order is deterministic. A skill paragraph that says "first do X, then Y" is a suggestion Claude can misread, drop, or interpret out of sequence.

## What to avoid

Step-by-step recipes that bake in assumptions about the starting state. Skills that read like a runbook with eight numbered steps, each one assuming the previous landed correctly. Skills that try to anticipate every branch ("if the file exists, do A; if it doesn't, do B; if it exists but is empty, do C") instead of stating the goal and letting Claude handle the branching.

## What to do instead

Open the skill with the goal in one sentence. Follow with the constraints — what must be true about the output, what must not happen, the success criteria. Mention the gotchas (Item 24). Then stop. If a deterministic sequence is essential, factor it into a script the skill invokes, and let the prose stay at the goal level.

A simple sniff test: read the skill body and ask whether a competent teammate handed only this could do the task. If the answer is "no, I'd need to also tell them X," the missing piece is usually a constraint or a goal — not a step.

## Example

Over-prescribed — fragile under reuse.

```markdown
# Add Database Index

1. Open `db/schema.prisma`.
2. Find the model.
3. Add the `@@index` directive on the chosen column.
4. Run `npx prisma migrate dev --name add_index`.
5. Open the generated file in `prisma/migrations/`.
6. Add `CONCURRENTLY` to the `CREATE INDEX` line.
7. Run `npx prisma migrate deploy`.
8. Commit.
```

The first time the schema file isn't where step 1 expects, or the table is small enough that `CONCURRENTLY` is overkill, the recipe breaks.

Goal-and-constraints — survives reuse.

```markdown
# Add Database Index

## Goal
Add an index that improves the target query without locking the table
on production.

## Constraints
- Use `CONCURRENTLY` for any table over 100k rows.
- Index name must follow `idx_<table>_<columns>` (linter enforces).
- Migration must include a paired rollback.
- Never combine an index add with a schema change in the same migration.

## Gotchas
- The migration runner runs `migrate deploy` in a transaction by
  default; `CONCURRENTLY` requires `--no-transaction`. The team's
  `scripts/migrate-index.sh` handles this — use it.
```

Claude can now adapt the steps to the actual situation while staying within the rules that matter.
