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
├── references/             # Local research only — NOT part of the book, gitignored
├── CLAUDE.md               # This file
├── README.md
└── book.toml               # mdBook config
```

Item numbers are **global** across all themes (item-01 through item-N). Each theme folder contains files named `item-NN.md`.

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
summary: "One-sentence human + agent takeaway — the single most important thing to remember."
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
- `item`: Global integer, unique across all themes
- `title`: Imperative or principle statement — the advice in one line
- `summary`: One sentence, self-contained — what an agent extracts first
- `claude_code_version`: Version when Item was written/last verified
- `status`: Set to `needs-review` when a Claude Code release may have changed the specifics
- `agent_steps`: Concrete, ordered, executable steps — written so Claude can follow them without reading the prose

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

## Things to Remember

- [Bullet 1 — mirrors things_to_remember in frontmatter]
- [Bullet 2]
- [Bullet 3]
```

**Length:** 1–2 rendered pages. Long enough to explain the *why*, short enough to read in 3 minutes.

---

## Writing principles

- **Prose is principle-based, not syntax-based.** The *why* is durable; specific field names and file paths go in examples only. When Claude Code changes a field name, update one code block, not the whole Item.
- **Title is the advice.** A reader scanning titles alone should learn something.
- **No comments in code examples** unless the why is non-obvious.
- **agent_steps are imperative and concrete.** They should work without reading the prose.
- **Things to Remember mirrors the frontmatter field.** Keep them in sync.

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
- Each PR must: follow the frontmatter schema, match the Item body structure, include a real `claude_code_version`, pass a review for principle-level writing (not just syntax documentation)

---

## License

MIT

---

## Publishing

mdBook → GitHub Pages. Config in `book.toml`.

---

## AI consumption (phased)

**Phase 1 (now):** Well-structured markdown Items readable by both humans and agents. An agent can read any Item and follow `agent_steps` directly.

**Phase 2:** A script in `scripts/` that generates a `CLAUDE.md` rule set from selected Items' `things_to_remember` fields.

**Phase 3:** A Claude Code skill in `.claude/skills/effective-claude-code/` that applies Items to a project on demand.

---

## Reference material

`references/` is committed during development so Claude Code Web can access it, but is **not part of the published book**. Strip it from git history before public release using:

```bash
git filter-repo --path references/ --invert-paths
```

Key sources:
- `references/claude-code-best-practice/` — shanraisshan's community best practices repo
- Official docs: https://code.claude.com/docs
