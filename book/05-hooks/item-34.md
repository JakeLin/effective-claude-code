---
item: 34
theme: hooks
title: "Make hooks fail loudly — design for the exit code, not the happy path"
tags: [hooks, failure, debugging, observability]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [29]
things_to_remember:
  - "A silently-broken hook is worse than no hook — the guarantee evaporates without a signal"
  - "Exit 0 = proceed, exit 2 = blocking error with stderr shown to user, other non-zero = non-blocking error"
  - "Write decisions as JSON on stdout; write diagnostics to stderr; never mix the two"
  - "Test every hook by deliberately triggering both the success and failure paths before relying on it"
agent_steps:
  - "In hook scripts, emit JSON decisions to stdout and diagnostics to stderr — never mix them on the same stream"
  - "Use exit 2 for blocking errors you want visible to the user; use exit 0 with a JSON decision for normal allow/deny flow"
  - "Add a fail-safe: if the hook script crashes or its dependencies are missing, log the error and exit non-zero rather than swallowing it"
  - "Before relying on a new hook, run a manual test that deliberately trips it — verify the failure path produces a visible signal"
---

## Why this matters

A hook is a promise. "This won't happen" or "this will always happen" or "we stop when the tests pass" — each is a guarantee the harness is supposed to enforce. A hook that silently does nothing because of a path typo, a missing dependency, or an unhandled error breaks the promise without telling anyone. The user thinks the guardrail is in place; it isn't. Worse, the failure correlates with exactly the cases the hook was meant to handle — the unusual ones — so the silent break shows up in production rather than during normal use.

The protocol the harness uses is small and specific: exit 0 means proceed (and stdout, if present, is parsed as a JSON decision); exit 2 means blocking error with stderr shown to the user; other non-zero codes mean non-blocking error. JSON decisions go on stdout; human-readable diagnostics go on stderr. Mixing them — printing a stack trace to stdout, or a JSON object to stderr — turns a parseable signal into noise the harness can't act on.

Designing for the failure path means three concrete habits. First, separate streams: every decision is JSON on stdout; every error message is plain text on stderr. Second, choose the exit code deliberately — `exit 2` when you genuinely want the user to see the error, `exit 1` for a soft warning, `exit 0` when the hook decided to let things proceed (with or without a JSON decision payload). Third, make missing dependencies loud: if your hook script needs `jq` and it's not installed, that should produce an error message and a non-zero exit, not a silent pass-through.

The other half is testing. Hooks fire on real events and there's no replay mechanism — once a destructive operation slipped through because the hook was broken, the damage is done. Before relying on a hook, run a manual test that deliberately trips it. For a `PreToolUse` guard: try to do the thing it should block, confirm the deny path produces a visible reason. For a `PostToolUse` formatter: edit a deliberately-broken file, confirm the failure surfaces. The test pays for itself the first time the hook would have silently broken.

## What to avoid

Hooks that catch all errors and exit 0 to "be safe." Hooks that mix JSON decisions with debug logging on stdout. Hook scripts that depend on tools (`jq`, `python3`, project-specific binaries) without checking that they're present. Hooks deployed without being tested against their failure case. Hooks whose stderr output is so noisy users learn to ignore it — making the loud signal indistinguishable from background chatter.

## What to do instead

Treat the hook script as production code. Validate inputs, check dependencies, separate stdout (decisions) from stderr (diagnostics), choose exit codes deliberately. Log enough on stderr to debug the hook itself when something goes wrong — but only when something is going wrong. On the success path, stay quiet so real failures are visible.

Run a manual test of every new hook against both paths before relying on it. Re-run the tests after any change to the hook or its dependencies.

## Example

A `PreToolUse` hook with proper stream and exit discipline:

```bash
#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null; then
  echo "guard-force-push: jq not installed — hook cannot evaluate input" >&2
  exit 2
fi

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

if [[ -z "$command" ]]; then
  exit 0
fi

if [[ "$command" =~ git[[:space:]]+push.*--force ]] && \
   [[ "$command" =~ (main|master|production) ]]; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Force-push to a protected branch is blocked."
    }
  }'
  exit 0
fi

exit 0
```

Three concrete habits: dependency check (jq must be present — if missing, exit 2 with a stderr message); stream separation (decisions to stdout via jq, errors to stderr via `>&2`); intentional exit codes (2 for missing dependency so the user sees it; 0 with JSON for the decide path; 0 silent for the no-op path).

To test it, manually trigger both paths once:

```bash
# Should deny:
echo '{"tool_input":{"command":"git push --force origin main"}}' | ./guard-force-push.sh

# Should allow:
echo '{"tool_input":{"command":"ls -la"}}' | ./guard-force-push.sh
```

Confirm the first produces the JSON deny on stdout and exit 0; the second produces empty output and exit 0. Once both paths are verified, the hook is safe to rely on. Until then, it's a promise that hasn't been checked.
