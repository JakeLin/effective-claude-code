# Effective Claude Code

*Concrete, actionable principles for using Claude Code well — for the humans who direct it and the agents that run it.*

Claude Code is not one tool but a ladder of them. At the bottom is the prompt you type. Above it sit the mechanisms this book is about: `CLAUDE.md` that persists what Claude should know, slash commands and skills that package procedures, subagents that isolate context, hooks that enforce guarantees, MCP servers that reach systems outside your shell, headless mode that turns the whole thing into infrastructure, and — at the top, still settling — agent teams and scheduled routines. Each rung is more powerful, and more expensive, than the one below it.

Read across the chapters and one pattern surfaces on its own, feature after feature: **the effective move is almost always the lowest rung that solves the problem — then bound its autonomy, then verify its output.** Reach for a subagent before a team, a prompt before a skill, a deny rule before a sandbox. Give the powerful thing a budget and a stopping condition. And never trust generated work until something other than the generator has confirmed it. That through-line wasn't imposed on the material; it kept appearing in it. This book names it rather than leaving it implicit, and most Items are a variation on it applied to one more rung.

## Who this is for

Two readers at once. For **humans**, each Item explains the *why* — the reasoning that makes a practice worth following, not just the rule. For **agents**, each Item carries a `things_to_remember` summary and a set of `agent_steps`: concrete, ordered actions to execute without reading the prose. The two halves reinforce each other rather than repeat — an agent that understands *why* a practice exists applies it better than one following a checklist.

## How to read an Item

Every Item follows the same shape: *why it matters*, *what to avoid*, *what to do instead*, and a worked *example*. The title is the advice in one line — scanning titles alone should teach you something. Items are numbered globally and written to stand alone: jump to the one you need, and follow the cross-references when a neighboring Item owns a mechanism in more depth.

## A note on stability

Chapters 1–9 cover stable, settled features. Chapters 10–12 — git worktrees, agent teams, scheduled routines — are beta or research-preview: the principles hold, but flags, limits, and exact behaviors are still moving, and those chapters say so. Treat the durable advice as settled and the specific numbers as provisional, and re-check the latter against the current docs.
