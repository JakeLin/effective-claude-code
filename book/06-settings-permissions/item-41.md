---
item: 41
theme: settings-permissions
title: "Match the permission mode to the task, not your impatience"
tags: [permissions, modes, plan-mode, acceptEdits, workflow]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [38, 42]
things_to_remember:
  - "Permission mode sets the default disposition for unmatched operations: `default` prompts, `acceptEdits` auto-accepts edits, `plan` is read-only, `bypassPermissions` skips checks"
  - "Pick the mode for the work in front of you — `plan` for exploration, `acceptEdits` for a trusted edit-heavy loop, `default` when you want to stay in the loop"
  - "`plan` mode is read-only and overrides allow rules — writes are blocked even if an Edit(...) rule would permit them, preserving the read-only guarantee"
  - "Mode is a per-session disposition, not a permanent setting — switch it as the task changes rather than living in the most permissive one"
agent_steps:
  - "Use plan mode when the task is investigation or design — it guarantees read-only exploration even against allow rules"
  - "Use acceptEdits when you're in a tight, trusted edit-test loop and prompting on every file write is pure friction"
  - "Use default mode when the work is consequential enough that you want to approve operations as they come"
  - "Switch modes as the task phase changes (explore → implement → verify) rather than defaulting to the most permissive mode"
---

## Why this matters

Permission mode sets the *default disposition* for operations that no `allow`, `ask`, or `deny` rule matches. In `default` mode, those operations prompt. In `acceptEdits`, file edits (and common filesystem commands like `mkdir` and `mv`) are auto-accepted while other operations still prompt. In `plan` mode, the session is read-only — exploration and analysis, no writes. In `bypassPermissions`, checks are skipped almost entirely. The mode isn't a convenience knob; it's a statement about how much you trust the work in front of you to proceed without your eyes on it.

The mistake is choosing the mode for your patience instead of for the task. Prompts are mildly annoying, so the path of least resistance is to live permanently in the most permissive mode that stops them — and now an investigation that should have touched nothing is auto-accepting edits, or a delicate production-adjacent change is sailing through without review. The right mode is the one that matches the *phase of work*: read-only when you're exploring, edit-accepting when you're grinding through a trusted refactor loop, prompting when the stakes are high enough that you want to approve operations as they happen.

`plan` mode deserves special mention because it offers a guarantee the others don't: it's read-only even against your allow rules. If you have `Edit(/src/**)` allowed but you're in plan mode, writes are still blocked — the mode overrides the allow to preserve the read-only contract. That makes plan mode genuinely safe for "go understand this codebase and propose an approach" tasks, where the worst outcome you want to permit is a wrong opinion, not a wrong edit. Knowing each mode's actual guarantee lets you pick deliberately instead of defaulting to whatever silences the most prompts.

## What to avoid

Living in `acceptEdits` (or worse) all the time because prompts annoy you, so exploration tasks quietly start writing files. Running an investigation in a write-capable mode when `plan` would have guaranteed read-only. Assuming `plan` mode is unsafe because you have edit allow rules — it overrides them. Treating mode as a set-once preference rather than a per-task choice you revisit as the work shifts from understanding to changing to verifying.

## What to do instead

Choose the mode by the phase of work. Investigating, reviewing, or designing? Use `plan` — its read-only guarantee holds even against allow rules, so you can explore freely without risking a stray write. Deep in a trusted edit-and-test loop where every file-write prompt is friction? `acceptEdits` removes exactly that friction while still prompting on the riskier operations. Doing something consequential where you want to see each operation? Stay in `default`. And switch as you move between phases rather than parking in the most permissive mode for the whole session.

## Example

Matching mode to phase across a single task:

```text
Phase 1 — understand the bug
  Mode: plan
  Why:  read-only by guarantee; even with Edit(/src/**) allowed,
        no file is touched while you investigate

Phase 2 — implement the fix
  Mode: acceptEdits
  Why:  tight edit-test loop; auto-accepting edits to src/ removes
        per-write friction, while git push / network calls still prompt

Phase 3 — review and ship
  Mode: default
  Why:  the push, the migration, the deploy are consequential —
        you want to approve each as it comes
```

Setting a project default mode is fine for the common case:

```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Starting sessions in `plan` is a safe default — a new session explores before it changes anything, and you step up to an edit-capable mode deliberately when you're ready to write. The point isn't which mode is "best"; it's that the mode should track what the task actually needs, and you should move it as the task moves.
