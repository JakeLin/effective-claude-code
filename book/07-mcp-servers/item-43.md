---
item: 43
theme: mcp-servers
title: "Reach for MCP when the capability lives outside your shell and filesystem"
tags: [mcp, mindset, when-to-use, integration]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [29, 44]
things_to_remember:
  - "MCP earns its place when Claude needs a system the shell and filesystem can't reach — a live database, a real browser, an external API, an issue tracker"
  - "If a CLI, script, or file already exposes the capability, use that — don't wrap it in an MCP server for no gain"
  - "MCP shines for stateful or interactive systems (a browser session, an authenticated API) where a one-shot shell command is awkward"
  - "The question isn't 'could an MCP server do this?' but 'is this reachable any simpler way?' — prefer the simpler way"
agent_steps:
  - "Before adding an MCP server, check whether the capability is already reachable via an existing CLI, script, or file the Bash/Read tools can use"
  - "Reach for MCP when the target is an external or stateful system (database, browser, hosted API, SaaS tool) that shell commands handle poorly"
  - "Prefer an existing well-maintained server over building your own; build one only when no tool exposes the capability"
  - "Reject MCP for tasks the filesystem and shell already cover — adding a server there is pure overhead"
ecc_meta:
  target: conversation
  action: suggest
  check: "always"
---

## Why this matters

MCP connects Claude to systems that the built-in tools can't touch. The Bash tool runs shell commands; Read, Edit, and Write work the filesystem. That covers an enormous amount of software work — but it stops at the edge of your machine. Claude can't natively query a running Postgres instance, click through a live web app, read your Jira board, or pull the current docs for a fast-moving library. MCP exists to bridge exactly that gap: a server adapts an external or stateful system into tools Claude can call. The right time to reach for it is when the capability genuinely lives *outside* the shell and filesystem.

The overreach is treating MCP as the default integration mechanism for everything. If a capability is already exposed by a command-line tool, Claude can just run it — `gh`, `psql`, `aws`, your project's own scripts are all reachable through Bash with zero extra setup. Wrapping those in an MCP server adds a process to manage, tools to load, and a trust decision to make, in exchange for nothing you didn't already have. The filesystem is the same story: if the data is a file, Read it. MCP is overhead when the simpler path already works, and the simpler path usually works.

Where MCP genuinely wins is stateful and interactive systems, where a one-shot shell command is the wrong shape. Driving a browser means maintaining a session across many actions — navigate, click, screenshot, inspect — which a sequence of `curl` calls models badly. An authenticated API with a real object model is cleaner as typed tools than as hand-assembled HTTP. Live documentation that changes faster than any training cutoff is something no local file holds. In those cases the server isn't overhead; it's the thing that makes the capability usable at all. The discriminating question is never "could an MCP server do this?" — almost anything could be an MCP server — but "is this reachable any simpler way?"

## What to avoid

Building or installing an MCP server to do something `gh`, `psql`, `docker`, or a project script already does through Bash. Reaching for MCP reflexively whenever an integration is mentioned, before checking whether the capability is already at hand. Writing a custom server for a one-off task that a single shell command would have handled. Treating "there's an MCP server for that" as a reason to use it, independent of whether you needed a server at all.

## What to do instead

Start by asking whether the capability is already reachable. Is there a CLI for it? A script in the repo? Is the data just a file? If so, use the tool you already have. Reserve MCP for systems the shell and filesystem can't reach well — live databases, real browsers, hosted APIs, external SaaS tools, fast-moving docs — and especially for stateful or interactive ones where a one-shot command is awkward. When you do need a server, prefer an existing, well-maintained one over building your own, and build only when nothing exposes the capability.

## Example

The discriminating question, applied:

```text
Task: "check the status of the latest CI run"
  Already reachable?  Yes — `gh run list` via Bash.
  Verdict:            No MCP server. Use the CLI you have.

Task: "read the contents of config.yaml"
  Already reachable?  Yes — it's a file. Read it.
  Verdict:            No MCP server.

Task: "click through the signup flow and screenshot each step"
  Already reachable?  No — stateful browser session, many actions.
  Verdict:            MCP (a browser server) is the right tool.

Task: "look up the current API for this fast-moving library"
  Already reachable?  No — newer than any training data, not a local file.
  Verdict:            MCP (a live-docs server) earns its place.
```

The first two are overhead as MCP servers and trivial with the built-in tools. The last two are awkward or impossible without one. The pattern holds across the board: MCP is for the systems your shell and filesystem can't reach, and reaching for it elsewhere just adds a server you didn't need.
