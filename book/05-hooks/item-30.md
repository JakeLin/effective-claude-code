---
item: 30
theme: hooks
title: "Block dangerous operations with `PreToolUse` and scoped matchers"
tags: [hooks, pretooluse, guardrails, safety]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [9, 29]
things_to_remember:
  - "`PreToolUse` fires before a tool runs and can block it — the only mechanism that prevents a destructive call before it happens"
  - "Use the matcher to narrow scope (`Bash`, `Edit|Write`, `mcp__github__merge_pull_request`) — broad matchers run a lot but rarely act"
  - "Return `permissionDecision: deny` with a reason so Claude understands what was blocked and can try a different approach"
  - "Pair guardrails with permissions — `PreToolUse` is the safety net when permission rules can't express the constraint"
agent_steps:
  - "When the user wants to block a specific destructive operation, write a `PreToolUse` hook with a matcher narrowed to the relevant tool and a script that inspects the input"
  - "In the hook script, emit `{\"hookSpecificOutput\": {\"hookEventName\": \"PreToolUse\", \"permissionDecision\": \"deny\", \"permissionDecisionReason\": \"<why>\"}}` on stdout to block with a clear reason"
  - "Prefer narrow matchers over broad ones — `Bash(rm *)` or `mcp__github__merge_pull_request` rather than `*`"
  - "Test the hook by deliberately triggering it once — verify the deny path produces a readable message Claude can act on"
---

## Why this matters

`PreToolUse` is the only mechanism that can stop a tool call *before* it happens. Permissions rules can ask the user, but they require human-in-the-loop attention and they only express what the rule language can match. `PreToolUse` runs arbitrary code against the tool input and decides allow, deny, or ask — and it does so in milliseconds, deterministically, every time. That's the right shape for guarding operations whose failure mode is destructive or irreversible.

The canonical use cases are exactly the ones whose damage you can't take back: `rm -rf` against the wrong path, `DROP TABLE` against prod, `git push --force` to a protected branch, an MCP tool that mutates a shared resource. For each, a `PreToolUse` hook can inspect the tool's input, recognize the dangerous shape, and deny it with a reason Claude can read and respond to. Claude doesn't have to remember the rule; the harness enforces it.

The matcher is the second half of the design. A `PreToolUse` hook with matcher `"*"` fires on every tool call and pays latency for events it can't possibly act on. A matcher like `"Bash"` narrows to shell commands — better, but the hook still runs on every `ls`. A matcher like `"Bash(rm *)"` or a regex like `"^(Bash|Edit|Write)$"` runs only when there's something to evaluate. Narrow matchers are also more honest about what the hook is for — they document the guarantee directly in the configuration.

The decision flow back to Claude matters too. Returning `permissionDecision: deny` without a `permissionDecisionReason` blocks the action but leaves Claude guessing at why. Returning it *with* a reason — "force-push to main is blocked; create a PR instead" — gives Claude something to react to, so the next move can route around the block rather than retry the same command.

## What to avoid

Broad `*` matchers paired with hook scripts that filter internally. Hooks that deny without a reason. Hooks that try to encode every permission rule from `settings.json` — those belong in `permissions`, not in a `PreToolUse` script. Guards that match on stale patterns (e.g., a regex that hasn't been updated for the new CLI version of a tool) and silently let through what they were meant to block.

## What to do instead

Identify the specific destructive operations whose failure is unrecoverable. Write a `PreToolUse` hook with a matcher narrowed to the relevant tool. In the script, parse `tool_input`, decide, and emit a JSON decision on stdout with a reason. Test by deliberately tripping it — confirm the deny path produces the message you intended, and confirm the script exits cleanly on the no-op path so it doesn't add latency for nothing.

## Example

A `PreToolUse` hook that blocks force-pushes to protected branches:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "./.claude/hooks/guard-force-push.sh" }
        ]
      }
    ]
  }
}
```

```bash
#!/usr/bin/env bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

if [[ "$command" =~ git[[:space:]]+push.*--force ]] && \
   [[ "$command" =~ (main|master|production) ]]; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Force-push to a protected branch is blocked. Create a PR or push to a feature branch instead."
    }
  }'
  exit 0
fi

exit 0
```

The matcher narrows to `Bash`. The script narrows further by inspecting the command. The deny path includes a reason that tells Claude what to do instead, so the next turn moves toward a safe approach rather than retrying the blocked one.

Guarding a destructive MCP tool works the same way:

```json
{
  "matcher": "mcp__github__merge_pull_request",
  "hooks": [
    { "type": "command", "command": "./.claude/hooks/require-approval-for-merge.sh" }
  ]
}
```

The same shape — narrow matcher, decisive script, clear reason — generalizes to any tool whose damage you can't take back.
