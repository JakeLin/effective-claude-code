---
item: 7
theme: memory
title: "Let auto memory absorb the corrections you'd otherwise repeat"
tags: [auto-memory, memory, complementary]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [1, 5]
things_to_remember:
  - "Auto memory is Claude's running notebook — complementary to your hand-written CLAUDE.md"
  - "Auto memory is machine-local; for team-shared rules, use CLAUDE.md instead"
  - "Audit it with `/memory` periodically — the files are plain markdown you can edit or delete"
  - "Promote useful auto-memory entries into CLAUDE.md when the whole team should see them"
agent_steps:
  - "When the user corrects a personal preference, save it to auto memory rather than proposing a CLAUDE.md edit"
  - "When the user corrects something the whole team should know, propose a CLAUDE.md edit instead"
  - "If asked what Claude remembers about this project, point to `/memory` and the auto-memory directory"
  - "Periodically suggest auditing auto memory if entries look stale, duplicative, or contradict CLAUDE.md"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

Auto memory is the system that lets Claude carry knowledge across sessions without you writing anything. When you correct Claude, state a preference, or explain something non-obvious about the repo, Claude decides whether to save a note to `~/.claude/projects/<project>/memory/`. The next session reads `MEMORY.md` at startup — the first 200 lines or 25KB — and starts with that context loaded.

It is complementary to CLAUDE.md, not a replacement. CLAUDE.md is what *you* commit for the team: build commands, architectural decisions, conventions everyone needs. Auto memory is what *Claude* learns about working with you on this repo: that you prefer `pnpm` to `npm`, that the integration tests need Redis running, that the design lead always asks about accessibility before approving frontend PRs. The two systems carry different shapes of knowledge — one is curated and shared, the other is incidental and personal.

The risk is treating auto memory as a black box. If you never run `/memory`, you don't know what Claude is carrying about you and this codebase across sessions. Stale entries persist; duplicates accumulate; useful learnings stay invisible to the team because they live in your machine-local notes.

## What to avoid

Letting auto memory stay invisible — never auditing what got saved. Putting team-shared rules into auto memory (it's machine-local; teammates won't see it). Keeping low-signal entries that bloat the index. Assuming auto memory will sort out conflicts with CLAUDE.md — it won't; Claude reads both and may pick arbitrarily when they disagree.

## What to do instead

Run `/memory` periodically — every couple of weeks, or whenever Claude does something that surprises you. The interface lists the auto-memory files alongside the CLAUDE.md files loaded in your session and lets you open and edit them directly. Treat the audit as cheap and routine; the files are plain markdown.

When you find a useful entry — something that would help any teammate on this repo — promote it. Copy the rule into CLAUDE.md and (if you want) delete the auto-memory version. When you find a stale or wrong entry, delete it. When you find an entry that contradicts CLAUDE.md, fix one or the other; don't leave them in conflict.

The division of labor that works: CLAUDE.md for "the team should know this", auto memory for "Claude should know this when working with me here". If you can't decide which a given rule is, write it in CLAUDE.md — the cost of over-sharing a useful rule is lower than the cost of hiding it in machine-local notes.

## Example

A `MEMORY.md` after a few weeks of work, and a follow-up CLAUDE.md edit promoting the entries that everyone should see.

```markdown
# ~/.claude/projects/myapp/memory/MEMORY.md

## Build & test
- Jake uses pnpm here, not npm.
- Integration tests need Redis running locally on port 6380 (non-default).
- `pnpm test:slow` takes ~12 minutes; Jake skips it locally and lets CI run it.

## Conventions Jake has corrected me on
- API responses use snake_case keys, not camelCase (corrected 2026-04-12, 2026-04-19).
- Don't use `any` in service-layer code — Jake reverts these in review.

## Editor & shell
- Jake uses fish, not bash. Aliases live in `~/.config/fish/config.fish`.
```

```markdown
# ./CLAUDE.md (after promotion)
- Use pnpm, not npm. (Was tripping up new contributors.)
- API responses use snake_case keys, not camelCase. The serializer in `src/api/serialize.ts` handles this.
- Don't use `any` in service-layer code — use `unknown` and narrow.

# Integration test setup (Redis port 6380) — left in auto memory; machine-specific.
# Editor preferences — left in auto memory; personal.
```
