---
item: 38
theme: settings-permissions
title: "Curate the allowlist deliberately — allow the safe and frequent, let the rest prompt"
tags: [permissions, allowlist, workflow, friction]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [29, 40, 41]
things_to_remember:
  - "The allowlist exists to remove friction on operations that are both safe and frequent — not to silence every prompt"
  - "Allow what you'd approve without thinking every time; leave anything consequential to prompt so you stay in the loop on decisions that matter"
  - "Build the allowlist incrementally from real prompts — approve-and-remember as they come up, rather than guessing a big list upfront"
  - "An allowlist that covers the boring 90% makes the 10% of prompts that remain meaningful again"
agent_steps:
  - "Add a tool/command to permissions.allow only when it is both safe to run unattended and run often enough that prompting is pure friction"
  - "Leave consequential operations (network writes, deploys, destructive commands, anything you'd want to eyeball) to prompt rather than allowlisting them"
  - "Grow the allowlist from real sessions — when a safe, repetitive prompt appears, approve it persistently rather than pre-populating speculative rules"
  - "Periodically review the allowlist and remove rules that are broader than the operations you actually trust"
---

## Why this matters

The permission allowlist is a friction tool, not a mute button. Its job is to stop Claude from asking you the same trivial question forty times a day — "can I run the tests?", "can I read this file?" — so your attention is spent only on the decisions that actually need a human. The temptation, after the tenth prompt, is to reach for the broadest possible grant and never be asked again. That's the wrong instinct, and it inverts the whole point of the system.

A good allowlist has a clean dividing line: a rule earns its place only if the operation is *both* safe to run unattended *and* frequent enough that prompting is pure overhead. Running the test suite is safe and constant — allow it. Reading source files is safe and constant — allow it. Pushing to a remote, deleting files, hitting a production endpoint, installing arbitrary packages — those are consequential, and a prompt there isn't friction, it's the system working. The prompt is your chance to catch a mistake before it happens, and you only get that chance on operations you didn't pre-approve.

The deeper payoff is that a well-curated allowlist *restores meaning to the prompts that remain*. If Claude asks permission for everything, you learn to mash approve without reading — and then the one prompt that actually mattered slips through on reflex. If the boring 90% is allowlisted away, the 10% of prompts you still see are, by construction, the consequential ones. You read them because there are few enough to read. The allowlist's real product isn't fewer prompts; it's prompts you still pay attention to.

## What to avoid

Allowlisting `Bash(*)` or otherwise granting whole tool families to stop being asked. Pre-populating a giant speculative allowlist before you've seen which operations actually recur. Adding a rule for a consequential operation — a deploy, a force-push, a destructive command — just because it came up twice. Approving prompts on reflex because there are so many that reading them stopped being viable.

## What to do instead

Build the allowlist incrementally, from real sessions. When a prompt appears for something safe and repetitive, approve it persistently so you're not asked again. When a prompt appears for something consequential, answer it each time — that recurring prompt is a feature. Keep the line clear in your head: safe *and* frequent gets allowlisted; everything else prompts. Review the list occasionally and tighten any rule that's broader than the set of operations you genuinely trust to run unattended.

## Example

An allowlist curated to the safe-and-frequent operations of a typical project:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Read(./src/**)"
    ]
  }
}
```

Notice what's *absent*: `git push`, `rm`, `npm install`, anything touching the network or production. Those still prompt — deliberately. The list covers the operations Claude performs constantly and that you'd approve without a second thought, and stops there.

Contrast with the anti-pattern — the broad grant that defeats the purpose:

```json
{
  "permissions": {
    "allow": ["Bash(*)"]
  }
}
```

This silences every Bash prompt, including the ones you'd have wanted to see. Now a destructive command runs as readily as a test command, and you've traded a few seconds of friction for the loss of every catch-it-before-it-happens moment. The narrow list above is more typing and far safer; the broad grant is the convenience that costs you exactly when it matters.
