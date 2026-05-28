---
item: 71
theme: scheduled-tasks
title: "Reach for `/loop` to repeat work within a conversation — and know it pauses with Claude Code"
tags: [scheduled-tasks, loop, cron, conversation-bound, beta]
claude_code_version: "2.1.154"
stability: beta
status: current
related_items: [72, 73, 74]
things_to_remember:
  - "`/loop <interval> <prompt-or-command>` repeats work inside the current conversation — built in, no setup"
  - "Loop tasks are conversation-bound: they pause when Claude Code closes and resume only if you resume that conversation before expiry"
  - "Tasks auto-expire after three days; a forgotten loop does not run forever"
  - "Manage tasks in natural language or through the underlying CronCreate, CronList, and CronDelete tools"
agent_steps:
  - "Schedule recurring in-session work with `/loop <interval> \"<prompt>\"` or `/loop <interval> /<command>`"
  - "Use it for things worth checking repeatedly while you work — deploy status, a watch-and-report, a periodic cleanup command"
  - "Remember the task pauses when Claude Code closes and only resumes if the same conversation is resumed before expiry; for durable work, use a routine instead (Item 73)"
  - "List and cancel scheduled tasks in natural language or with the cron tools rather than leaving stale loops running"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

`/loop` is the simplest way to put Claude on a timer. You give it an interval and something to run — a prompt or a slash command — and it schedules that work to repeat: `/loop 10m "check the deploy status and tell me if it changed"`, or `/loop 5m /simplify`. For the common want — "keep doing this small thing every few minutes while I work on something else" — it's exactly the right amount of machinery.

The one fact that governs everything about `/loop` is that it is *conversation-bound*. The task belongs to the current conversation. If Claude Code closes, the task pauses; if you resume the same conversation before the task expires, the task resumes. This is not a background daemon, not an OS-level cron job, not durable cloud automation. That scoping is a feature for its intended use — a loop that watches your deploy while you code should obviously stop when you're done coding — but it's a trap if you mistake it for durable scheduling.

Two more constraints keep loops well-behaved. Cron's granularity bottoms out at one minute, so `/loop` is for minute-scale-and-up cadences, not sub-second polling; requests in seconds round to the nearest minute. And recurring tasks auto-expire after three days, which is a deliberate guardrail: a loop you forget about doesn't run forever, it lapses on its own. Manage active tasks by asking Claude what is scheduled, asking it to cancel a task by id, or using the underlying CronCreate, CronList, and CronDelete tools. Use `/loop` for what it's for — repeated work inside the current conversation — and keep its conversation-bound, minute-granular, self-expiring nature firmly in mind.

## What to avoid

Setting up a `/loop`, closing Claude Code, and expecting it to keep running like a daemon. Reaching for `/loop` for sub-minute polling, below cron's granularity. Treating it as production-grade scheduling rather than a conversation-bound convenience. Leaving stale loops running instead of cancelling them when the work is done.

## What to do instead

Use `/loop <interval> <prompt-or-command>` for work worth repeating while you're in a conversation — status checks, watch-and-report, a periodic cleanup command. Keep its nature in mind: conversation-bound, minute-granular at finest, and self-expiring after three days. List and cancel tasks in natural language or with the cron tools when you're finished. And when the work genuinely needs to outlive the conversation, don't stretch `/loop` to cover it — promote it to a routine, which the later Item covers.

## Example

In-session loops for the right kind of work:

```text
> /loop 10m "check deploy status; only ping me if it changed"
> /loop 5m /simplify
> /loop 30m "summarize new errors in the running log"
```

Each repeats on its interval while the conversation is active, pauses when Claude Code is closed, and can resume if you resume the same conversation before expiry. Managing them:

```text
> what scheduled tasks are active?
> cancel the deploy-status loop
```

The boundary that matters, stated plainly:

```text
Fine:  /loop watches your deploy while you keep working in the same conversation.
Trap:  you set the loop, close Claude Code, and assume it is still checking.
       It is paused. Durable automation wants a routine (Item 73).
```

`/loop` is a conversation-bound tool, and once you internalize that boundary, it's a clean way to offload small repeated chores while you focus elsewhere.
