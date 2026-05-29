---
item: 50
theme: orchestration-workflows
title: "Make Claude plan before it implements anything non-trivial"
tags: [planning, plan-mode, rpi, workflow]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [41, 51, 55]
things_to_remember:
  - "Separate thinking from doing: have Claude research and propose a plan before it edits a single file"
  - "Plan mode is read-only by guarantee — Claude explores and proposes, but can't change anything until you approve"
  - "Review and edit the plan while it's cheap to change; a wrong plan caught here costs minutes, caught after implementation costs hours"
  - "For larger work, make the phases explicit (research → plan → implement) with a gate between each"
agent_steps:
  - "For any non-trivial task, enter plan mode (Shift+Tab to cycle, or --permission-mode plan) before making changes"
  - "Let Claude read the relevant code and propose a concrete, phased plan rather than starting to edit immediately"
  - "Review the proposed plan, edit it where it's wrong or thin, and only then approve to switch into an edit-capable mode"
  - "For larger features, run distinct phases — research/feasibility, then planning, then implementation — with a human checkpoint between them"
---

## Why this matters

The fastest way to waste an hour with Claude is to let it start editing before it understands the problem. A model that jumps straight to code commits to an approach implied by its first guess, and every subsequent edit reinforces that guess. If the guess was wrong — wrong file, wrong abstraction, wrong assumption about how the existing system works — you don't find out until the change is half-built and entangled, and unwinding it costs far more than the planning would have. Separating *thinking* from *doing* is the single highest-leverage workflow habit, and it's why plan-first beats code-first on anything beyond a trivial edit.

Plan mode is the mechanism that makes this safe and reviewable. It's read-only by guarantee (Item 41): Claude can read files, search, and run read-only commands to understand the codebase, but it cannot write until you approve. The output is a concrete, usually phased plan you can actually read. Crucially, the plan is *cheap to change*. Catching "this should extend the existing handler, not add a parallel one" while it's a line in a plan costs seconds; catching it after Claude has written the parallel handler costs an unwind. The review step is where your judgment enters at the moment it's most leveraged — before any code exists.

For larger work, make the phases explicit rather than implicit. A research → plan → implement structure puts a gate between understanding the problem, deciding the approach, and building it. The research phase can even reach a go / no-go verdict on feasibility before anyone designs anything; the planning phase produces the roadmap; implementation executes it phase by phase. Each gate is a chance to redirect cheaply. This is the same plan-first principle scaled up: the bigger the task, the more the separation pays, because the cost of discovering a wrong assumption grows with how much you've built on top of it.

## What to avoid

Letting Claude edit files on the first turn of a non-trivial task, before it has read the code it's about to change. Approving a proposed plan without reading it, so the review gate becomes a rubber stamp. Treating plan mode as a formality to tab through on the way to "real" work. Skipping the research phase on a large feature and discovering only mid-implementation that the approach was infeasible.

## What to do instead

Default to plan mode for anything non-trivial. Let Claude read the relevant code and propose a concrete, phased plan before touching a file — its read-only guarantee means exploration can't accidentally become modification. Then actually review the plan: edit the phases that are wrong or thin, push back on shaky assumptions, and only approve once it reflects the approach you want. For larger features, separate the phases explicitly with a checkpoint between research, planning, and implementation, so a wrong turn is caught while it's still cheap to correct.

## Example

The plan-first loop on a normal task:

```text
1. Enter plan mode (Shift+Tab to cycle, or start with --permission-mode plan)
2. Ask: "Plan how to add rate limiting to the public API"
3. Claude reads the routing layer, the existing middleware, the config —
   read-only, no edits — and proposes:
     Phase 1: add a token-bucket limiter in middleware/
     Phase 2: wire it into the public routes only
     Phase 3: add config + tests
4. You review: "Phase 2 is wrong — we gate at the gateway, not per-route.
   Limit there instead." Edit the plan.
5. Approve → mode switches to edit-capable → Claude implements the
   corrected plan.
```

The redirect in step 4 cost one sentence. Had Claude implemented the per-route version first, the same correction would have meant ripping out and rewriting Phase 2's code. Scaled up, the same shape becomes explicit phases for a big feature:

```text
research/   → is this feasible, does it fit the architecture?   [GO/NO-GO gate]
plan/       → user stories, design, phased roadmap              [review gate]
implement/  → build phase by phase, with checks at each         [verify gate]
```

Each arrow is a cheap place to change course. The pattern is identical at both scales: understand, propose, review, *then* build — never the other way around.
