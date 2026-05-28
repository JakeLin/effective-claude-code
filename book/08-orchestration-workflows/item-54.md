---
item: 54
theme: orchestration-workflows
title: "Get a second opinion from a fresh agent or a different model"
tags: [review, verification, cross-model, subagents, quality]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [21, 52, 53]
things_to_remember:
  - "The context that wrote the code shares its blind spots — a fresh reviewer catches what the author cannot see"
  - "A review subagent starts with a clean context and judges the work on its merits, not on the reasoning that produced it"
  - "A different model brings genuinely different failure modes — cross-model review surfaces issues a same-model check misses"
  - "Have the reviewer check against the plan and the requirements, not just the diff in isolation"
agent_steps:
  - "After implementation, spawn a review subagent with a clean context to critique the change against the plan and requirements"
  - "For high-stakes work, get a review from a different model (e.g. via another CLI) so different blind spots are covered"
  - "Give the reviewer the plan or requirements as the standard to judge against, not only the raw diff"
  - "Treat review findings as input to another verify-fix loop, not as a final sign-off to skip"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

Self-verification (the previous Item) catches what a *test* can catch. It can't catch what the author can't see — and the context that wrote the code is exactly the context least able to see its own blind spots. The same chain of reasoning that produced a subtle design flaw will tend to re-bless it on review, because it's reasoning from the same premises. This is the well-known problem that authors miss their own bugs, and it applies to models as much as to people: a context that just spent twenty turns convincing itself an approach is right is not the context that will notice the approach is wrong. You need fresh eyes, and you need them structurally, not as a hope.

A review subagent provides exactly that. It starts with a clean context, sees the change without the twenty turns of rationalization that led to it, and judges the work on its merits. Because it didn't make the decisions, it isn't invested in them — it reads the diff the way a reviewer on the team would, asking "is this actually right?" rather than "does this match what I intended?" That independence is the value. It's the verification analog of the delegation Item: the subagent's separate context is what makes its judgment independent, just as it's what made its legwork cheap.

A *different model* raises this further. Two instances of the same model share not just the local reasoning but the underlying failure modes — the same classes of mistake, the same blind spots in the same places. A different model brings a genuinely different distribution of errors, so it catches things a same-model review structurally tends to miss. This is the basis of the cross-model workflow: plan and implement with one model, review and verify with another, so each step is checked by something that fails differently than it. In all cases, give the reviewer a standard to judge against — the plan, the acceptance criteria — not just the diff in a vacuum, and feed what it finds back into another fix-and-verify pass rather than treating the review as a final stamp.

## What to avoid

Treating the implementing context's own "looks correct to me" as review — it shares the blind spots that produced the work. Reviewing only the diff with no reference to the plan or requirements, so the reviewer can't tell whether the change does the right thing, only whether it's internally tidy. Assuming a second pass by the same model in the same context adds independent signal; mostly it re-confirms. Collecting review findings and then shipping anyway without acting on them.

## What to do instead

Build a fresh-eyes review into the workflow. After implementation, spawn a review subagent with a clean context and have it critique the change against the plan and the requirements, not just the diff. For high-stakes work, get the review from a *different* model — through another CLI or agent — so different failure modes are covered. Hand the reviewer the standard to judge against. Then treat its findings as the input to another verify-and-fix loop, closing them out the way you'd close out failing tests.

## Example

Fresh-context review as a workflow step:

```text
1. Implement the feature; self-verify (tests green) per Item 53.
2. Spawn a review subagent — clean context — with:
     "Here is the plan (plan/PLAN.md) and the diff. Review the
      implementation against the plan. Flag correctness bugs,
      missed requirements, and risky shortcuts."
3. Reviewer (no stake in the decisions) returns:
     - Phase 2 acceptance criterion 'rate-limit headers on 429' not met
     - Window reset uses local time; should be UTC
4. Feed both back into a fix-and-verify loop until they're closed.
```

The reviewer caught a *missed requirement* (criterion not met) and a *latent bug* (timezone) — neither of which a test written by the author was likely to cover, precisely because the author didn't think of them. Scaled to high stakes, the cross-model version swaps in a different engine:

```text
Terminal 1 (model A):  plan, then implement
Terminal 2 (model B):  review the plan, later verify the implementation
```

Model B fails differently than model A, so it flags issues A's own review would tend to wave through. The principle holds at both scales: the check that matters most comes from something that doesn't share the author's blind spots.
