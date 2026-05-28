---
name: effective-claude-code
description: Apply Effective Claude Code book principles to a project's Claude setup. Use when someone asks to improve their Claude Code setup, apply best practices, or configure Claude Code for a project. Also triggers on "apply item-N", "apply chapter-N", "apply hooks/memory/settings/subagents", or "how should I configure Claude Code".
---

# Effective Claude Code

You apply principles from *Effective Claude Code* — a book of 74 concrete, actionable items — to a developer's project. Read the project first, identify gaps, explain what you'll do and why, then write clean rules after the developer confirms.

The references live next to this file. Read `references/index.md` first — it maps every item to its chapter file.

## Always start by reading the project

Before asking questions or writing anything, audit the project — even when arguments are given:

- Read `CLAUDE.md` — note what's there, what's vague, what topics are missing
- Check `.claude/settings.json` — note `permissions.allow`, `permissions.deny`
- Check `.claude/rules/` — what files exist
- Check `.claude/commands/`, `.claude/agents/`, `.claude/skills/` — note what exists
- Scan `package.json`, `pyproject.toml`, or directory structure for project type

Use what you find to infer coverage. Skip topics already well-covered. Only surface gaps.

## Invocation forms

**No arguments** — read the project, then open with what you found:
> "I see a Python data pipeline with a 20-line CLAUDE.md and no `.claude/settings.json`. The biggest gaps are hooks and permissions. Anything feeling painful, or should I work through both?"

No menus. Let the audit lead the conversation.

**Specific items:** `apply item-1 item-17`
→ Read `references/index.md`, load the relevant chapter files, extract only those items.

**A chapter:** `apply hooks` or `apply chapter-5`
→ Load that chapter's reference file. Stay scoped to it.

**All stable rules:** `apply all`
→ Load all 9 stable chapter files (ch01–ch09). Skip beta unless asked.

| Chapter | Aliases | File |
|---------|---------|------|
| 1 Memory & CLAUDE.md | memory, claude-md | references/ch01-memory.md |
| 2 Commands | commands | references/ch02-commands.md |
| 3 Subagents | subagents, agents | references/ch03-subagents.md |
| 4 Skills | skills | references/ch04-skills.md |
| 5 Hooks | hooks | references/ch05-hooks.md |
| 6 Settings & Permissions | settings, permissions | references/ch06-settings-permissions.md |
| 7 MCP Servers | mcp | references/ch07-mcp-servers.md |
| 8 Orchestration | orchestration, workflows | references/ch08-orchestration.md |
| 9 CLI & Headless | cli, headless | references/ch09-cli-headless.md |
| 10 Git Worktrees *(beta)* | worktrees | references/beta/ch10-git-worktrees.md |
| 11 Agent Teams *(beta)* | teams | references/beta/ch11-agent-teams.md |
| 12 Scheduled Tasks *(beta)* | scheduled, routines | references/beta/ch12-scheduled-tasks.md |

## Triage

Each item's `ecc-meta` block says:
- `target` — `claude-md`, `settings-json`, `claude-rules`, or `conversation`
- `action` — `add` (missing, write it), `fix` (wrong, propose change), or `suggest` (behavioural tip, no file)
- `check` — what to look for to decide if action is needed

If an item has no `ecc-meta`: use judgment, default to `claude-md`.

`conversation`-target items don't write to any file — collect them and show at the end as Tips.

Flag anything outside the requested scope as a side note — don't expand scope without asking.

## Confirm before writing

**Single item** — one line: what + why, then ask:
> "I'll add a rule to keep CLAUDE.md under 200 lines — Claude reads files partially, so rules near the bottom quietly stop working. Apply?"

**Batch** — show the full plan, then ask:
```
🔴 Fix:
  • item-4: CLAUDE.md is 340 lines — propose splitting into .claude/rules/

🟡 Add:
  • item-30: No PreToolUse hook — will add destructive-command guardrail
  • item-38: No allowlist in settings.json — will add starter allow block

💡 Tips:
  • item-7, item-41

Proceed?
```

## Writing rules

Write to the target the item specifies:
- `claude-md` → append to `CLAUDE.md`
- `settings-json` → write or update `.claude/settings.json`
- `claude-rules` → create `.claude/rules/<topic>.md`
- `agents` → read `.claude/agents/<name>.md` files, propose specific fixes (weak descriptions, missing `tools:` field), write after confirmation

Write clean bullets. No item numbers, no book references anywhere in the files.

## After applying

If there were file changes, tell the user the count and what to actually watch for:
> "Added 6 rules across hooks and settings. The biggest change: Claude will now ask before running `rm`, `DROP TABLE`, or `git push --force`."

If there were no file changes, say "No file changes for this project."

## Tips and learn more

At the end, show `conversation`-target items as project-specific advice — connect each principle to what you found in the audit, then offer the item number for anyone who wants to read further. Keep it to 2–3 tips and 2–3 item pointers.

> **Worth knowing:** You have several custom agents — when briefing them, include the files and conclusions already established in the main thread. Agents start cold with no memory of the conversation (item-17).
>
> **Go deeper:** Item-30 covers PreToolUse hook patterns in detail. Item-7 covers when to promote auto-memory entries into CLAUDE.md.
