---
item: 72
theme: scheduled-tasks
title: "Match the scheduler to how long the work must outlive your conversation"
tags: [scheduled-tasks, routines, cron, decision, beta]
claude_code_version: "2.1.154"
stability: beta
status: current
related_items: [71, 73, 57]
things_to_remember:
  - "The schedulers differ by lifetime: `/loop` is conversation-bound, a routine is cloud-persistent, OS cron / CI is machine- or infra-bound"
  - "Use `/loop` for work that only needs to run while you're in the conversation; it pauses when Claude Code closes"
  - "Use a routine (or OS cron / GitHub Actions) for work that must run unattended, on a schedule, whether or not your machine is on"
  - "The failure mode is mismatching: a conversation-bound loop pauses the moment you close Claude Code"
agent_steps:
  - "Before scheduling, ask how long the work must keep running: just this conversation, or independently of it?"
  - "For conversation-only cadence, use `/loop` (Item 71)"
  - "For work that must survive the conversation and run unattended, use a cloud routine (Item 73), OS cron, or GitHub Actions"
  - "Never rely on a conversation-bound loop for production or always-on automation"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

There's more than one way to put Claude on a schedule, and they aren't interchangeable — they differ in *lifetime*, which is the one axis that determines whether your automation actually runs when you need it. A `/loop` task belongs to a conversation and pauses when Claude Code closes. A cloud routine runs on managed infrastructure independent of your machine. OS-level cron or a CI system like GitHub Actions runs on a host or in a pipeline whether or not Claude is even open. Picking among them isn't about which is most powerful; it's about matching the scheduler to how long the work has to keep going.

The decision is a single question: *does this work need to outlive this conversation?* If the answer is no — you want something checked repeatedly only while you're actively working — then `/loop` is correct and its conversation binding is exactly what you want, since the loop should pause when the conversation is gone. If the answer is yes — the work must run tonight while your laptop is closed, or every morning before you're awake, or whenever a PR opens — then a conversation-bound loop is the wrong tool entirely, and you need a routine or an infrastructure-level scheduler that persists on its own. Same scheduling instinct, opposite mechanisms, and the dividing line is lifetime.

The failure mode is always the same mismatch in the same direction: using a conversation-bound loop for work that needed to persist. It's insidious because it *looks* like it works — you set the loop, see it fire once, and walk away satisfied. Then you close Claude Code and the automation pauses, with no persistent daemon continuing the check, and you discover the gap only when the thing you were "monitoring" went unmonitored for hours. The headless chapter made the point that unattended work has to stand on its own; this is the scheduling corollary. Decide the required lifetime *first*, then pick the scheduler that provides it — and never let a convenience loop masquerade as durable automation.

## What to avoid

Using `/loop` for anything that must keep running after you close Claude Code — it won't. Assuming all the scheduling options are roughly equivalent and reaching for the handiest one. Setting up a conversation-bound monitor for a production concern and discovering the silent gap only after something went unwatched. Spinning up heavyweight cloud infrastructure for a check you only need during today's work session, where `/loop` would do.

## What to do instead

Ask the lifetime question before you schedule anything: must this outlive the conversation or not? If not, use `/loop` and accept that it pauses when Claude Code closes. If so, use a cloud routine, OS cron, or GitHub Actions — something that persists independently of your machine and runs unattended. Let the required lifetime pick the mechanism, and never lean on a conversation-bound loop for production or always-on work.

## Example

The lifetime question, routed to the right scheduler:

```text
"Watch this deploy while I finish the PR."
  Lifetime: just this conversation.
  → /loop 5m "check deploy status"          (conversation-bound — pauses when Claude Code closes)

"Every morning at 7am, summarize overnight errors and post to Slack."
  Lifetime: independent of any session, on a clock.
  → a cloud routine (Item 73)                (persists, runs unattended)

"On every PR to main, run the security review."
  Lifetime: event-driven, infra-bound.
  → GitHub Actions calling `claude -p` (Ch 9), or a routine's GitHub trigger

"Nightly cleanup on the build server."
  Lifetime: host-bound, always-on.
  → OS cron on that host invoking headless Claude
```

Only the first wants `/loop`; the rest must outlive any conversation and so need a persistent scheduler. The mistake to never make is the first mechanism doing the last three jobs — a loop set up and abandoned, looking healthy right up until you close Claude Code and it quietly pauses.
