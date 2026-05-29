---
item: 71
theme: scheduled-tasks
title: "Reach for `/loop` to repeat work within a session — and know it dies with the session"
tags: [scheduled-tasks, loop, cron, session-scoped, beta]
claude_code_version: "2.1.150"
stability: beta
status: needs-review
related_items: [72, 74]
things_to_remember:
  - "`/loop <interval> <prompt-or-command>` repeats work on a cron schedule from inside a session — built in, no setup"
  - "Loop tasks are session-scoped: they live in memory and stop the moment Claude exits — not a background daemon"
  - "Cron granularity bottoms out at 1 minute, and recurring tasks auto-expire after a few days so forgotten loops don't run forever"
  - "Manage tasks with the cron tools (create/list/delete); cancel a job by id when you're done with it"
agent_steps:
  - "Schedule recurring in-session work with `/loop <interval> \"<prompt>\"` or `/loop <interval> /<command>`"
  - "Use it for things worth checking repeatedly while you work — deploy status, a watch-and-report, a periodic cleanup command"
  - "Remember the task stops when the session ends; for work that must survive the session, use a routine instead (Item 73)"
  - "List and cancel scheduled tasks with the cron tools rather than leaving stale loops running"
---

## Why this matters

`/loop` is the simplest way to put Claude on a timer. You give it an interval and something to run — a prompt or a slash command — and it schedules that work to repeat: `/loop 10m "check the deploy status and tell me if it changed"`, or `/loop 5m /simplify`. It's a built-in skill with nothing to install, and under the hood it uses cron tools (create, list, delete) to manage the schedule. For the common want — "keep doing this small thing every few minutes while I work on something else" — it's exactly the right amount of machinery.

The one fact that governs everything about `/loop` is that it's *session-scoped*. The scheduled task lives in the memory of your running Claude session; when that session exits, the task stops with it. This is not a background daemon, not an OS-level cron job, not something that keeps running after you close the terminal. That scoping is a feature for its intended use — a loop that watches your deploy while you code should obviously stop when you're done coding — but it's a trap if you mistake it for durable scheduling. A `/loop` you set up and then quit out of simply isn't running anymore, silently, and the next Item is entirely about not making that mistake.

Two more constraints keep loops well-behaved. Cron's granularity bottoms out at one minute, so `/loop` is for minute-scale-and-up cadences, not sub-second polling. And recurring tasks auto-expire after a few days, which is a deliberate guardrail: a loop you forget about doesn't run forever, it lapses on its own. (The exact expiry window is one of the beta specifics still settling — don't build on a precise number.) Manage active tasks with the cron tools and cancel a job by its id when you're finished, rather than letting stale loops accumulate. Use `/loop` for what it's for — repeated work inside a live session — and keep its session-scoped, minute-granular, self-expiring nature firmly in mind.

## What to avoid

Setting up a `/loop` and quitting the session, expecting it to keep running — it stopped when Claude exited. Reaching for `/loop` for sub-minute polling, below cron's granularity. Treating it as production-grade scheduling rather than an in-session convenience. Leaving stale loops running instead of cancelling them when the work is done.

## What to do instead

Use `/loop <interval> <prompt-or-command>` for work worth repeating while you're in a session — status checks, watch-and-report, a periodic cleanup command. Keep its nature in mind: session-scoped (stops when Claude exits), minute-granular at finest, and self-expiring after a few days. List and cancel tasks with the cron tools when you're finished. And when the work genuinely needs to outlive the session, don't stretch `/loop` to cover it — promote it to a routine, which the later Item covers.

## Example

In-session loops for the right kind of work:

```text
> /loop 10m "check deploy status; only ping me if it changed"
> /loop 5m /simplify
> /loop 30m "summarize new errors in the running log"
```

Each repeats on its interval for as long as the session is alive. Managing them:

```text
> cron list                 # see active scheduled tasks
> cron cancel <job-id>      # stop one when you're done
```

The boundary that matters, stated plainly:

```text
Fine:  /loop watches your deploy while you keep working in the same session.
Trap:  you set the loop, close the terminal, and assume it's still checking.
       It isn't — it died with the session. That job wants a routine (Item 73).
```

`/loop` is a live-session tool, and once you internalize that it stops when Claude does, it's a clean way to offload small repeated chores while you focus elsewhere.
