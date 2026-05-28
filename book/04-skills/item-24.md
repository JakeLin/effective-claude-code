---
item: 24
theme: skills
title: "Skills earn their keep on gotchas and non-obvious knowledge — update them every time Claude hits a new failure mode"
tags: [skills, gotchas, iteration, knowledge]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [1, 3]
things_to_remember:
  - "The highest-signal content in a skill is what pushes Claude out of its defaults — gotchas, conventions, project-specific footguns"
  - "Don't restate what Claude already knows; it's context overhead with no behavior change"
  - "Treat skills as living artifacts — the gotchas section should grow every time Claude makes a mistake using the skill"
  - "Capture the *specific failure*, not a general principle — 'never use camelCase here, the API expects snake_case' beats 'follow API conventions'"
agent_steps:
  - "When writing a new skill, lead with what's non-obvious — defaults Claude would get wrong, project-specific conventions, footguns from the team's history"
  - "When Claude fails while using a skill, add the failure to the skill's gotchas section before fixing it — capture the lesson"
  - "Periodically review skills for content that restates obvious behavior; trim it"
  - "Make gotchas specific: file paths, exact patterns to avoid, concrete wrong vs. right examples"
---

## Why this matters

A skill that restates things Claude already does correctly is pure overhead — it costs context, it costs the maintenance burden of keeping it current, and it changes no behavior. The signal in a skill is the delta from default: the convention Claude wouldn't have guessed, the gotcha that bites first-timers, the project-specific reason a normal approach fails here. Without that signal, the skill is decoration.

Anthropic's internal experience converged on the same conclusion: the most useful section of any skill is the gotchas section, and the best skills are the ones where the gotchas section grew over time. A skill written from scratch on day one captures what the author predicted would be hard. The skill that's been in use for six months captures what was *actually* hard — the failures, the misreads, the wrong defaults Claude picked. That accumulated knowledge is what makes a skill compound in value.

The iteration loop is concrete: when Claude makes a mistake using a skill, the first move is to fix the skill, not just the immediate output. Add a gotcha. Be specific — the exact pattern that failed, what should happen instead. "Don't use camelCase for column names; this API is snake_case" is useful. "Follow naming conventions" is not. The next time Claude reaches for that skill, the gotcha is in context, and the failure doesn't repeat.

## What to avoid

Skills that read like a beginner tutorial of a library Claude already knows. Skills that restate generic best practices ("write clear code," "handle errors") with no project-specific content. Skills that get written once and never updated, even after the team has accumulated three distinct ways Claude misuses them.

## What to do instead

Front-load the non-obvious. Lead the skill body with the defaults Claude would otherwise get wrong, the conventions specific to this project, the footguns drawn from real failure modes. Maintain an explicit `Gotchas` section (or sibling file) and update it the moment Claude trips. Capture the failure concretely — file paths, exact patterns, wrong-vs-right examples — not as a general principle.

When you reach for the same correction in a code review more than twice, that's a gotcha. Add it to the relevant skill before the third time.

## Example

Low-signal — restates defaults.

```markdown
# Writing API Endpoints

When writing an endpoint, you should:
- Handle errors gracefully
- Validate input
- Return appropriate status codes
- Write tests
```

Claude already does this. The skill adds nothing.

High-signal — captures what's project-specific.

```markdown
# Writing API Endpoints

## Gotchas

- **Auth wrapper is required.** Every endpoint must be wrapped in
  `requireSessionAuth()` from `src/auth/middleware.ts`. The legacy
  `authenticate()` helper exists but does not refresh the session cookie
  and will silently log users out on long requests.

- **Don't return raw DB rows.** All responses go through
  `serializeForApi()` in `src/api/serialize.ts`. Raw rows leak
  internal columns like `tenant_id` that we exclude from external
  responses.

- **Pagination cursors are opaque base64.** Do not synthesize cursors
  from row IDs — the format is `base64({id, tenant_id, hmac})` and
  the client validates the HMAC. See `src/api/cursor.ts`.

- **Error responses use `{error: {code, message}}`, not `{message}`.**
  The mobile client crashes on the bare-message shape.
```

The second version reads like notes from someone who's been bitten. That's because it is.
