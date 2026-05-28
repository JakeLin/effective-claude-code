---
item: 69
theme: agent-teams
title: "Coordinate teammates through a shared task list and a lead, on independent slices"
tags: [agent-teams, coordination, task-list, lead, beta]
claude_code_version: "2.1.150"
stability: beta
status: current
related_items: [55, 66, 68]
things_to_remember:
  - "Teammates coordinate through a shared task list — they claim tasks, track dependencies, and go idle when done"
  - "A lead session forms the team, assigns work, and steers; it can gate on `TeammateIdle` and `TaskCompleted` events"
  - "Slice the work so each teammate owns an independent, low-dependency piece — coupled slices serialize the team or collide"
  - "Dependencies in the task list keep order correct so a teammate doesn't start work whose inputs aren't ready"
agent_steps:
  - "Structure team work as a shared task list with one independent slice per teammate"
  - "Designate a lead to form the team, assign tasks, and coordinate; let it listen for TeammateIdle/TaskCompleted to gate quality"
  - "Encode ordering with task dependencies so teammates don't start work before its inputs exist"
  - "Minimize cross-slice coupling and shared files so teammates progress in parallel rather than blocking each other"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

A team without coordination is just several sessions editing the same repo at cross-purposes. What makes it a *team* is the shared task list: a single durable list of work that every teammate can see, where teammates claim tasks, record progress, and go idle when their part is done. This is the same task-list machinery from the orchestration chapter (Item 55), now serving as the coordination substrate for independent sessions rather than the memory of one. Because the list is shared and durable, the team has a common source of truth for what's done and what's left — without it, parallel sessions have no way to divide work or avoid redoing each other's.

A team also needs a lead. One session forms the team, assigns the initial slices, and steers as work proceeds — and crucially, the lead is where quality gates live. Hooks like `TeammateIdle` (a teammate has finished and is waiting) and `TaskCompleted` (a unit of work is done) give the lead programmatic moments to check results, assign follow-on work, or hold the team to a standard before declaring done. This mirrors the verification and review Items from orchestration: the lead is the place to put the "is this actually right?" check, so the team converges on correct work rather than just finishing fast.

The part that most determines whether a team helps is how you *slice* the work. Teammates pay off only when their slices are independent — each one a piece that can progress without waiting on another and without editing the same files. Couple the slices tightly and the team serializes (everyone blocks on one shared piece) or collides (two teammates fighting the same code), and you've paid N× cost for no parallelism. Dependencies in the task list handle the unavoidable ordering — a slice whose inputs aren't ready stays blocked until they are — but the goal is to *minimize* those dependencies in how you carve the work. Independent slices, a shared list to coordinate them, and a lead to gate quality: that's the whole coordination model, and getting the slicing right is what turns N sessions into N× the progress instead of N× the cost.

## What to avoid

Spawning teammates with no shared task structure, so they duplicate or undercut each other's work. Carving the work into tightly-coupled slices that force teammates to block on one another or edit the same files. Leaving no lead to assign work and check results, so the team finishes fast but wrong. Ignoring `TeammateIdle`/`TaskCompleted` and missing the natural moments to gate quality or hand out follow-on work.

## What to do instead

Coordinate through the shared task list: one independent, low-dependency slice per teammate, with dependencies encoded only where ordering is genuinely required. Designate a lead to form the team, assign work, and steer — and have it listen for `TeammateIdle` and `TaskCompleted` to enforce quality gates and dispatch follow-on tasks. Above all, slice for independence: minimize shared files and cross-slice coupling so teammates run in true parallel instead of serializing or colliding.

## Example

A well-sliced team coordinating through a shared list:

```text
Lead forms the team and seeds the shared task list:

  ☐ teammate A → build the REST endpoints        (no deps)
  ☐ teammate B → build the client SDK            (no deps)
  ☐ teammate C → write integration tests         (blockedBy: A, B)

A and B run in true parallel — different modules, no shared files.
C's task stays blocked until A and B complete, then C claims it.

Lead listens for TaskCompleted:
  - on A done and B done → C unblocks automatically
  - on C done → lead runs the review gate before declaring the feature done
```

The slices are independent where they can be (A and B) and ordered only where they must be (C depends on both), so the parallelism is real and nothing collides. Contrast a bad slicing — A, B, and C all editing the same handler file — where the team serializes on that file and the N× cost buys nothing. The shared list divides the work, the dependencies keep order correct, and the lead gates the result: coordinate that way and the team earns its weight.
