---
item: 68
theme: agent-teams
title: "Reach for an agent team only when subagents and a single session both fall short"
tags: [agent-teams, subagents, cost, decision, beta]
claude_code_version: "2.1.150"
stability: beta
status: current
related_items: [52, 15]
things_to_remember:
  - "A teammate is a full independent session (its own context, CLAUDE.md, MCP, skills); a subagent is a context fork that returns a summary"
  - "Teams are heavyweight — N teammates means N full sessions and roughly N× the token cost"
  - "Use a team only for genuinely parallel, independent workstreams that each need full project context and run long without blocking each other"
  - "For sequential work, same-file edits, or tight dependencies, a single session or subagents is cheaper and simpler"
agent_steps:
  - "Before forming a team, ask whether the work is genuinely parallel and independent — if not, use a single session"
  - "If a side task just needs isolated legwork returning a summary, use a subagent, not a teammate"
  - "Choose a team only when each workstream needs its own full context and the streams can progress without blocking each other"
  - "Weigh the N× token cost of N teammates against the parallelism gained before spawning a team"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

Agent teams sit at the top of a ladder of options, and the temptation is to reach for the top rung first. The rungs are: a single session (one context, sequential work), subagents (context forks that do isolated legwork and return a summary to one parent), and teams (multiple full, independent sessions coordinating as peers). Each is more powerful and more expensive than the last. A team is genuinely different from subagents — a teammate is a *whole* Claude Code session with its own context window, its own loaded CLAUDE.md, MCP servers, and skills, and teammates coordinate with each other directly rather than reporting up to a single parent. That's real multi-agent parallelism, not one mind delegating.

The weight is the catch. N teammates is N full sessions, which means roughly N times the token cost, plus a coordination problem that a single session simply doesn't have. That cost is justified only by a specific shape of work: genuinely parallel, genuinely independent workstreams, each of which needs full project context and can run for a long stretch without waiting on the others. Three teammates owning three loosely-coupled modules, or testing three competing debugging hypotheses in parallel, or investigating a question from three angles — these earn the cost because the parallelism is real and the streams don't block each other. The independence is what makes the spend pay off.

When the work *isn't* that shape, something cheaper is also better. Sequential work — finish one thing, start the next — wants a single session; spinning up a team adds cost and coordination for parallelism you can't use. Tightly-coupled work, or edits to the same files, wants a single session too, because teammates working the same code is the collision problem of the worktrees chapter at a larger scale. And a side task that just needs isolated legwork returning a compact answer is the textbook subagent case (Item 52) — a full teammate is overkill for it. The rule is to climb the ladder only as far as the work demands: single session by default, subagents for isolated legwork, and a team only when both of those genuinely fall short.

## What to avoid

Forming a team for sequential work, paying N× cost for parallelism the task can't use. Using teammates where subagents fit — a side investigation that returns a summary doesn't need a full independent session. Putting teammates on tightly-coupled code or the same files, recreating collision problems at session scale. Reaching for the most powerful primitive by default instead of the cheapest one that fits.

## What to do instead

Climb the ladder deliberately. Default to a single session for sequential or tightly-coupled work. Use subagents when a side task needs isolated legwork that returns a summary. Reserve an agent team for the case it's built for: genuinely parallel, independent workstreams that each need full project context and can progress without blocking one another — and only after weighing the N× token cost against the parallelism you'll actually gain.

## Example

The decision, walked down the ladder:

```text
Task: "fix this one failing test"
  → Single session. Sequential, one context. No team, no subagent.

Task: "find everywhere the legacy API is called" (then implement a fix)
  → Subagent for the search (noisy legwork, compact result),
    main session implements. Item 52, not a team.

Task: "migrate three independent, loosely-coupled services at once,
       each needing full project context, over several hours"
  → Agent team. Three teammates, three workstreams, real parallelism
    that justifies 3× the token cost.

Task: "refactor the auth module, then update its callers, then its tests"
  → Single session. Tightly coupled and sequential — a team would
    only add cost and collisions.
```

Only the third task clears the bar: parallel, independent, full-context, long-running. The others are cheaper and cleaner one rung down. The question to ask before forming a team is always the same — is this genuinely parallel and independent enough to be worth N full sessions? — and most of the time the honest answer sends you back to a single session or a subagent.
