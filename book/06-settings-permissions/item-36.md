---
item: 36
theme: settings-permissions
title: "Know which settings file wins before you edit one"
tags: [settings, hierarchy, precedence, configuration]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [2, 37]
things_to_remember:
  - "Settings layer by precedence: managed policy > CLI flags > project-local > project-shared > user — higher layers override lower ones"
  - "Most array settings (like permission rules) concatenate across layers; scalar settings take the highest-precedence value"
  - "If a setting isn't taking effect, a higher layer is overriding it — check managed and CLI flags before editing the file you assume is in charge"
  - "`deny` rules win regardless of layer — a lower-priority deny still blocks a higher-priority allow"
agent_steps:
  - "When a setting isn't behaving, enumerate the layers in precedence order (managed, CLI flags, .claude/settings.local.json, .claude/settings.json, ~/.claude/settings.json) and find the highest one that sets the key"
  - "Put the change in the layer that matches its scope: org policy → managed; personal-everywhere → user; team-shared → project; personal-this-repo → project-local"
  - "Remember array settings concatenate across layers — adding an allow rule in one file does not remove a deny rule in another"
  - "Use the interactive config UI or /permissions to inspect the effective merged result rather than guessing from one file"
---

## Why this matters

Claude Code reads its configuration from several `settings.json` files stacked in a fixed precedence order. From lowest to highest: your user settings (`~/.claude/settings.json`), the project's committed settings (`.claude/settings.json`), the project's personal un-committed settings (`.claude/settings.local.json`), command-line flags for the session, and — above all of them — an organization-deployed *managed* policy. When the same key is set in two layers, the higher layer wins. When it's an array — like the permission `allow` list — the layers concatenate instead of replacing.

This matters because the failure mode is silent. You edit `.claude/settings.json`, set `model` to `opus`, restart, and Claude keeps using something else — because your user settings, or a managed policy, set it higher up. Nothing errors. The setting is just quietly overridden, and you waste twenty minutes editing the wrong file. The cascade is invisible until you know it exists, and then it's obvious every time.

The mental model that keeps you out of trouble: each layer has a *scope* it's meant for. Managed policy is for things the org must guarantee regardless of what any developer wants. User settings are your personal defaults across every project. Committed project settings are what the whole team shares. Project-local settings are your personal tweaks for one repo that shouldn't reach the others. Put each change in the layer whose scope matches its intent, and the precedence rules stop being a surprise.

## What to avoid

Editing a setting, seeing no effect, and editing the same file harder. Assuming the project `settings.json` is authoritative when a managed policy or your own user settings sit above it. Expecting an `allow` rule you just added to cancel out a `deny` rule somewhere else — it won't; `deny` wins regardless of which layer it lives in. Treating array settings like scalar ones and wondering why old rules from another file are still active.

## What to do instead

When a setting misbehaves, walk the layers top-down — managed, CLI flags, project-local, project-shared, user — and find the highest one that touches the key. That's the one in charge. Then place your change in the layer that matches its scope rather than the first file you opened. For arrays, remember you're adding to a merged set, not replacing a list. When in doubt, inspect the effective merged result through the config UI or `/permissions` rather than reasoning about one file in isolation.

## Example

The same key resolved through the layers:

```jsonc
// ~/.claude/settings.json (user — lowest writable)
{ "model": "sonnet" }

// .claude/settings.json (project, committed)
{ "model": "opus" }

// .claude/settings.local.json (project, git-ignored)
{ "model": "haiku" }
```

The session runs on `haiku` — the highest writable layer that sets `model` wins. If the org ships a managed policy pinning `model`, that beats all three. And `--model opus` on the command line beats everything except managed policy, for that session only.

Permission arrays behave differently — they merge:

```jsonc
// .claude/settings.json
{ "permissions": { "allow": ["Bash(npm run test:*)"] } }

// ~/.claude/settings.json
{ "permissions": { "deny": ["Bash(curl:*)"] } }
```

The effective permission set has *both* rules: `npm run test:*` is allowed and `curl` is denied. Neither file overrode the other — they concatenated. The takeaway is to edit the layer that matches the change's scope, and to read the merged result, not a single file, when reasoning about what Claude can actually do.
