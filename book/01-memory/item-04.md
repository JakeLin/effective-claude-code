---
item: 4
theme: memory
title: "Keep each CLAUDE.md under 200 lines"
tags: [claude-md, size, context-budget]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [1, 3]
things_to_remember:
  - "Every line in CLAUDE.md loads into every session — treat the file as a context budget"
  - "Past 200 lines, adherence drops measurably"
  - "`@path` imports help organize for humans but don't reduce context cost"
  - "When the file grows, move path-specific rules to `.claude/rules/` and delete stale ones"
agent_steps:
  - "When CLAUDE.md crosses 150 lines, propose an audit before adding more rules"
  - "Identify rules that only apply to specific paths and propose moving them to `.claude/rules/` with `paths:` frontmatter"
  - "Flag rules that duplicate, conflict, or no longer match the codebase and propose removal"
---

## Why this matters

Every line in CLAUDE.md is loaded into context at the start of every session, alongside the conversation that comes after. A 500-line CLAUDE.md taxes every interaction — whether the rules in lines 200–500 matter for today's task or not. That's a real cost in tokens, and a less obvious cost in adherence: Claude is measurably more likely to skim past or miss specific rules in long files.

The Claude Code docs target 200 lines as the upper end for reliable adherence. The number isn't magic — it's the point at which longer prose starts to look like documentation Claude scans rather than instructions Claude follows. The fix when you cross it isn't tighter writing within the same file; it's splitting.

The trap is that each individual rule feels worth keeping. Each was added in response to a real correction; deleting it feels like regressing. But the cost-benefit shifted: a rule that helped on the day it was added might now be making twenty unrelated rules slightly less likely to land.

## What to avoid

Letting CLAUDE.md grow unbounded as the project does — adding rules without ever relocating or removing any. Treating `@path` imports as a way around the size budget: imported files load at startup too, and consume the same context. Cramming chapter-specific or subsystem-specific rules into the root file when they only matter sometimes.

## What to do instead

Audit when the file crosses ~150 lines, not when it crosses 200 — that gives you headroom. Three moves to know:

- **Path-specific rules → `.claude/rules/`** with a `paths:` glob, so they only load when Claude touches matching files (Item 6).
- **Personal preferences → `~/.claude/CLAUDE.md`** instead of the project file, so they stay with you across projects (Item 5).
- **Stale rules → deleted.** Outdated rules are worse than missing ones; Claude will follow them.

Treat the 200-line target as a budget. Each line should earn its slot by being needed in every session — not by having once been useful.

## Example

A bloated project CLAUDE.md, audited and split.

```markdown
# Before — 340 lines (truncated)

## Conventions
- ... 40 lines of general project rules ...

## Testing
- pnpm test runs unit tests
- pnpm test:integration runs DB-backed tests
- ... 60 lines on testing patterns, fixture files, when to mock ...

## API design
- ... 80 lines on handler structure, error shape, validation ...

## Frontend
- ... 90 lines on component layout, Tailwind conventions, state ...

## Personal preferences (jake)
- ... 40 lines, mostly editor and shell aliases ...

## Outdated (Stripe v2 → v3 migration notes, completed Q4 2025)
- ... 30 lines ...
```

```text
# After
./CLAUDE.md                       ~80 lines  (general conventions only)
./.claude/rules/testing.md        paths: tests/**, src/**/*.test.ts
./.claude/rules/api.md            paths: src/api/**
./.claude/rules/frontend.md       paths: src/components/**, src/pages/**
~/.claude/CLAUDE.md               (personal preferences moved here)
# Stripe migration notes deleted.
```
