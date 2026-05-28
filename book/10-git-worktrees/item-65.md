---
item: 65
theme: git-worktrees
title: "Keep worktrees cheap — symlink the heavy directories, sparse-checkout the rest"
tags: [worktrees, disk, performance, cleanup, beta]
claude_code_version: "2.1.150"
stability: beta
status: current
related_items: [64]
things_to_remember:
  - "Each worktree is a full checkout on disk — running many of them duplicates large directories unless you intervene"
  - "Symlink heavy, regenerable directories (node_modules, caches) into worktrees with `worktree.symlinkDirectories` instead of copying them"
  - "Use `worktree.sparsePaths` to check out only the directories a worktree needs in a large monorepo"
  - "Let the startup cleanup sweep (`cleanupPeriodDays`) reap orphaned worktrees so they don't accumulate"
agent_steps:
  - "When running many worktrees, set `worktree.symlinkDirectories` for large regenerable dirs (e.g. node_modules, .cache) to avoid duplicating them"
  - "In a large monorepo, set `worktree.sparsePaths` so each worktree checks out only the paths it needs"
  - "Rely on the `cleanupPeriodDays` startup sweep to remove orphaned subagent worktrees; don't let stale trees pile up"
  - "Treat disk cost as a function of (worktree count × checkout size) and shrink the second factor when the first grows"
ecc_meta:
  target: settings-json
  action: add
  check: ".claude/settings.json has no worktree.symlinkDirectories configured and project has large regenerable directories (node_modules, .venv, .cache)"
---

## Why this matters

A worktree is a real checkout — every file on disk, its own copy. That's exactly what makes it isolated, and it's also what makes it expensive at scale. One extra worktree is nothing; the parallelism this chapter is built around means *many* worktrees, and the disk cost is the worktree count times the checkout size. In a project with a multi-gigabyte `node_modules` or a large monorepo, five worktrees can mean five copies of everything, and the duplication turns the productivity win into a disk problem. The fix isn't fewer worktrees — it's smaller ones.

Two settings shrink the per-worktree footprint, and they target the two sources of bloat. `worktree.symlinkDirectories` handles the heavy, *regenerable* directories — `node_modules`, build caches — by symlinking them into each worktree from the main repo instead of duplicating them. These directories don't need to be independent per worktree; they're derived artifacts, so sharing one copy is both correct and far cheaper. `worktree.sparsePaths` handles the monorepo case: with sparse-checkout, a worktree writes only the directories it actually needs to disk and leaves the rest unmaterialized, so a session working on one package doesn't carry the other forty. Together they keep each worktree to roughly the size of the work it's doing, not the size of the whole repo.

The last piece is not letting old worktrees accumulate. Subagent worktrees in particular are created and abandoned constantly, and orphaned trees left on disk are pure waste. The startup cleanup sweep governed by `cleanupPeriodDays` reaps these automatically, so the steady state stays bounded rather than growing every session. The mental model is simple: isolation costs disk, that cost scales with how many worktrees you run, and you control it by making each checkout lean (symlink the heavy regenerable dirs, sparse-checkout only what's needed) and letting cleanup remove the dead ones. Do that and you can run a fleet of worktrees without watching your disk fill up.

## What to avoid

Spinning up many worktrees of a heavy project with default settings, duplicating `node_modules` and caches into every one. Checking out an entire large monorepo into each worktree when a session only touches one package. Letting orphaned subagent worktrees pile up because cleanup was disabled or the period set too long. Treating disk as free and discovering the cost only when the volume fills.

## What to do instead

Make each worktree lean. Symlink the heavy, regenerable directories with `worktree.symlinkDirectories` so they're shared rather than copied. In a monorepo, set `worktree.sparsePaths` so each worktree materializes only the paths it needs. Leave the `cleanupPeriodDays` sweep enabled so orphaned trees get reaped. Scale the parallelism freely, and keep the per-worktree footprint small enough that the count doesn't matter.

## Example

Settings that keep a fleet of worktrees affordable:

```jsonc
// .claude/settings.json
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"],
    "sparsePaths": ["packages/web", "shared/utils"]
  },
  "cleanupPeriodDays": 30
}
```

With this, a new worktree shares one `node_modules` instead of copying gigabytes, materializes only the two package paths a session needs rather than the whole monorepo, and orphaned trees are swept after 30 idle days. The contrast is the default-everything setup: ten worktrees, ten full `node_modules`, ten complete monorepo checkouts, and a steadily filling disk — the parallelism working against you. Shrink the checkout and the same ten worktrees cost a fraction as much, which is what lets the count grow without the disk becoming the bottleneck.
