# Agent Teams

> **Beta.** Agent Teams are experimental — enabled behind a flag, with an API that is still changing. The principles here are durable, but treat the exact flags, modes, and config layout as provisional and re-check them against the current docs before depending on them.

An *agent team* is several full Claude Code sessions running at once and coordinating on shared work. This is the part worth pausing on, because it sounds like subagents and isn't. A subagent is a context *fork* inside one session: it does isolated legwork and hands a summary back to the parent, and subagents can't talk to each other. A teammate is a whole independent session — its own context window, its own CLAUDE.md, MCP servers, and skills loaded — and teammates coordinate directly through a shared task list. Subagents extend one mind's reach; a team is several minds working in parallel.

That extra power is also extra weight. N teammates means N full sessions, which means roughly N times the token cost and a genuine coordination problem to manage. Teams pay off only when the work is genuinely parallel — independent workstreams that each need full project context and can run for a long stretch without blocking each other. For sequential work, same-file edits, or anything with tight dependencies, a single session or a few subagents is cheaper and simpler.

This is the shortest chapter in the book, and deliberately so: the feature is the newest, the API is the least settled, and the honest set of durable principles is small. Three Items cover it — when a team is the right tool at all (versus subagents or one session), how teammates coordinate through a shared task list and a lead, and how to treat a feature that is still explicitly experimental.
