# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 8 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 8 --agent-steps -->

## Orchestration & Workflows

### Make Claude plan before it implements anything non-trivial [#50]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Separate thinking from doing: have Claude research and propose a plan before it edits a single file
- Plan mode is read-only by guarantee — Claude explores and proposes, but can't change anything until you approve
- Review and edit the plan while it's cheap to change; a wrong plan caught here costs minutes, caught after implementation costs hours
- For larger work, make the phases explicit (research → plan → implement) with a gate between each

**Agent steps:**
1. For any non-trivial task, enter plan mode (Shift+Tab to cycle, or --permission-mode plan) before making changes
2. Let Claude read the relevant code and propose a concrete, phased plan rather than starting to edit immediately
3. Review the proposed plan, edit it where it's wrong or thin, and only then approve to switch into an edit-capable mode
4. For larger features, run distinct phases — research/feasibility, then planning, then implementation — with a human checkpoint between them

### Treat the context window as a budget you actively manage [#51]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- The context window is finite, and output quality degrades as it fills — a bloated context makes Claude slower and less accurate
- Compact deliberately (around half-full) rather than waiting for auto-compaction to fire at an arbitrary moment
- Clear context between unrelated tasks so old, irrelevant history stops competing for attention
- Break work into chunks that each fit comfortably under half the window, so no single step runs out of room

**Agent steps:**
1. Watch context usage (/context) and run /compact with focusing instructions at roughly 50% rather than letting it auto-fire
2. Use /clear when starting an unrelated task so prior history doesn't dilute the new one
3. Scope each task or subtask to fit comfortably under half the context window; split anything larger
4. Move large side-investigations into subagents (their own context) instead of letting them fill the main window

### Delegate side-quests to subagents to keep the main thread focused [#52]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Fan independent legwork out to parallel subagents — each returns a compact summary, so the main thread reasons over conclusions, not file dumps
- Delegate work whose process is noisy but whose result is compact: broad searches, large-file exploration, parallel checks
- Independent subagents run in parallel, giving roughly N× effective context for fan-out work
- Don't delegate the understanding you need to keep — offload the legwork, retain the judgment

**Agent steps:**
1. When a side task would flood the main context with reads and tool calls but yields a compact answer, delegate it to a subagent
2. Run independent investigations as parallel subagents rather than sequentially in the main thread
3. Keep the synthesis, decisions, and code you must reason about in the main thread; offload only the legwork
4. Right-size delegation: scope the subagent's task so its returned summary is what the main thread actually needs

### Close every workflow with a verification loop Claude runs itself [#53]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- The iteration loop — generate, verify, fix — is what separates plausible output from working output
- Give Claude a way to check its own work: run the tests, type-check, take a screenshot, hit the endpoint
- Verification only counts if Claude actually observes the result and acts on it — 'I added a test' is not 'the test passed'
- A failing check Claude can see and re-run is worth more than any amount of careful prose about correctness

**Agent steps:**
1. After implementing, have Claude run the relevant verification — test suite, type-checker, linter, build, or a live check — and read the output
2. Loop on failures: Claude fixes, re-runs, and repeats until the check actually passes, rather than declaring done after the edit
3. For UI or runtime behavior, verify by observation (screenshot, endpoint response, log) not by inspection of the code alone
4. Make the verification command explicit and runnable so Claude can close the loop without asking how to check

### Get a second opinion from a fresh agent or a different model [#54]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- The context that wrote the code shares its blind spots — a fresh reviewer catches what the author cannot see
- A review subagent starts with a clean context and judges the work on its merits, not on the reasoning that produced it
- A different model brings genuinely different failure modes — cross-model review surfaces issues a same-model check misses
- Have the reviewer check against the plan and the requirements, not just the diff in isolation

**Agent steps:**
1. After implementation, spawn a review subagent with a clean context to critique the change against the plan and requirements
2. For high-stakes work, get a review from a different model (e.g. via another CLI) so different blind spots are covered
3. Give the reviewer the plan or requirements as the standard to judge against, not only the raw diff
4. Treat review findings as input to another verify-fix loop, not as a final sign-off to skip

### Drive multi-step work through a task list, not the conversation [#55]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- A task list externalizes the plan into durable state — work survives compaction, session end, and crashes instead of living only in the conversation
- Break multi-step work into tasks small enough to each fit comfortably under half the context window
- Tasks can declare dependencies (this blocks that), so the order is encoded in the list rather than re-derived each turn
- A shared task-list id lets multiple sessions or agents coordinate on the same work

**Agent steps:**
1. For multi-step work, create a task list with one task per independently-completable, verifiable chunk
2. Size each task to fit under half the context window so it can be done and verified without running out of room
3. Encode ordering with task dependencies (blockedBy/blocks) rather than relying on conversation order
4. Use a shared task-list id (CLAUDE_CODE_TASK_LIST_ID) when multiple sessions or agents need to coordinate on the same work

### Compose workflows from the primitive that fits each step [#56]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- The harness is a composition system: commands, subagents, skills, and hooks each do something the others can't — match each step to the right one
- Command = invokable entry point; subagent = isolated context + tools; skill = reusable domain knowledge; hook = deterministic enforcement
- A real workflow chains them: a command orchestrates, agents do isolated work, skills supply knowledge, hooks guarantee invariants
- Reach for the primitive whose property you need, not the one you reach for by habit — the leverage is in the fit

**Agent steps:**
1. Decompose a workflow into steps and ask, per step, which property is needed: an entry point, context isolation, reusable knowledge, or a hard guarantee
2. Use a command as the invokable orchestration entry point for a repeatable workflow
3. Use subagents for steps needing isolated context or parallelism; skills for knowledge reused across steps; hooks for invariants that must hold
4. Chain them (command → agent → skill, with hooks enforcing gates) rather than forcing one primitive to do another's job

