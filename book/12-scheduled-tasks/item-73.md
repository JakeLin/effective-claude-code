---
item: 73
theme: scheduled-tasks
title: "Promote work that must run unattended to a routine"
tags: [scheduled-tasks, routines, triggers, automation, beta]
claude_code_version: "2.1.150"
stability: beta
status: needs-review
related_items: [71, 72, 74]
things_to_remember:
  - "A routine runs on managed cloud infrastructure, so it persists and fires whether or not your machine or session is running"
  - "Routines support more than a clock: schedule triggers, an API/webhook trigger, and source-control event triggers (e.g. on a PR)"
  - "They inherit your connected integrations (MCP connectors), so a routine can act on real systems unattended"
  - "Routines are a research preview — powerful, but the least settled surface here; confirm capabilities against current docs"
agent_steps:
  - "When work must run unattended and survive your session, create a routine rather than stretching `/loop`"
  - "Pick the trigger that fits: a schedule for time-based work, an API trigger for externally-kicked runs, a source-event trigger for PR/release reactions"
  - "Rely on the routine's connected integrations to let it act on the systems it needs, and scope those deliberately"
  - "Treat routines as experimental — verify available triggers and limits against current docs before depending on them"
---

## Why this matters

When the previous Item's lifetime question comes back "this must run independently of me," a routine is the answer. Unlike a session-scoped loop, a routine runs on Anthropic-managed infrastructure: it persists on its own, and it fires whether or not your machine is on or any session is open. That's the categorical difference — a routine is durable automation, not an in-session convenience. The morning error summary, the nightly report, the recurring cleanup that has to happen regardless of where you are: these are routine work, because they need to keep running after you've closed everything and gone home.

Routines are also more flexible than a clock. A `/loop` is purely time-based, but a routine supports several *trigger* types. A schedule trigger handles the recurring-or-one-off time case. An API trigger lets an external system kick the routine via an HTTP call, so other automation can invoke Claude on demand. And a source-control event trigger fires the routine in response to repository events — a pull request opened, a release cut — which makes a routine a natural way to react to your development workflow without a human in the loop. Choosing the trigger that matches *what should start the work* is the main design decision, the same way choosing the scheduler by lifetime was the decision in the previous Item.

Two things make routines genuinely capable and genuinely worth caution. They inherit your connected integrations — the MCP connectors you've set up — so a routine isn't just thinking in a vacuum; it can read and act on real systems unattended, which is exactly what makes it useful and exactly why the next Item's guardrails matter so much. And they are, as of this writing, a research preview: the most experimental surface in a beta chapter, with triggers, limits, and behavior still taking shape. Use routines for what they're uniquely good at — persistent, trigger-driven, unattended work that acts on real systems — but verify the current capabilities against the docs rather than trusting any fixed description, this one included.

## What to avoid

Stretching `/loop` to cover work that needs to persist beyond your session, when a routine is the built-for-it tool. Defaulting to a schedule trigger when an API or source-event trigger matches what should actually start the work. Forgetting that a routine acts on your connected integrations, and leaving those broader than the routine needs. Building something load-bearing on a research-preview surface without confirming its current limits.

## What to do instead

For unattended work that must outlive your session, create a routine. Choose the trigger by what should start it: a schedule for time-based runs, an API trigger for externally-initiated ones, a source-control event trigger to react to PRs or releases. Scope the integrations it inherits to what it actually needs to touch. And because routines are a research preview, confirm available triggers, limits, and behavior against current docs — and pair any routine with the guardrails of the next Item, since it runs unattended and can act on real systems.

## Example

Matching the trigger to what should start the work:

```text
Schedule trigger — time-based, recurring or one-off:
  "Every weekday at 7am: summarize overnight errors, post to Slack."

API trigger — started by an external call:
  another system POSTs to the routine to kick a build-report run on demand.

Source-control event trigger — reacts to repo activity:
  "On every PR to main: run the security review and comment findings."
```

Why a routine and not `/loop` for these: each must run with no session open — at 7am before you're working, the instant a teammate's PR lands, whenever an external system calls. A session-scoped loop can't do any of them, because there's no session. And because the routine inherits your connectors, the 7am job can actually reach Slack and the PR job can actually comment — which is the capability that makes routines useful and the reason the unattended-guardrail Item that follows applies to every one of them.
