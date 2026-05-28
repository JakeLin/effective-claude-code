# Memory & CLAUDE.md

Every Claude Code session starts with an empty context window. Two systems carry knowledge across sessions: **CLAUDE.md files** that you write to give Claude persistent instructions, and **auto memory** that Claude writes for itself as it learns from your corrections. Both load at the start of every conversation.

This is the first chapter because it is the single highest-leverage thing you can do with Claude Code. A well-tended CLAUDE.md improves output quality across every other feature in this book — skills, commands, hooks, subagents — because they all run with CLAUDE.md in context.

The Items in this chapter cover, in order: the mindset of treating CLAUDE.md as living shared knowledge; the mental model that separates it from enforcement; how to write entries Claude will actually follow; how to keep it from bloating; where to put it for the scope it applies to; how to scale past a single file with `.claude/rules/`; and how auto memory fits in alongside.
