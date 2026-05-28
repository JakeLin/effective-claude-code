# Effective Claude Code — Build Guide

This is the working repository for **Effective Claude Code**, an open source book in the style of the Effective series (Effective C++, Effective Java, Effective Python). This file gives Claude orienting context. Detailed writing rules for Items live in `.claude/rules/items.md`, loaded automatically when editing files under `book/`.

---

## What this book is

A structured collection of numbered Items — each one a concrete, actionable principle for using Claude Code well. Written for human developers AND AI agents. Humans learn the *why*; agents read the frontmatter and execute the `agent_steps`.

## Audience

Both human developers and AI agents. Human is the primary voice — the Effective series always explains *reasoning*, not just rules. An AI agent that understands *why* a practice exists applies it better than one following a checklist.

---

## Repository layout

- `book/` — chapters and Items, one folder per theme, `item-NN.md` per Item
- `book/_item-template.md` — canonical template for new Items (copy to start)
- `.claude/rules/items.md` — detailed writing rules, loaded when editing `book/**`
- `.claude/skills/` — Phase 3 apply skill (planned)
- `scripts/` — Phase 2 CLAUDE.md generator (planned)
- `references/` — local research, committed during development, stripped before release

Item numbers are **global and stable** across all themes (item-01 through item-N). Once assigned, an Item number is never renumbered. If an Item is removed, its number is **retired** — never reused. This keeps every `related_items` cross-reference valid forever.

---

## Chapter order (importance-ranked, stable-first)

Chapters 1–9 are stable Claude Code features; chapters 10–12 are beta (chapter intros include a "subject to change" note).

| # | Theme | Stability |
|---|-------|-----------|
| 01 | Memory & CLAUDE.md | Stable |
| 02 | Commands | Stable |
| 03 | Subagents | Stable |
| 04 | Skills | Stable |
| 05 | Hooks | Stable |
| 06 | Settings & Permissions | Stable |
| 07 | MCP Servers | Stable |
| 08 | Orchestration & Workflows | Stable |
| 09 | CLI & Headless Mode | Stable |
| 10 | Git Worktrees | Beta |
| 11 | Agent Teams | Beta |
| 12 | Scheduled Tasks & Routines | Beta |

---

## License & publishing

- License: CC-BY-4.0. See `LICENSE`. Attribution required; commercial reuse allowed. Covers both prose and code in this repository.
- Build: mdBook → GitHub Pages. Config in `book.toml`.

---

## AI consumption (phased)

- **Phase 1 (now):** Markdown Items readable by humans and agents. An agent can read any Item and follow `agent_steps` directly.
- **Phase 2:** A script in `scripts/` that generates a `CLAUDE.md` rule set from selected Items' `things_to_remember` fields.
- **Phase 3:** A Claude Code skill in `.claude/skills/effective-claude-code/` that applies Items to a project on demand.

---

## Reference material

`references/` is committed during development so Claude Code Web can access it, but is **not part of the published book**. Strip it from git history before public release using:

```bash
git filter-repo --path references/ --invert-paths
```

Key sources:
- `references/claude-code-best-practice/` — shanraisshan's community best practices repo
- Official docs: https://code.claude.com/docs
