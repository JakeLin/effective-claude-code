# Sample Skill

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

Use this skill when the task touches `src/api/handlers/**`.

## Gotchas

- Wrap every handler with `requireSessionAuth()` from `src/auth/middleware.ts`.
- Do not use the legacy `authenticate()` helper; it does not refresh session cookies.
- Do not return raw database rows; use `serializeForApi()` from `src/api/serialize.ts`.
- Error responses use `{error: {code, message}}`, not `{message}`.

## Verification

- Run `pnpm test -- api`.
- Run `pnpm typecheck`.
- If the endpoint has integration coverage, run `pnpm test:integration -- <resource>`.
```
