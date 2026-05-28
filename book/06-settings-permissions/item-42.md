---
item: 42
theme: settings-permissions
title: "Confine bypass mode to a sandbox you can throw away"
tags: [permissions, bypass, sandbox, security, isolation]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [36, 37, 40, 41, 60]
things_to_remember:
  - "bypassPermissions / --dangerously-skip-permissions removes the safety net — only run it where a worst-case action can't hurt anything you care about"
  - "The right home for bypass is an isolated, disposable environment: a fresh container, an ephemeral VM, a throwaway worktree — not your laptop on a repo with prod credentials"
  - "Prefer sandboxing (sandbox.enabled, filesystem + network allowlists) over bypass when you want autonomy with guardrails still in place"
  - "deny rules and a few protected paths still apply under bypass, but don't rely on them — bypass means assuming the checks are gone"
agent_steps:
  - "Only enable bypassPermissions or --dangerously-skip-permissions inside an isolated, disposable environment where the blast radius is contained"
  - "Before bypassing, confirm there are no real credentials, no production access, and nothing irreversible reachable from the working directory"
  - "Prefer enabling sandbox (sandbox.enabled) with filesystem and network allowlists to get autonomy while keeping OS-level guardrails"
  - "Never use bypass mode on a developer machine with live access just to stop permission prompts"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

`bypassPermissions` mode — and its CLI form `--dangerously-skip-permissions` — turns off the permission system almost entirely. Claude runs commands and writes files without asking. The word "dangerously" is in the flag name on purpose: you've removed the layer whose entire job is to catch a destructive or mistaken action before it executes. There are legitimate uses for this, but every one of them shares a precondition — the environment is built so that the worst thing Claude could do is *fine*.

That precondition is the whole Item. Bypass is appropriate in a fresh container that gets discarded after the run, an ephemeral CI VM, a throwaway git worktree with no credentials in reach — places where a wrong command destroys nothing you can't recreate in seconds. It is *not* appropriate on your everyday laptop, in a repo that has production database URLs in its `.env`, with your SSH keys and cloud credentials a directory away. The same command that's harmless in a disposable container is catastrophic there. The mode didn't change; the blast radius did, and the blast radius is the only thing that makes bypass safe or reckless.

When you want Claude to work autonomously but you *can't* make the environment fully disposable, reach for sandboxing instead of bypass. With `sandbox.enabled`, bash commands run under OS-level isolation, and you can grant autonomy within bounds — `filesystem.allowWrite` and `denyWrite` paths, `network.allowedDomains` and `deniedDomains` — so Claude proceeds without prompts but still can't write outside the project or exfiltrate to an arbitrary host. That's the better default for "let it run unattended": the guardrails stay up, they're just enforced by the OS instead of by a prompt. Bypass removes the guardrails; sandbox relocates them somewhere the model can't argue with.

## What to avoid

Using `--dangerously-skip-permissions` on a developer machine that has live credentials and production access, just to stop being prompted. Treating bypass as a productivity setting rather than an isolation-dependent one. Assuming the handful of still-protected paths under bypass (`.git`, shell config, the filesystem-root circuit breaker) make it broadly safe — they're a thin backstop, not the safety net. Reaching for bypass when what you actually wanted was unattended autonomy *with* guardrails, which is what sandbox mode provides.

## What to do instead

Decide first whether the environment is disposable. If a worst-case action can't hurt anything you care about — fresh container, ephemeral VM, throwaway worktree, no real credentials reachable — bypass is reasonable there. If it isn't disposable, don't bypass: enable sandboxing and scope its filesystem and network allowlists so Claude gets autonomy while the OS keeps it inside the lines. Either way, before you turn off prompts, look at what's actually reachable from the working directory — credentials, production access, irreversible operations — and make sure the answer is "nothing that matters."

## Example

Bypass, where it belongs — an ephemeral, credential-free environment:

```bash
# Inside a fresh, disposable container with no real secrets mounted
claude --dangerously-skip-permissions -p "refactor the parser and run the tests"
```

The container is thrown away when the run finishes. The worst Claude can do is break a copy of the code that didn't exist an hour ago and won't exist an hour from now.

Sandbox, for autonomy *with* guardrails on a non-disposable machine:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "filesystem": {
      "denyWrite": ["~/.ssh/**", "/etc/**"]
    },
    "network": {
      "allowedDomains": ["registry.npmjs.org", "github.com"],
      "deniedDomains": ["*"]
    }
  }
}
```

Here Claude runs bash without prompting on every command — but under OS-level isolation it can't write to your SSH keys, can't touch `/etc`, and can only reach the two domains the build actually needs. That's the shape to default to when you want unattended work but can't make the environment disposable: keep the guardrails, just move them down into the OS where the model can't talk its way past them. Reserve bare bypass for the throwaway box where there's nothing left to guard.
