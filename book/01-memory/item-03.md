---
item: 3
theme: memory
title: "Write instructions specific enough to verify"
tags: [claude-md, writing, specificity, adherence]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [1, 2]
things_to_remember:
  - "Concreteness is the single biggest determinant of CLAUDE.md adherence"
  - "If you can't verify a rule was followed, Claude probably can't tell either"
  - "Replace soft verbs (handle, consider, try, properly) with commands and paths"
  - "Rules that include exact commands, paths, or file names work; rules that don't, don't"
agent_steps:
  - "When asked to add a rule to CLAUDE.md, check whether it names specific commands, paths, or file names"
  - "If the rule uses soft verbs (properly, nicely, correctly, handle, consider), propose a concrete rewrite"
  - "When the user phrases an instruction vaguely, ask what 'correct' looks like in this codebase and capture the concrete answer"
---

## Why this matters

Adherence to CLAUDE.md correlates almost entirely with how specifically the rule is written. "Use 2-space indentation" reliably works. "Format code properly" almost never does. The difference isn't that Claude is being lazy with the second one — it's that "properly" requires Claude to invent a standard, and the standard it invents won't match yours session to session.

The same principle is what makes good code review work: specific feedback ("rename `data` to `usersByEmail`") changes behavior, vague feedback ("clean up the variable names") doesn't. CLAUDE.md inherits this property from prose generally. Concrete rules are followed because they leave no judgment call.

A second benefit: specific rules are testable. "API handlers live in `src/api/handlers/`" is a `git grep` away from being verified. "Keep files organized" is not. If you can't tell at a glance whether a rule was followed, you can't notice it being violated, and you can't improve it.

## What to avoid

Aspirational language: "write maintainable code", "follow best practices", "be careful with X". Soft verbs that defer decisions to Claude: "handle errors appropriately", "consider performance", "try to keep it simple". Rules that depend on shared subjective judgment Claude doesn't have. Adverbs that sound like rigor but aren't: "properly", "correctly", "carefully", "nicely".

## What to do instead

Convert every rule into something that names a command, a path, a file, a constant, or a verifiable outcome. When you find yourself writing "properly" or "correctly", stop and ask: *properly how?* What would *improper* look like? Capture that.

A useful test: read the rule out loud and ask whether a new teammate could follow it on day one without asking a clarifying question. If yes, it's specific enough. If they'd need to ask "what counts as X?", the rule needs to answer that in the rule.

## Example

The same intentions, written badly and well.

```markdown
## Conventions
- Write good tests
- Handle errors properly
- Keep components small
- Format code nicely
- Use the framework correctly
```

```markdown
## Conventions
- Every new public function in `src/api/` needs a test in the matching `__tests__/` directory.
- Service-layer code returns `Result<T, E>`; only the HTTP boundary throws.
- React components in `src/components/` stay under 150 lines — split when you cross it.
- Run `pnpm format` before committing. CI rejects diffs that change on `pnpm format --check`.
- Use the `<Form>` component for forms, not raw `<form>` tags. (`<Form>` wires up our validation hook.)
```
