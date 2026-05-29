---
item: 9
theme: commands
title: "Pick `/clear`, `/compact`, or `/rewind` based on what state you want to keep"
tags: [commands, sessions, context]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [8, 51]
things_to_remember:
  - "`/clear` for topic switches, `/compact` for same task with full context, `/rewind` to undo a bad turn"
  - "`/compact` keeps task and conversation continuity; `/clear` discards everything but the file-system state"
  - "`/rewind` recovers without restarting and can roll back code too"
  - "Use `/branch` when you want both the current path and a divergent one — not either/or"
agent_steps:
  - "When context is nearly full but the task is unfinished, propose `/compact` with focus instructions describing what to keep"
  - "When the user has finished a task and is starting an unrelated one, propose `/clear`"
  - "When a recent turn produced the wrong direction, propose `/rewind` rather than `/clear`"
  - "When the user wants to explore an alternative path while keeping the current one, propose `/branch` (alias `/fork`)"
---

## Why this matters

The three session primitives look adjacent but solve different problems. `/clear` starts a new conversation — context goes to zero, file system stays as it is, the prior conversation is recoverable from `/resume`. `/compact` summarizes the current conversation into a smaller representation and keeps going; the task and continuity survive, the verbatim history doesn't. `/rewind` steps back to a previous turn (alias `/checkpoint` and `/undo`) — both conversation and, if configured, code can return to an earlier state.

Confusing them is expensive in characteristic ways. `/clear` when you meant `/compact` loses the task and you re-explain it from scratch. `/compact` when you meant `/rewind` summarizes the bad turn into the compacted history and you carry the error forward. `/rewind` when you meant `/clear` lands you back somewhere in the middle of a finished task and you spend a turn navigating out.

The mental model that makes the choice obvious: ask what state you want to keep. *Everything except this conversation* → `/clear`. *The task and outcome, but free up context* → `/compact`. *Walk back to before something went wrong* → `/rewind`. *Both paths from a decision point* → `/branch`.

## What to avoid

Treating these as interchangeable "reset" commands. Reaching for `/clear` reflexively when the conversation feels long — that's usually a `/compact` situation. Using `/compact` to escape a bad turn — the bad turn gets baked into the summary. Restarting Claude Code entirely when `/rewind` would have taken you back to the point you wanted.

## What to do instead

Match the command to the state you want preserved. When context is filling but you're mid-task, `/compact` with focus instructions ("keep the architectural decisions, drop the file reads") preserves what matters. When you're switching topics for real, `/clear` is cleaner and your old conversation is still in `/resume`. When something went sideways in the last few turns, `/rewind` is the targeted fix.

`/branch` (or `/fork`) is the underused one. When you're about to try a risky refactor or explore a design alternative, branching means the current conversation is preserved untouched while you experiment.

## Example

A scenario for each:

```text
> [10 turns into a payment integration, context at 78%]
> /compact keep the schema decisions and the test results; drop the file reads

[task continues with a smaller, focused history]
```

```text
> [finished the payment work, want to start a docs cleanup]
> /clear

[fresh conversation; previous one available via /resume]
```

```text
> [Claude just refactored a file the wrong way]
> /rewind

[picker appears showing previous turns; select the turn before the bad refactor]
```

```text
> [at a fork between two valid implementations]
> /branch try-event-sourcing

[current conversation preserved; new branch starts for the experiment]
```
