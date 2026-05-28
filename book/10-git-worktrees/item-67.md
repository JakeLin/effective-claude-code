---
item: 67
theme: git-worktrees
title: "Name and organize your worktrees so you can navigate them"
tags: [worktrees, ergonomics, workflow, statusline, beta]
claude_code_version: "2.1.150"
stability: beta
status: current
related_items: [64]
things_to_remember:
  - "Running many worktrees is only a win if you can tell them apart — name them by task, not by a random hash"
  - "Set up shell aliases or named terminal tabs so you can hop between worktrees in a keystroke"
  - "Show the current branch and context usage in your statusline so each session announces which worktree it is"
  - "A dedicated, long-lived worktree for read-only work (logs, queries, exploration) keeps your task trees clean"
agent_steps:
  - "Name worktrees and their branches after the task they hold, so the fleet is legible at a glance"
  - "Add shell aliases or named/colored terminal tabs to switch between worktrees quickly"
  - "Customize the statusline to show the git branch (and context usage) so each session identifies its worktree"
  - "Keep a dedicated worktree for read-only exploration (log reading, queries) separate from active task trees"
---

## Why this matters

The throughput win from many worktrees has a failure mode: a pile of indistinguishable checkouts you can't navigate. Five sessions across five trees only helps if you know, at a glance, which is which — otherwise you waste the time you saved hunting for the right terminal and double-checking which branch you're about to commit on. Once parallelism is the point, *legibility* of the fleet becomes a real concern, and a little organization up front is what keeps a dozen worktrees from becoming a dozen sources of confusion.

The ergonomics that practitioners converge on are small and worth copying. Name worktrees and their branches after the task they hold, not a default hash, so the name itself tells you what's inside. Set up shell aliases or named, color-coded terminal tabs so switching between trees is a keystroke rather than a `cd` you have to think about. Customize the statusline to show the current git branch and context usage, so every session announces which worktree it is the instant you look at it — no guessing, no accidental commit to the wrong branch. None of these change what worktrees *do*; they change whether you can run many of them without losing track.

One organizational pattern earns special mention: a dedicated, long-lived worktree for read-only work — reading logs, running queries, general exploration — kept separate from the trees where active changes happen. It gives you a stable place to investigate without polluting a task branch with stray state, and it means your task worktrees stay focused on the one change each is making. The broader principle is that a fleet of worktrees is a small system you operate, and like any system it benefits from naming, fast navigation, and clear signals about what's what. Spend the few minutes on ergonomics and the parallelism stays a win instead of curdling into chaos.

## What to avoid

Letting worktrees keep default hash-like names so you can't tell them apart. Navigating a fleet by `cd`-ing around and squinting at paths. Running several sessions with no branch indicator, then committing to the wrong one. Doing throwaway log-reading and queries inside an active task worktree and leaving it cluttered with unrelated state.

## What to do instead

Treat the worktree fleet as something you operate. Name worktrees and branches after their task so they're legible. Add shell aliases or named, color-coded terminal tabs to switch in a keystroke. Put the git branch and context usage in your statusline so each session identifies itself. And keep a dedicated worktree for read-only exploration, separate from the trees doing active work, so your task worktrees stay clean and focused.

## Example

Ergonomics for a navigable fleet:

```bash
# Task-named worktrees and quick-hop aliases
alias wa='cd ~/wt/auth-refactor && claude -c'
alias wb='cd ~/wt/payments-tests && claude -c'
alias wlogs='cd ~/wt/analysis'        # dedicated read-only tree

# Statusline that announces the worktree (configured via /statusline)
#   ⎇ auth-refactor   ctx 38%
```

The names carry the meaning — `auth-refactor`, `payments-tests`, `analysis` — so you always know which tree you're in, the aliases make switching instant, and the statusline shows the branch so you never commit to the wrong one. The `analysis` tree is the read-only pattern: a stable spot for reading logs and running queries that keeps the two task trees uncluttered. Contrast a fleet of `worktree-3f9a2c` directories navigated by hand — same isolation, but you spend the saved time just finding your place. The organization is cheap and it's what makes running many worktrees actually feel faster.
