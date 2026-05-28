# Commands

A command is anything you trigger with `/`. Claude Code ships about eighty of them: **built-in commands** that run fixed harness logic (`/clear`, `/compact`, `/init`, `/memory`, `/model`, `/context`) and **bundled skills** shipped as prompt-based instructions (`/debug`, `/code-review`, `/run`, `/verify`, `/loop`). User-authored slash commands also exist — they live in `.claude/skills/` and get their own treatment in Chapter 4.

This chapter is about the commands you get for free. Almost every common Claude Code operation has a slash command that beats asking in prose: session management, model and effort switches, context observability, code review, verification, configuration. The Items teach which to reach for and when, with one running goal — replace long-form chat with one keystroke whenever the harness already does the work.

The Items build outward from a mindset (treat the slash menu as your first reach), through the session and observability primitives you'll use every hour, into the review and verification skills that bracket meaningful changes, and finish with the management surfaces that replace hand-editing configuration.
