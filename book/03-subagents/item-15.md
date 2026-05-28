---
item: 15
theme: subagents
title: "Spawn a subagent to protect your main context, not to feel productive"
tags: [subagents, mindset, context]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [2, 5]
things_to_remember:
  - "Subagents are context firewalls — their value is what they keep *out* of the main thread, not what they put in"
  - "If the work fits in one or two tool calls inline, a subagent costs more than it saves"
  - "Good fits: large searches, doc reading, dependency audits, anything that would dump pages into the main context"
  - "Each subagent is a fresh process with no memory of the conversation — the briefing cost is real"
agent_steps:
  - "Before spawning a subagent, ask whether the work would meaningfully pollute the main context if done inline — if not, do it inline"
  - "When delegating, plan for a short summary back, not a transcript — the parent should not need to re-read the child's tool output"
  - "Use a subagent for parallel independent work, large-surface research, or operations whose intermediate state you don't want to carry forward"
---

## Why this matters

The instinct most users develop is that subagents are about parallelism or speed. That framing leads to overuse — spawning a subagent for a two-grep lookup, splitting a tidy sequential task into pieces that have to be re-stitched, treating "Agent" as the default verb. The real value is narrower and more important: a subagent runs with its own context window, and only its final message comes back. Whatever it read, searched, or printed stays in the child. The parent thread keeps the conclusion and forgets the noise.

That property — context isolation — is what makes long sessions stay coherent. A 30-tool-call codebase exploration that lives in the main thread fills the context with grep output, file excerpts, and dead ends. The same work delegated to a subagent returns 200 words of synthesis. Multiplied across a session, that difference is the gap between a thread that still tracks the goal at hour three and one that's drowning in its own history.

The right question before spawning is not "is this parallelizable?" but "would doing this inline pollute the main context with stuff I won't need later?" Searches across the whole repo: yes. Reading three docs to find one fact: yes. Editing one file you already have open: no — the inline version is faster and the context cost is negligible.

## What to avoid

Treating subagent calls as a productivity flourish — spawning one to "feel like work is happening" when the work would be one tool call inline. Splitting a sequential task into parallel children just because you can, then spending the next turn reconciling their conflicting changes. Spawning a subagent to do something whose intermediate output you *want* to see and reason about in the main thread.

## What to do instead

Use a subagent when at least one of these holds: the work is large-surface enough that doing it inline would dump pages of tool output into the main thread; it's genuinely independent of other work that's running concurrently; or you want a clean reasoning context for a fresh problem unpolluted by prior assumptions. If none of those apply, just do it inline.

Plan the *return shape* before spawning. "Report in under 200 words" and "answer these three specific questions" are how you get value back from the firewall. A subagent that returns a 2000-word transcript has defeated the purpose.

## Example

Inline — appropriate for a small, scoped change.

```text
> change the timeout in src/api/client.ts from 5s to 10s

[grep for timeout, Edit, done — three tool calls, no subagent needed]
```

Subagent — appropriate for large-surface research that would otherwise flood the thread.

```text
> figure out which call sites still use the old auth helper, and whether
  any of them need migration work before we delete it

Agent(subagent_type="Explore",
      description="Audit old auth helper call sites",
      prompt="Find every call site of `legacyAuthorize` in this repo.
              For each, classify it as (a) trivially migratable to
              `authorize`, (b) needs adapter work, (c) actively
              relied on for behavior the new helper changes. Report
              a table — file:line, classification, one-line reason.
              Under 300 words.")
```

The child reads thirty files; the parent gets a table.
