# Skills

A skill is a folder under `.claude/skills/<name>/` (or `~/.claude/skills/<name>/` for personal scope) containing a `SKILL.md` with YAML frontmatter and any number of supporting files — references, scripts, config, examples. The frontmatter describes when the skill should run; the body explains how. Claude picks up skill descriptions at session start and can invoke a skill three ways: the user types `/skill-name`, Claude routes to it automatically when its description matches an intent, or it gets preloaded into a subagent.

Skills are the most-used extension surface in Claude Code for a reason. They live next to your code, version with your repo, compose with subagents, and load lazily — descriptions stay in context but full content only inflates when invoked. Done well, a single skill can absorb weeks of "here's how we do X" instructions the team keeps repeating.

This chapter starts with what a skill actually *is* (a folder, not a markdown file), then covers the routing surface (description, `disable-model-invocation`), what kind of content earns its keep (gotchas and non-obvious knowledge, not defaults), how to write a skill that survives reuse (goals + constraints, not prescriptions), how skills relate to agents and commands, how they compose into subagents, and how to scope them across project, personal, plugin, and nested monorepo locations.
