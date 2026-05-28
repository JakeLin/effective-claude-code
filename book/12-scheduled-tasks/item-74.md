---
item: 74
theme: scheduled-tasks
title: "Fence every recurring autonomous run — cost and risk repeat with each iteration"
tags: [scheduled-tasks, guardrails, cost, safety, notifications, beta]
claude_code_version: "2.1.150"
stability: beta
status: current
related_items: [60, 35, 73]
things_to_remember:
  - "A scheduled task multiplies the unattended-run risk by every iteration — cost, permissions, and mistakes all repeat on a timer"
  - "Bound each run the way you'd bound any headless job (turn and budget limits, scoped tools) — then it's bounded per tick"
  - "Give the task a clear exit or escalation condition so it doesn't run pointlessly or compound a failure forever"
  - "Route each iteration's outcome through notification hooks so a silent loop doesn't drift unwatched"
agent_steps:
  - "Apply the headless guardrails (Item 60) to each scheduled run: turn limit, budget cap, and a scoped, pre-approved toolset"
  - "Define an exit or escalation condition so the task stops or pings you instead of looping uselessly or repeating a failure"
  - "Use the per-iteration hooks (UserPromptSubmit/Stop) to notify on meaningful results, not on every tick"
  - "Periodically review active scheduled tasks and routines, and cancel any that have outlived their purpose"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

A scheduled task is a headless run (Chapter 9) that happens over and over with nobody watching — which means every risk of an unattended run is now multiplied by the number of iterations. A single headless job that costs a few cents and might take a wrong turn is one thing; the same job on a five-minute loop is that cost and that risk every five minutes, indefinitely, while you're not there. Cost compounds tick by tick. A permission that can't be answered blocks every run, or worse, a too-broad grant fires every run. A mistake doesn't happen once — it repeats on the schedule. Recurrence turns small, bounded risks into accumulating ones, and that's the thing a scheduled task asks you to account for.

The good news is that the defenses are the ones you already have, applied per iteration. Everything the headless chapter said about fencing an unattended run (Item 60) applies to each tick of a scheduled task: a turn limit so a single run can't spin, a budget cap so it fails cheap, and a scoped, pre-approved toolset so there's no prompt waiting for a human who isn't there. Bound the individual run and you've bounded every run. Add to that a clear *exit or escalation condition* — a reason for the task to stop, or to ping you instead of continuing — so it doesn't loop pointlessly long after its purpose is served, and doesn't quietly compound the same failure forever. A recurring task without a stopping condition is a recurring task you'll find still running, wrongly, weeks later.

The last piece is visibility, and scheduled tasks hand you the hook for it: each iteration fires the same lifecycle hooks as any turn, so you can route a meaningful outcome to a notification channel (Item 35) — a Slack ping when the deploy status actually changed, an alert when a check fails — rather than letting the loop run silent. The discipline that closes the chapter mirrors the one that ran through it: an autonomous, recurring, unattended run is the most leveraged and the most dangerous way to use Claude, so fence each iteration, give the whole thing a way to stop, and wire it to tell you when something matters. Then review your active tasks and routines now and then, and cancel the ones that have outlived their purpose — because the one you forgot is the one still spending.

## What to avoid

Putting a task on a schedule with no per-run budget or turn cap, so cost and risk accrue every tick unattended. Assuming an interactive permission will be there to catch a dangerous action — on a timer, no one is watching. Scheduling a task with no exit or escalation condition, so it loops forever or repeats a failure indefinitely. Running a silent loop with no notifications, then discovering it drifted hours or days ago. Leaving stale tasks and routines active long after they stopped being useful.

## What to do instead

Treat each iteration as a headless run and fence it accordingly: turn limit, budget cap, scoped and pre-approved tools (Item 60). Give the task an exit or escalation condition so it stops, or pings you, instead of looping uselessly or compounding a fault. Use the per-iteration hooks to surface meaningful outcomes through notifications (Item 35), so a silent loop can't drift unwatched. And review active scheduled tasks and routines periodically, cancelling any that have outlived their purpose.

## Example

A recurring task, fenced and observable, versus a runaway:

```text
Fenced — each tick is bounded, it knows when to stop, and it speaks up:
  - per-run guardrails: turn limit, budget cap, only the tools the check needs
  - exit/escalation: stop after N clean runs; on failure, ping instead of retrying forever
  - visibility: Stop hook notifies Slack only when the result is meaningful

Runaway — the same task with none of that:
  - /loop or a routine with no per-run cap → cost accrues every interval, unattended
  - a broad toolset and no human → a wrong action repeats on every tick
  - no exit condition, no notifications → still running, possibly wrong, weeks later
```

The principle is the headline of the whole headless story, raised to a schedule: autonomy without a human is only safe inside bounds you set in advance, and a *recurring* autonomous run needs those bounds on every iteration plus a way to stop and a way to tell you what happened. Fence the tick, cap the spend, define the exit, wire the notification — and a scheduled task becomes a quiet, trustworthy helper instead of a meter you forgot was running.
