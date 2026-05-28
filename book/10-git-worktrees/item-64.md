---
item: 64
theme: git-worktrees
title: "Run parallel Claude sessions in worktrees instead of juggling one checkout"
tags: [worktrees, parallelism, isolation, beta]
claude_code_version: "2.1.150"
stability: beta
status: current
related_items: [20, 51]
things_to_remember:
  - "A worktree gives each Claude session its own branch and working directory, so parallel sessions never collide"
  - "Start an isolated session with `claude -w` (or `--worktree`) rather than branch-switching in a shared checkout"
  - "`worktree.baseRef` controls where new worktrees branch from: `fresh` (clean from the remote default branch) or `head` (your current local state)"
  - "Parallel sessions are the biggest single throughput win — the worktree is what makes the parallelism safe"
agent_steps:
  - "To run a session in isolation, start it with `claude -w` so it gets its own git worktree and branch"
  - "Reach for a worktree whenever a second concurrent session would otherwise fight the first over the working directory"
  - "Set `worktree.baseRef` to `fresh` for a clean tree from the remote, or `head` to include current local tracked changes"
  - "Use plain branches for sequential work; use worktrees when work runs concurrently"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

The bottleneck in working with Claude is rarely the model — it's that you can usually only watch one session at a time. The way past that is to run several at once, and the obstacle to *that* is the working directory. A single checkout has one set of files on disk and one checked-out branch; two Claude sessions sharing it collide immediately, with one switching branches under the other, edits landing in the wrong place, and state turning to mush. Worktrees remove the obstacle by giving each session its own tree and branch. Run three Claudes in three worktrees and they proceed in genuine parallel, oblivious to each other, because there's nothing shared to fight over.

Starting one is a single flag: `claude -w` launches the session in a fresh worktree instead of the main checkout. The decision of *when* to use it is simple — reach for a worktree whenever work is concurrent. Sequential work (finish one task, start the next) is fine in a plain branch in your main checkout. The moment you want a second session running *while* the first is still going, that second session wants its own worktree, because concurrency without isolation is where the collisions live. This is the practical counterpart to the orchestration chapter's parallelism: worktrees are what make running things side by side safe rather than chaotic.

The one knob worth knowing up front is where a new worktree branches from, controlled by `worktree.baseRef`. The `fresh` default branches from the remote's default branch, giving a clean tree that matches what's pushed — ideal for independent new work. Setting it to `head` branches from your current local state instead, carrying along uncommitted tracked changes — useful when the parallel work needs to build on what you have in progress. Pick based on whether the new session should start clean or start from where you are; everything else about the worktree just works like the repository it came from.

## What to avoid

Trying to run two concurrent Claude sessions in one checkout and fighting the constant branch-switch and file collisions. Avoiding parallelism entirely because juggling branches by hand feels error-prone — that's the problem worktrees exist to solve. Reaching for a worktree for purely sequential work, where a plain branch is simpler. Forgetting that `baseRef` decides clean-from-remote versus from-your-local-state, and starting from the wrong base.

## What to do instead

When you want concurrency, give each session its own worktree with `claude -w`. Keep plain branches for sequential work, and reserve worktrees for the case they're built for: more than one session making progress at the same time. Set `worktree.baseRef` deliberately — `fresh` for clean, independent work; `head` when the new session should carry your current local changes. Then treat each worktree as the ordinary repository it is, and let the parallelism be the win.

## Example

Fanning a few independent tasks across worktrees:

```bash
# Terminal 1 — isolated session for the auth refactor
claude -w
> refactor the auth module

# Terminal 2 — a second, fully independent session, no collision
claude -w
> write integration tests for the payments API

# Terminal 3 — a third, in parallel
claude -w
> update the API docs for v2
```

Three sessions, three worktrees, three branches — none touching the others' files. Choosing the base for a new worktree:

```jsonc
// .claude/settings.json
{ "worktree": { "baseRef": "fresh" } }   // clean from origin/<default>
// or
{ "worktree": { "baseRef": "head"  } }   // from current local HEAD, with tracked changes
```

The contrast is the single-checkout approach: `git checkout feature-a`, start Claude, then needing branch B and either stopping the first session or watching it thrash as the branch changes underneath it. Worktrees turn that serialized, collision-prone juggling into clean parallel progress — which is why the practice scales from three sessions to dozens.
