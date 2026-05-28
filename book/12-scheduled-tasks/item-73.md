---
item: 73
theme: scheduled-tasks
title: "Promote work that must run unattended to a routine"
tags: [scheduled-tasks, routines, triggers, automation, beta]
claude_code_version: "2.1.154"
stability: beta
status: current
related_items: [71, 72, 74]
things_to_remember:
  - "Create persistent routines with `/schedule`; they run on managed cloud infrastructure whether or not your machine or session is running"
  - "Routines can start from schedules, external webhooks, GitHub events, or email triggers"
  - "They run with the integrations you explicitly connect, so a routine can act on real systems unattended"
  - "Routines are plan- and platform-gated; confirm your account, platform, triggers, and limits before depending on them"
agent_steps:
  - "When work must run unattended and survive the conversation, create a routine with `/schedule` rather than stretching `/loop`"
  - "Pick the trigger that fits: a schedule for time-based work, a webhook for external systems, a GitHub trigger for repo events, or email for incoming messages"
  - "Connect only the integrations the routine needs, and scope those deliberately"
  - "Verify plan availability, platform support, triggers, and limits against current docs before depending on a routine"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

When the previous Item's lifetime question comes back "this must run independently of me," a routine is the answer. Unlike a conversation-bound loop, a routine runs on Anthropic-managed infrastructure: it persists on its own, and it fires whether or not your machine is on or any session is open. You create it through `/schedule`, describe the task, choose a trigger, and connect the integrations it needs. That's the categorical difference — a routine is durable automation, not an in-session convenience. The morning error summary, the nightly report, the recurring cleanup that has to happen regardless of where you are: these are routine work, because they need to keep running after you've closed everything and gone home.

Routines are also more flexible than a clock. A `/loop` is time-based, but a routine supports several *trigger* types. A schedule trigger handles the recurring-or-one-off time case. A webhook trigger lets an external system kick the routine via an HTTP call, so other automation can invoke Claude on demand. A GitHub trigger fires in response to repository events — a pull request opened, a release cut — which makes a routine a natural way to react to your development workflow without a human in the loop. Email triggers can start work from incoming messages. Choosing the trigger that matches *what should start the work* is the main design decision, the same way choosing the scheduler by lifetime was the decision in the previous Item.

Two things make routines genuinely capable and genuinely worth caution. They use the integrations you explicitly connect, so a routine isn't just thinking in a vacuum; it can read and act on real systems unattended, which is exactly what makes it useful and exactly why the next Item's guardrails matter so much. And they are plan- and platform-gated, with documented limits that matter in production. Use routines for what they're uniquely good at — persistent, trigger-driven, unattended work that acts on real systems — but verify your account, platform, trigger, and limit details against the docs rather than trusting any fixed description, this one included.

## What to avoid

Stretching `/loop` to cover work that needs to persist beyond your conversation, when a routine is the built-for-it tool. Defaulting to a schedule trigger when a webhook, GitHub, or email trigger matches what should actually start the work. Forgetting that a routine acts through connected integrations, and leaving those broader than the routine needs. Building something load-bearing without confirming your current plan, platform, trigger, and limit constraints.

## What to do instead

For unattended work that must outlive your conversation, create a routine with `/schedule`. Choose the trigger by what should start it: a schedule for time-based runs, a webhook for externally-initiated ones, a GitHub trigger for repo events, or an email trigger for incoming messages. Scope the connected integrations to what the routine actually needs to touch. Confirm available triggers, limits, and behavior against current docs — and pair any routine with the guardrails of the next Item, since it runs unattended and can act on real systems.

## Example

Matching the trigger to what should start the work:

```text
Schedule trigger — time-based, recurring or one-off:
  "Every weekday at 7am: summarize overnight errors, post to Slack."

Webhook trigger — started by an external call:
  another system POSTs to the routine to kick a build-report run on demand.

GitHub trigger — reacts to repo activity:
  "On every PR to main: run the security review and comment findings."

Email trigger — reacts to incoming messages:
  "When a vendor sends an invoice: extract the amount and file it."
```

Why a routine and not `/loop` for these: each must run with no conversation open — at 7am before you're working, the instant a teammate's PR lands, whenever an external system calls, or when an email arrives. A conversation-bound loop can't do any of them, because there's no active conversation to carry it. And because the routine can use connected integrations, the 7am job can actually reach Slack and the PR job can actually comment — which is the capability that makes routines useful and the reason the unattended-guardrail Item that follows applies to every one of them.
