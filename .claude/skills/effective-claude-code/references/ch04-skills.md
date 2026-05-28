# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable only; chapters 4 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 4 --agent-steps -->

## Skills

### Treat a skill as a folder, not a markdown file [#22]
<!-- ecc-meta: target="conversation" action="suggest" check=".claude/skills/ exists — check whether any skill is a bare SKILL.md with no supporting files" -->
- A skill is a folder — `SKILL.md` is the entry point, but supporting files are where the leverage compounds
- Split long reference material into sibling files (`references/api.md`, `examples/`, `gotchas.md`) and point to them from `SKILL.md`
- Ship scripts in the skill folder when a deterministic step is better than asking Claude to reason it out
- `SKILL.md` and the description always load; supporting files load only when Claude reads them — use that for progressive disclosure

**Agent steps:**
1. When authoring a skill, keep `SKILL.md` short and reference long-form material in sibling files rather than inlining it
2. Place deterministic helpers (validators, parsers, generators) as scripts in the skill folder and invoke them from `SKILL.md`
3. For skills that need user-specific setup, store the configuration in `config.json` in the skill folder and read it at invocation time

### Write `description` for the router; use `disable-model-invocation` when auto-invocation is wrong [#23]
<!-- ecc-meta: target="conversation" action="suggest" check=".claude/skills/ exists — review description fields for vague or label-style wording that won't trigger routing" -->
- `description` is the routing rule — it tells Claude *when* to invoke, not *what* the skill is
- Name the trigger explicitly: 'Use when X', 'Use when the user asks for Y' — vague descriptions never fire
- Set `disable-model-invocation: true` for destructive or expensive skills you want users to invoke deliberately
- Set `user-invocable: false` for background knowledge that should never appear in the `/` menu

**Agent steps:**
1. When authoring a skill, write the `description` as a trigger criterion ('Use when…'), not a label
2. For destructive skills (deploys, drops, force-pushes), set `disable-model-invocation: true` so they only fire on explicit user invocation
3. For skills that exist purely as background knowledge for Claude, set `user-invocable: false` to hide them from the `/` menu
4. Audit existing skills: if Claude never auto-invokes one, rewrite the description as a trigger criterion before assuming the skill is broken

### Skills earn their keep on gotchas and non-obvious knowledge — update them every time Claude hits a new failure mode [#24]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- The highest-signal content in a skill is what pushes Claude out of its defaults — gotchas, conventions, project-specific footguns
- Don't restate what Claude already knows; it's context overhead with no behavior change
- Treat skills as living artifacts — the gotchas section should grow every time Claude makes a mistake using the skill
- Capture the *specific failure*, not a general principle — 'never use camelCase here, the API expects snake_case' beats 'follow API conventions'

**Agent steps:**
1. When writing a new skill, lead with what's non-obvious — defaults Claude would get wrong, project-specific conventions, footguns from the team's history
2. When Claude fails while using a skill, add the failure to the skill's gotchas section before fixing it — capture the lesson
3. Periodically review skills for content that restates obvious behavior; trim it
4. Make gotchas specific: file paths, exact patterns to avoid, concrete wrong vs. right examples

### Give a skill goals and constraints, not prescribed steps [#25]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Skills are reused in contexts you didn't anticipate — prescriptions break when the situation deviates
- State the goal, the constraints, and the success criteria; let Claude pick the steps
- If a step really must run in a specific order, make it a script — don't railroad it in prose
- When in doubt, ask: would a competent teammate handle this if I gave them only this skill body? If yes, ship it; if no, you're under-specifying the *what*, not the *how*

**Agent steps:**
1. When writing a skill body, lead with the goal and the constraints, not the sequence of actions
2. Replace 'first do X, then Y, then Z' patterns with 'achieve X subject to constraints A, B, C'
3. If a strict order is genuinely required (e.g., migrations must run before code deploy), enforce it via a script or a hook rather than via prose
4. Audit existing skills for over-prescription: where they read like a recipe rather than a brief

### Default to a skill before reaching for an agent or a command [#26]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Resolution preference is skill → agent → command — Claude reaches for the lightest fit first
- Skills run inline (no extra context window) and auto-invoke from `description` — usually the right default
- Promote to an agent when the work needs context isolation, persistent memory, or a different permission mode
- Promote to a command when the workflow must be user-initiated and never auto-fire

**Agent steps:**
1. When authoring a new extension, start with a skill; only promote to an agent or command if the skill form misses a requirement
2. Promote to an agent when the work would pollute the main context (large-surface research, autonomous multi-step exploration) or needs a permission mode like `acceptEdits`/`plan`
3. Promote to a command when the workflow must only run on explicit user invocation (no auto-discovery, no preload)
4. Resist the temptation to write three siblings (skill + agent + command) for the same task — pick the one that fits and ship it

### Preload skills into the subagents that need them; fork to a subagent only when context isolation is the point [#27]
<!-- ecc-meta: target="conversation" action="suggest" check=".claude/agents/ and .claude/skills/ both exist — check whether agents with recurring knowledge dependencies preload the relevant skills" -->
- `skills:` on an agent preloads full skill content at startup — bake domain knowledge into a specialized agent
- `context: fork` on a skill runs the skill in an isolated subagent context — use when the skill's intermediate work shouldn't pollute the main thread
- Preload is for knowledge an agent always needs; fork is for runtime context isolation
- Don't fork by default — inline skills are cheaper and keep results in the main reasoning context

**Agent steps:**
1. When a custom subagent has a recurring knowledge dependency, list the skill under `skills:` in the agent's frontmatter so it loads at agent startup
2. Use `context: fork` on a skill when its work would dump significant tool output into the main thread (large research, doc reading)
3. When forking, set `agent: Explore` or `agent: Plan` for read-only forks — they skip CLAUDE.md to keep context small
4. Audit `context: fork` usage: if the skill's result is short and the parent immediately reasons about it, the fork is probably wasted overhead

### Scope each skill where it applies — project, personal, plugin, nested [#28]
<!-- ecc-meta: target="conversation" action="suggest" check=".claude/skills/ exists — verify skills are scoped to the right level (project vs personal) for this repo type" -->
- Project skills (`.claude/skills/`) are team-shared and version with the repo; personal skills (`~/.claude/skills/`) are yours across projects
- In monorepos, nested `.claude/skills/` under a package load automatically when Claude works in that package's files
- Plugin skills are namespaced (`plugin:skill-name`) — use when distributing across many repos or teams
- Skill descriptions always count against the context budget — don't ship a skill globally if it's only useful in one place

**Agent steps:**
1. Place team-shared skills in `.claude/skills/<name>/` at the repo root and commit them; place your personal skills in `~/.claude/skills/<name>/`
2. In a monorepo, put package-specific skills under `packages/<pkg>/.claude/skills/` so they load only when working inside that package
3. When the same skill would be useful across many repos under your control, package it as a plugin and distribute via marketplace
4. Audit skills periodically: any skill no team member invokes after a month is probably scoped wrong or under-described

