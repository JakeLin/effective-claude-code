---
item: 14
theme: commands
title: "Manage agents, skills, hooks, and permissions through their `/` interfaces, not config files"
tags: [commands, configuration, management]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [7, 8]
things_to_remember:
  - "`/agents`, `/skills`, `/hooks`, `/permissions`, `/mcp`, `/plugin`, `/memory` are interactive UIs over the underlying configs"
  - "The UIs show current state, validate input, and surface options you'd miss editing JSON"
  - "Editing JSON is still fine — but reach for the UI when uncertain about field names or precedence"
  - "Use `/doctor` to diagnose configuration problems before going spelunking in settings"
agent_steps:
  - "When the user wants to change permissions, propose `/permissions` instead of editing `settings.json` directly"
  - "When the user wants to add, inspect, or edit a subagent, propose `/agents` rather than hand-editing the .claude/agents/ file"
  - "When the user wants to know what's loaded (skills, hooks, MCP servers), propose the matching `/` command first"
  - "Before diagnosing a config problem by reading files, run `/doctor` — it catches common failure modes faster"
---

## Why this matters

Claude Code exposes interactive `/` commands for nearly every configurable surface: `/agents` for subagents, `/skills` for skill visibility and overrides, `/hooks` for lifecycle hooks, `/permissions` for tool allow/ask/deny rules, `/mcp` for MCP server connections and OAuth, `/plugin` for plugin management, `/memory` for CLAUDE.md and auto-memory, `/config` for the rest. Each one shows current state, validates input, and surfaces options the underlying JSON doesn't make obvious — like which scope a rule lives in, which overrides apply, and which entries are active versus orphaned.

Hand-editing the config files works and is sometimes faster for known changes. But for anything you're not 100% sure about — field name, valid value, scope precedence, whether a setting is currently overridden by a higher-priority file — the interactive UIs are the safer path. They prevent the silent-failure mode where a typo in `settings.json` causes Claude Code to load partial configuration without telling you.

`/doctor` is the diagnostic counterpart. When something configuration-related is misbehaving, `/doctor` is the first reach, not the last. It catches install issues, settings problems, and common misconfigurations with explicit status icons and a `f` keystroke to apply fixes.

## What to avoid

Memorizing JSON field names you could look up by pressing `/permissions` and tabbing through. Editing a settings file when you're not sure which scope's settings file actually owns the rule — the UIs make precedence visible; the files don't. Diagnosing a broken configuration by reading source code when `/doctor` would have told you the answer in a second.

## What to do instead

Default to the slash command for the surface you're touching. `/permissions` for permission rules. `/agents` for subagents. `/hooks` for hooks. `/skills` to see what's loaded and adjust visibility. `/mcp` to add or reauthorize a server. `/memory` to audit CLAUDE.md and auto-memory together. Drop down to JSON editing when you know the change you want and the UI doesn't expose it.

`/doctor` belongs in your routine when anything feels off — slow startup, missing skills, unexpected permission prompts, a hook that won't fire. It's faster than triaging by inspection.

## Example

Same change, UI versus file edit.

```text
> /permissions
[interactive picker: scope, rule type (allow/ask/deny), pattern; saves to
 the correct settings file with no risk of mistyping the key name]
```

```json
// settings.local.json — fine if you know the schema
{
  "permissions": {
    "allow": ["Bash(npm test:*)"]
  }
}
```

Adding an MCP server:

```text
> /mcp
[picker for transport, command, env vars, OAuth flow if needed; rule
 lands in the right scope file]
```

Diagnosing a misbehaving setup:

```text
> /doctor

✓ Installation
✓ Auth
✗ Hooks  — PreToolUse hook for "Bash" command exited non-zero
✓ MCP servers
Press f to attempt fixes for failed checks.
```
