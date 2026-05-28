---
item: 51
theme: orchestration-workflows
title: "Treat the context window as a budget you actively manage"
tags: [context, compaction, workflow, performance]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [50, 52]
things_to_remember:
  - "The context window is finite, and output quality degrades as it fills — a bloated context makes Claude slower and less accurate"
  - "Compact deliberately (around half-full) rather than waiting for auto-compaction to fire at an arbitrary moment"
  - "Clear context between unrelated tasks so old, irrelevant history stops competing for attention"
  - "Break work into chunks that each fit comfortably under half the window, so no single step runs out of room"
agent_steps:
  - "Watch context usage (/context) and run /compact with focusing instructions at roughly 50% rather than letting it auto-fire"
  - "Use /clear when starting an unrelated task so prior history doesn't dilute the new one"
  - "Scope each task or subtask to fit comfortably under half the context window; split anything larger"
  - "Move large side-investigations into subagents (their own context) instead of letting them fill the main window"
---

## Why this matters

Output quality on real work is a function of the *effective context* the model sees — and that context window is finite. As it fills, two things happen, both bad. The model has to attend to more material per turn, which makes it slower and dilutes its focus on what currently matters; and the relevant signal — the file you're editing, the test that's failing — gets buried under turns of history that have stopped being relevant. A context window that's 90% full of an hour-old tangent is a context window doing 10% useful work. Managing the budget isn't housekeeping; it's directly protecting the quality of every subsequent response.

The lever for this is compaction, and the discipline is to use it *deliberately*. Compaction summarizes prior turns into a compact form, freeing space while preserving the thread. The harness can do this automatically when the window gets dangerously full — but auto-compaction fires at an arbitrary moment, often mid-thought, and summarizes whatever happens to be there. Compacting yourself at around half-full, with instructions about what to keep ("preserve the API design decisions, drop the file-by-file exploration"), gives you a clean, focused context at a moment you chose, summarized around what you know matters. Predictable beats arbitrary.

Two habits make the budget easier to keep. First, clear context between unrelated tasks: when you finish the auth refactor and move to a documentation fix, the auth history is pure noise for the new task, and clearing it restores a full window. Second, size the work to the budget — break a large task into chunks that each fit comfortably under half the window, so no single step exhausts its room and forces a mid-step compaction. And when a side-investigation would itself fill the window (reading a large dependency, exploring an unfamiliar subsystem), that's exactly what subagents are for — a separate context, covered in the next Item. The through-line: the window is a resource, and spending it on stale or irrelevant material is spending it on nothing.

## What to avoid

Running a long session without ever compacting, until quality quietly degrades and you blame the model. Letting auto-compaction fire at an arbitrary point instead of compacting deliberately at a good one. Carrying an entire unrelated prior task in context while starting a new one. Pointing Claude at a task so large it can't fit the relevant material under the window at once, then wondering why it loses the thread halfway through.

## What to do instead

Treat context as a budget you watch and spend on purpose. Keep an eye on usage and compact at roughly half-full, with instructions about what to preserve, rather than waiting for the automatic fallback. Clear context when you switch to an unrelated task so old history stops competing for attention. Size each task or subtask to fit comfortably under half the window, splitting anything bigger. And push large side-investigations into subagents so they consume their own context instead of yours.

## Example

Deliberate management across a session:

```text
[ context 18% ]  Start: plan and implement the rate limiter.
[ context 47% ]  Limiter done, tests passing.
                 → /compact "keep the limiter design and the test
                    command; drop the file-by-file exploration"
[ context 12% ]  Clean, focused context. Continue with config wiring.

Switching to an unrelated task:
[ context 40% ]  Limiter work fully done and committed.
                 → /clear
[ context  3% ]  Fresh window for the unrelated docs fix.
```

Contrast the unmanaged session: never compacting, never clearing, until the window is 95% full of three finished tasks and auto-compaction fires mid-edit, summarizing away the detail you were actually using. Same model, sharply worse results — because by then the effective context is mostly stale history. The fix costs two commands used at the right moments: compact around half-full, clear between unrelated tasks, and keep each step sized to fit.
