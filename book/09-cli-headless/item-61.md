---
item: 61
theme: cli-headless
title: "Chain headless turns with session IDs, not one giant prompt"
tags: [headless, sessions, state, resume, workflow]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [51, 55, 59]
things_to_remember:
  - "Headless runs are stateless by default — each `-p` invocation starts fresh unless you carry the session forward"
  - "Capture the `session_id` from JSON output and pass it to `--resume` to continue with full context on the next turn"
  - "`--continue` resumes the most recent session in the directory; `--fork-session` branches a session without mutating the original"
  - "Chain focused turns instead of one mega-prompt — each step stays small, observable, and individually verifiable"
agent_steps:
  - "Run the first turn with `--output-format json` and capture `.session_id`"
  - "Continue the conversation by passing that id to `--resume <id>` on subsequent invocations"
  - "Use `--continue` for the simple case of resuming the latest session in the current directory"
  - "Use `--fork-session` to branch from an existing session when you want to try a path without altering the original"
  - "Break multi-step headless work into a sequence of resumed turns rather than one prompt that does everything"
---

## Why this matters

Each `claude -p` invocation is, by default, a fresh start — it runs, prints, exits, and forgets. That's the right default for a Unix utility, but it means multi-step headless work needs a way to carry context from one turn to the next. The naive workaround is to cram the entire job into a single enormous prompt so it all happens in one stateless run. That fights everything the earlier chapters argued for: a mega-prompt is hard to bound, hard to observe, and hard to verify, and when it fails you re-run the whole thing instead of the step that broke. Statefulness across invocations is what lets headless work stay composed instead of monolithic.

Session IDs provide that statefulness. Run the first turn with `--output-format json`, read `.session_id` from the envelope (the same envelope from the structured-output Item), and pass it to `--resume` on the next invocation — the new turn picks up with the full prior context intact. Now a multi-step job is a *sequence* of focused turns, each small enough to bound with limits and check before moving on, rather than one opaque run. It's the headless expression of the same principle the orchestration chapter applied interactively: break the work into steps, keep each step in budget, verify as you go. The session id is just how the thread survives between processes.

The convenience variants cover the common shapes. `--continue` resumes the most recent session in the current directory without your having to track an id — handy for a quick follow-up in the same working context. `--fork-session` branches from an existing session into a new one, so you can explore an alternative path without mutating the original — useful when a script needs to try several continuations from a common setup, or when you want a checkpoint you can return to. Between explicit `--session-id`/`--resume`, the convenience of `--continue`, and the branching of `--fork-session`, you have the full vocabulary to script stateful conversations out of individually stateless commands — which is what turns a pile of one-shot invocations into a coherent automated workflow.

## What to avoid

Packing a whole multi-step job into one giant prompt to avoid dealing with state — it's unbounded, opaque, and all-or-nothing to re-run. Throwing away the `session_id` from the first turn and then having no way to continue with context. Re-feeding the entire prior conversation as text into each new prompt by hand when `--resume` carries it for you. Mutating a session you wanted to preserve, when `--fork-session` would have branched a throwaway copy.

## What to do instead

Carry the thread explicitly. Capture `session_id` from the first turn's JSON and pass it to `--resume` to continue with full context; reach for `--continue` when you just need the latest session in the directory. Use `--fork-session` to branch when you want to try a path without disturbing the original. And structure multi-step headless work as a chain of focused, resumed turns — each one small, bounded, and verifiable — rather than a single prompt that tries to do the whole job at once.

## Example

Chaining turns by threading the session id:

```bash
# Turn 1 — capture the session id from the JSON envelope
sid=$(claude -p "analyze the schema and propose a migration plan" \
        --output-format json | jq -r '.session_id')

# Turn 2 — resume with full context, bounded per step
claude -p "implement phase 1 of the plan" \
  --resume "$sid" --max-turns 10 --max-budget-usd 0.40

# Turn 3 — still the same thread
claude -p "now phase 2, and run the tests" \
  --resume "$sid" --max-turns 10 --max-budget-usd 0.40
```

Each turn is small, capped, and checkable — and if phase 2 fails, you re-run *phase 2*, not the entire job. The convenience forms for common cases:

```bash
# resume the most recent session here, no id bookkeeping
claude -p "address the review comment about error handling" --continue

# branch to try an alternative without touching the original session
claude -p "what if we sharded by tenant instead?" --resume "$sid" --fork-session
```

The contrast is the mega-prompt — "analyze the schema, plan the migration, implement every phase, and run the tests" in one stateless shot — which is unbounded, hard to observe, and forces a full re-run on any failure. Threading the session turns that into a sequence of small steps you can bound and verify, which is exactly the composed shape headless work should have.
