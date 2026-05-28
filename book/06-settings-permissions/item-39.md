---
item: 39
theme: settings-permissions
title: "Scope permission rules to the narrowest specifier that works"
tags: [permissions, specifiers, bash, glob, security]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [38, 40]
things_to_remember:
  - "A rule like `Bash(npm run test:*)` grants exactly what you mean; `Bash(*)` grants everything and means nothing"
  - "Bash matching is word-boundary aware and per-subcommand: `Bash(safe *)` does NOT authorize `safe && rm -rf /` — each command in a chain must match on its own"
  - "Read/Edit/Write rules use gitignore-style path globs with prefixes (`//` absolute, `~/` home, `/` project-root, `./` relative)"
  - "Prefer many narrow rules over one broad one — the narrow rule fails safe, the broad rule fails open"
agent_steps:
  - "Write each permission rule as the tightest specifier that still covers the real operation — name the command and arguments, not the whole tool"
  - "For Bash, use a space before `*` to respect word boundaries (`Bash(ls *)` matches `ls -la` but not `lsof`)"
  - "Rely on compound-command splitting: a prefix rule authorizes only the subcommand it matches, so chained commands each need their own match or will prompt"
  - "For file tools, use the path-prefix conventions to scope rules to specific directories rather than granting all paths"
ecc_meta:
  target: settings-json
  action: fix
  check: ".claude/settings.json contains broad rules like 'Bash(*)' or 'Edit(*)'"
---

## Why this matters

A permission rule is a specifier, and its breadth is a security decision. `Bash(npm run test:*)` authorizes precisely the test scripts and nothing else. `Bash(npm run *)` authorizes every npm script, including ones that don't exist yet. `Bash(*)` authorizes every shell command on the machine. Each step wider trades a little less typing for a lot more blast radius, and the widest rules are the ones most likely to authorize something you never intended.

The matcher is smarter than a naive glob, and that's load-bearing. Bash matching respects word boundaries — `Bash(ls *)`, with the space, matches `ls -la` but not `lsof`, because `lsof` is a different word. More importantly, compound commands are split on shell operators (`&&`, `||`, `;`, `|`) and each subcommand must match a rule independently. So `Bash(npm test *)` does *not* authorize `npm test && rm -rf /` — the `rm` half has no matching rule and will prompt. This is exactly why narrow rules are safe: an attacker (or a confused model) can't smuggle a dangerous command in by chaining it onto an allowed one. A blanket `Bash(*)` throws that protection away.

File-tool rules follow gitignore-style path globbing with a prefix vocabulary worth memorizing: `//` for an absolute filesystem path, `~/` for your home directory, `/` for the project root, and `./` or a bare pattern for the current directory. `Edit(/src/**)` scopes edits to the project's source tree; `Read(~/.zshrc)` names one file in your home directory. The same principle applies as with Bash — name the smallest region that covers the real work, because a rule that grants more than the task needs is a rule that will eventually grant something the task never wanted.

## What to avoid

Reaching for `Bash(*)`, `Edit(*)`, or `Read(*)` because enumerating the real operations is tedious. Writing `Bash(git *)` when you only ever need `git status`, `git diff`, and `git log`. Forgetting word boundaries and granting `Bash(ls*)` (no space), which matches `lsof`, `lsblk`, and anything else starting with `ls`. Assuming a prefix rule on a safe command also covers that command chained to a dangerous one — it doesn't, but writing rules as if it did leads to over-broad grants.

## What to do instead

Write the tightest specifier that still covers the operation you actually perform. Name the command and its argument shape, not the whole tool. Use the space-before-`*` form to keep word boundaries intact. Lean on the compound-command splitting rather than fighting it — let chained commands prompt, because that's the safety property doing its job. For file tools, use the path prefixes to scope rules to real directories. Many narrow rules read longer but fail safe; one broad rule reads shorter and fails open.

## Example

Narrow rules that say exactly what they mean:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Edit(/src/**)",
      "Read(/docs/**)"
    ]
  }
}
```

Each rule covers a real, recurring operation and stops at its edge. `git push` isn't covered, `rm` isn't covered, edits outside `src/` aren't covered — they prompt.

The protection these rules provide, made concrete:

```text
Allowed by Bash(npm run test:*):   npm run test:unit
Still prompts (rm has no rule):    npm run test:unit && rm -rf build
Matched by Bash(ls *):             ls -la
NOT matched by Bash(ls *):         lsof -i :3000
```

The second line is the point: because the matcher splits on `&&` and checks each subcommand, the dangerous half can't ride in on the allowed half. A blanket `Bash(*)` would have run the whole chain without a word. The narrow rule is what turns "Claude can run my tests" into a guarantee rather than a hope.
