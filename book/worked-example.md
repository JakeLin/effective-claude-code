# Worked Example: Evolving a Claude Code Setup

This example shows how the book's primitives fit together on a normal project. The point is not to install every mechanism. The point is to promote a rule only when the next rung solves a real problem.

## 1. Start with project memory

Run `/init`, then prune the result. Keep facts Claude needs every session: commands, architecture boundaries, test expectations, and recurring project-specific gotchas.

```markdown
# Project context

## Build and test
- Run `pnpm test` for unit tests.
- Run `pnpm typecheck` before committing TypeScript changes.
- Run `pnpm test:integration` for files under `src/api/` or `src/db/`.

## Code layout
- API handlers live in `src/api/handlers/<resource>.ts`.
- Shared database helpers live in `src/db/`, never inside handlers.
```

## 2. Move narrow rules to narrower scope

If a rule applies only under one path, move it into `.claude/rules/` instead of making every Claude Code session carry it globally.

```markdown
# API handler rules

Applies to `src/api/handlers/**`.

- Wrap every handler with `requireSessionAuth()`.
- Return errors as `{error: {code, message}}`.
- Never return raw database rows; use `serializeForApi()`.
```

## 3. Package repeated work as a skill

When you keep pasting the same procedure, turn it into a skill. Put the non-obvious parts first.

```text
.claude/skills/write-api-endpoint/
  SKILL.md
  templates/
    handler.ts
```

```markdown
---
name: write-api-endpoint
description: Use when adding or changing API handlers under src/api/handlers.
---

# Writing API Endpoints

## Gotchas

- Use `requireSessionAuth()`, not the legacy `authenticate()` helper.
- Responses must pass through `serializeForApi()`.
- Error responses use `{error: {code, message}}`.
```

## 4. Promote consequential failures to hooks

If a failure is expensive and mechanical to detect, do not rely on memory alone. Add a hook or permission rule.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git push --force*)",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-force-push.sh"
          }
        ]
      }
    ]
  }
}
```

## 5. Bound permissions

Allow the commands Claude Code runs constantly, keep risky operations on ask, and deny operations that should never happen in this repo.

```json
{
  "permissions": {
    "allow": [
      "Bash(pnpm test*)",
      "Bash(pnpm typecheck)",
      "Bash(git status*)"
    ],
    "deny": [
      "Bash(git push --force*)",
      "Bash(rm -rf*)"
    ]
  }
}
```

## 6. Close the loop with evidence

After the change, Claude Code should run the relevant checks, read the output, fix failures, and repeat until the signal is clean.

```text
1. Implement the endpoint.
2. Run `pnpm test -- users`.
3. Read the failure.
4. Fix the issue.
5. Re-run `pnpm test -- users`.
6. Run `pnpm typecheck`.
7. Report the passing checks.
```

## 7. Capture the lesson

If the work exposed a new recurring gotcha, update the right artifact before moving on: `CLAUDE.md` for broad project context, `.claude/rules/` for path-specific rules, a skill for reusable procedure knowledge, or a hook for a hard guarantee.
