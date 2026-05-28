# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 6 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 6 --agent-steps --output .claude/skills/effective-claude-code/references/ch06-settings-permissions.md -->

## Settings & Permissions

### Know which settings file wins before you edit one [#36]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Settings layer by precedence: managed policy > CLI flags > project-local > project-shared > user — higher layers override lower ones
- Most array settings (like permission rules) concatenate across layers; scalar settings take the highest-precedence value
- If a setting isn't taking effect, a higher layer is overriding it — check managed and CLI flags before editing the file you assume is in charge
- `deny` rules win regardless of layer — a lower-priority deny still blocks a higher-priority allow

**Agent steps:**
1. When a setting isn't behaving, enumerate the layers in precedence order (managed, CLI flags, .claude/settings.local.json, .claude/settings.json, ~/.claude/settings.json) and find the highest one that sets the key
2. Put the change in the layer that matches its scope: org policy → managed; personal-everywhere → user; team-shared → project; personal-this-repo → project-local
3. Remember array settings concatenate across layers — adding an allow rule in one file does not remove a deny rule in another
4. Use the interactive config UI or /permissions to inspect the effective merged result rather than guessing from one file

### Commit team settings; gitignore the personal overrides [#37]
<!-- ecc-meta: target="settings-json" action="fix" check=".claude/settings.json missing, or .claude/settings.local.json not in .gitignore" -->
- `.claude/settings.json` is team-shared and belongs in git; `.claude/settings.local.json` is personal and belongs in .gitignore
- Anything that should be true for every developer on the repo goes in the committed file; anything specific to your machine or taste goes local
- Never put secrets, API keys, or personal absolute paths in the committed settings — those go in local settings or environment
- A committed settings.json is documentation: it tells every teammate (and every fresh Claude session) what this repo expects

**Agent steps:**
1. Put team-wide configuration — shared permission rules, project model choice, hooks the whole team needs — in .claude/settings.json and commit it
2. Put personal or machine-specific overrides — your own allow rules, local paths, experimental toggles — in .claude/settings.local.json
3. Ensure .claude/settings.local.json is listed in .gitignore; if it isn't, add it
4. Before committing settings.json, scan it for secrets, tokens, and personal absolute paths and move any to local settings or env

### Curate the allowlist deliberately — allow the safe and frequent, let the rest prompt [#38]
<!-- ecc-meta: target="settings-json" action="add" check=".claude/settings.json has no permissions.allow block" -->
- The allowlist exists to remove friction on operations that are both safe and frequent — not to silence every prompt
- Allow what you'd approve without thinking every time; leave anything consequential to prompt so you stay in the loop on decisions that matter
- Build the allowlist incrementally from real prompts — approve-and-remember as they come up, rather than guessing a big list upfront
- An allowlist that covers the boring 90% makes the 10% of prompts that remain meaningful again

**Agent steps:**
1. Add a tool/command to permissions.allow only when it is both safe to run unattended and run often enough that prompting is pure friction
2. Leave consequential operations (network writes, deploys, destructive commands, anything you'd want to eyeball) to prompt rather than allowlisting them
3. Grow the allowlist from real sessions — when a safe, repetitive prompt appears, approve it persistently rather than pre-populating speculative rules
4. Periodically review the allowlist and remove rules that are broader than the operations you actually trust

### Scope permission rules to the narrowest specifier that works [#39]
<!-- ecc-meta: target="settings-json" action="fix" check=".claude/settings.json contains broad rules like 'Bash(*)' or 'Edit(*)'" -->
- A rule like `Bash(npm run test:*)` grants exactly what you mean; `Bash(*)` grants everything and means nothing
- Bash matching is word-boundary aware and per-subcommand: `Bash(safe *)` does NOT authorize `safe && rm -rf /` — each command in a chain must match on its own
- Read/Edit/Write rules use gitignore-style path globs with prefixes (`//` absolute, `~/` home, `/` project-root, `./` relative)
- Prefer many narrow rules over one broad one — the narrow rule fails safe, the broad rule fails open

**Agent steps:**
1. Write each permission rule as the tightest specifier that still covers the real operation — name the command and arguments, not the whole tool
2. For Bash, use a space before `*` to respect word boundaries (`Bash(ls *)` matches `ls -la` but not `lsof`)
3. Rely on compound-command splitting: a prefix rule authorizes only the subcommand it matches, so chained commands each need their own match or will prompt
4. For file tools, use the path-prefix conventions to scope rules to specific directories rather than granting all paths

### Use deny rules as the safety net nothing can override [#40]
<!-- ecc-meta: target="settings-json" action="add" check=".claude/settings.json has no permissions.deny block" -->
- Evaluation order is deny → ask → allow, and deny wins across every settings layer — a deny rule cannot be overridden by any allow
- Deny the things that must never happen regardless of mode or allowlist: reading secrets (`.env`), touching credential files, destructive commands
- Deny rules hold even in acceptEdits and bypass-adjacent flows — they're the floor, not a default you can step around
- A short, well-chosen deny list is cheaper insurance than auditing every allow rule for what it might accidentally permit

**Agent steps:**
1. Add deny rules for anything that must never run or be read: secret files, credential stores, production-destructive commands
2. Rely on evaluation order — deny is checked first and beats any matching allow or ask rule at any layer
3. Put critical deny rules in committed project settings (and managed policy where available) so they protect the whole team
4. Treat the deny list as a hard floor independent of permission mode — verify secrets stay denied even under acceptEdits

### Match the permission mode to the task, not your impatience [#41]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Permission mode sets the default disposition for unmatched operations — six modes: `default` (prompts), `acceptEdits` (auto-accepts edits), `dontAsk` (auto-denies), `auto` (classifier-based), `plan` (read-only), `bypassPermissions` (skips checks)
- Pick the mode for the work in front of you — `plan` for exploration, `acceptEdits` for a trusted edit-heavy loop, `default` when you want to stay in the loop
- `plan` mode is read-only and overrides allow rules — writes are blocked even if an Edit(...) rule would permit them, preserving the read-only guarantee
- Mode is a per-session disposition, not a permanent setting — switch it as the task changes rather than living in the most permissive one

**Agent steps:**
1. Use plan mode when the task is investigation or design — it guarantees read-only exploration even against allow rules
2. Use acceptEdits when you're in a tight, trusted edit-test loop and prompting on every file write is pure friction
3. Use default mode when the work is consequential enough that you want to approve operations as they come
4. Switch modes as the task phase changes (explore → implement → verify) rather than defaulting to the most permissive mode

### Confine bypass mode to a sandbox you can throw away [#42]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- bypassPermissions / --dangerously-skip-permissions removes the safety net — only run it where a worst-case action can't hurt anything you care about
- The right home for bypass is an isolated, disposable environment: a fresh container, an ephemeral VM, a throwaway worktree — not your laptop on a repo with prod credentials
- Prefer sandboxing (sandbox.enabled, filesystem + network allowlists) over bypass when you want autonomy with guardrails still in place
- deny rules and a few protected paths still apply under bypass, but don't rely on them — bypass means assuming the checks are gone

**Agent steps:**
1. Only enable bypassPermissions or --dangerously-skip-permissions inside an isolated, disposable environment where the blast radius is contained
2. Before bypassing, confirm there are no real credentials, no production access, and nothing irreversible reachable from the working directory
3. Prefer enabling sandbox (sandbox.enabled) with filesystem and network allowlists to get autonomy while keeping OS-level guardrails
4. Never use bypass mode on a developer machine with live access just to stop permission prompts

