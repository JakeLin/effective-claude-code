# Sample `CLAUDE.md`

```markdown
# Project Guide

## Build and test

- Install dependencies with `pnpm install`.
- Run `pnpm test` for unit tests.
- Run `pnpm typecheck` before committing TypeScript changes.
- Run `pnpm test:integration` before changing `src/api/` or `src/db/`.

## Repository layout

- `src/api/handlers/` contains API handlers, one resource per file.
- `src/db/` contains shared database helpers.
- `tests/fixtures/` contains canonical test data. Prefer fixtures over inline mocks.

## Conventions

- Migration files are append-only once merged.
- New environment variables must be added to `.env.example` in the same commit.
- Public API responses must use `serializeForApi()` before returning database data.

## Verification

- Run the narrowest relevant test first.
- Run the full type-check before reporting completion.
- For UI changes, verify the running app visually, not by source inspection alone.
```
