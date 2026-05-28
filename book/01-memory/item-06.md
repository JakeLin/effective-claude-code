---
item: 6
theme: memory
title: "Move path-specific guidance into `.claude/rules/`"
tags: [claude-md, rules, path-scoping, scaling]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [4, 5]
things_to_remember:
  - "Rules in `.claude/rules/` with `paths:` frontmatter load only when Claude touches matching files"
  - "Use narrow globs — `src/api/**/*.ts`, not `**/*`"
  - "One file per subsystem so the team knows where to add rules"
  - "Rules without `paths:` frontmatter load unconditionally — same context cost as CLAUDE.md"
agent_steps:
  - "When asked to add a rule that starts with 'when working in <path>' or only applies to specific files, propose `.claude/rules/<topic>.md` with a `paths:` glob instead of CLAUDE.md"
  - "Check that `paths:` globs are narrow enough that the rule loads only for relevant files"
  - "When creating a new rule file, group it by subsystem (e.g., `testing.md`, `api.md`) rather than by author or date"
---

## Why this matters

A rule that only matters in `src/api/` doesn't need to be in context when Claude is working on documentation. A rule that only applies to `*.tsx` files doesn't need to be in context when Claude is writing a migration. Putting those rules in CLAUDE.md taxes every session, including the ones that have nothing to do with them. Multiplied across a real project — frontend rules, backend rules, testing rules, migration rules, infra rules — you end up with hundreds of lines of context cost for rules that are relevant a fraction of the time.

`.claude/rules/*.md` with a `paths:` frontmatter field solves this. The rule is discovered at session start but only injected into context when Claude reads a file matching the glob. Frontend developers don't pay for backend conventions; nobody pays for API rules while editing the README. This is the primary mechanism for scaling Claude Code guidance past what fits in a single CLAUDE.md.

The other benefit is organizational: one file per subsystem makes it obvious where to add a new rule, which makes the system contribute-able. A flat CLAUDE.md eventually requires authors to scroll to find the right section; a `.claude/rules/api.md` file requires no searching.

## What to avoid

Letting CLAUDE.md grow with subsystem-specific rules. (A rule that starts "When working in `src/api/`…" is a candidate for relocation, not a candidate for CLAUDE.md.) Path-scoped rules with overly broad globs — `paths: ["**/*"]` defeats the entire mechanism. Rule files without `paths:` frontmatter at all — they load unconditionally and offer no advantage over putting the content in CLAUDE.md.

## What to do instead

For each rule, ask: "When does this matter?" If the answer is "only when touching X", move it to `.claude/rules/X.md` with a `paths:` glob narrow enough to match X and nothing else. Use the subsystem boundary the codebase already has — if your tests live in `tests/**`, that's your `paths:` glob.

Organize by topic, not by author or date. `testing.md`, `api.md`, `migrations.md`, `frontend.md`. New contributors know where to add a testing rule because there's a file called `testing.md`. This matters more than it sounds: rule files only stay useful if people remember to add to them.

## Example

A path-scoped rule file alongside a project CLAUDE.md.

```markdown
# ./CLAUDE.md (project-wide rules only)
- Build: `pnpm build`. Test: `pnpm test`.
- All code goes in `src/`. Anything in `scripts/` is throwaway tooling.
```

```markdown
# ./.claude/rules/api.md
---
paths:
  - "src/api/**/*.ts"
---

- Handlers live in `src/api/handlers/<resource>.ts`, one file per resource.
- Every handler returns `Result<Response, ApiError>` — never throw at this layer.
- Validate input with the `validate()` helper from `src/api/validation.ts`, not ad-hoc.
- Responses use snake_case keys. The serializer in `src/api/serialize.ts` handles this if you pass it your `Result.ok` value.
```

```markdown
# ./.claude/rules/migrations.md
---
paths:
  - "db/migrations/**/*.sql"
---

- Migrations are append-only once merged. Editing a merged migration breaks every other dev's local DB.
- Every migration has a paired rollback in `db/migrations/down/`.
- Run `pnpm db:lint` before committing — it catches the common locking pitfalls (see `db/MIGRATIONS.md`).
```
