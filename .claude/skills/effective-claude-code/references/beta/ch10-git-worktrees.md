# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable + beta; chapters 10 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 10 --include-beta --agent-steps -->

## Git Worktrees *(beta)*

### Run parallel Claude sessions in worktrees instead of juggling one checkout [#64]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- A worktree gives each Claude session its own branch and working directory, so parallel sessions never collide
- Start an isolated session with `claude -w` (or `--worktree`) rather than branch-switching in a shared checkout
- `worktree.baseRef` controls where new worktrees branch from: `fresh` (clean from the remote default branch) or `head` (your current local state)
- Parallel sessions are the biggest single throughput win — the worktree is what makes the parallelism safe

**Agent steps:**
1. To run a session in isolation, start it with `claude -w` so it gets its own git worktree and branch
2. Reach for a worktree whenever a second concurrent session would otherwise fight the first over the working directory
3. Set `worktree.baseRef` to `fresh` for a clean tree from the remote, or `head` to include current local tracked changes
4. Use plain branches for sequential work; use worktrees when work runs concurrently

### Keep worktrees cheap — symlink the heavy directories, sparse-checkout the rest [#65]
<!-- ecc-meta: target="settings-json" action="add" check=".claude/settings.json has no worktree.symlinkDirectories configured and project has large regenerable directories (node_modules, .venv, .cache)" -->
- Each worktree is a full checkout on disk — running many of them duplicates large directories unless you intervene
- Symlink heavy, regenerable directories (node_modules, caches) into worktrees with `worktree.symlinkDirectories` instead of copying them
- Use `worktree.sparsePaths` to check out only the directories a worktree needs in a large monorepo
- Let the startup cleanup sweep (`cleanupPeriodDays`) reap orphaned worktrees so they don't accumulate

**Agent steps:**
1. When running many worktrees, set `worktree.symlinkDirectories` for large regenerable dirs (e.g. node_modules, .cache) to avoid duplicating them
2. In a large monorepo, set `worktree.sparsePaths` so each worktree checks out only the paths it needs
3. Rely on the `cleanupPeriodDays` startup sweep to remove orphaned subagent worktrees; don't let stale trees pile up
4. Treat disk cost as a function of (worktree count × checkout size) and shrink the second factor when the first grows

### Give each parallel agent its own worktree so they never collide [#66]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Set `isolation: \"worktree\"` on a subagent so it works in its own tree, not the shared working directory
- Worktree isolation is what makes many agents editing the same repo at once safe rather than chaotic
- `worktree.bgIsolation` governs background agents — keep them out of the main checkout until explicitly entered
- Large fan-out work (mass migrations via `/batch`) relies on each agent getting its own worktree

**Agent steps:**
1. For a subagent that edits files concurrently with others, set `isolation: \"worktree\"` in its definition
2. Keep `worktree.bgIsolation` at its isolating default so background agents don't edit the main checkout unexpectedly
3. For large parallelizable changesets, fan out across worktree agents (e.g. via `/batch`) so each works an independent copy
4. Reserve shared-directory (non-isolated) agents for read-only or strictly sequential work

### Name and organize your worktrees so you can navigate them [#67]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Running many worktrees is only a win if you can tell them apart — name them by task, not by a random hash
- Set up shell aliases or named terminal tabs so you can hop between worktrees in a keystroke
- Show the current branch and context usage in your statusline so each session announces which worktree it is
- A dedicated, long-lived worktree for read-only work (logs, queries, exploration) keeps your task trees clean

**Agent steps:**
1. Name worktrees and their branches after the task they hold, so the fleet is legible at a glance
2. Add shell aliases or named/colored terminal tabs to switch between worktrees quickly
3. Customize the statusline to show the git branch (and context usage) so each session identifies its worktree
4. Keep a dedicated worktree for read-only exploration (log reading, queries) separate from active task trees

