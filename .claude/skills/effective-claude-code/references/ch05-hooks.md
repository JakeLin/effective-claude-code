# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 5 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 5 --agent-steps -->

## Hooks

### Reach for a hook only when you need a guarantee, not a nudge [#29]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Hooks are deterministic harness logic — the model can't ignore them
- Use a hook when the cost of a single failure is real; use CLAUDE.md or a skill when probabilistic compliance is fine
- Every hook costs latency on every matching event — don't pay for guarantees you don't need
- If you find yourself writing 'please always do X' in CLAUDE.md three times, X is probably a hook

**Agent steps:**
1. Before adding a hook, ask whether a CLAUDE.md instruction or skill gotcha would handle the case 95% of the time — if yes, prefer the softer mechanism
2. Reach for a hook when the failure mode is destructive, security-relevant, or otherwise expensive to recover from
3. When a CLAUDE.md instruction has had to be restated or strengthened more than twice, promote it to a hook
4. Audit existing hooks for ones that fire constantly but rarely act — they're paying latency for no guarantee

### Block dangerous operations with `PreToolUse` and scoped matchers [#30]
<!-- ecc-meta: target="settings-json" action="add" check=".claude/settings.json has no hooks.PreToolUse configured" -->
- `PreToolUse` fires before a tool runs and can block it — the only mechanism that prevents a destructive call before it happens
- Use the matcher to narrow scope (`Bash`, `Edit|Write`, `mcp__github__merge_pull_request`) — broad matchers run a lot but rarely act
- Return `permissionDecision: deny` with a reason so Claude understands what was blocked and can try a different approach
- Pair guardrails with permissions — `PreToolUse` is the safety net when permission rules can't express the constraint

**Agent steps:**
1. When the user wants to block a specific destructive operation, write a `PreToolUse` hook with a matcher narrowed to the relevant tool and a script that inspects the input
2. In the hook script, emit `{\"hookSpecificOutput\": {\"hookEventName\": \"PreToolUse\", \"permissionDecision\": \"deny\", \"permissionDecisionReason\": \"<why>\"}}` on stdout to block with a clear reason
3. Prefer narrow matchers over broad ones — `Bash(rm *)` or `mcp__github__merge_pull_request` rather than `*`
4. Test the hook by deliberately triggering it once — verify the deny path produces a readable message Claude can act on

### Use `PostToolUse` to keep the working tree in a known state [#31]
<!-- ecc-meta: target="settings-json" action="add" check=".claude/settings.json has no hooks.PostToolUse for Edit|Write" -->
- `PostToolUse` runs after a tool succeeds — the right place to enforce invariants the model shouldn't have to remember
- Auto-run formatters, linters, and type-checkers after `Edit|Write` to keep the diff in a canonical state
- Surface failures back to Claude via stderr and a non-zero exit so the next turn can react
- Keep `PostToolUse` hooks fast — they run on every matching edit and the user is waiting

**Agent steps:**
1. Configure `PostToolUse` hooks matching `Edit|Write` to run the project's formatter and quick lint check
2. On lint or type-check failure, exit non-zero and write the error to stderr so Claude sees it and can fix on the next turn
3. Limit the hook to commands that finish in seconds — a 30-second test suite belongs in CI, not in `PostToolUse`
4. Use `PostToolUseFailure` (separate event) to react to *tool* failures, not to lint failures of successful edits

### Use the `Stop` hook to drive Claude toward a terminal condition [#32]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- `Stop` fires when Claude finishes a turn — a hook there can decide whether the work is actually done
- Return `{decision: 'block', reason: '...'}` to keep Claude going; return success to release control to the user
- Use a deterministic check (tests pass, lints clean, file exists) as the terminal condition — not 'does it look done'
- Cap the loop with a max-turns or an external timeout — a runaway Stop hook will burn tokens until something else stops it

**Agent steps:**
1. When the user wants Claude to keep working until a condition is met, write a `Stop` hook that runs the check and returns `{decision: 'block', reason: '...'}` while the condition is unmet
2. Make the terminal condition deterministic — exit codes of tests, type-checks, validators — not subjective judgments
3. Include the actual failure output in the `reason` so Claude has the diagnostic to act on next turn
4. Always pair the hook with an upper bound (max turns, wall-clock timeout) to prevent runaway loops

### Scope hooks to the skills and agents that need them — not every session [#33]
<!-- ecc-meta: target="conversation" action="suggest" check=".claude/settings.json has 3 or more hooks — some may be better scoped to a skill or agent" -->
- Hooks in `settings.json` fire on every session; skill- and agent-scoped hooks fire only when that skill or agent is active
- Use skill-scoped hooks for opinionated guardrails you only want during certain workflows (`/careful`, `/freeze`)
- Use agent-scoped hooks when the guarantee belongs to a specific subagent's responsibilities
- Skill/agent frontmatter `hooks:` supports all hook event types — the distinction from `settings.json` is scope (on-demand vs. always-on), not event availability

**Agent steps:**
1. When a hook represents a workflow-specific guarantee, attach it to the skill's frontmatter `hooks:` field rather than `settings.json`
2. When a hook represents an agent-specific guarantee, attach it to the agent's frontmatter `hooks:` field
3. Reserve `settings.json` hooks for guarantees that should apply across every session — protected-branch guards, working-tree formatters, organization-wide rules
4. If a `settings.json` hook is only active during one type of work, move it to a skill that gets invoked for that work

### Make hooks fail loudly — design for the exit code, not the happy path [#34]
<!-- ecc-meta: target="conversation" action="suggest" check=".claude/settings.json has hooks configured — verify hook scripts handle failure paths explicitly" -->
- A silently-broken hook is worse than no hook — the guarantee evaporates without a signal
- Exit 0 = proceed, exit 2 = blocking error with stderr fed back to Claude, other non-zero = non-blocking error
- Write decisions as JSON on stdout; write diagnostics to stderr; never mix the two
- Test every hook by deliberately triggering both the success and failure paths before relying on it

**Agent steps:**
1. In hook scripts, emit JSON decisions to stdout and diagnostics to stderr — never mix them on the same stream
2. Use exit 2 for blocking errors you want visible to the user; use exit 0 with a JSON decision for normal allow/deny flow
3. Add a fail-safe: if the hook script crashes or its dependencies are missing, log the error and exit non-zero rather than swallowing it
4. Before relying on a new hook, run a manual test that deliberately trips it — verify the failure path produces a visible signal

### Route notifications through hooks; stop watching the spinner [#35]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Hooks turn lifecycle events into out-of-band signals — Slack pings, sounds, webhook calls — so you don't have to watch the terminal
- Common patterns: `PermissionRequest` to Slack (Claude needs you), `SubagentStop`/`Stop` to a sound or webhook (work is done), `Notification` for harness alerts
- Use `async: true` on notification hooks so they don't block Claude's loop
- Scope what you get pinged about — getting paged on every event teaches you to ignore them

**Agent steps:**
1. When the user wants to be notified when Claude needs attention or finishes, set up a hook on `PermissionRequest`, `Stop`, or `SubagentStop` that posts to their notification channel
2. Use HTTP hook handlers for webhook destinations (Slack, Pushover, ntfy.sh) — these are first-class hook types
3. Set `async: true` on notification hooks so the Claude session doesn't wait for the network round-trip
4. Narrow the matcher or add a script-side filter so notifications only fire for events worth acting on

