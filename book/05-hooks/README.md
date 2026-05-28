# Hooks

A hook is a deterministic handler the harness runs in response to a lifecycle event — a tool about to fire, a tool that just finished, the user submitting a prompt, Claude finishing a turn, a subagent starting or stopping, a session beginning or ending. Hooks live in `settings.json` (under the `hooks` key), or scoped to a skill or subagent via their frontmatter. The harness invokes them; Claude doesn't decide whether they run.

That's the whole point. Where CLAUDE.md and skills are *suggestion* (Claude reads them and usually follows), hooks are *enforcement* (the harness gates the action regardless of what the model wanted). A `PreToolUse` hook on `Bash(rm *)` can block destructive shell commands even if the prompt accidentally asked for one. A `PostToolUse` hook on `Edit|Write` can run the formatter automatically. A `Stop` hook can keep Claude going until the tests pass. The whole surface is built around the idea that some guarantees shouldn't depend on a model's compliance.

This chapter starts with the mindset — when to reach for a hook versus a softer mechanism — then walks the three highest-leverage event families (`PreToolUse` for guardrails, `PostToolUse` for invariants, `Stop` for terminal conditions), then covers scoping, failure handling, and using hooks for out-of-band notifications so you can stop watching the spinner.
