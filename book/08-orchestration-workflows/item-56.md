---
item: 56
theme: orchestration-workflows
title: "Compose workflows from the primitive that fits each step"
tags: [composition, commands, subagents, skills, harness]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [8, 15, 22, 29]
things_to_remember:
  - "The harness is a composition system: commands, subagents, skills, and hooks each do something the others can't — match each step to the right one"
  - "Command = invokable entry point; subagent = isolated context + tools; skill = reusable domain knowledge; hook = deterministic enforcement"
  - "A real workflow chains them: a command orchestrates, agents do isolated work, skills supply knowledge, hooks guarantee invariants"
  - "Reach for the primitive whose property you need, not the one you reach for by habit — the leverage is in the fit"
agent_steps:
  - "Decompose a workflow into steps and ask, per step, which property is needed: an entry point, context isolation, reusable knowledge, or a hard guarantee"
  - "Use a command as the invokable orchestration entry point for a repeatable workflow"
  - "Use subagents for steps needing isolated context or parallelism; skills for knowledge reused across steps; hooks for invariants that must hold"
  - "Chain them (command → agent → skill, with hooks enforcing gates) rather than forcing one primitive to do another's job"
---

## Why this matters

By this point the book has covered the primitives individually; orchestration is the payoff, and it rests on one idea: the harness is a *composition* system, not a prompt-delivery system. Each primitive provides a capability the others structurally cannot. A command is an invokable, repeatable entry point. A subagent is an isolated context window with its own tools, runnable in parallel. A skill is reusable domain knowledge that loads when relevant. A hook is deterministic code the harness runs whether or not the model wants it. These aren't four flavors of the same thing — they're four different properties, and "a strong prompt" can't substitute for any of them, because prompts operate at the layer where the model sees tokens and these operate at layers before, after, and around that.

Good workflow design follows from taking that seriously. Decompose the work into steps and, for each, ask which *property* the step needs. Does it need to be invokable on demand and repeatable? That's a command. Does it generate noisy intermediate work but a compact result, or need to run alongside other work? Subagent. Does it apply knowledge — a domain's conventions, an API's quirks — reused across steps or projects? Skill. Must something hold no matter what the model decides — tests pass before stop, secrets never read? Hook. Matching the step to the primitive whose property it needs is what makes a workflow reliable instead of merely clever.

The trap is reaching for one primitive by habit and bending it to do another's job — stuffing orchestration logic into a sprawling CLAUDE.md, or asking a prompt to "always" do something a hook should guarantee, or inlining knowledge into a command that a skill should carry. The composed alternative is the recurring pattern of this whole book: a command orchestrates the flow, subagents do the isolated legwork, skills supply the knowledge each step needs, and hooks enforce the gates between steps. Each does what only it can, and the workflow is the assembly. The leverage isn't in any single primitive — it's in the fit between each step and the primitive that matches it.

## What to avoid

Forcing one primitive to do another's job: orchestration logic crammed into CLAUDE.md, knowledge inlined into a command instead of a skill, a prompt asked to guarantee what only a hook can enforce. Reaching for the primitive you're most comfortable with rather than the one whose property the step needs. Building a monolithic mega-prompt when the work is really a composition of distinct steps. Treating the four primitives as interchangeable because "they all become tokens eventually."

## What to do instead

Design the workflow as a composition. Break it into steps and pick, per step, the primitive whose property the step actually requires — entry point (command), isolated context or parallelism (subagent), reusable knowledge (skill), hard guarantee (hook). Chain them so each does only what it's best at, rather than overloading one. When a step's needs don't match the primitive you instinctively reached for, switch primitives — the fit is where the leverage is.

## Example

A release-notes workflow, decomposed by property and composed from the matching primitives:

```text
/release-notes v2.4.0                          ← command: invokable entry point

  Step 1  gather merged PRs since last tag      → subagent (Explore):
            noisy search, compact result, own context
  Step 2  draft the notes                       → skill (release-notes-style):
            reusable house format + tone, loaded when relevant
  Step 3  verify every PR link resolves         → subagent: parallel checks
  Step 4  block commit if CHANGELOG unchanged   → hook (PreToolUse on commit):
            deterministic guarantee, not a request
```

Each step uses the primitive whose property it needs: the command makes the whole thing repeatable, the subagents isolate noisy work and parallelize checks, the skill carries the formatting knowledge so it isn't re-explained each run, and the hook makes the changelog invariant non-negotiable. Try to collapse this into one big prompt and you lose all four properties — no clean entry point, no context isolation, knowledge re-pasted every time, and a "please update the changelog" the model can skip. Composed, it's reliable; flattened, it's a hope. That gap is the reason the primitives exist as distinct things — and the reason orchestration is a skill worth practicing.
