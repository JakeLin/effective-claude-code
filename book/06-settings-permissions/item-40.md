---
item: 40
theme: settings-permissions
title: "Use deny rules as the safety net nothing can override"
tags: [permissions, deny, secrets, security, guardrails]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [29, 38, 39]
things_to_remember:
  - "Evaluation order is deny → ask → allow, and deny wins across every settings layer — a deny rule cannot be overridden by any allow"
  - "Deny the things that must never happen regardless of mode or allowlist: reading secrets (`.env`), touching credential files, destructive commands"
  - "Deny rules hold even in acceptEdits and bypass-adjacent flows — they're the floor, not a default you can step around"
  - "A short, well-chosen deny list is cheaper insurance than auditing every allow rule for what it might accidentally permit"
agent_steps:
  - "Add deny rules for anything that must never run or be read: secret files, credential stores, production-destructive commands"
  - "Rely on evaluation order — deny is checked first and beats any matching allow or ask rule at any layer"
  - "Put critical deny rules in committed project settings (and managed policy where available) so they protect the whole team"
  - "Treat the deny list as a hard floor independent of permission mode — verify secrets stay denied even under acceptEdits"
---

## Why this matters

The three permission lists are not peers. Rules are evaluated `deny` first, then `ask`, then `allow`, and the first match wins — which means a `deny` rule beats any `allow` rule that would otherwise match, no matter which settings layer either one lives in. A teammate's broad `allow`, your own `acceptEdits` mode, a generous managed grant — none of them can override a `deny`. That asymmetry is the whole reason the deny list is worth caring about: it's the one part of the permission system that fails closed.

This makes `deny` the right home for the small set of things that must *never* happen. Reading `.env` or a credentials file leaks secrets into the model's context and possibly into logs or a commit. A `DROP TABLE` against the wrong database, a force-push to main, an `rm -rf` at the wrong path — these aren't "ask me first" operations, they're "never, regardless of what the prompt says" operations. Putting them in `deny` means no allowlist mistake, no overeager mode, and no confused prompt can route around them. The guarantee lives in the harness, not in the model's judgment.

The economics favor a deny list, too. You could try to keep every `allow` rule perfectly scoped so nothing dangerous ever slips through — but that's a standing audit burden, and one over-broad rule undoes it. A handful of `deny` rules is cheaper and more robust: instead of proving that *nothing* you allowed is dangerous, you assert directly that *these specific dangerous things* are off the table. Deny the secrets and the irreversibles explicitly, and the allowlist can be a little loose without becoming a liability.

## What to avoid

Relying solely on a carefully-scoped allowlist to keep secrets safe, with no explicit `deny` — one broad allow rule and the protection is gone. Assuming `acceptEdits` or a permissive mode will still somehow protect secret files; modes don't override deny, but the *absence* of a deny rule leaves nothing to enforce. Leaving destructive commands merely un-allowlisted (so they prompt) when they should be denied outright. Scattering deny rules only in personal local settings where they don't protect teammates.

## What to do instead

Write down the short list of things that must never happen and encode each as a `deny` rule: secret and credential files under `Read(...)` deny, irreversible or production-destructive commands under `Bash(...)` deny. Put them in committed project settings so the whole team is covered, and in managed policy where an org needs to guarantee them. Trust the evaluation order — deny is checked first and wins — and treat the list as a hard floor that holds independent of permission mode. Then verify it: confirm a denied secret file stays denied even when you switch into `acceptEdits`.

## Example

A deny list as a safety net under a working allowlist:

```json
{
  "permissions": {
    "allow": [
      "Edit(/src/**)",
      "Bash(npm run test:*)",
      "Bash(git *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Bash(git push --force:*)",
      "Bash(rm -rf /:*)"
    ]
  }
}
```

Note the interaction: `Bash(git *)` in `allow` is broad enough to cover `git push --force` — but the `deny` rule beats it, because deny is evaluated first. The force-push is blocked despite the matching allow. Likewise, every `Read` of source is permitted, yet `.env` and `secrets/` stay unreadable. The allowlist can stay convenient precisely because the deny list catches the things that must never get through — and nothing in any layer, no mode, can talk the harness out of a deny.
