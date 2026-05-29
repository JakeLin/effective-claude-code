---
item: 60
theme: cli-headless
title: "Put a budget and a turn limit on every unattended run"
tags: [headless, guardrails, budget, max-turns, permissions, safety]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [40, 42, 57, 74]
things_to_remember:
  - "An unattended run with no limits is a runaway — there's no human to stop a loop that's burning turns and money"
  - "Bound spend and length with `--max-budget-usd` and `--max-turns`; both are hard stops the harness enforces"
  - "Scope what the run can do with `--allowedTools` / `--tools` / `--disallowedTools` and a tight `--permission-mode`, since no one will answer prompts"
  - "In headless contexts there's no permission prompt to fall back on — pre-decide every tool the run may use"
agent_steps:
  - "On every headless/unattended invocation, set `--max-turns` and `--max-budget-usd` to hard-cap length and spend"
  - "Restrict tools explicitly with `--tools` or `--allowedTools`, and deny dangerous ones with `--disallowedTools`"
  - "Choose a `--permission-mode` that doesn't depend on a human (e.g. a locked-down mode), since prompts can't be answered"
  - "Avoid `--dangerously-skip-permissions` unless the run is inside a disposable, isolated environment (Item 42)"
---

## Why this matters

Interactively, you are the circuit breaker: if Claude gets stuck in a loop, pursues a wrong approach, or starts running up cost, you see it and stop it. Headless, that circuit breaker is gone. A `claude -p` run in CI or cron executes to completion with nobody watching, which means an agentic loop that should have taken three turns and a few cents can — if something goes sideways — churn for dozens of turns and dollars before anything notices. An unattended run with no limits isn't autonomous; it's unsupervised, and the difference is whether there's a hard stop the run can hit on its own.

The harness provides those hard stops, and they belong on every unattended invocation. `--max-turns` caps the number of agentic turns, so a loop terminates instead of spinning. `--max-budget-usd` caps API spend, so a run that goes wrong fails cheap instead of expensive. Both are enforced by the harness, not requested of the model — the run exits when it hits the limit regardless of what Claude "wants" to do next. They're the headless equivalent of standing over the session ready to intervene: pre-committed limits that fire without you. The cost of setting them is one flag each; the cost of omitting them is a runaway you only discover from the bill or the CI minutes.

The other half is what the run is *allowed to do*. Interactively, an unexpected dangerous action hits a permission prompt and waits for you. Headless, there's no one to answer that prompt — so the permission has to be decided before the run starts, not during it. Scope the toolset explicitly with `--tools` or `--allowedTools`, deny the sharp edges with `--disallowedTools`, and pick a `--permission-mode` that doesn't assume a human is present. This is the unattended face of the whole permissions chapter: the same allow/deny discipline (Item 40) and the same caution about bypass mode (Item 42), applied where there's no prompt to fall back on. And `--dangerously-skip-permissions` in a headless run is doubly dangerous — no prompts *and* no checks — so reserve it for the disposable, isolated environments that Item made the precondition.

## What to avoid

Launching a headless run with no `--max-turns` or `--max-budget-usd`, so a stuck loop has no ceiling. Assuming "it'll probably be fine" because the task is small — the runaway case is exactly the one you didn't expect. Leaving the toolset wide open in an unattended run because you didn't think about what it might reach for. Using `--dangerously-skip-permissions` in CI on a real repo with real credentials, where no prompt and no check is a recipe for an irreversible mistake.

## What to do instead

Fence every unattended run up front. Set `--max-turns` and `--max-budget-usd` as hard caps on length and spend — cheap to add, decisive when something goes wrong. Scope capability explicitly: `--tools` or `--allowedTools` to grant only what the task needs, `--disallowedTools` to block the dangerous ones, and a `--permission-mode` that works without a human to answer prompts. Treat bypass mode as off-limits outside a disposable, isolated environment. The goal is a run that can't exceed bounds you set before you walked away.

## Example

A bounded, scoped headless invocation — the shape every unattended run should have:

```bash
claude -p "fix lint errors in src/ and re-run the linter" \
  --max-turns 15 \
  --max-budget-usd 0.50 \
  --allowedTools "Read,Edit,Bash(npm run lint:*)" \
  --permission-mode acceptEdits
```

Every axis is fenced: at most 15 turns, at most 50 cents, only the three tool capabilities the task needs, and an edit-accepting mode that never waits on a prompt that can't be answered. If the run loops or misbehaves, it hits a wall and exits rather than running up the bill.

Contrast the runaway waiting to happen:

```bash
claude -p "fix everything wrong with the codebase" --dangerously-skip-permissions
```

No turn cap, no budget cap, every tool available, and all permission checks off — in an environment that may have real credentials. Unattended, this can churn for a long time and do real damage before anyone sees it. The fix isn't more cleverness in the prompt; it's the limits. Set the budget and the turn count first, scope the tools to the job, and only reach for bypass inside something you could throw away.
