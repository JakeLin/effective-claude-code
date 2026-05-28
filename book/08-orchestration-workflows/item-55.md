---
item: 55
theme: orchestration-workflows
title: "Drive multi-step work through a task list, not the conversation"
tags: [task-list, workflow, persistence, multi-session]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [50, 51, 69]
things_to_remember:
  - "A task list externalizes the plan into durable state — work survives compaction, session end, and crashes instead of living only in the conversation"
  - "Break multi-step work into tasks small enough to each fit comfortably under half the context window"
  - "Tasks can declare dependencies (this blocks that), so the order is encoded in the list rather than re-derived each turn"
  - "A shared task-list id lets multiple sessions or agents coordinate on the same work"
agent_steps:
  - "For multi-step work, create a task list with one task per independently-completable, verifiable chunk"
  - "Size each task to fit under half the context window so it can be done and verified without running out of room"
  - "Encode ordering with task dependencies (blockedBy/blocks) rather than relying on conversation order"
  - "Use a shared task-list id (CLAUDE_CODE_TASK_LIST_ID) when multiple sessions or agents need to coordinate on the same work"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

A multi-step task held only in the conversation is held in the most fragile place available. The conversation gets compacted — and the plan, now summarized, loses detail. The session ends, or the context is cleared, and the thread of "what's done, what's next" goes with it. Long work that lives only in chat history is one compaction away from Claude losing the plot: re-deriving what it already decided, redoing finished steps, or dropping ones it never reached. A task list fixes this by externalizing the plan into durable state — tasks persist on disk, independent of the conversation, so the work survives compaction, session end, and crashes.

That durability changes how the work behaves. Each task is an explicitly-tracked unit with a status, so "what's done and what's left" is a fact you can read rather than something Claude reconstructs from history every turn. It pairs directly with the two earlier Items: the plan-first habit produces the steps, and the context-budget habit says each step should fit under half the window — a task list is where those steps live, sized so each one can be completed *and verified* without exhausting context. Breaking the work this way also creates natural checkpoints; a task is the right granularity to finish, verify, and gate on before moving to the next.

Tasks also carry structure the conversation can't. Dependencies — this task blocks that one — encode the order in the list itself, so Claude doesn't have to re-derive sequencing from the chat each time, and a task won't start before its blockers are done. And because the list is durable shared state, multiple sessions or agents can coordinate on it: point them at the same task-list id and they see the same statuses, pick up unblocked work, and resume where another left off. For anything spanning more than a handful of steps — or more than one session — the task list is the difference between work that holds its shape and work that frays every time the context turns over.

## What to avoid

Running a ten-step implementation entirely in the conversation, then losing the plan to a compaction halfway through. Making tasks so large that a single one can't be completed and verified within the context budget. Relying on conversation order to remember sequencing, so a cleared or compacted context scrambles what depends on what. Spinning up parallel sessions on the same work with no shared list, so they duplicate effort or collide.

## What to do instead

For multi-step work, put the plan in a task list. Create one task per independently-completable, verifiable chunk, and size each to fit comfortably under half the context window so it can be done and checked without running out of room. Encode ordering with dependencies rather than trusting conversation order, so the sequence survives a context turnover. When more than one session or agent needs to work the same plan, give them a shared task-list id so they coordinate on one durable source of truth instead of diverging copies.

## Example

Multi-step work as durable tasks instead of chat history:

```text
Task list: "oauth-integration"
  1. [done]        Add OAuth client config            (no deps)
  2. [done]        Implement Google provider          (blockedBy: 1)
  3. [in_progress] Implement GitHub provider          (blockedBy: 1)
  4. [pending]     Wire providers into login UI       (blockedBy: 2,3)
  5. [pending]     Integration tests + docs           (blockedBy: 4)
```

After a `/compact` between tasks 2 and 3, the conversation summary may be lossy — but the task list isn't. Claude reads it, sees 1–2 done and 4–5 blocked until 3 lands, and picks up exactly at task 3. Nothing was re-derived from fading history. For multi-session work, share the id:

```bash
CLAUDE_CODE_TASK_LIST_ID=oauth-integration claude
```

A second session started the same way sees the same statuses and can take an unblocked task while the first works another. The list, not the conversation, is the source of truth for what's done and what's next — which is exactly why the work survives everything the conversation doesn't.
