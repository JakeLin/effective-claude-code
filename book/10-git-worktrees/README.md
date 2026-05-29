# Git Worktrees

> **Beta.** Worktree support in Claude Code is stable enough to rely on day to day, but the specifics — flag names, settings keys, defaults — are still moving. Treat the principles here as durable and re-check the exact syntax against the current docs.

A git *worktree* is a built-in git feature: it lets one repository have several working trees checked out at once, each on its own branch, each with its own files on disk. Claude Code leans on this to solve a problem that shows up the moment you want more than one Claude working at a time — in a single checkout, two concurrent sessions step on each other constantly, with branch switches blocking, files changing underfoot, and working state getting tangled. Give each session its own worktree and the collisions vanish: every Claude has its own tree, its own branch, its own clean slate.

That unlocks the practice the Claude Code team rates as its single biggest productivity multiplier — running many sessions in parallel. Instead of one Claude you babysit, you fan work across three, five, or dozens of worktrees, each making progress independently, and you check in on them as they finish. The same mechanism powers parallel *subagents* (each in its own isolated tree) and large fan-out migrations across the whole codebase.

This is a short chapter because the durable principles are few, even though the technique is powerful. It covers when to reach for a worktree over a plain branch and how to start one, how to keep worktrees from drowning you in duplicated disk, how to isolate parallel agents so they never collide, and a few ergonomics for navigating a fleet of them without losing track.
