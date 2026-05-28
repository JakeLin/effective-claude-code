# Subagents

A subagent is a separate Claude process that the main session can spawn to do a piece of work. It runs with its own context window, its own tool list, optionally its own model, and returns a single summary message back to the parent. Five subagents ship built-in (`general-purpose`, `Explore`, `Plan`, `statusline-setup`, `claude-code-guide`); custom ones live in `.claude/agents/<name>.md` as markdown with YAML frontmatter.

The whole point is **context isolation**. A subagent can grep through fifty files and read twenty of them, and the main thread only sees the conclusion. That's what makes long sessions stay coherent — noise lives in the child, signal comes back to the parent.

This chapter starts with the mindset (context firewall, not productivity theatre), then shows when the built-ins already do the job, then how to write a custom subagent that gets routed to, scoped tightly, and briefed well. The last two Items cover orchestration — parallel versus background — and verification, because an agent's summary describes what it *intended* to do, not what it actually did.
