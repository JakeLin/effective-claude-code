# Editorial Plan — Effective Claude Code

Working document tracking the content-excellence + ship-readiness passes.
Dev artifact; not part of the published book.

## Guardrails (every content step)
- Never touch verified facts, code blocks, frontmatter values, or the 4-section structure.
- Cut only padding/redundancy/throat-clearing — not substance or examples.
- Vary, don't scrub, crutch phrases — replace where formulaic, keep where natural.
- Preserve voice; match the surrounding register.
- One commit per step, pushed (env is ephemeral).

## Track 1 — Content excellence
- [x] Step 1 — Ch 1 Memory (calibration; 1 edit — already tight) ✓ signed off
- [x] Step 2 — Ch 2 Commands (item-08, item-13)
- [x] Step 3 — Ch 3 Subagents (item-16, item-18)
- [x] Step 4 — Ch 4 Skills (item-26, item-27)
- [x] Step 5 — Ch 5 Hooks (29/30/31/33/35 de-crutch + item-34 correctness fix)
- [x] Step 6 — Ch 6 Settings & Permissions (item-41; rest natural)
- [x] Step 7 — Ch 7 MCP (item-43, item-44, item-47)
- [x] Step 8 — Ch 8 Orchestration (item-50, item-56)
- [x] Step 9 — Ch 9 CLI & Headless (item-62, item-63 + tighten)
- [x] Step 10 — Ch 10 Worktrees — reviewed, clean, no edits
- [x] Step 11 — Ch 11 Agent Teams (item-68, item-70)
- [x] Step 12 — Ch 12 Scheduled Tasks — reviewed, clean, no edits
- [ ] Step 13 — Forward-reference pass (whole book)
- [ ] Step 14 — Final consistency sweep (re-count crutches; voice read-through)

## Track 2 — Structure & build
- [ ] Step 15 — mdBook plumbing: book.toml + SUMMARY.md (exclude _item-template.md)
- [ ] Step 16 — Verify build (install mdbook or document CI step)

## Track 3 — Release prep (user-gated, last)
- [ ] Step 17 — FACT_CHECK_REPORT.md + EDITORIAL_PLAN.md disposition (keep/move/delete)
- [ ] Step 18 — ⏸ references/ strip (destructive; user authorizes)

## Crutch baseline (for Step 14 comparison)
- "the right X": 29 items | "isn't X; it's Y": 9 | "The mistake is": 7
- "load-bearing": 6 | "the discipline is": 6 | "earns its place/keep": 8
