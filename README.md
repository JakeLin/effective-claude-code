# Effective Claude Code

*74 concrete principles for using Claude Code well — in the style of Effective C++, Effective Java, and Effective Python.*

Most Claude Code knowledge lives in docs (what features *do*) or chat tips (what worked once). This book fills the gap: **when** to reach for each feature, **why** one approach beats another, and **how** to compose them into workflows that stay small and strong.

A taste:

> - *"Use CLAUDE.md for context, hooks for guarantees"* — CLAUDE.md is advice Claude can ignore. If a rule MUST run, write a hook.
> - *"Keep each CLAUDE.md under 200 lines"* — every line loads into every session. Past 200, useful rules drown in noise.
> - *"Verify what the agent did, not what it said it did"* — an agent's summary describes intent, not outcome. Read the diff.

---

## See it in action

Run the bundled skill on any project and Claude audits your setup, identifies gaps, and writes clean rules after you confirm:

```
> /effective-claude-code apply chapter-1

I see a monorepo with a CLAUDE.md and no .claude/rules/.
The biggest gap is path-specific rules loaded globally.

🟡 Add:
  • Your frontend architecture rules only apply when editing src/web/ —
    extract to .claude/rules/frontend.md with paths: ["src/web/**"]

💡 Tips:
  • Auto memory is healthy — promote entries the whole team should see into CLAUDE.md
  • Scope separation is correct (team rules in CLAUDE.md, private config gitignored)

Proceed?
```

One command. Claude reads your project, triages Items against what's already there, skips what's covered, and proposes only what's missing — no item numbers in your files, no book references, just clean rules applied to your setup.

---

## Structure

74 Items across 12 themed chapters — stable features first, beta features last:

| Chapter | Theme | Items |
|---------|-------|-------|
| 1 | [Memory & CLAUDE.md](book/01-memory/) | 1–7 |
| 2 | [Commands](book/02-commands/) | 8–14 |
| 3 | [Subagents](book/03-subagents/) | 15–21 |
| 4 | [Skills](book/04-skills/) | 22–28 |
| 5 | [Hooks](book/05-hooks/) | 29–35 |
| 6 | [Settings & Permissions](book/06-settings-permissions/) | 36–42 |
| 7 | [MCP Servers](book/07-mcp-servers/) | 43–49 |
| 8 | [Orchestration & Workflows](book/08-orchestration-workflows/) | 50–56 |
| 9 | [CLI & Headless Mode](book/09-cli-headless/) | 57–63 |
| 10 | [Git Worktrees](book/10-git-worktrees/) *(beta)* | 64–67 |
| 11 | [Agent Teams](book/11-agent-teams/) *(beta)* | 68–70 |
| 12 | [Scheduled Tasks & Routines](book/12-scheduled-tasks/) *(beta)* | 71–74 |

Chapters 1–9 cover stable, settled features. Chapters 10–12 cover beta features where principles hold but exact syntax may change.

---

## How to use

**Read online:** [Effective Claude Code](https://jakelin.github.io/effective-claude-code) — or browse the [`book/`](book/) directory on GitHub. Start with Items 1, 3, 8, 29, and 53 for the fastest impact.

**Install the skill:**

```bash
npx skills add JakeLin/effective-claude-code
```

Then invoke it:

```
/effective-claude-code                     # audit your project, find gaps
/effective-claude-code apply hooks         # apply one chapter
/effective-claude-code apply item-30       # apply specific items
/effective-claude-code apply all           # apply all 63 stable items
```

---

## Contributing

Contributions are welcome. Each Item must:

- Follow the frontmatter schema (see `book/_item-template.md`)
- Be written as a durable principle, not a syntax reference
- Include a real `claude_code_version` when last verified
- Match the body structure: *Why it matters* → *What to avoid* → *What to do instead* → *Example*

Open a PR with your proposed Item. Reviews focus on principle-level quality — is the *why* clear enough that an agent applying it in an unforeseen context would make the right call?

---

## Resources & Acknowledgments

- [Claude Code official docs](https://docs.anthropic.com/en/docs/claude-code) — the authoritative reference for features, flags, and configuration
- [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) — community feature documentation and implementation examples that informed this book's research

---

## License

[CC-BY-4.0](LICENSE). Attribution required; commercial reuse allowed.
