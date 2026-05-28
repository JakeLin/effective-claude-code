# Summary

[Introduction](README.md)

- [Choose the Right Claude Code Primitive](choose-the-right-tool.md)
- [Worked Example: Evolving a Claude Code Setup](worked-example.md)

# Memory & CLAUDE.md

- [Memory & CLAUDE.md](01-memory/README.md)
  - [Item 1: Treat CLAUDE.md as a living team artifact, not a one-time setup](01-memory/item-01.md)
  - [Item 2: Use CLAUDE.md for context, hooks for guarantees](01-memory/item-02.md)
  - [Item 3: Write instructions specific enough to verify](01-memory/item-03.md)
  - [Item 4: Keep each CLAUDE.md under 200 lines](01-memory/item-04.md)
  - [Item 5: Place instructions at the scope where they actually apply](01-memory/item-05.md)
  - [Item 6: Move path-specific guidance into `.claude/rules/`](01-memory/item-06.md)
  - [Item 7: Let auto memory absorb the corrections you'd otherwise repeat](01-memory/item-07.md)

# Commands

- [Commands](02-commands/README.md)
  - [Item 8: Reach for a built-in command before reasoning in prose](02-commands/item-08.md)
  - [Item 9: Pick `/clear`, `/compact`, or `/rewind` based on what state you want to keep](02-commands/item-09.md)
  - [Item 10: Use `/context` and `/usage` as routine telemetry, not as a fire drill](02-commands/item-10.md)
  - [Item 11: Switch `/model`, `/effort`, and `/fast` mid-conversation, not at the start of the next one](02-commands/item-11.md)
  - [Item 12: Verify changes against the running app with `/run` and `/verify`, not just tests](02-commands/item-12.md)
  - [Item 13: Match review depth to stakes — `/code-review`, `/review`, `/ultrareview`](02-commands/item-13.md)
  - [Item 14: Manage agents, skills, hooks, and permissions through their `/` interfaces, not config files](02-commands/item-14.md)

# Subagents

- [Subagents](03-subagents/README.md)
  - [Item 15: Spawn a subagent to protect your main context, not to feel productive](03-subagents/item-15.md)
  - [Item 16: Default to built-in agents before writing your own](03-subagents/item-16.md)
  - [Item 17: Brief a subagent like a stranger — goal, context, constraints, response shape](03-subagents/item-17.md)
  - [Item 18: Write the `description` field so Claude routes work to the right agent](03-subagents/item-18.md)
  - [Item 19: Restrict tools and pick the cheapest model that does the job](03-subagents/item-19.md)
  - [Item 20: Run independent agents in parallel; use background only for genuinely-async work](03-subagents/item-20.md)
  - [Item 21: Verify what the agent did, not what it said it did](03-subagents/item-21.md)

# Skills

- [Skills](04-skills/README.md)
  - [Item 22: Treat a skill as a folder, not a markdown file](04-skills/item-22.md)
  - [Item 23: Write `description` for the router; use `disable-model-invocation` when auto-invocation is wrong](04-skills/item-23.md)
  - [Item 24: Skills earn their keep on gotchas and non-obvious knowledge — update them every time Claude hits a new failure mode](04-skills/item-24.md)
  - [Item 25: Give a skill goals and constraints, not prescribed steps](04-skills/item-25.md)
  - [Item 26: Default to a skill before reaching for an agent or a command](04-skills/item-26.md)
  - [Item 27: Preload skills into the subagents that need them; fork to a subagent only when context isolation is the point](04-skills/item-27.md)
  - [Item 28: Scope each skill where it applies — project, personal, plugin, nested](04-skills/item-28.md)

# Hooks

- [Hooks](05-hooks/README.md)
  - [Item 29: Reach for a hook only when you need a guarantee, not a nudge](05-hooks/item-29.md)
  - [Item 30: Block dangerous operations with `PreToolUse` and scoped matchers](05-hooks/item-30.md)
  - [Item 31: Use `PostToolUse` to keep the working tree in a known state](05-hooks/item-31.md)
  - [Item 32: Use the `Stop` hook to drive Claude toward a terminal condition](05-hooks/item-32.md)
  - [Item 33: Scope hooks to the skills and agents that need them — not every session](05-hooks/item-33.md)
  - [Item 34: Make hooks fail loudly — design for the exit code, not the happy path](05-hooks/item-34.md)
  - [Item 35: Route notifications through hooks; stop watching the spinner](05-hooks/item-35.md)

# Settings & Permissions

- [Settings & Permissions](06-settings-permissions/README.md)
  - [Item 36: Know which settings file wins before you edit one](06-settings-permissions/item-36.md)
  - [Item 37: Commit team settings; gitignore the personal overrides](06-settings-permissions/item-37.md)
  - [Item 38: Curate the allowlist deliberately — allow the safe and frequent, let the rest prompt](06-settings-permissions/item-38.md)
  - [Item 39: Scope permission rules to the narrowest specifier that works](06-settings-permissions/item-39.md)
  - [Item 40: Use deny rules as the safety net nothing can override](06-settings-permissions/item-40.md)
  - [Item 41: Match the permission mode to the task, not your impatience](06-settings-permissions/item-41.md)
  - [Item 42: Confine bypass mode to a sandbox you can throw away](06-settings-permissions/item-42.md)

# MCP Servers

- [MCP Servers](07-mcp-servers/README.md)
  - [Item 43: Reach for MCP when the capability lives outside your shell and filesystem](07-mcp-servers/item-43.md)
  - [Item 44: Install fewer servers than you think you need](07-mcp-servers/item-44.md)
  - [Item 45: Add each server at the scope that matches who needs it](07-mcp-servers/item-45.md)
  - [Item 46: Keep credentials out of committed config — inject them at connect time](07-mcp-servers/item-46.md)
  - [Item 47: Let MCP tools stay deferred; load upfront only what you reach for every turn](07-mcp-servers/item-47.md)
  - [Item 48: Treat a new MCP server as untrusted code, and its output as untrusted input](07-mcp-servers/item-48.md)
  - [Item 49: Govern MCP access with permission rules and managed allowlists](07-mcp-servers/item-49.md)

# Orchestration & Workflows

- [Orchestration & Workflows](08-orchestration-workflows/README.md)
  - [Item 50: Make Claude plan before it implements anything non-trivial](08-orchestration-workflows/item-50.md)
  - [Item 51: Treat the context window as a budget you actively manage](08-orchestration-workflows/item-51.md)
  - [Item 52: Delegate side-quests to subagents to keep the main thread focused](08-orchestration-workflows/item-52.md)
  - [Item 53: Close every workflow with a verification loop Claude runs itself](08-orchestration-workflows/item-53.md)
  - [Item 54: Get a second opinion from a fresh agent or a different model](08-orchestration-workflows/item-54.md)
  - [Item 55: Drive multi-step work through a task list, not the conversation](08-orchestration-workflows/item-55.md)
  - [Item 56: Compose workflows from the primitive that fits each step](08-orchestration-workflows/item-56.md)

# CLI & Headless Mode

- [CLI & Headless Mode](09-cli-headless/README.md)
  - [Item 57: Reach for headless mode when no human is in the loop](09-cli-headless/item-57.md)
  - [Item 58: Treat `claude -p` as a Unix utility — pipe in, parse out, compose](09-cli-headless/item-58.md)
  - [Item 59: Ask for structured output when a program reads the result](09-cli-headless/item-59.md)
  - [Item 60: Put a budget and a turn limit on every unattended run](09-cli-headless/item-60.md)
  - [Item 61: Chain headless turns with session IDs, not one giant prompt](09-cli-headless/item-61.md)
  - [Item 62: Append to the system prompt for rules; replace it only for a different agent](09-cli-headless/item-62.md)
  - [Item 63: Graduate to the Agent SDK when the script becomes a product](09-cli-headless/item-63.md)

# Git Worktrees

- [Git Worktrees](10-git-worktrees/README.md)
  - [Item 64: Run parallel Claude sessions in worktrees instead of juggling one checkout](10-git-worktrees/item-64.md)
  - [Item 65: Keep worktrees cheap — symlink the heavy directories, sparse-checkout the rest](10-git-worktrees/item-65.md)
  - [Item 66: Give each parallel agent its own worktree so they never collide](10-git-worktrees/item-66.md)
  - [Item 67: Name and organize your worktrees so you can navigate them](10-git-worktrees/item-67.md)

# Agent Teams

- [Agent Teams](11-agent-teams/README.md)
  - [Item 68: Reach for an agent team only when subagents and a single session both fall short](11-agent-teams/item-68.md)
  - [Item 69: Coordinate teammates through a shared task list and a lead, on independent slices](11-agent-teams/item-69.md)
  - [Item 70: Treat agent teams as experimental — enable them deliberately and expect change](11-agent-teams/item-70.md)

# Scheduled Tasks & Routines

- [Scheduled Tasks & Routines](12-scheduled-tasks/README.md)
  - [Item 71: Reach for `/loop` to repeat work within a conversation — and know it pauses with Claude Code](12-scheduled-tasks/item-71.md)
  - [Item 72: Match the scheduler to how long the work must outlive your conversation](12-scheduled-tasks/item-72.md)
  - [Item 73: Promote work that must run unattended to a routine](12-scheduled-tasks/item-73.md)
  - [Item 74: Fence every recurring autonomous run — cost and risk repeat with each iteration](12-scheduled-tasks/item-74.md)

# Appendix

- [Reusable Starting Points](appendix/README.md)
  - [Sample `CLAUDE.md`](appendix/sample-claude-md.md)
  - [Sample skill](appendix/sample-skill.md)
  - [Sample hook](appendix/sample-hook.md)
  - [Sample permissions](appendix/sample-permissions.md)
  - [Sample headless wrapper](appendix/sample-headless-wrapper.md)
