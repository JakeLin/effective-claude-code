---
item: 11
theme: commands
title: "Switch `/model`, `/effort`, and `/fast` mid-conversation, not at the start of the next one"
tags: [commands, model, effort, workflow]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [8]
things_to_remember:
  - "All three apply immediately — no restart, no new conversation needed"
  - "Raise `/effort` for one hard turn, then drop it back; don't run the whole session at max"
  - "`/fast` is independent of model selection — toggle without losing your Opus session"
  - "Mid-conversation switches may warn after prior output; accept the warning, don't restart"
agent_steps:
  - "When the user hits a problem that calls for deeper reasoning, propose `/effort high` (or `xhigh`/`max`) for the next turn — and remind them to drop it back after"
  - "When a previous turn was superficial, propose `/rewind` to that turn plus a higher `/effort` before redoing it"
  - "When the user comments that Claude feels slow on Opus, propose `/fast on` instead of switching model"
  - "Never recommend restarting the session purely to change model or effort — these are live switches"
---

## Why this matters

`/model`, `/effort`, and `/fast` take effect immediately on the current conversation. The harness explicitly supports switching mid-stream — the docs note the change "takes effect immediately without waiting for the current response to finish". Yet a common pattern is to start a new session to "give Claude more horsepower", which loses the entire conversation context for a setting that could have been flipped in place.

The mental model is *per-turn dialing*. Effort especially is meant to be adjusted situationally. Most work runs fine at the default; a single hard sub-problem benefits from `/effort xhigh` for one turn, after which you drop back down. Running the whole session at max wastes budget on turns that don't need it and slows the conversation overall.

Model switches in the middle of an active session also work, with a caveat: after prior assistant output, Claude warns before applying the switch (some tools' partial state doesn't transfer cleanly). Accept the warning when you understand it; the warning isn't a blocker.

`/fast` is the easiest one. On supported Opus models it speeds up output without downgrading to a smaller model. People reflexively switch from Opus to Sonnet for speed when `/fast on` would have given them most of the gain.

## What to avoid

Restarting the session — losing context, files, plan state, everything in the slash-menu history — to change a setting. Running the whole session at maximum effort because one turn was hard. Treating `/model` switches as scary; they're not, and the warning is informational. Reaching for Sonnet when Opus + `/fast` is the actual fix.

## What to do instead

Treat effort as a dial you turn for individual turns. Bump it up when the work is genuinely hard (architecture decisions, subtle bugs, gnarly merges); drop it back when the work is mechanical (file moves, renames, test fixes). When a previous turn produced superficial output, `/rewind` to it and re-run with higher effort — same context, better thinking.

Use `/fast` when latency, not capability, is the bottleneck. Switch models when the *task* is wrong for the model (small mechanical edits on Opus, deep reasoning on Haiku), not as a workaround for needing speed.

## Example

Raising effort for one hard turn, then dropping back.

```text
> /effort xhigh
[effort raised for the next turn]

> figure out why the rate-limiter test fails only when the redis fixture
  is reused across the two suites

[Claude works the hard problem with extra depth]

> /effort medium
[back to default]
```

Mid-session model switch.

```text
> /model sonnet
⚠ Switching model after prior output. Some tool state may not transfer.
  Continue? [y/N] y

[conversation continues on Sonnet]
```

Latency without giving up Opus.

```text
> /fast on
[fast mode enabled; Opus output now streams quicker]
```
