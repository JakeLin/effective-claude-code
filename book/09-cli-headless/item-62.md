---
item: 62
theme: cli-headless
title: "Append to the system prompt for rules; replace it only for a different agent"
tags: [headless, system-prompt, configuration, customization]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [1, 57]
things_to_remember:
  - "`--append-system-prompt` adds your instructions on top of the defaults; `--system-prompt` throws the defaults away entirely"
  - "The default system prompt carries tool guidance, safety, and coding conventions — replacing it drops all of that"
  - "Append for per-run rules, formatting, or persona tweaks; replace only when you genuinely want a different agent from scratch"
  - "When in doubt, append — replacing is the rare, deliberate choice, not the default"
agent_steps:
  - "To add behavior to a headless run (rules, output format, tone), use `--append-system-prompt` (or `--append-system-prompt-file`) and keep the defaults"
  - "Use `--system-prompt` / `--system-prompt-file` only when you intend a fundamentally different agent and accept losing the default tool guidance and safety"
  - "Prefer append unless you have a specific reason to discard the built-in prompt"
  - "For project conventions that should always apply, prefer CLAUDE.md over per-invocation prompt flags"
---

## Why this matters

Headless runs let you shape the system prompt from the command line, and there are two flags that look similar but do opposite things. `--append-system-prompt` keeps Claude Code's default system prompt and adds your text on top of it. `--system-prompt` *replaces* the default entirely with your text. The distinction is easy to gloss over and expensive to get wrong, because the default prompt is not boilerplate — it carries the tool-use guidance that makes the agentic loop work, the safety behavior, and the coding conventions that produce sensible output. Replace it casually and you've silently removed all of that.

Most of the time, what you actually want is *append*. You're adding a constraint for this run — "respond only in JSON," "follow our commit-message format," "you are reviewing for security, be strict" — on top of an agent that should still know how to use its tools and behave safely. Append does exactly that: your instructions layer onto a fully-functional agent. Reaching for replace to add a rule is like rebuilding the engine to change the radio station; you get your rule and lose everything else that was working. The default-friendly choice is append, and it covers the large majority of headless customization.

Replace is justified only when you genuinely want a *different agent* — one whose entire behavior you're defining from scratch, where the defaults would actively get in the way. That's a real but uncommon need: a narrowly-scoped transformer that should behave nothing like a coding agent, for instance. When you do replace, do it knowingly, accepting that you're now responsible for any tool guidance and safety framing the task needs, because the defaults that provided them are gone. And note the boundary with earlier chapters: durable project conventions that should *always* apply belong in CLAUDE.md (Chapter 1), not in a flag repeated on every invocation — the prompt flags are for per-run shaping, not for the standing rules that memory already handles.

## What to avoid

Using `--system-prompt` to tack on a single rule, unknowingly discarding the default tool guidance, safety, and conventions in the process. Treating the two flags as interchangeable because their names rhyme. Replacing the system prompt and then being puzzled when the agent uses tools poorly or behaves unexpectedly — you removed the guidance that prevented that. Repeating the same project conventions in `--append-system-prompt` on every call when they belong in CLAUDE.md.

## What to do instead

Default to append. For per-run rules, output formatting, or a persona tweak, use `--append-system-prompt` (or the file variant) so your instructions sit on top of a still-functional agent. Reserve `--system-prompt` for the rare case where you truly want a different agent built from scratch, and when you use it, accept ownership of the tool and safety guidance you're choosing to drop. For conventions that should always apply, put them in CLAUDE.md rather than in a flag you repeat every time.

## Example

Append — add a rule, keep the working agent:

```bash
git diff --staged | claude -p "review this diff" \
  --append-system-prompt "You are a strict security reviewer. Flag any
secret, injection risk, or unsafe deserialization. Be concise."
```

The agent still has its full tool guidance and safety behavior; your reviewer instructions are layered on top. This covers almost all headless customization.

Replace — a deliberately different agent, defaults intentionally gone:

```bash
cat raw.txt | claude -p "convert to our changelog format" \
  --system-prompt "You are a text formatter. Output only the reformatted
text, nothing else. Do not explain."
```

Here you *want* none of the coding-agent defaults — it's a pure formatter — so replacing is justified, and you've accepted that no default tool or safety framing remains. The mistake to avoid is using that second form when you meant the first: if you only wanted to add the "output only" rule to a normal agent, append it. And if "convert to our changelog format" were a standing project convention rather than a one-off, it would live in CLAUDE.md, not on the command line. Append by default; replace on purpose.
