---
item: 8
theme: commands
title: "Reach for a built-in command before reasoning in prose"
tags: [commands, mindset, workflow]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: []
things_to_remember:
  - "If you're typing a request, check `/help` first — there's a good chance a command does it directly"
  - "Built-in commands run as harness logic — deterministic, no tokens, no guessing at intent"
  - "`/powerup` walks through built-ins interactively; worth ten minutes once per release"
  - "The slash menu is large and changing — re-scan after upgrades, don't trust your old mental list"
agent_steps:
  - "Before composing a chat instruction for the user, scan whether a built-in command (`/diff`, `/context`, `/usage`, `/permissions`, `/agents`, etc.) does it directly — propose the command name"
  - "When the user asks something the harness exposes as a command, recommend the command rather than executing the equivalent through tool calls"
  - "After each Claude Code release, point the user at `/release-notes` and `/powerup` to surface new commands"
---

## Why this matters

Claude Code ships roughly eighty commands. Each one was added because a recurring user need was concrete and deterministic enough to bake into the harness: show the diff, summarize the conversation, change the model, audit memory, edit hooks, undo a turn. When the harness already does the thing, asking Claude to do it in prose is slower (a turn of generation versus a keystroke), softer (probabilistic answer versus measured one), and more expensive (tokens versus zero).

The trap is that the slash menu is *too* useful — most users learn `/clear` and `/compact` early and stop exploring. The interesting commands are deeper in the list: `/context` for what's actually filling your conversation, `/rewind` for undoing a turn, `/effort` for raising depth on the next response, `/diff` for inspecting uncommitted work, `/agents` and `/permissions` and `/hooks` for managing config you'd otherwise hand-edit. None of them are obscure. They're just not surfaced unless you go looking.

The orientation that pays off: treat the slash menu as your first reach for any harness-level operation. If you find yourself describing what you want in chat, pause and check whether a `/` command does it. After every Claude Code upgrade, spend ten minutes with `/release-notes` and `/powerup` so you know what's new.

## What to avoid

Asking Claude "how much context am I using?" instead of running `/context`. Asking for an estimated cost instead of `/usage`. Typing "show me the diff" instead of `/diff`. Restarting Claude Code to change the model instead of `/model`. Anything where the harness has a measured answer and you're asking Claude to guess.

## What to do instead

Build a habit of scanning the slash menu before composing prose. Read the release notes when a Claude Code upgrade lands; the surface area moves. Treat `/help` and `/powerup` as part of onboarding for new teammates — going through them once saves months of typing requests Claude can't fulfill as well as the harness.

This isn't about avoiding chat. It's about reserving chat for the work only Claude can do — reasoning, code, decisions — and letting the harness handle anything mechanical.

## Example

Same intent, prose versus command.

```text
> can you tell me roughly how full the context window is right now?

Based on my read of the conversation, you've used maybe 30–40% of your
context window. There's been a fair bit of tool output …
```

```text
> /context

[grid showing 38% used, 14% from MCP tool results, 4% from CLAUDE.md,
 with a warning that one tool result is consuming 9% on its own]
```
