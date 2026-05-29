---
item: 66
theme: git-worktrees
title: "Give each parallel agent its own worktree so they never collide"
tags: [worktrees, subagents, parallelism, batch, beta]
claude_code_version: "2.1.150"
stability: beta
status: current
related_items: [20, 52, 64]
things_to_remember:
  - "Set `isolation: \"worktree\"` on a subagent so it works in its own tree, not the shared working directory"
  - "Worktree isolation is what makes many agents editing the same repo at once safe rather than chaotic"
  - "`worktree.bgIsolation` governs background agents — keep them out of the main checkout until explicitly entered"
  - "Large fan-out work (mass migrations via `/batch`) relies on each agent getting its own worktree"
agent_steps:
  - "For a subagent that edits files concurrently with others, set `isolation: \"worktree\"` in its definition"
  - "Keep `worktree.bgIsolation` at its isolating default so background agents don't edit the main checkout unexpectedly"
  - "For large parallelizable changesets, fan out across worktree agents (e.g. via `/batch`) so each works an independent copy"
  - "Reserve shared-directory (non-isolated) agents for read-only or strictly sequential work"
---

## Why this matters

The previous chapters established that parallel subagents multiply throughput; worktrees are what make that parallelism *safe* when the agents write. Two subagents editing files in the same working directory at once is the same collision problem as two interactive sessions sharing a checkout — edits interleave, one agent's changes vanish under another's, and the result is incoherent. Setting `isolation: "worktree"` on a subagent gives it its own tree to work in, so concurrent agents modify their own copies and their results are merged deliberately afterward rather than racing into one directory. Isolation converts "many agents on one repo" from chaos into clean parallel work.

This is essential the moment agents are doing concurrent *writes*. Read-only or strictly sequential agents can share the main checkout harmlessly — there's nothing to collide over. But a fan-out where several agents each change code at the same time needs per-agent isolation, full stop. There's also a background-agent dimension: `worktree.bgIsolation` controls whether background agents may touch the main checkout, and its isolating default keeps them in their own trees until explicitly brought into the working copy. That default is a guardrail — it prevents a background job from quietly editing the files you're working in, which is exactly the surprise isolation is meant to prevent.

The principle scales all the way up. Large mechanical changes across a whole codebase — a mass migration, a sweeping refactor — are the canonical fan-out job, and tooling like `/batch` distributes them across many worktree agents, each working an independent copy of the repo in parallel. Dozens or hundreds of agents can make progress at once precisely because no two share a working directory. The rule is constant from two agents to two hundred: if they write concurrently, isolate each in its own worktree; if they don't, you don't need to. Get that boundary right and parallel agents become a force multiplier instead of a merge nightmare.

## What to avoid

Running multiple file-editing subagents in the shared working directory and getting interleaved, clobbered changes. Disabling or loosening `worktree.bgIsolation` so a background agent edits the main checkout while you're working in it. Attempting a large parallel migration without per-agent isolation, then untangling the collision afterward. Over-isolating trivial read-only agents, where a worktree is needless overhead.

## What to do instead

Isolate agents that write concurrently. Set `isolation: "worktree"` on subagents that edit files alongside others, so each works its own tree and results merge deliberately. Keep `worktree.bgIsolation` at its isolating default so background agents stay out of your checkout until explicitly entered. For large parallelizable changesets, fan out across worktree agents so each gets an independent copy. Leave non-isolated, shared-directory agents for read-only or sequential work, where isolation would only add cost.

## Example

A subagent isolated for concurrent editing:

```yaml
---
name: migrator
description: Migrates one package to the new API
isolation: worktree
---
```

Several `migrator` agents can now run at once, each in its own tree, none clobbering another's edits. Background isolation kept safe by default:

```jsonc
// .claude/settings.json
{ "worktree": { "bgIsolation": "worktree" } }
```

Background agents work their own trees and can't silently change the files in your main checkout. And the large-scale shape — fan-out across many worktree agents for a mass change:

```text
/batch  → interviews you, then spawns N worktree agents:
  agent 1 → migrate packages/a   (own worktree)
  agent 2 → migrate packages/b   (own worktree)
  ...
  agent N → migrate packages/n   (own worktree)
```

Each agent edits an independent copy in parallel; nothing collides because nothing is shared. The same boundary decides every case — concurrent writers get their own worktree, everything else doesn't need one.
