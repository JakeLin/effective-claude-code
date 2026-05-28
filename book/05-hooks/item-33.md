---
item: 33
theme: hooks
title: "Scope hooks to the skills and agents that need them — not every session"
tags: [hooks, scope, skills, agents]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [5, 28]
things_to_remember:
  - "Hooks in `settings.json` fire on every session; skill- and agent-scoped hooks fire only when that skill or agent is active"
  - "Use skill-scoped hooks for opinionated guardrails you only want during certain workflows (`/careful`, `/freeze`)"
  - "Use agent-scoped hooks when the guarantee belongs to a specific subagent's responsibilities"
  - "Skill/agent frontmatter `hooks:` supports a subset of events (mostly tool lifecycle and stop) — global events still need `settings.json`"
agent_steps:
  - "When a hook represents a workflow-specific guarantee, attach it to the skill's frontmatter `hooks:` field rather than `settings.json`"
  - "When a hook represents an agent-specific guarantee, attach it to the agent's frontmatter `hooks:` field"
  - "Reserve `settings.json` hooks for guarantees that should apply across every session — protected-branch guards, working-tree formatters, organization-wide rules"
  - "If a `settings.json` hook is only active during one type of work, move it to a skill that gets invoked for that work"
---

## Why this matters

Not every guarantee belongs to every session. A hook that blocks edits outside `src/` is exactly right while you're in cleanup mode, and wrong the rest of the time. A hook that prevents any Bash command outside a known allowlist is great for a junior-onboarding workflow and oppressive for daily use. Putting either in `settings.json` makes them always-on; putting them in a skill or agent frontmatter makes them on-demand.

The mechanism is simple. Skill and agent frontmatter both expose a `hooks:` field that registers lifecycle hooks scoped to that skill or agent's activation. Invoke the skill (or spawn the agent), and the hooks live for the duration of that scope. When the skill ends or the agent stops, the hooks go with it. This is the right shape for guardrails tied to a specific mode of work — they impose their cost only when their guarantee is wanted.

The canonical examples come from the Anthropic team's own usage. A `/careful` skill that activates a `PreToolUse` hook blocking `rm -rf`, `DROP TABLE`, and force-push for the rest of the session — useful before destructive work, off the rest of the time. A `/freeze` skill that blocks any `Edit` or `Write` outside a specific directory — useful when you're cleaning up one module and don't want Claude wandering. Neither belongs in `settings.json`; both belong scoped to the skill that invokes them.

The carve-out: skill and agent frontmatter only support a subset of hook events — `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PostToolUseFailure`, `Stop`, `SubagentStop`. Session-level events (`SessionStart`, `SessionEnd`, `UserPromptSubmit`, etc.) only register in `settings.json`. For most workflow-specific guardrails, the tool-lifecycle subset is exactly what you need.

## What to avoid

Putting every hook in `settings.json` because it's the first place documented. Skill-scoped hooks that try to enforce session-wide guarantees — they only fire while the skill is active and silently miss the rest of the time. Hooks duplicated across many skills when they really belong globally — that's drift waiting to happen.

## What to do instead

Decide the hook's scope by asking *when should this guarantee apply?* If the answer is "always, on every session" — `settings.json`. If the answer is "only when we're doing X" — attach it to the skill or agent that represents X. Reserve `settings.json` for hooks that genuinely apply across every session: protected-branch guards, working-tree formatters, organization-wide rules.

Watch the boundary: if a `settings.json` hook is checking *whether* a workflow is active before doing anything, that hook probably belongs on the workflow's skill instead.

## Example

A skill that activates a "careful mode" guardrail only while invoked:

```yaml
---
name: careful
description: Use when about to do destructive or production-risky work. Activates guardrails that block rm -rf, DROP TABLE, force-pushes, and unguarded kubectl deletes for the rest of the session.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: ${CLAUDE_SKILL_DIR}/scripts/block-destructive.sh
---

# Careful Mode

You are operating with elevated guardrails. The hook will block
destructive shell operations for the rest of this session. If
you need to bypass one, explain why and the user can disable
the skill.
```

```bash
#!/usr/bin/env bash
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')

block() {
  jq -n --arg r "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $r
    }
  }'
}

case "$cmd" in
  *"rm -rf"*)              block "rm -rf blocked under /careful"; exit 0 ;;
  *"DROP TABLE"*)          block "DROP TABLE blocked under /careful"; exit 0 ;;
  *"git push --force"*)    block "force-push blocked under /careful"; exit 0 ;;
  *"kubectl delete"*)      block "kubectl delete blocked under /careful"; exit 0 ;;
esac
exit 0
```

The user types `/careful` before a risky workflow. The hook activates for the rest of the session. When the session ends, the guardrail disappears. The cost is paid only when the guarantee is wanted.

Contrast with what belongs in `settings.json` — guarantees you always want, like the format-on-edit hook from Item 31 or the protected-branch guard from Item 30. Different shape, different scope, both correct in their own place.
