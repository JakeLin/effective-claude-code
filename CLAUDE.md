# Effective Claude Code — Build Guide

This is the working repository for **Effective Claude Code**, an open source book in the style of the Effective series (Effective C++, Effective Java, Effective Python). This file gives Claude Code full context for building and maintaining the book.

---

## What this book is

A structured collection of numbered Items — each one a concrete, actionable principle for using Claude Code well. Written for human developers AND AI agents. Humans learn the *why*; agents read the frontmatter and execute the `agent_steps`.

---

## Audience

Both human developers and AI agents. Human is the primary voice — the Effective series always explains *reasoning*, not just rules. An AI agent that understands *why* a practice exists applies it better than one following a checklist.

---

## Repository structure

```
effective-claude-code/
├── book/
│   ├── _item-template.md   # Frontmatter + body template for new Items
│   ├── 01-memory/          # Items 1–N for Memory & CLAUDE.md
│   ├── 02-commands/        # Items for Commands
│   ├── 03-subagents/       # Items for Subagents
│   ├── 04-skills/          # Items for Skills
│   ├── 05-hooks/           # Items for Hooks
│   ├── 06-settings/        # Items for Settings & Permissions
│   ├── 07-mcp/             # Items for MCP Servers
│   ├── 08-orchestration/   # Items for Orchestration & Workflows
│   ├── 09-cli/             # Items for CLI & Headless Mode
│   ├── 10-worktrees/       # Items for Git Worktrees (beta)
│   ├── 11-agent-teams/     # Items for Agent Teams (beta)
│   └── 12-scheduled-tasks/ # Items for Scheduled Tasks & Routines (beta)
├── .claude/
│   └── skills/             # Phase 2: apply skill
├── scripts/                # Phase 2: CLAUDE.md generator
├── references/             # Local research — committed during development, stripped from history before release
├── CLAUDE.md               # This file
├── README.md
└── book.toml               # mdBook config
```

Item numbers are **global and stable** across all themes (item-01 through item-N). Once assigned, an Item number is never renumbered. If an Item is removed or deprecated, its number is **retired** — never reused. This keeps every `related_items` cross-reference valid forever. Each theme folder contains files named `item-NN.md`.

---

## Chapter order (importance-ranked, stable-first)

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

## Item count

Variable per theme based on available material. Target ~5–6 Items per theme on average (medium density). Let the topic dictate depth — do not pad thin themes or truncate rich ones.

---

## Frontmatter schema (full)

Every Item file starts with this YAML frontmatter:

```yaml
---
item: 7
theme: skills
title: "Prefer skills over slash commands for reusable multi-step workflows"
tags: [skills, reusability, automation]
claude_code_version: "2.1.150"
stability: stable        # stable | beta | deprecated
status: current          # current | needs-review | deprecated
related_items: [8, 12]
things_to_remember:
  - "Skills persist across sessions; commands are one-shot"
  - "Use when_to_use: to help Claude auto-discover the skill"
  - "Skills are shared via git — commit them for the whole team"
agent_steps:
  - "Check if .claude/skills/ directory exists, create it if not"
  - "Create .claude/skills/<name>/SKILL.md"
  - "Add frontmatter: name, description, when_to_use"
  - "Write the skill body as imperative step-by-step instructions"
  - "Commit the file so the whole team benefits"
---
```

**Field rules:**
- `item`: Global integer, unique across all themes. Stable forever — never renumbered, retired numbers never reused.
- `title`: Imperative or principle statement — the advice in one line. A reader scanning titles alone should learn something.
- `claude_code_version`: Version when the Item was **last verified** to still be accurate. Update lazily when you re-verify; the real staleness signal is `status: needs-review`.
- `status`: Set to `needs-review` when a Claude Code release may have changed the specifics.
- `things_to_remember`: 2–4 bullets. The first bullet is the one-line takeaway an agent extracts. This field is the **single source of truth** — it is rendered onto the page by the mdBook build, not duplicated in the body.
- `agent_steps`: Concrete, ordered, executable steps — written so Claude can follow them without reading the prose.

---

## Item body structure

After the frontmatter, every Item follows this prose structure:

