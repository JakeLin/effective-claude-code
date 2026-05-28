# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 9 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 9 --agent-steps --output .claude/skills/effective-claude-code/references/ch09-cli-headless.md -->

## CLI & Headless Mode

### Reach for headless mode when no human is in the loop [#57]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Headless mode (`claude -p`) runs one non-interactive turn and exits — use it whenever there's no human to answer prompts or catch mistakes
- Interactive is for collaboration and exploration; headless is for scripts, CI, git hooks, and batch jobs
- Headless has no one to approve permissions or redirect a wrong turn, so the run must be self-contained and bounded up front
- If you'd run a shell command in the context, headless Claude fits the same slot — it's a program, not just a chat

**Agent steps:**
1. Use `claude -p \"prompt\"` (print mode) for any non-interactive context: CI steps, git hooks, cron jobs, batch processing, shell pipelines
2. Use the interactive REPL for collaborative, exploratory work where you steer turn by turn
3. Before running headless, make the invocation self-contained — no prompt is coming, so all context and constraints go in up front
4. Pair headless mode with explicit guardrails (later Items) since there's no human to stop a runaway

### Treat `claude -p` as a Unix utility — pipe in, parse out, compose [#58]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- `claude -p` reads stdin and writes stdout, so it composes with other tools in a pipeline like any Unix command
- Pipe data in (`cat file | claude -p ...`) and pipe results onward (`| jq`, `> out.txt`) — no copy-paste, no TUI scraping
- Use the exit code: a headless run can signal pass/fail so a script or CI step can branch on it
- Keep each invocation focused on one transformation; chain small steps rather than one do-everything prompt

**Agent steps:**
1. Feed input via stdin (`cat data | claude -p \"...\"`) rather than embedding large content in the prompt string
2. Pipe the output to the next tool (`| jq`, `| tee`, `> file`) so Claude is one stage in a pipeline
3. Have the run signal success/failure through its exit code so callers can branch (`if claude -p ...; then`)
4. Compose several small, single-purpose invocations instead of one monolithic prompt when steps are distinct

### Ask for structured output when a program reads the result [#59]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Use `--output-format json` when a program consumes the result — you get a stable envelope with the result, session id, and cost, not prose to scrape
- Use `--json-schema` when you need the model's answer itself to be validated structured data, not just wrapped in metadata
- Parse fields (`jq -r '.result'`, `.session_id`, `.total_cost_usd`) instead of regex-ing free text
- Plain text output is for humans and simple pipes; structured output is for machines that branch on the result

**Agent steps:**
1. When a script will parse the result, pass `--output-format json` and read fields with `jq` rather than scraping text
2. Capture `.session_id` from the JSON envelope to chain follow-up turns, and `.total_cost_usd` for cost tracking
3. When the answer must be machine-validated structured data, pass `--json-schema` so output conforms to your schema
4. Reserve default text output for human-read results and simple file/pipe redirection

### Put a budget and a turn limit on every unattended run [#60]
<!-- ecc-meta: target="conversation" action="suggest" check="project has CI/CD configuration or headless Claude usage — remind about budget and tool limits for unattended runs" -->
- An unattended run with no limits is a runaway — there's no human to stop a loop that's burning turns and money
- Bound spend and length with `--max-budget-usd` and `--max-turns`; both are hard stops the harness enforces
- Scope what the run can do with `--allowedTools` / `--tools` / `--disallowedTools` and a tight `--permission-mode`, since no one will answer prompts
- In headless contexts there's no permission prompt to fall back on — pre-decide every tool the run may use

**Agent steps:**
1. On every headless/unattended invocation, set `--max-turns` and `--max-budget-usd` to hard-cap length and spend
2. Restrict tools explicitly with `--tools` or `--allowedTools`, and deny dangerous ones with `--disallowedTools`
3. Choose a `--permission-mode` that doesn't depend on a human (e.g. a locked-down mode), since prompts can't be answered
4. Avoid `--dangerously-skip-permissions` unless the run is inside a disposable, isolated environment (Item 42)

### Chain headless turns with session IDs, not one giant prompt [#61]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Headless runs are stateless by default — each `-p` invocation starts fresh unless you carry the session forward
- Capture the `session_id` from JSON output and pass it to `--resume` to continue with full context on the next turn
- `--continue` resumes the most recent session in the directory; `--fork-session` branches a session without mutating the original
- Chain focused turns instead of one mega-prompt — each step stays small, observable, and individually verifiable

**Agent steps:**
1. Run the first turn with `--output-format json` and capture `.session_id`
2. Continue the conversation by passing that id to `--resume <id>` on subsequent invocations
3. Use `--continue` for the simple case of resuming the latest session in the current directory
4. Use `--fork-session` to branch from an existing session when you want to try a path without altering the original
5. Break multi-step headless work into a sequence of resumed turns rather than one prompt that does everything

### Append to the system prompt for rules; replace it only for a different agent [#62]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- `--append-system-prompt` adds your instructions on top of the defaults; `--system-prompt` throws the defaults away entirely
- The default system prompt carries tool guidance, safety, and coding conventions — replacing it drops all of that
- Append for per-run rules, formatting, or persona tweaks; replace only when you genuinely want a different agent from scratch
- When in doubt, append — replacing is the rare, deliberate choice, not the default

**Agent steps:**
1. To add behavior to a headless run (rules, output format, tone), use `--append-system-prompt` (or `--append-system-prompt-file`) and keep the defaults
2. Use `--system-prompt` / `--system-prompt-file` only when you intend a fundamentally different agent and accept losing the default tool guidance and safety
3. Prefer append unless you have a specific reason to discard the built-in prompt
4. For project conventions that should always apply, prefer CLAUDE.md over per-invocation prompt flags

### Graduate to the Agent SDK when the script becomes a product [#63]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- The Agent SDK (TypeScript and Python) is the same harness as the CLI, exposed programmatically via a `query()` primitive
- Shelling out to `claude -p` is right for scripts and glue; the SDK is right when automation becomes an application
- The SDK gives you typed message streams, programmatic hooks, permission callbacks, and real error handling — things shell parsing fakes badly
- Don't reach for the SDK prematurely — a shell pipeline is simpler until you need the control the SDK provides

**Agent steps:**
1. Use `claude -p` for one-off automation, glue scripts, CI steps, and pipelines
2. Move to the Agent SDK (`@anthropic-ai/claude-agent-sdk` or `claude-agent-sdk`) when building an application that embeds Claude as a component
3. Choose the SDK when you need to iterate over message events, handle permissions in code, register hooks programmatically, or do structured error handling and retries
4. Stay with the CLI when a shell pipeline already does the job cleanly — adopt the SDK for control, not by default

