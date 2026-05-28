# Effective Claude Code

An open source book in the style of the Effective series (Effective C++, Effective Java, Effective Python) — a collection of numbered Items, each one a concrete principle for using Claude Code well.

Readable by humans and AI agents alike. Humans learn the *why*; agents follow the `agent_steps` to apply each Item to their projects.

---

## Structure

The book is organized into 12 themed chapters, stable features first:

| Chapter | Theme |
|---------|-------|
| 1 | Memory & CLAUDE.md |
| 2 | Commands |
| 3 | Subagents |
| 4 | Skills |
| 5 | Hooks |
| 6 | Settings & Permissions |
| 7 | MCP Servers |
| 8 | Orchestration & Workflows |
| 9 | CLI & Headless Mode |
| 10 | Git Worktrees |
| 11 | Agent Teams |
| 12 | Scheduled Tasks & Routines |

Each chapter contains numbered Items. Item numbers are global across the book (Item 1 through Item N).

---

## Contributing

Contributions are welcome. Each Item must:

- Follow the frontmatter schema (see `CLAUDE.md`)
- Be written as a durable principle, not a syntax reference
- Include a real `claude_code_version` when written
- Match the Item body structure: Why → Avoid → Do instead → Example → Things to Remember

Open a PR with your proposed Item. The author reviews for principle-level quality before merging.

---

## License

[CC-BY-4.0](LICENSE). Attribution required; commercial reuse allowed.
