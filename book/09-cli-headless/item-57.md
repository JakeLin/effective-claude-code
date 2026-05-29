---
item: 57
theme: cli-headless
title: "Reach for headless mode when no human is in the loop"
tags: [headless, automation, cli, mindset]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [58, 60, 72]
things_to_remember:
  - "Headless mode (`claude -p`) runs one non-interactive turn and exits — use it whenever there's no human to answer prompts or catch mistakes"
  - "Interactive is for collaboration and exploration; headless is for scripts, CI, git hooks, and batch jobs"
  - "Headless has no one to approve permissions or redirect a wrong turn, so the run must be self-contained and bounded up front"
  - "If you'd run a shell command in the context, headless Claude fits the same slot — it's a program, not just a chat"
agent_steps:
  - "Use `claude -p \"prompt\"` (print mode) for any non-interactive context: CI steps, git hooks, cron jobs, batch processing, shell pipelines"
  - "Use the interactive REPL for collaborative, exploratory work where you steer turn by turn"
  - "Before running headless, make the invocation self-contained — no prompt is coming, so all context and constraints go in up front"
  - "Pair headless mode with explicit guardrails (later Items) since there's no human to stop a runaway"
---

## Why this matters

Claude Code has two fundamentally different modes of operation, and choosing the wrong one makes everything downstream harder. The interactive REPL is a collaboration: you watch each turn, answer permission prompts, and redirect when the approach drifts. Headless mode — `claude -p "prompt"` — is the opposite: one non-interactive turn, result printed to stdout, process exits. It exists for every situation where there is no human sitting there to participate. A CI job, a git pre-commit hook, a cron task, a loop over five hundred files, a stage in a shell pipeline — none of these have a person to answer "can I run this?" or to notice that Claude went down the wrong path on turn three.

That absence of a human is the whole design constraint, and it inverts the habits that work interactively. Interactively, you *are* the safety mechanism and the course-corrector; the session can be loose because you're there to tighten it. Headless, you've left the room before the run starts. Everything the run needs — the full context, the constraints, the definition of done — has to be in the invocation up front, because nothing can be added mid-flight. And everything that could go wrong unattended has to be fenced in advance, because there's no one to hit Ctrl-C. The later Items in this chapter are mostly consequences of this single fact.

The useful mental shift is to stop thinking of headless Claude as "a chatbot I'm scripting" and start thinking of it as a *program* — a command-line tool that takes input and produces output and an exit code. If you'd reach for a shell command, a script, or a small CLI in some automation, headless Claude fits the same slot, just with a language model inside. That framing is what makes the rest natural: programs get composed into pipelines, emit machine-readable output, run under resource limits, and carry state explicitly. A chatbot does none of those things; a Unix program does all of them, and headless Claude is the latter.

## What to avoid

Trying to drive automation through the interactive REPL — scripting keystrokes, scraping the TUI — when `-p` is built for exactly that. Using headless mode for genuinely exploratory work where you'd benefit from steering each turn, and then being frustrated that you can't intervene. Launching a headless run as if a human will be there to approve a permission or redirect it — there won't be. Treating headless Claude as a chat session that happens to be scripted, rather than as a bounded program.

## What to do instead

Pick the mode by whether a human is in the loop. Collaborative, exploratory, steer-as-you-go work belongs in the interactive REPL. Anything unattended — CI, hooks, cron, batch, pipelines — belongs in headless mode. When you go headless, make the invocation self-contained: put all the context and constraints in up front, because no follow-up prompt is coming. And treat the run as a program, which means giving it the guardrails (budgets, turn limits, scoped tools) the later Items cover, since you won't be there to stop it.

## Example

The same capability, in its two modes:

```bash
# Interactive — you're present, steering, approving as you go.
claude
> help me refactor the auth module

# Headless — no human; a CI step that must run start to finish alone.
claude -p "review the staged diff for security issues; exit non-zero if any are critical"
```

Where headless naturally slots in — anywhere you'd put a command in automation:

```bash
# git hook
claude -p "check this commit message follows our convention" < "$1"

# batch over many items
for f in src/**/*.md; do
  claude -p "fix broken links in this file" < "$f"
done

# a stage in a pipeline
cat build.log | claude -p "summarize the first failing test and its cause"
```

None of these have a person to answer a prompt or catch a wrong turn — which is precisely why they're headless, and precisely why each will need the guardrails the rest of the chapter adds. The decision is simple: human in the loop, go interactive; no human, go headless and make the run stand on its own.
