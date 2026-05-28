# Effective Claude Code — Item Index

74 items across 12 chapters. Stable items (1–63) are ready for production.
Beta items (64–74, chapters 10–12) are correct but details may shift — re-check against current docs.

## Stable chapters

| Chapter | Theme | Items | Reference file |
|---------|-------|-------|----------------|
| 1 | Memory & CLAUDE.md | 1–7 | ch01-memory.md |
| 2 | Commands | 8–14 | ch02-commands.md |
| 3 | Subagents | 15–21 | ch03-subagents.md |
| 4 | Skills | 22–28 | ch04-skills.md |
| 5 | Hooks | 29–35 | ch05-hooks.md |
| 6 | Settings & Permissions | 36–42 | ch06-settings-permissions.md |
| 7 | MCP Servers | 43–49 | ch07-mcp-servers.md |
| 8 | Orchestration & Workflows | 50–56 | ch08-orchestration.md |
| 9 | CLI & Headless Mode | 57–63 | ch09-cli-headless.md |

## Beta chapters

| Chapter | Theme | Items | Reference file |
|---------|-------|-------|----------------|
| 10 | Git Worktrees | 64–67 | beta/ch10-git-worktrees.md |
| 11 | Agent Teams | 68–70 | beta/ch11-agent-teams.md |
| 12 | Scheduled Tasks & Routines | 71–74 | beta/ch12-scheduled-tasks.md |

## All item titles

| # | Title | Chapter |
|---|-------|---------|
| 1 | Treat CLAUDE.md as a living team artifact, not a one-time setup | 1 |
| 2 | Use CLAUDE.md for context, hooks for guarantees | 1 |
| 3 | Write instructions specific enough to verify | 1 |
| 4 | Keep each CLAUDE.md under 200 lines | 1 |
| 5 | Place instructions at the scope where they actually apply | 1 |
| 6 | Move path-specific guidance into `.claude/rules/` | 1 |
| 7 | Let auto memory absorb the corrections you'd otherwise repeat | 1 |
| 8 | Reach for a built-in command before reasoning in prose | 2 |
| 9 | Pick `/clear`, `/compact`, or `/rewind` based on what state you want to keep | 2 |
| 10 | Use `/context` and `/usage` as routine telemetry, not as a fire drill | 2 |
| 11 | Switch `/model`, `/effort`, and `/fast` mid-conversation, not at the start of the next one | 2 |
| 12 | Verify changes against the running app with `/run` and `/verify`, not just tests | 2 |
| 13 | Match review depth to stakes — `/code-review`, `/review`, `/ultrareview` | 2 |
| 14 | Manage agents, skills, hooks, and permissions through their `/` interfaces | 2 |
| 15 | Spawn a subagent to protect your main context, not to feel productive | 3 |
| 16 | Default to built-in agents before writing your own | 3 |
| 17 | Brief a subagent like a stranger — goal, context, constraints, response shape | 3 |
| 18 | Write the `description` field so Claude routes work to the right agent | 3 |
| 19 | Restrict tools and pick the cheapest model that does the job | 3 |
| 20 | Run independent agents in parallel; use background only for genuinely-async work | 3 |
| 21 | Verify what the agent did, not what it said it did | 3 |
| 22 | Treat a skill as a folder, not a markdown file | 4 |
| 23 | Write `description` for the router; use `disable-model-invocation` when auto-invocation is wrong | 4 |
| 24 | Skills earn their keep on gotchas — update them every time Claude hits a new failure mode | 4 |
| 25 | Give a skill goals and constraints, not prescribed steps | 4 |
| 26 | Default to a skill before reaching for an agent or a command | 4 |
| 27 | Preload skills into the subagents that need them | 4 |
| 28 | Scope each skill where it applies — project, personal, plugin, nested | 4 |
| 29 | Reach for a hook only when you need a guarantee, not a nudge | 5 |
| 30 | Block dangerous operations with `PreToolUse` and scoped matchers | 5 |
| 31 | Use `PostToolUse` to keep the working tree in a known state | 5 |
| 32 | Use the `Stop` hook to drive Claude toward a terminal condition | 5 |
| 33 | Scope hooks to the skills and agents that need them — not every session | 5 |
| 34 | Make hooks fail loudly — design for the exit code, not the happy path | 5 |
| 35 | Route notifications through hooks; stop watching the spinner | 5 |
| 36 | Know which settings file wins before you edit one | 6 |
| 37 | Commit team settings; gitignore the personal overrides | 6 |
| 38 | Curate the allowlist deliberately | 6 |
| 39 | Scope permission rules to the narrowest specifier that works | 6 |
| 40 | Use deny rules as the safety net nothing can override | 6 |
| 41 | Match the permission mode to the task, not your impatience | 6 |
| 42 | Confine bypass mode to a sandbox you can throw away | 6 |
| 43 | Reach for MCP when the capability lives outside your shell and filesystem | 7 |
| 44 | Install fewer servers than you think you need | 7 |
| 45 | Add each server at the scope that matches who needs it | 7 |
| 46 | Keep credentials out of committed config — inject them at connect time | 7 |
| 47 | Let MCP tools stay deferred; load upfront only what you reach for every turn | 7 |
| 48 | Treat a new MCP server as untrusted code, and its output as untrusted input | 7 |
| 49 | Govern MCP access with permission rules and managed allowlists | 7 |
| 50 | Make Claude plan before it implements anything non-trivial | 8 |
| 51 | Treat the context window as a budget you actively manage | 8 |
| 52 | Delegate side-quests to subagents to keep the main thread focused | 8 |
| 53 | Close every workflow with a verification loop Claude runs itself | 8 |
| 54 | Get a second opinion from a fresh agent or a different model | 8 |
| 55 | Drive multi-step work through a task list, not the conversation | 8 |
| 56 | Compose workflows from the primitive that fits each step | 8 |
| 57 | Reach for headless mode when no human is in the loop | 9 |
| 58 | Treat `claude -p` as a Unix utility — pipe in, parse out, compose | 9 |
| 59 | Ask for structured output when a program reads the result | 9 |
| 60 | Put a budget and a turn limit on every unattended run | 9 |
| 61 | Chain headless turns with session IDs, not one giant prompt | 9 |
| 62 | Append to the system prompt for rules; replace it only for a different agent | 9 |
| 63 | Graduate to the Agent SDK when the script becomes a product | 9 |
| 64 | Run parallel Claude sessions in worktrees instead of juggling one checkout | 10 (beta) |
| 65 | Keep worktrees cheap — symlink the heavy directories, sparse-checkout the rest | 10 (beta) |
| 66 | Give each parallel agent its own worktree so they never collide | 10 (beta) |
| 67 | Name and organize your worktrees so you can navigate them | 10 (beta) |
| 68 | Reach for an agent team only when subagents and a single session both fall short | 11 (beta) |
| 69 | Coordinate teammates through a shared task list and a lead, on independent slices | 11 (beta) |
| 70 | Treat agent teams as experimental — enable them deliberately and expect change | 11 (beta) |
| 71 | Reach for `/loop` to repeat work within a conversation — and know it pauses with Claude Code | 12 (beta) |
| 72 | Match the scheduler to how long the work must outlive your conversation | 12 (beta) |
| 73 | Promote work that must run unattended to a routine | 12 (beta) |
| 74 | Fence every recurring autonomous run — cost and risk repeat with each iteration | 12 (beta) |
