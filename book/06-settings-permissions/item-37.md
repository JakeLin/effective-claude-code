---
item: 37
theme: settings-permissions
title: "Commit team settings; gitignore the personal overrides"
tags: [settings, git, collaboration, settings-local]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [4, 36]
things_to_remember:
  - "`.claude/settings.json` is team-shared and belongs in git; `.claude/settings.local.json` is personal and belongs in .gitignore"
  - "Anything that should be true for every developer on the repo goes in the committed file; anything specific to your machine or taste goes local"
  - "Never put secrets, API keys, or personal absolute paths in the committed settings — those go in local settings or environment"
  - "A committed settings.json is documentation: it tells every teammate (and every fresh Claude session) what this repo expects"
agent_steps:
  - "Put team-wide configuration — shared permission rules, project model choice, hooks the whole team needs — in .claude/settings.json and commit it"
  - "Put personal or machine-specific overrides — your own allow rules, local paths, experimental toggles — in .claude/settings.local.json"
  - "Ensure .claude/settings.local.json is listed in .gitignore; if it isn't, add it"
  - "Before committing settings.json, scan it for secrets, tokens, and personal absolute paths and move any to local settings or env"
---

## Why this matters

There are two project-scoped settings files and the difference between them is who they're for. `.claude/settings.json` is committed to the repository — it's the configuration the whole team shares, and it travels with the code. `.claude/settings.local.json` is git-ignored — it's yours, for this repo, on this machine, and it never reaches a teammate. The split exists so that shared decisions and personal ones don't fight over the same file.

Getting this split right pays off in two directions. The committed file becomes living documentation: when a new developer clones the repo — or when a fresh Claude session starts in CI — the project's permission rules, model choice, and hooks are already there, no setup required. The team's conventions are encoded once and enforced by the harness for everyone. Meanwhile the local file absorbs everything that *shouldn't* be standardized: your personal allowlist for tools you trust, an absolute path that only exists on your laptop, an experiment you're not ready to inflict on the team.

The failure mode of ignoring the split is two-sided. Put personal tweaks in the committed file and you push your machine-specific paths and half-baked experiments onto everyone. Worse, put a secret — an API key, a token — in the committed file and you've leaked it into git history, where deleting it later doesn't really remove it. Secrets and personal state belong in local settings or environment variables; the committed file should contain nothing you'd be unhappy to see on a teammate's screen.

## What to avoid

Putting an API key or token in `.claude/settings.json` — it's now in git history forever. Committing your personal absolute paths or experimental toggles, so they break for everyone else. Leaving `.claude/settings.local.json` out of `.gitignore`, so your personal overrides get committed by accident. Treating the two files as interchangeable and dumping everything into whichever one you opened first.

## What to do instead

Decide each setting by its audience. Should this be true for every developer on the repo? Committed `settings.json`. Is it specific to you, your machine, or a passing experiment? Local `settings.local.json`. Is it a secret? Neither file as plaintext — use an environment variable or a credential helper. Confirm `.claude/settings.local.json` is in `.gitignore` before you write anything personal into it, and give the committed file a quick scan for leaked secrets and personal paths before every commit.

## Example

A committed `.claude/settings.json` — shared, safe, documentary:

```json
{
  "permissions": {
    "allow": ["Bash(npm run test:*)", "Bash(npm run lint:*)"],
    "deny": ["Read(./.env)", "Read(./secrets/**)"]
  }
}
```

Every teammate who clones the repo inherits these rules; a fresh session in CI does too. The file tells anyone reading it what this project expects.

A git-ignored `.claude/settings.local.json` — personal, never shared:

```json
{
  "permissions": {
    "allow": ["Bash(docker compose *)"]
  },
  "env": {
    "MY_LOCAL_FIXTURES": "/Users/me/fixtures"
  }
}
```

The `docker compose` allowance is your call, not the team's. The absolute path only exists on your machine. Neither belongs in the committed file — and the `.gitignore` entry guarantees they stay out. Secrets, notably, appear in *neither* file as plaintext: a token would live in an environment variable or a credential helper, never checked into git.
