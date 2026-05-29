---
item: 70
theme: agent-teams
title: "Treat agent teams as experimental — enable them deliberately and expect change"
tags: [agent-teams, experimental, beta, configuration, stability]
claude_code_version: "2.1.150"
stability: beta
status: needs-review
related_items: [68]
things_to_remember:
  - "Agent teams are gated behind an experimental flag (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) — they're opt-in, not default"
  - "The feature is the least settled in Claude Code: flags, run modes, and config layout may change between releases"
  - "Run mode matters — in-process keeps teammates in one terminal; split-pane modes need tmux or iTerm2, not every terminal"
  - "Don't build critical, unattended automation on a moving experimental API — use teams interactively while they stabilize"
agent_steps:
  - "Enable teams explicitly with the experimental env var; don't assume the feature is on by default"
  - "Pick a run mode that matches your terminal — in-process anywhere, split-pane only where tmux/iTerm2 supports it"
  - "Re-verify flag names, modes, and config layout against current docs rather than trusting older examples"
  - "Keep agent teams out of load-bearing unattended pipelines until the API stabilizes; prefer interactive use for now"
---

## Why this matters

Agent teams are the newest and least settled capability in this book, and that status should shape how you use them. The feature is gated behind an explicit experimental flag — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — which is itself the signal: opt-in, not on by default, and offered with the understanding that it's still taking shape. The principles in the previous two Items (when a team beats subagents, how teammates coordinate) are durable, but the *specifics* — flag names, run modes, where team config lives, the exact coordination events — are the parts most likely to shift between releases. Knowing which is which keeps you from building on the parts that move.

The practical consequence is in two places. First, enablement and run mode are real choices, not boilerplate. You turn teams on deliberately with the env var, and you pick a display mode that fits your environment: in-process keeps every teammate in your one terminal and works anywhere, while split-pane modes give each teammate its own pane but depend on tmux or iTerm2 and won't work in terminals (like VS Code's) that don't support them. Picking the mode your setup actually supports avoids a frustrating first run. Second — and this is the caution that matters most — an experimental API is the wrong foundation for critical, unattended automation. A flag rename or a behavior change in a future release will break a pipeline that depended on today's exact interface, and unattended is exactly where that break hurts most.

So the posture is: use agent teams, but use them with the provisionality the feature deserves. Drive them interactively, where you're present to adapt when something changes, rather than wiring them into the headless pipelines of Chapter 9 where you've walked away. Re-check the flags and config against current docs rather than trusting an example from three releases ago. This Item carries `status: needs-review` on purpose — it's the one most likely to need updating, and that's the honest state of an experimental feature. Treat the durable principles as settled and the surface details as a moving target, and you get the value of teams without betting on an interface that hasn't finished forming.

## What to avoid

Assuming agent teams are available by default and being surprised when nothing happens without the flag. Choosing a split-pane run mode in a terminal that doesn't support it. Copying exact flags and config from old examples without checking they still hold. Building critical, unattended automation on the experimental API, so a future release quietly breaks a pipeline you weren't watching.

## What to do instead

Enable teams explicitly with the experimental env var, and choose a run mode your terminal actually supports — in-process anywhere, split-pane only with tmux or iTerm2. Re-verify the current flags, modes, and config layout against the docs rather than trusting stale examples. And keep teams in interactive use, where you can adapt to changes, until the API stabilizes — don't make a moving experimental feature the foundation of critical unattended work.

## Example

Enabling teams deliberately, with a mode that fits:

```bash
# Opt in explicitly — not on by default
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude

# In-process: all teammates in this one terminal, works anywhere
claude --teammate-mode in-process

# Split panes: a pane per teammate — only with tmux or iTerm2
tmux new -s dev
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --teammate-mode tmux
```

The right posture, contrasted:

```text
Good:  interactive team session for a parallel refactor — you're present,
       and a flag change mid-feature is a minor annoyance you adapt to.

Risky: a nightly headless pipeline that depends on today's exact team flags
       and config — a future release renames something and it breaks while
       no one is watching.
```

The durable advice (when and how to use a team) holds; the surface (flags, modes, config paths) is provisional. Use teams for the parallelism, keep them interactive while the feature settles, and re-check the specifics each release — which is exactly what an experimental feature asks of you.
