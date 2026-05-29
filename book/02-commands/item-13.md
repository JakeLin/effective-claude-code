---
item: 13
theme: commands
title: "Match review depth to stakes — `/code-review`, `/review`, `/ultrareview`"
tags: [commands, review, code-quality, bundled-skills]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [8]
things_to_remember:
  - "`/code-review` reviews the current diff at adjustable depth (low/medium/high/max/ultra)"
  - "`/review` opens a local PR review; `/ultrareview` runs a deep multi-agent cloud review"
  - "Pick by what's at risk — a one-line fix doesn't need /ultrareview; a payment flow does"
  - "`/code-review --fix` applies findings to the working tree; `--comment` posts to the PR"
agent_steps:
  - "Before committing user-facing or high-stakes changes, propose `/code-review` at an effort matched to the change — low for mechanical, high for behavioral, ultra for critical"
  - "Before merging a PR, suggest `/review` for a local sweep; for high-stakes changes also suggest `/ultrareview`"
  - "When the user asks Claude to review work it just wrote, prefer `/code-review` — it brings a fresh review pass instead of self-evaluation"
  - "Skip review commands when the diff is mechanical and small (typos, formatting, trivial renames)"
---

## Why this matters

There are three review pathways with very different cost and depth profiles. `/code-review` is a bundled skill that reviews the current diff at a configurable effort level — quick high-confidence findings at low/medium, broader (and noisier) coverage at high/max, and a deep multi-agent cloud review at ultra. `/review` opens a local PR review session for the current branch. `/ultrareview` (the same as `/code-review ultra`) runs the deep cloud review and is the heaviest option.

The common mistake is treating them as a single "review my work" command and either over-investing on small changes or under-investing on big ones. Running `/ultrareview` on a typo PR burns the budget for nothing; running nothing on a payment flow saves five minutes and ships a vulnerability.

The other reason to know all three: they read the change differently. `/code-review` operates on the diff and is fast feedback during development. `/review` is local PR-scoped — it picks up the description, context, and full change set. `/ultrareview` spawns multiple cloud agents to dig into edge cases, security, performance, and consistency, and produces a structured report. Which one depends on where you are: writing, about to merge, about to ship.

`--fix` and `--comment` change what happens with findings. `--fix` applies high-confidence findings to your working tree directly, which is great for low-stakes cleanups and dangerous for anything subtle. `--comment` posts inline comments to the PR for human review.

## What to avoid

Reflex review every diff at the same depth regardless of stakes. Trusting `/code-review --fix` on changes you don't understand — accepting fixes you can't evaluate is how bugs get baked in. Skipping review on the assumption that tests caught everything. Asking Claude in chat to "review what you just did" when `/code-review` runs a real review pass that catches things Claude won't notice about its own work.

## What to do instead

Pick the depth by what's at risk. Use `/code-review` low or medium for quick passes during development. Step up to high or max before committing user-facing changes. Reserve `/ultrareview` (or `/code-review ultra`) for changes where being wrong is genuinely expensive — auth, payments, migrations, anything load-bearing.

For PR-level review, `/review` is the routine answer; `/ultrareview` is the second pass on the high-stakes ones. `--fix` is right when the findings are mechanical and obvious; `--comment` is right when humans should weigh in.

## Example

Three review depths for three stakes levels.

```text
> [touched a string in the UI]
> /code-review low

[finds a typo and an unused import; quick to apply]
```

```text
> [implemented a new API endpoint]
> /code-review high

[finds a missing input validation, a race in the cache write, and a
response that leaks an internal error message]
```

```text
> [refactored the payment retry logic]
> /code-review ultra
   # or equivalently: /ultrareview

[multi-agent cloud review produces a structured report on idempotency,
retry budgets, observability gaps, and a subtle interaction with the
outbox table]
```

PR sweep before merging.

```text
> /review

[local review of branch vs. main, with prioritized findings]
```
