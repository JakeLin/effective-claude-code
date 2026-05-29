---
item: 2
theme: memory
title: "Use CLAUDE.md for context, hooks for guarantees"
tags: [claude-md, hooks, enforcement, mental-model]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [1, 29]
things_to_remember:
  - "CLAUDE.md is context Claude reads, not configuration the harness enforces"
  - "If a rule MUST run, write a hook; CLAUDE.md is advice"
  - "Capitalization and stern language don't elevate context to enforcement"
  - "Use deny-permissions for actions that must be blocked, not CLAUDE.md prose"
agent_steps:
  - "When the user adds a rule to CLAUDE.md framed as ALWAYS / NEVER / MUST, ask whether failure to follow it would be a serious problem"
  - "If serious, propose a hook (PreToolUse to block before, PostToolUse to enforce after) in addition to or instead of the CLAUDE.md entry"
  - "For 'must not happen' rules tied to specific tools or paths, propose a `permissions.deny` rule rather than CLAUDE.md prose"
---

## Why this matters

CLAUDE.md content is delivered to the model as a user message at the start of the conversation. Claude reads it and tries to follow it, but nothing about that mechanism enforces compliance — the model is making probabilistic decisions, and your instruction is one input among many. This is the most consequential mental model in the chapter, because it determines which tool you reach for when reliability matters.

The misconception that bites teams: writing "ALWAYS run `pnpm test` before committing" in CLAUDE.md and being surprised when Claude doesn't. Capitalization is not a mechanism. Stronger language nudges the probability upward, but the answer to "must this happen every time?" is never CLAUDE.md alone. Hooks run as shell commands at fixed lifecycle events regardless of what Claude decides. Permission denies block tool calls before they execute. CLAUDE.md is advice the model sees; hooks and permissions are the actual enforcement layer.

The practical test: imagine Claude skips this rule once. Is that "annoying but recoverable" or "we lost data / shipped a secret / broke prod"? Annoying belongs in CLAUDE.md. Serious belongs in a hook.

## What to avoid

Coercing reliability with louder language. "MUST", "NEVER", "ALWAYS", red banners, repeated reminders — they all live at the same enforcement layer (none). Putting security rules in CLAUDE.md as your defense ("never read `.env` files") instead of denying the tool. Re-litigating the same correction in chat instead of reaching for the layer that actually enforces.

## What to do instead

Decide by consequence, not by emphasis. Rules whose violation would be a real problem belong in hooks or permission denies, even if they're also in CLAUDE.md for documentation. Keep CLAUDE.md for behavioral *shape* — what good output looks like, conventions, preferences, defaults Claude should reach for. Anything that has to happen on every run gets a `PostToolUse` or `Stop` hook; anything that must not happen gets `PreToolUse` or `permissions.deny`.

When a CLAUDE.md rule keeps getting violated despite being there, that's a signal it should have been a hook from the start. Chapter 5 covers writing hooks in detail.

## Example

A rule that belongs in CLAUDE.md, and one that needed to be a hook.

```markdown
## Code conventions
- Prefer `Result<T, E>` over throwing in service-layer code.
- API responses use snake_case keys, never camelCase.
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-direct-prod-deploy.sh"
          }
        ]
      }
    ]
  }
}
```
