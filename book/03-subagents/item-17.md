---
item: 17
theme: subagents
title: "Brief a subagent like a stranger — goal, context, constraints, response shape"
tags: [subagents, prompting, delegation]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: [1, 15]
things_to_remember:
  - "A subagent starts with no memory of your conversation — anything it needs to know has to be in the prompt"
  - "State the goal, the context you've already established, and the shape of the response you want back"
  - "Don't write 'based on your findings, fix the bug' — that delegates the synthesis you should be doing"
  - "For lookups, hand over the exact thing; for investigations, hand over the question, not prescribed steps"
agent_steps:
  - "Before sending a subagent prompt, check that someone reading it cold could act on it without seeing this conversation"
  - "Include relevant file paths, prior conclusions, and ruled-out options in the prompt — do not assume the subagent will rediscover them"
  - "Specify the desired response length and shape (e.g., 'under 200 words', 'a table of file:line:reason')"
  - "Avoid prompts that punt synthesis back to the agent ('based on your findings, decide what to do') — make the decision yourself in the parent thread"
---

## Why this matters

A subagent is a fresh Claude process. It hasn't read the conversation. It doesn't know what you've already tried, what you've ruled out, or what the user actually cares about. The CLAUDE.md files in scope will load, but everything else in your context — including the *reason* this task exists — has to be reconstructed from the prompt you send.

That's why terse, command-style delegation produces shallow, generic work. "Fix the auth bug" sends an agent with no idea which file, which bug, or which constraints. It will pick a plausible-looking issue and confidently report a fix to something you weren't asking about. The prompt didn't fail because the agent is weak; it failed because the briefing was a fragment of an idea the parent thread already had context for.

The fix is to brief the subagent the way you'd brief a smart colleague who just walked into the room mid-discussion. State the goal. Give the context that's load-bearing — file paths, prior attempts, things you've already ruled out, the actual constraints. And specify the response shape: how long, in what form, answering which specific questions. "Under 200 words" and "report as a table" are not stylistic flourishes; they're how you keep the return inside the context budget you spawned the subagent to protect.

There's a subtler trap: prompts that delegate *understanding* rather than work. "Based on your findings, fix the bug" or "based on the research, implement it" push synthesis onto the agent. That looks efficient but it isn't — the synthesis is the part you should be doing in the parent thread, with full context of the user's goal. Make the agent do the lookups and the legwork; you do the decisions.

## What to avoid

Two-word prompts. Prompts that reference "the issue we discussed" without restating what the issue is. Prompts that prescribe steps when the premise might be wrong ("first do X, then do Y" — but X is the wrong starting point and the agent now wastes its turns on dead premise). Prompts that ask the agent to make a judgment call only the parent thread has context for.

## What to do instead

Write the prompt so it stands alone. State the goal in the first sentence. Drop in the relevant file paths, what you already know, what you've already ruled out, and what you specifically need answered. Specify the response shape — length, format, and what counts as "done." For lookups, give the exact query; for investigations, give the question.

If you find yourself writing "based on your findings, do X" — stop. Have the agent return the findings, and do X yourself in the next turn.

## Example

Terse — fails for predictable reasons.

```text
Agent(description="Fix the login bug",
      prompt="Look at the login code and fix the bug. Tests are failing.")
```

The agent doesn't know which file, which test, which bug. It will pick something.

Self-contained — gives the agent enough to do real work.

```text
Agent(subagent_type="general-purpose",
      description="Diagnose login 401 on iOS",
      prompt="On iOS Safari, /api/login returns 401 even with valid
              credentials. Web and Android work. We've ruled out the
              token signing path (verified by hand). The suspect is
              cookie SameSite handling in
              `src/auth/cookie-policy.ts:42-90`, which was changed
              last week (commit a3f2b1). Investigate whether that
              change set SameSite=Strict for /api/login responses
              and whether iOS Safari is dropping the cookie on the
              redirect from /oauth/callback. Report: yes/no, the
              specific lines that cause it, and the minimal fix.
              Under 250 words.")
```

The second prompt makes the agent's job small and well-defined. The agent doesn't have to rediscover the user's context; the parent thread does the synthesis on the way back.
