---
item: 52
theme: orchestration-workflows
title: "Delegate side-quests to subagents to keep the main thread focused"
tags: [subagents, context-isolation, delegation, parallelism]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [15, 16, 51]
things_to_remember:
  - "A subagent runs in its own context window and returns only a summary — the main thread gets the conclusion, not the file dumps"
  - "Delegate work whose process is noisy but whose result is compact: broad searches, large-file exploration, parallel checks"
  - "Independent subagents run in parallel, giving roughly N× effective context for fan-out work"
  - "Don't delegate the understanding you need to keep — offload the legwork, retain the judgment"
agent_steps:
  - "When a side task would flood the main context with reads and tool calls but yields a compact answer, delegate it to a subagent"
  - "Run independent investigations as parallel subagents rather than sequentially in the main thread"
  - "Keep the synthesis, decisions, and code you must reason about in the main thread; offload only the legwork"
  - "Right-size delegation: scope the subagent's task so its returned summary is what the main thread actually needs"
---

## Why this matters

The previous Item framed context as a budget; subagents are the most powerful way to spend it well. A subagent runs in its *own* context window, does its work there, and returns only a summary to the main thread. That separation is the whole point: a broad codebase search might read forty files to answer one question, and if it runs in your main context, those forty files are now sitting in it, crowding out everything else. Run it in a subagent and the main thread receives the answer — "the auth flow lives in `middleware/session.ts`, here's how it works" — without the forty files. The legwork happened somewhere else; only the conclusion came back.

This makes subagents the right tool for a specific shape of work: noisy process, compact result. Sweeping a large directory to find where something is defined. Reading an unfamiliar dependency to understand its API. Running several independent checks at once. In each, the *doing* generates a lot of intermediate material and the *answer* is small. Delegation also unlocks parallelism — independent subagents execute concurrently, so fanning three investigations out to three subagents gives you roughly three times the effective context working at once and returns three summaries instead of serializing the reads through one window. For fan-out work, that's a multiplier you can't get any other way.

But delegation has a sharp limit, and it's the same one the subagents chapter drew: don't delegate the understanding you need to keep. A subagent returns a summary, and a summary is lossy — it's the right trade when you need a *conclusion* (where is X, does Y compile, what does Z do) and the wrong trade when you need to *internalize* something to make the next decision. If the texture of what's being read matters to your judgment — the design you're about to critique, the code you're about to extend — read it in the main thread. The rule is clean: offload the legwork, retain the judgment. Subagents preserve your context for the thinking that has to happen in it.

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
