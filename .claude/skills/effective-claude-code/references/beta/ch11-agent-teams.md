# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable + beta; chapters 11 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 11 --include-beta --agent-steps --output .claude/skills/effective-claude-code/references/beta/ch11-agent-teams.md -->

## Agent Teams *(beta)*

### Reach for an agent team only when subagents and a single session both fall short [#68]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- A teammate is a full independent session (its own context, CLAUDE.md, MCP, skills); a subagent is a context fork that returns a summary
- Teams are heavyweight — N teammates means N full sessions and roughly N× the token cost
- Use a team only for genuinely parallel, independent workstreams that each need full project context and run long without blocking each other
- For sequential work, same-file edits, or tight dependencies, a single session or subagents is cheaper and simpler

**Agent steps:**
1. Before forming a team, ask whether the work is genuinely parallel and independent — if not, use a single session
2. If a side task just needs isolated legwork returning a summary, use a subagent, not a teammate
3. Choose a team only when each workstream needs its own full context and the streams can progress without blocking each other
4. Weigh the N× token cost of N teammates against the parallelism gained before spawning a team

### Coordinate teammates through a shared task list and a lead, on independent slices [#69]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Teammates coordinate through a shared task list — they claim tasks, track dependencies, and go idle when done
- A lead session forms the team, assigns work, and steers; it can gate on `TeammateIdle` and `TaskCompleted` events
- Slice the work so each teammate owns an independent, low-dependency piece — coupled slices serialize the team or collide
- Dependencies in the task list keep order correct so a teammate doesn't start work whose inputs aren't ready

**Agent steps:**
1. Structure team work as a shared task list with one independent slice per teammate
2. Designate a lead to form the team, assign tasks, and coordinate; let it listen for TeammateIdle/TaskCompleted to gate quality
3. Encode ordering with task dependencies so teammates don't start work before its inputs exist
4. Minimize cross-slice coupling and shared files so teammates progress in parallel rather than blocking each other

### Treat agent teams as experimental — enable them deliberately and expect change [#70]
<!-- ecc-meta: target="conversation" action="suggest" check="CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS env var is set or agent teams are in use" -->
- Agent teams are gated behind an experimental flag (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) — they're opt-in, not default
- The feature is experimental: flags, run modes, coordination behavior, and limitations may change between releases
- Known limits matter: session resumption, task coordination, and graceful shutdown are not yet mature enough for unattended pipelines — use teams interactively while they stabilize
- Run mode matters — in-process keeps teammates in one terminal; split-pane modes need tmux or iTerm2, not every terminal

**Agent steps:**
1. Enable teams explicitly with the experimental env var; don't assume the feature is on by default
2. Pick a run mode that matches your terminal — in-process anywhere, split-pane only where tmux/iTerm2 supports it
3. Re-verify flag names, modes, limitations, and config layout against current docs rather than trusting older examples
4. Keep agent teams out of load-bearing unattended pipelines until the API stabilizes; prefer interactive use for now

