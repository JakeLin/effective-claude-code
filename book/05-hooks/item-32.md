---
item: 32
theme: hooks
title: "Use the `Stop` hook to drive Claude toward a terminal condition"
tags: [hooks, stop, automation, loops]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [9]
things_to_remember:
  - "`Stop` fires when Claude finishes a turn — a hook there can decide whether the work is actually done"
  - "Return `{decision: 'block', reason: '...'}` to keep Claude going; return success to release control to the user"
  - "Use a deterministic check (tests pass, lints clean, file exists) as the terminal condition — not 'does it look done'"
  - "Cap the loop with a max-turns or an external timeout — a runaway Stop hook will burn tokens until something else stops it"
agent_steps:
  - "When the user wants Claude to keep working until a condition is met, write a `Stop` hook that runs the check and returns `{decision: 'block', reason: '...'}` while the condition is unmet"
  - "Make the terminal condition deterministic — exit codes of tests, type-checks, validators — not subjective judgments"
  - "Include the actual failure output in the `reason` so Claude has the diagnostic to act on next turn"
  - "Always pair the hook with an upper bound (max turns, wall-clock timeout) to prevent runaway loops"
---

## Why this matters

By default, Claude finishes a turn and returns control to the user. The `Stop` hook intercepts that handoff: it runs when the model is about to stop and can decide *no, you're not done — keep going*. That single capability turns an interactive session into a goal-driven loop. The most common form: run the tests; if they fail, return `{decision: "block", reason: "tests failed: <output>"}`, and Claude keeps working until the tests pass. Combine it with the SDK or headless mode and you have deterministic outcomes from a stochastic system — the harness enforces the terminal condition, and the model just keeps iterating toward it.

The shape that works has two parts. First, the terminal condition has to be deterministic — an exit code, a file existing, a lint pass, a type-check result. "Does it look right" is not a terminal condition; "did `npm test` exit 0" is. Second, the failure path has to give Claude something to act on. Returning `block` with no reason means Claude knows to keep going but has no diagnostic — it'll loop without converging. Returning `block` with the actual stderr from the failing test gives Claude exactly the context the next turn needs.

The danger is that a `Stop` hook with no upper bound can drive the model forever. If the terminal condition is unreachable — broken test infrastructure, an external dependency that's down, a goal Claude has misread — the loop burns tokens until something else intervenes. Always cap it. The SDK exposes a max-turns flag; CI runners impose wall-clock timeouts; even an interactive session benefits from the hook itself counting iterations and giving up after a threshold.

## What to avoid

`Stop` hooks with subjective conditions ("looks complete to me") that always block. `Stop` hooks that return `block` without including the diagnostic — Claude knows to continue but doesn't know what to fix. Loops without an upper bound. Treating `Stop` as the place to do *any* end-of-turn work (logging, notifications) — the event family for that is different, and a `Stop` hook is for the binary decision "are we done?"

## What to do instead

Pick a deterministic check that captures the goal — tests passing, build green, file written, lint clean. Wrap it in a `Stop` hook that runs the check and decides. On block, include the diagnostic in the reason. Set a max-iteration cap, either via the SDK invocation or inside the hook itself. Treat the hook as part of the contract: when the loop ends, the goal really is met.

## Example

A `Stop` hook that keeps Claude going until the tests pass:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "./.claude/hooks/until-green.sh" }
        ]
      }
    ]
  }
}
```

```bash
#!/usr/bin/env bash
output=$(npm test 2>&1)
if [[ $? -eq 0 ]]; then
  exit 0
fi

iter_file=".claude/.until-green-count"
count=$(cat "$iter_file" 2>/dev/null || echo 0)
if (( count >= 10 )); then
  rm -f "$iter_file"
  jq -n --arg out "$output" '{
    decision: "block",
    reason: "Tests still failing after 10 iterations. Stopping to avoid runaway loop. Last output:\n\($out)\n\nReport the diagnosis instead of looping further."
  }'
  exit 0
fi
echo $((count + 1)) > "$iter_file"

jq -n --arg out "$output" '{
  decision: "block",
  reason: "Tests are still failing. Address the failure and try again:\n\($out)"
}'
```

When `npm test` exits 0, the hook exits 0 — control returns to the user, loop ends. When it fails, the hook returns `decision: block` with the actual test output, so the next turn starts with the diagnostic in context. The iteration counter caps the loop at ten attempts so a misread goal doesn't burn tokens indefinitely.

The same pattern works for any goal you can encode as an exit code: "build until type-check passes," "iterate until the schema validator approves," "keep refining until the benchmark beats the threshold." `Stop` is what turns Claude from an interactive assistant into a deterministic worker against an objective the harness knows how to check.
