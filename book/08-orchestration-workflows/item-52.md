---
item: 52
theme: orchestration-workflows
title: "Delegate side-quests to subagents to keep the main thread focused"
tags: [subagents, context-isolation, delegation, parallelism]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [15, 16, 20, 51]
things_to_remember:
  - "Fan independent legwork out to parallel subagents — each returns a compact summary, so the main thread reasons over conclusions, not file dumps"
  - "Delegate work whose process is noisy but whose result is compact: broad searches, large-file exploration, parallel checks"
  - "Independent subagents run in parallel, giving roughly N× effective context for fan-out work"
  - "Don't delegate the understanding you need to keep — offload the legwork, retain the judgment"
agent_steps:
  - "When a side task would flood the main context with reads and tool calls but yields a compact answer, delegate it to a subagent"
  - "Run independent investigations as parallel subagents rather than sequentially in the main thread"
  - "Keep the synthesis, decisions, and code you must reason about in the main thread; offload only the legwork"
  - "Right-size delegation: scope the subagent's task so its returned summary is what the main thread actually needs"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

A subagent is a context firewall: its own window, returning only a summary (Item 15). This Item is about the orchestration move that firewall unlocks — *fan-out*. When a task needs several independent pieces of legwork — find the call sites, learn the existing API, locate the tests — spawn a subagent for each, run them concurrently (Item 20), and let the main thread reason over the conclusions instead of the dozens of files the agents read to produce them. The legwork happens in N separate contexts; only N short answers come back.

The pattern fits a specific shape of work: noisy process, compact result. A broad directory sweep, an unfamiliar dependency to map, a batch of independent checks — each generates a lot of intermediate material and yields a small answer. Fanning them out makes that a multiplier: three investigations across three subagents put roughly three times the effective context to work at once and collapse the wall-clock time, because the reads happen in parallel instead of serializing through a single window. For fan-out work, that's leverage you can't get any other way.

The limit is the one the subagents chapter already drew (Item 15): offload the legwork, not the judgment. A summary is lossy — the right trade when you need a *conclusion* (where is X, does Y compile), the wrong one when you need to *internalize* something to make the next call. If the texture matters — the design you're about to critique, the code you're about to extend — read it in the main thread. Fan-out multiplies your reach for facts; it doesn't replace the thinking that has to happen where you can see it.

## What to avoid

Running a broad, file-heavy search directly in the main thread and letting its dozens of reads bury the actual task. Serializing independent investigations one after another when they could fan out in parallel. Delegating the core understanding — the design, the critical code path — and then trying to make a judgment call from a lossy summary. Over-delegating trivial work, where spawning a subagent costs more than just doing it inline.

## What to do instead

Delegate work whose process is noisy but whose result is compact: broad searches, large-file or dependency exploration, batches of independent checks. Fan independent investigations out to parallel subagents to multiply your effective context and collapse the wall-clock time. Keep the synthesis, the decisions, and any code you must reason about in the main thread — offload the legwork, not the thinking. And scope each delegated task so the summary that comes back is exactly what the main thread needs to proceed.

## Example

Delegating the noisy-process / compact-result work, in parallel:

```text
Main thread task: "add a feature flag to gate the new checkout flow"

Fan out three subagents (own contexts, run concurrently):
  Agent A → "find every place the checkout flow is entered"      → returns 4 call sites
  Agent B → "how does the existing feature-flag system work?"    → returns the API + example
  Agent C → "what tests cover checkout?"                         → returns 3 test files

Main thread receives three short summaries — not the ~30 files the
agents read between them — and now implements the flag with a full,
uncluttered context.
```

Contrast the boundary: the *implementation itself* — wiring the flag into those four call sites, editing the code you have to get right — stays in the main thread, because that's the judgment you can't delegate to a summary. The pattern is to push the reading outward and keep the reasoning inward: subagents go get the facts, the main thread decides what to do with them.
