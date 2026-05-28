# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 1 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 1 --agent-steps --output .claude/skills/effective-claude-code/references/ch01-memory.md -->

## Memory & CLAUDE.md

### Treat CLAUDE.md as a living team artifact, not a one-time setup [#1]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- CLAUDE.md compounds — every recurring correction belongs in it
- Edit it the same week you find the gap; commit the rule alongside the code change that motivated it
- Prune ruthlessly — stale rules cause Claude to follow stale conventions
- Treat `/init` as a starting point, not a finishing point

**Agent steps:**
1. When the user corrects a mistake Claude should have known not to make, propose adding a rule to CLAUDE.md and offer the diff
2. Before adding a new rule, check whether a similar rule already exists; update the existing one rather than duplicating
3. Phrase new rules concretely — commands, paths, file names — not vague verbs
4. When the rule is motivated by a specific code change, suggest committing the CLAUDE.md update in the same commit
5. If asked to prune CLAUDE.md, flag rules that conflict, no longer match the codebase, or duplicate other rules

### Use CLAUDE.md for context, hooks for guarantees [#2]
<!-- ecc-meta: target="claude-md" action="add" check="CLAUDE.md has MUST/NEVER rules but project already has hooks or settings.json — skip if no enforcement layer exists yet" -->
- CLAUDE.md is context Claude reads, not configuration the harness enforces
- If a rule MUST run, write a hook; CLAUDE.md is advice
- Capitalization and stern language don't elevate context to enforcement
- Use deny-permissions for actions that must be blocked, not CLAUDE.md prose

**Agent steps:**
1. When the user adds a rule to CLAUDE.md framed as ALWAYS / NEVER / MUST, ask whether failure to follow it would be a serious problem
2. If serious, propose a hook (PreToolUse to block before, PostToolUse to enforce after) in addition to or instead of the CLAUDE.md entry
3. For 'must not happen' rules tied to specific tools or paths, propose a `permissions.deny` rule rather than CLAUDE.md prose

### Write instructions specific enough to verify [#3]
<!-- ecc-meta: target="claude-md" action="fix" check="Actionable rules in CLAUDE.md use vague verbs (properly, handle, consider) instead of specific commands or paths" -->
- Concreteness is the single biggest determinant of CLAUDE.md adherence
- If you can't verify a rule was followed, Claude probably can't tell either
- Replace soft verbs (handle, consider, try, properly) with commands and paths
- Rules that include exact commands, paths, or file names work; rules that don't, don't

**Agent steps:**
1. When asked to add a rule to CLAUDE.md, check whether it names specific commands, paths, or file names
2. If the rule uses soft verbs (properly, nicely, correctly, handle, consider), propose a concrete rewrite
3. When the user phrases an instruction vaguely, ask what 'correct' looks like in this codebase and capture the concrete answer

### Keep each CLAUDE.md under 200 lines [#4]
<!-- ecc-meta: target="claude-md" action="fix" check="CLAUDE.md line count > 200" -->
- Every line in CLAUDE.md loads into every session — treat the file as a context budget
- Past the 200-line target, adherence gets harder because useful rules compete with more noise
- `@path` imports help organize for humans but don't reduce context cost
- When the file grows, move path-specific rules to `.claude/rules/` and delete stale ones

**Agent steps:**
1. When CLAUDE.md crosses 150 lines, propose an audit before adding more rules
2. Identify rules that only apply to specific paths and propose moving them to `.claude/rules/` with `paths:` frontmatter
3. Flag rules that duplicate, conflict, or no longer match the codebase and propose removal

### Place instructions at the scope where they actually apply [#5]
<!-- ecc-meta: target="claude-md" action="suggest" check="CLAUDE.md may contain personal preferences or machine-specific rules that shouldn't be shared with the team" -->
- Project CLAUDE.md is for the team; user CLAUDE.md is for you; CLAUDE.local.md is for this project but private
- Personal preferences in the project file leak to your teammates
- Project-specific rules in `~/.claude/CLAUDE.md` follow you into every other project
- Ancestor CLAUDE.md files load eagerly; descendants load lazily; siblings never share

**Agent steps:**
1. When asked to add a rule, decide its scope before its content — team-shared, personal-global, or personal-project
2. Propose `./CLAUDE.md` for team-shared rules, `~/.claude/CLAUDE.md` for personal-global, `./CLAUDE.local.md` for personal-project
3. If proposing `./CLAUDE.local.md`, confirm it is in `.gitignore` — if not, propose adding it

### Move path-specific guidance into `.claude/rules/` [#6]
<!-- ecc-meta: target="claude-rules" action="fix" check="CLAUDE.md contains rules that start with 'when working in', 'for files in', or reference specific subdirectories" -->
- Rules in `.claude/rules/` with `paths:` frontmatter load only when Claude touches matching files
- Use narrow globs — `src/api/**/*.ts`, not `**/*`
- One file per subsystem so the team knows where to add rules
- Rules without `paths:` frontmatter load unconditionally — same context cost as CLAUDE.md

**Agent steps:**
1. When asked to add a rule that starts with 'when working in <path>' or only applies to specific files, propose `.claude/rules/<topic>.md` with a `paths:` glob instead of CLAUDE.md
2. Check that `paths:` globs are narrow enough that the rule loads only for relevant files
3. When creating a new rule file, group it by subsystem (e.g., `testing.md`, `api.md`) rather than by author or date

### Let auto memory absorb the corrections you'd otherwise repeat [#7]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Auto memory is Claude's running notebook — complementary to your hand-written CLAUDE.md
- Auto memory is machine-local; for team-shared rules, use CLAUDE.md instead
- Audit it with `/memory` periodically — the files are plain markdown you can edit or delete
- Promote useful auto-memory entries into CLAUDE.md when the whole team should see them

**Agent steps:**
1. When the user corrects a personal preference, save it to auto memory rather than proposing a CLAUDE.md edit
2. When the user corrects something the whole team should know, propose a CLAUDE.md edit instead
3. If asked what Claude remembers about this project, point to `/memory` and the auto-memory directory
4. Periodically suggest auditing auto memory if entries look stale, duplicative, or contradict CLAUDE.md

