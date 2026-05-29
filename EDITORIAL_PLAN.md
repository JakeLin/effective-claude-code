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
- [ ] **Step 1 — ⏸ CALIBRATION: Ch 1 Memory (items 1–7)** — de-crutch + targeted tighten + title check. Await sign-off before scaling.
- [ ] Step 2 — Ch 2 Commands (8–14)
- [ ] Step 3 — Ch 3 Subagents (15–21)
- [ ] Step 4 — Ch 4 Skills (22–28)
- [ ] Step 5 — Ch 5 Hooks (29–35) — fold in item-34 nit ("user"→"Claude")
- [ ] Step 6 — Ch 6 Settings & Permissions (36–42)
- [ ] Step 7 — Ch 7 MCP (43–49)
- [ ] Step 8 — Ch 8 Orchestration (50–56)
- [ ] Step 9 — Ch 9 CLI & Headless (57–63) — heaviest tightening
- [ ] Step 10 — Ch 10 Worktrees (64–67) [beta — light touch]
- [ ] Step 11 — Ch 11 Agent Teams (68–70) [beta — light touch]
- [ ] Step 12 — Ch 12 Scheduled Tasks (71–74) [beta — light touch]
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
