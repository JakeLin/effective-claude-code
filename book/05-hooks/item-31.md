---
item: 31
theme: hooks
title: "Use `PostToolUse` to keep the working tree in a known state"
tags: [hooks, posttooluse, formatters, invariants]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [9, 11]
things_to_remember:
  - "`PostToolUse` runs after a tool succeeds — the right place to enforce invariants the model shouldn't have to remember"
  - "Auto-run formatters, linters, and type-checkers after `Edit|Write` to keep the diff in a canonical state"
  - "Surface failures back to Claude via stderr and a non-zero exit so the next turn can react"
  - "Keep `PostToolUse` hooks fast — they run on every matching edit and the user is waiting"
agent_steps:
  - "Configure `PostToolUse` hooks matching `Edit|Write` to run the project's formatter and quick lint check"
  - "On lint or type-check failure, exit non-zero and write the error to stderr so Claude sees it and can fix on the next turn"
  - "Limit the hook to commands that finish in seconds — a 30-second test suite belongs in CI, not in `PostToolUse`"
  - "Use `PostToolUseFailure` (separate event) to react to *tool* failures, not to lint failures of successful edits"
---

## Why this matters

`PostToolUse` runs immediately after a tool succeeds. It's where you enforce invariants that aren't worth asking the model to remember: run the formatter so the diff is canonical, run a quick lint pass to catch obvious mistakes, run a type-check on the touched files. These are mechanical operations whose value is consistency — they don't depend on Claude understanding the project's style; the harness just makes the project's style true.

The leverage is not just that the work happens — it's that the working tree is always in a known state between turns. Without `PostToolUse`, the model edits a file, the lint failure shows up two turns later when CI runs, and the original context for the change is gone. With `PostToolUse` running a formatter and lint on every edit, the failure surfaces in the same turn — Claude sees the lint error in the same context that produced the edit and can fix it before moving on. That's the loop that keeps a session from accumulating sediment.

The constraint is latency. `PostToolUse` runs on every matching event, and the user is waiting for the next turn while it runs. A formatter that takes 200ms is invisible; a test suite that takes 30 seconds is unusable. The rule of thumb: anything that should run on every edit goes in `PostToolUse`; anything that takes long enough to notice goes in CI or in an explicit `/verify` step the user invokes.

Failures should be loud. Exit non-zero and write the diagnostic to stderr. The harness surfaces stderr to Claude, so the next turn starts with the error visible — no separate prompt needed. A silent `PostToolUse` failure (exit 0 even though the lint errored) is worse than no hook at all; the working tree drifts and nobody notices until much later.

## What to avoid

`PostToolUse` hooks that run the entire test suite on every edit — the latency is unacceptable and the failure mode (slow turns) trains users to disable hooks. Hooks that silently swallow errors. Hooks that try to do more than enforce invariants — running deploy steps, sending notifications, or anything else that should live in a different event family.

## What to do instead

Use `PostToolUse` with a tight matcher (`Edit|Write`, or specific file patterns) and run only the operations that finish in well under a second. Formatters, fast linters, type-checks scoped to changed files. Exit non-zero on failure with the diagnostic on stderr. Save slower verification — full test suites, integration checks — for explicit `/verify` invocations or CI.

For tool *failures* (not lint failures on success), use `PostToolUseFailure` instead. The two events have different signatures and different intents.

## Example

A `PostToolUse` hook running format-and-lint on every code edit:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "./.claude/hooks/format-and-lint.sh" }
        ]
      }
    ]
  }
}
```

```bash
#!/usr/bin/env bash
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path')

case "$path" in
  *.ts|*.tsx|*.js|*.jsx)
    npx prettier --write "$path" >/dev/null
    if ! npx eslint --quiet "$path" 1>&2; then
      exit 2
    fi
    ;;
  *.py)
    ruff format "$path" >/dev/null
    if ! ruff check "$path" 1>&2; then
      exit 2
    fi
    ;;
esac
```

Prettier and ruff format inline; eslint and ruff-check surface failures on stderr. When the lint fails, exit 2 — Claude sees the diagnostic in the next turn and fixes the edit before moving on. When everything passes, exit 0 silently and the user never notices the hook ran.

The pattern generalizes: `mypy`/`tsc` for type-checking changed files, `terraform fmt`/`tflint` for infra changes, `cargo fmt`/`cargo clippy` for Rust. The shape is always the same — narrow matcher, fast command, loud failure, silent success.
