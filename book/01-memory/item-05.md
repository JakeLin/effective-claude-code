---
item: 5
theme: memory
title: "Place instructions at the scope where they actually apply"
tags: [claude-md, scope, hierarchy, local]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [1, 4]
things_to_remember:
  - "Project CLAUDE.md is for the team; user CLAUDE.md is for you; CLAUDE.local.md is for this project but private"
  - "Personal preferences in the project file leak to your teammates"
  - "Project-specific rules in `~/.claude/CLAUDE.md` follow you into every other project"
  - "Ancestor CLAUDE.md files load eagerly; descendants load lazily; siblings never share"
agent_steps:
  - "When asked to add a rule, decide its scope before its content — team-shared, personal-global, or personal-project"
  - "Propose `./CLAUDE.md` for team-shared rules, `~/.claude/CLAUDE.md` for personal-global, `./CLAUDE.local.md` for personal-project"
  - "If proposing `./CLAUDE.local.md`, confirm it is in `.gitignore` — if not, propose adding it"
---

## Why this matters

CLAUDE.md loads from four scopes: managed (org-wide, deployed by IT), user (`~/.claude/CLAUDE.md`, personal across all projects), project (`./CLAUDE.md`, team-shared via git), and local (`./CLAUDE.local.md`, personal to this project, gitignored). Each scope exists because rules have different audiences, and putting a rule in the wrong scope creates noise without value.

The common failure has two shapes. *Project rules in the personal global file*: your `~/.claude/CLAUDE.md` says "API handlers go in `src/api/handlers/`" and now every Python project, every script, every unrelated repo gets that rule injected. Or *personal preferences in the project file*: you commit "be terse, no preamble" to `./CLAUDE.md` and impose your conversational style on the whole team. Both look harmless. Both dilute adherence — Claude sees rules that don't apply to today's work, and adherence to the rules that *do* apply drops with the noise.

The loading rules are the other half. CLAUDE.md files in ancestor directories (`/`, `~`, project root, working dir) load eagerly at session start. CLAUDE.md files in descendant directories load lazily — only when Claude reads files in those directories. Siblings never share. Internalizing this means you stop being surprised by what's in context.

## What to avoid

Committing "I prefer short responses" to `./CLAUDE.md`. Putting "this project uses pnpm not npm" in `~/.claude/CLAUDE.md`. Checking sandbox URLs, test credentials, or per-machine paths into the project file. Forgetting to add `CLAUDE.local.md` to `.gitignore` and committing it by accident.

## What to do instead

Decide the audience before you write the rule:

- **Managed policy** — org-wide standards your IT or security team enforces. You probably don't write these; if you do, it's a separate process from regular contributions.
- **`~/.claude/CLAUDE.md`** (user) — preferences that follow *you* across every project: how terse you want responses, your editor of choice, shell aliases Claude should know about.
- **`./CLAUDE.md`** (project) — rules every collaborator on this repo should see. Build commands, conventions, architectural decisions. Committed to git.
- **`./CLAUDE.local.md`** (local) — your private overrides for this project. Sandbox URLs, dev test data, "skip the long-running test on my machine". Gitignored. Running `/init` and picking the personal option sets this up.

When in doubt, ask: "If I leave this team tomorrow, should this rule leave with me?" If yes, it's user or local. If no, it's project.

## Example

The same four kinds of rule, each placed at the correct scope.

```text
/Library/Application Support/ClaudeCode/CLAUDE.md   # managed (org)
~/.claude/CLAUDE.md                                  # user (you, every project)
./CLAUDE.md                                          # project (team, committed)
./CLAUDE.local.md                                    # local (you, this project, gitignored)
```

```markdown
# ~/.claude/CLAUDE.md
- Default to terse responses. Skip preamble unless I ask for it.
- I use fish, not bash — assume shell aliases live in `~/.config/fish/`.
```

```markdown
# ./CLAUDE.md
- Build: `pnpm build`. Test: `pnpm test` (skips DB tests) or `pnpm test:integration`.
- API handlers go in `src/api/handlers/<resource>.ts`, one file per resource.
- Migrations are append-only once merged — never edit a merged migration.
```

```markdown
# ./CLAUDE.local.md (gitignored)
- My dev DB is at `postgres://localhost:5433/myapp_dev` (non-default port).
- Skip `pnpm test:slow` on my machine — I run it in CI only.
```
