---
item: 20
theme: subagents
title: "Run independent agents in parallel; use background only for genuinely-async work"
tags: [subagents, parallelism, background, orchestration]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [15, 64, 66, 68]
things_to_remember:
  - "Multiple Agent calls in one message run concurrently — that's the parallelism win, not `run_in_background`"
  - "Use background mode when you have other work to do while the agent runs, not as a default"
  - "Don't parallelize agents whose outputs feed each other — sequence them so the second has the first's result"
  - "After a parallel batch, reconcile in the parent — don't ask one of the children to merge the others' findings"
agent_steps:
  - "When delegating multiple independent tasks, send all Agent tool calls in a single message — they will run in parallel"
  - "If task B needs B's prompt to depend on task A's result, sequence them across turns — do not parallelize"
  - "Reserve `run_in_background: true` for cases where the parent will actually do other work while waiting"
  - "After parallel agents return, do the reconciliation in the parent thread rather than spawning another agent to merge"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

Two different mechanisms get conflated as "parallelism" and they do different things. Multiple Agent calls in a single assistant message run **concurrently** — the harness fans them out, all of them work, and their results come back together. That's the lever you reach for when you have several independent pieces of work and want them to overlap in wall-clock time. `run_in_background: true` is **asynchrony** — the agent runs while the parent does other things, and the result arrives later as a notification. The parent doesn't block on it.

Most users want concurrent, not asynchronous. Concurrent is for "I have three independent investigations and want all three results to come back so I can decide." Asynchronous is for "I'm going to keep doing other work and I'll handle the result whenever it shows up." If you `run_in_background` an agent and then sit there waiting for it, you've picked the wrong tool — you wanted a foreground call with a sibling foreground call running alongside it.

The other half of orchestration is sequencing. Agents whose prompts depend on prior agents' outputs must be sequenced across turns — you can't put both in one message because the second's prompt doesn't exist yet. The mistake here is parallelizing tasks that aren't actually independent and then having to patch up the conflicting results in a third agent call.

Reconciliation is a parent-thread responsibility. After parallel agents return, the synthesis — which finding matters, which conflict to resolve which way — belongs to the parent, where the full context of the user's goal lives. Spawning yet another agent to merge the results pushes that decision into a process that doesn't have the context to make it well.

## What to avoid

Putting `run_in_background: true` on agents whose result you immediately need. Sending dependent agents in parallel and then writing a third one to resolve the conflicts they create. Sequencing independent agents across turns when one parallel message would have done. Polling for background agents in a sleep loop — the harness notifies on completion.

## What to do instead

Decide first whether the tasks are independent or dependent. Independent: send them all in one message as separate Agent calls; they fan out concurrently. Dependent: sequence them across turns, feeding the prior result into the next prompt. Reserve background mode for the cases where you have genuinely separate work to do while waiting.

After parallel agents return, do the reconciliation in the parent thread. That's where the context to make the decision lives.

## Example

Parallel — three independent investigations sent in one message.

```text
Agent(subagent_type="Explore",
      description="API call site audit",
      prompt="List all call sites of `legacyClient.fetch` ...")

Agent(subagent_type="Explore",
      description="Migration script inventory",
      prompt="List every file under `db/migrations/` and classify ...")

Agent(subagent_type="Explore",
      description="Feature flag usage map",
      prompt="Find all references to `growthbook` ...")
```

Three concurrent children, three results back, one turn of wall-clock time.

Sequenced — the second's prompt depends on the first.

```text
Turn 1:
Agent(description="Find the failing test's call graph",
      prompt="The test `auth/login.test.ts:42` is failing. Map the
              call graph of the code path it exercises. Report
              filenames and function names only.")

[parent receives the call graph]

Turn 2:
Agent(description="Diff the call graph against last green commit",
      prompt="Given this call graph: [...], diff each function against
              the version at commit a3f2b1 (last known green) and
              report which changed.")
```

Background — appropriate only when the parent has other work to do.

```text
Agent(description="Generate full API client from updated spec",
      run_in_background=true,
      prompt="Regenerate the TypeScript API client from
              `openapi.yaml`. This usually takes 90 seconds. Report
              files written.")

[parent goes back to editing tests; harness notifies when the
 regeneration finishes]
```