```markdown
## Why this matters

[2–3 paragraphs: the principle, what goes wrong without it, real-world consequence.
Write at the principle level — durable reasoning, not version-specific syntax.]

## What to avoid

[Short example of the anti-pattern — what most developers do instead and why it fails.]

## What to do instead

[The correct approach with concrete explanation.]

## Example

[Code block or file snippet showing a real implementation.]
```

The "Things to Remember" list comes from the `things_to_remember` frontmatter field and is rendered onto the page by the mdBook build — do not write it into the body.

**Length:** 1–2 rendered pages. Long enough to explain the *why*, short enough to read in 3 minutes.

---

## Writing principles

- **Prose is principle-based, not syntax-based.** The *why* is durable; specific field names and file paths go in examples only. When Claude Code changes a field name, update one code block, not the whole Item.
- **Title is the advice.** A reader scanning titles alone should learn something.
- **No comments in code examples** unless the why is non-obvious.
- **agent_steps are imperative and concrete.** They should work without reading the prose.
- **`things_to_remember` lives only in frontmatter.** The mdBook build renders it onto the page; do not transcribe it into the body.

---

## Staleness handling

- Write prose as durable principles (rarely needs updating)
- Code examples and frontmatter samples carry `claude_code_version`
- Set `status: needs-review` on Items when a Claude Code release changes their specifics
- Beta-theme chapters (10–12) carry an explicit "subject to change" note at the chapter intro

---

## Contribution model

- Author writes initial Items for each theme
- Community submits corrections and new Items via PR
- New Items start by copying `book/_item-template.md` — the template is the canonical schema
- Each PR must: follow the frontmatter schema, match the Item body structure, include a real `claude_code_version`, pass a review for principle-level writing (not just syntax documentation)

---

## License

CC-BY-4.0. See `LICENSE` for the full text. Attribution required; commercial reuse allowed. Covers both prose and code in this repository.

---

## Publishing

mdBook → GitHub Pages. Config in `book.toml`.

---

## AI consumption (phased)

**Phase 1 (now):** Well-structured markdown Items readable by both humans and agents. An agent can read any Item and follow `agent_steps` directly.

**Phase 2:** A script in `scripts/` that generates a `CLAUDE.md` rule set from selected Items' `things_to_remember` fields.

**Phase 3:** A Claude Code skill in `.claude/skills/effective-claude-code/` that applies Items to a project on demand.

---

## Building workflow

### Per-theme process (repeat for each of the 12 chapters in order)

1. **Research**: Read the relevant files in `references/claude-code-best-practice/` (best-practice, tips, reports, implementation) AND fetch the official docs page for the theme from `https://code.claude.com/docs`.
2. **Propose titles**: Draft 5–7 candidate Item titles for the theme. Present them to the user for approval, cuts, reordering, or additions.
3. **Calibrate (chapter 1 only)**: For the first chapter, write the intro `README.md` + the first `item-NN.md` in full and wait for user review on voice, structure, and length before continuing. From chapter 2 onward, the title-approval gate in step 2 is the only checkpoint — proceed straight to bulk writing unless a deliberate style shift is needed.
4. **Bulk write**: Write all remaining Items for the theme in one pass.
5. **Commit**: One commit per completed theme. Message names the chapter and lists Item titles.

### Cross-references

Write `related_items` opportunistically as you go — at the time of writing chapter N, link backward to any relevant Items in chapters 1..N-1. After all 12 themes are complete, do a single **forward-link** pass to add references that point from earlier Items to later ones.

### Chapter structure per theme folder

Each `book/NN-theme/` folder contains:
- `README.md` — chapter intro: what the feature is (beginner-friendly, ~150 words), why it matters, how Items build on each other. Beta chapters (10–12) include an explicit "subject to change" note.
- `item-NN.md` — one file per Item, global item numbering across the whole book

---

## Reference material

`references/` is committed during development so Claude Code Web can access it, but is **not part of the published book**. Strip it from git history before public release using:

```bash
git filter-repo --path references/ --invert-paths
```

Key sources:
- `references/claude-code-best-practice/` — shanraisshan's community best practices repo
- Official docs: https://code.claude.com/docs
