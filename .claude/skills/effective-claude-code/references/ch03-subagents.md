# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 3 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 3 --agent-steps -->

## Subagents

### Spawn a subagent to protect your main context, not to feel productive [#15]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Subagents are context firewalls — their value is what they keep *out* of the main thread, not what they put in
- If the work fits in one or two tool calls inline, a subagent costs more than it saves
- Good fits: large searches, doc reading, dependency audits, anything that would dump pages into the main context
- Each subagent is a fresh process with no memory of the conversation — the briefing cost is real

**Agent steps:**
1. Before spawning a subagent, ask whether the work would meaningfully pollute the main context if done inline — if not, do it inline
2. When delegating, plan for a short summary back, not a transcript — the parent should not need to re-read the child's tool output
3. Use a subagent for parallel independent work, large-surface research, or operations whose intermediate state you don't want to carry forward

### Default to built-in agents before writing your own [#16]
<!-- ecc-meta: target="conversation" action="suggest" check=".claude/agents/ exists with custom agents — review whether any duplicate built-in Explore, Plan, or general-purpose" -->
- Start with the bundled subagents — most real delegations are covered by `Explore`, `Plan`, or `general-purpose`
- `Explore` is read-only and runs on Haiku — fast, cheap, and incapable of accidental writes
- `Plan` is for design work before code: codebase reading plus implementation strategy, no edits
- Write a custom subagent only when the built-ins miss — usually domain tools, MCP scope, or a recurring instruction pattern

**Agent steps:**
1. Before authoring a `.claude/agents/<name>.md`, check whether `Explore`, `Plan`, `general-purpose`, `statusline-setup`, or `claude-code-guide` already fits
2. For codebase search and 'where is X used' questions, prefer `Explore` over `general-purpose`
3. For 'design how to implement Y' questions before any code is written, prefer `Plan`
4. Author a custom subagent only when the built-in either lacks the tools, the MCP servers, or the recurring instructions you'd otherwise repeat in every prompt

### Brief a subagent like a stranger — goal, context, constraints, response shape [#17]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- A subagent starts with no memory of your conversation — anything it needs to know has to be in the prompt
- State the goal, the context you've already established, and the shape of the response you want back
- Don't write 'based on your findings, fix the bug' — that delegates the synthesis you should be doing
- For lookups, hand over the exact thing; for investigations, hand over the question, not prescribed steps

**Agent steps:**
1. Before sending a subagent prompt, check that someone reading it cold could act on it without seeing this conversation
2. Include relevant file paths, prior conclusions, and ruled-out options in the prompt — do not assume the subagent will rediscover them
3. Specify the desired response length and shape (e.g., 'under 200 words', 'a table of file:line:reason')
4. Avoid prompts that punt synthesis back to the agent ('based on your findings, decide what to do') — make the decision yourself in the parent thread

### Write the `description` field so Claude routes work to the right agent [#18]
<!-- ecc-meta: target="agents" action="fix" check=".claude/agents/ exists — review description fields for vague or missing routing triggers" -->
- `description` is what the harness reads to decide which agent fits a task — write it as routing copy, not a label
- Name the triggers explicitly: 'Use when X', 'Use PROACTIVELY when Y' — vague descriptions get bypassed
- Auto-invocation only fires when the description's triggers are unambiguous and the keyword `PROACTIVELY` is present
- If you find yourself manually invoking your own subagent by name, the description is too weak

**Agent steps:**
1. Write `description` as routing copy: name the triggering situation, what the agent does, and what it returns — not a bare label
2. State triggers explicitly with 'Use when X'; add the keyword `PROACTIVELY` only when Claude should reach for the agent unprompted
3. Add a scope-narrowing clause ('Do NOT use for ...') when the agent must stay in its lane
4. Update the description in the same edit whenever you change the agent's responsibilities
5. If you catch yourself invoking your own subagent by name, rewrite the description — it's too weak to route on

### Restrict tools and pick the cheapest model that does the job [#19]
<!-- ecc-meta: target="agents" action="fix" check=".claude/agents/ exists — check for missing tools: field or overly broad tool lists" -->
- Subagents inherit every tool by default — narrow `tools` to what the job actually needs
- Read-only agents should be enforced read-only via the tool list, not by hoping the prompt is followed
- Match `model` to the work: Haiku for search and lookups, Sonnet for most code work, Opus only for genuinely hard reasoning
- `effort` overrides session effort for this agent — useful when one delegated step deserves more depth than the rest of the session

**Agent steps:**
1. When authoring a subagent, list the minimum set of tools in `tools:` — start narrow and add only when something fails
2. For research, audit, and 'find where X happens' agents, exclude Write, Edit, and Bash from the tool list
3. Set `model: haiku` for codebase search and reading-heavy work; reserve `opus` for reasoning-heavy tasks
4. Use `effort` to bump a delegated step without raising effort for the whole session

### Run independent agents in parallel; use background only for genuinely-async work [#20]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Multiple Agent calls in one message run concurrently — that's the parallelism win, not `run_in_background`
- Use background mode when you have other work to do while the agent runs, not as a default
- Don't parallelize agents whose outputs feed each other — sequence them so the second has the first's result
- After a parallel batch, reconcile in the parent — don't ask one of the children to merge the others' findings

**Agent steps:**
1. When delegating multiple independent tasks, send all Agent tool calls in a single message — they will run in parallel
2. If task B needs B's prompt to depend on task A's result, sequence them across turns — do not parallelize
3. Reserve `run_in_background: true` for cases where the parent will actually do other work while waiting
4. After parallel agents return, do the reconciliation in the parent thread rather than spawning another agent to merge

### Verify what the agent did, not what it said it did [#21]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- An agent's return message describes intent — it is not evidence of outcome
- For code-writing agents, read the diff before accepting their summary
- For research agents, spot-check by opening one or two of the files they cite
- Treat 'all tests pass' from an agent as a claim until you see the test runner output

**Agent steps:**
1. Treat every subagent summary as a claim to verify, not as established fact
2. For code-writing agents, run `git diff` or `git status` and review the change before reporting completion
3. For research or audit agents, open one or two cited files and confirm the finding exists
4. For agents that ran tests or builds, check the actual runner output rather than the agent's summary of it
5. When reporting to the user, attribute unverified agent claims ('the agent reports X') rather than stating them as your own

