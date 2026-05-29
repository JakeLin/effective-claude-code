---
item: 29
theme: hooks
title: "Reach for a hook only when you need a guarantee, not a nudge"
tags: [hooks, mindset, determinism]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [9]
things_to_remember:
  - "Hooks are deterministic harness logic — the model can't ignore them"
  - "Use a hook when the cost of a single failure is real; use CLAUDE.md or a skill when probabilistic compliance is fine"
  - "Every hook costs latency on every matching event — don't pay for guarantees you don't need"
  - "If you find yourself writing 'please always do X' in CLAUDE.md three times, X is probably a hook"
agent_steps:
  - "Before adding a hook, ask whether a CLAUDE.md instruction or skill gotcha would handle the case 95% of the time — if yes, prefer the softer mechanism"
  - "Reach for a hook when the failure mode is destructive, security-relevant, or otherwise expensive to recover from"
  - "When a CLAUDE.md instruction has had to be restated or strengthened more than twice, promote it to a hook"
  - "Audit existing hooks for ones that fire constantly but rarely act — they're paying latency for no guarantee"
---

## Why this matters

The three knowledge mechanisms — CLAUDE.md, skills, and hooks — sit on a spectrum from soft to hard. CLAUDE.md is durable instruction the model reads on every session and *usually* follows. Skills are descriptions Claude routes to when intents match and *usually* applies. Hooks are different: they're deterministic harness logic that runs whether the model wants them to or not. The model can't forget a `PreToolUse` hook the way it can forget a CLAUDE.md instruction. That's the whole point.

That difference is also the cost calculus. Hooks fire on every matching event, run a process (or HTTP call), and add latency. That's a price worth paying when the failure mode they prevent is real — a force-push to main, a `DROP TABLE` against the wrong database, a deployment to prod without the safety check. It's not a price worth paying for things the model already does correctly 99% of the time, or for tastes that a CLAUDE.md note would handle. A hook that almost never fires is paying latency on every event for a guarantee you don't really need.

The decision rule is concrete. Reach for a hook when: the cost of a single failure is real (security, destruction, expensive recovery); the rule is mechanical and easy to express as a matcher; or you've already restated the instruction in CLAUDE.md multiple times and Claude still drifts. Reach for the softer mechanism otherwise.

## What to avoid

Hooks that exist to enforce taste — "always use double quotes" — when a linter or formatter (run by a `PostToolUse` hook if you must, but really by a CI step) would handle it just as well. Hooks that try to encode the entire team CLAUDE.md as `UserPromptSubmit` filters. Hooks that match every event but only act on a narrow case — the matcher is the wrong shape.

## What to do instead

Start with CLAUDE.md or a skill. Watch what Claude actually does. If a specific failure mode keeps recurring despite written instruction, and the failure is consequential, promote it to a hook. Keep the hook's matcher narrow so it only fires when it might act. Treat each hook as paying ongoing latency for an ongoing guarantee — and make sure both sides of that trade are real.

## Example

CLAUDE.md — the right place for taste-level guidance the model usually follows.

```markdown
## Git workflow

- Never force-push without explicit user request.
- Prefer creating new commits over amending pushed commits.
```

Hook — for when the cost of "usually follows" is too high.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/block-force-push-to-main.sh"
          }
        ]
      }
    ]
  }
}
```

The CLAUDE.md note is sufficient for taste. The hook exists because "rewrite main's history" isn't recoverable by saying "oh, sorry" — so the guarantee has to live in the harness, not the prompt.
