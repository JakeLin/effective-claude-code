# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 2 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 2 --agent-steps -->

## Commands

### Reach for a built-in command before reasoning in prose [#8]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- If you're typing a request, check `/help` first — there's a good chance a command does it directly
- Built-in commands run as harness logic — deterministic, no tokens, no guessing at intent
- `/powerup` walks through built-ins interactively; worth ten minutes once per release
- The slash menu is large and changing — re-scan after upgrades, don't trust your old mental list

**Agent steps:**
1. Before composing a chat instruction for the user, scan whether a built-in command (`/diff`, `/context`, `/usage`, `/permissions`, `/agents`, etc.) does it directly — propose the command name
2. When the user asks something the harness exposes as a command, recommend the command rather than executing the equivalent through tool calls
3. After each Claude Code release, point the user at `/release-notes` and `/powerup` to surface new commands

### Pick `/clear`, `/compact`, or `/rewind` based on what state you want to keep [#9]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- `/clear` for topic switches, `/compact` for same task with full context, `/rewind` to undo a bad turn
- `/compact` keeps task and conversation continuity; `/clear` discards everything but the file-system state
- `/rewind` recovers without restarting and can roll back code too
- Use `/branch` when you want both the current path and a divergent one — not either/or

**Agent steps:**
1. When context is nearly full but the task is unfinished, propose `/compact` with focus instructions describing what to keep
2. When the user has finished a task and is starting an unrelated one, propose `/clear`
3. When a recent turn produced the wrong direction, propose `/rewind` rather than `/clear`
4. When the user wants to explore an alternative path while keeping the current one, propose `/branch` (alias `/fork`)

### Use `/context` and `/usage` as routine telemetry, not as a fire drill [#10]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Check `/context` early in a long task — see what's filling context before you're forced to `/compact`
- `/usage` shows session cost and plan usage; check before launching another expensive operation
- `/context` flags context-heavy tools, memory bloat, and capacity warnings — read the warnings
- `/insights` surfaces longer-term patterns across sessions when something feels off generally

**Agent steps:**
1. When the user starts a long-running task or context appears to be filling, suggest `/context` so they see what's loaded before it becomes a problem
2. Before launching multiple parallel agents or a long-running operation, suggest checking `/usage` to know what budget remains
3. If `/context` shows a single tool result dominating, name the call and propose a less verbose alternative (paginate, summarize, narrower glob)

### Switch `/model`, `/effort`, and `/fast` mid-conversation, not at the start of the next one [#11]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- All three apply immediately — no restart, no new conversation needed
- Raise `/effort` for one hard turn, then drop it back; don't run the whole session at max
- `/fast` is independent of model selection — toggle without losing your Opus session
- Mid-conversation switches may warn after prior output; accept the warning, don't restart

**Agent steps:**
1. When the user hits a problem that calls for deeper reasoning, propose `/effort high` (or `xhigh`/`max`) for the next turn — and remind them to drop it back after
2. When a previous turn was superficial, propose `/rewind` to that turn plus a higher `/effort` before redoing it
3. When the user comments that Claude feels slow on Opus, propose `/fast on` instead of switching model
4. Never recommend restarting the session purely to change model or effort — these are live switches

### Verify changes against the running app with `/run` and `/verify`, not just tests [#12]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Tests verify code; `/verify` and `/run` verify behavior against the running app
- `/run` launches and drives your app so you can see a change working in the real environment
- `/run-skill-generator` records a per-project recipe so subsequent runs don't re-discover setup
- Run `/run-skill-generator` once per project, again when the launch process changes

**Agent steps:**
1. After implementing a user-facing feature, propose `/verify` to confirm it works in the real app — even if tests pass
2. On first use in a project that needs more than a vanilla launch (DB, env vars, build step), propose `/run-skill-generator` to capture the recipe
3. If `/run` or `/verify` fails because setup steps are missing, suggest re-running `/run-skill-generator` to update the recipe rather than patching manually
4. Skip /run and /verify when the change is purely internal (refactor, comments, formatting) and behavior cannot have shifted

### Match review depth to stakes — `/code-review`, `/review`, `/ultrareview` [#13]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- `/code-review` reviews the current diff at adjustable depth (low/medium/high/max/ultra)
- `/review` opens a local PR review; `/ultrareview` runs a deep multi-agent cloud review
- Pick by what's at risk — a one-line fix doesn't need /ultrareview; a payment flow does
- `/code-review --fix` applies findings to the working tree; `--comment` posts to the PR

**Agent steps:**
1. Before committing user-facing or high-stakes changes, propose `/code-review` at an effort matched to the change — low for mechanical, high for behavioral, ultra for critical
2. Before merging a PR, suggest `/review` for a local sweep; for high-stakes changes also suggest `/ultrareview`
3. When the user asks Claude to review work it just wrote, prefer `/code-review` — it brings a fresh review pass instead of self-evaluation
4. Skip review commands when the diff is mechanical and small (typos, formatting, trivial renames)

### Manage agents, skills, hooks, and permissions through their `/` interfaces, not config files [#14]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- `/agents`, `/skills`, `/hooks`, `/permissions`, `/mcp`, `/plugin`, `/memory` are interactive UIs over the underlying configs
- The UIs show current state, validate input, and surface options you'd miss editing JSON
- Editing JSON is still fine — but reach for the UI when uncertain about field names or precedence
- Use `/doctor` to diagnose configuration problems before going spelunking in settings

**Agent steps:**
1. When the user wants to change permissions, propose `/permissions` instead of editing `settings.json` directly
2. When the user wants to add, inspect, or edit a subagent, propose `/agents` rather than hand-editing the .claude/agents/ file
3. When the user wants to know what's loaded (skills, hooks, MCP servers), propose the matching `/` command first
4. Before diagnosing a config problem by reading files, run `/doctor` — it catches common failure modes faster

