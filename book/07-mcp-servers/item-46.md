---
item: 46
theme: mcp-servers
title: "Keep credentials out of committed config — inject them at connect time"
tags: [mcp, secrets, security, authentication, configuration]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [37, 45]
things_to_remember:
  - "Never hardcode API keys, tokens, or secrets in committed `.mcp.json` — they end up in git history forever"
  - "Use environment-variable expansion (`${VAR}`) in `.mcp.json` so the file references a secret without containing it"
  - "For dynamic or short-lived credentials, use a headers helper that generates auth at connect time, or OAuth where the server supports it"
  - "The committed config should describe how to connect, not carry the secret that authorizes the connection"
agent_steps:
  - "When a server needs a secret, reference it via `${VAR}` expansion in `.mcp.json` and supply the value through the environment, never inline"
  - "For tokens that rotate or expire, configure a headers helper command that emits fresh auth headers at connection time"
  - "Prefer OAuth for servers that support it — Claude Code completes the flow without any stored static secret"
  - "Before committing `.mcp.json`, scan it for literal keys/tokens and replace any with env-var references"
---

## Why this matters

An MCP server that talks to an authenticated system needs a credential, and the dangerous shortcut is to paste that credential straight into `.mcp.json`. Since project-scoped `.mcp.json` is committed to git, a hardcoded key doesn't just sit in the working file — it lands in the repository history, where deleting it later doesn't actually remove it. Anyone with repo access, now or in the future, can recover it. A secret committed once is a secret you must rotate, not a secret you can quietly delete. The committed config should describe *how* to connect; it must not carry the thing that *authorizes* the connection.

The clean substitute is environment-variable expansion. `.mcp.json` supports `${VAR}` (and `${VAR:-default}`) syntax in fields like `url`, `command`, `args`, `env`, and `headers`. The file references the secret by name, the value lives in the environment, and the committed artifact contains a pointer rather than a payload. A teammate cloning the repo gets the connection recipe and supplies their own value; the repository history stays clean. This is the same discipline as keeping secrets out of `settings.json` — the secret belongs in the environment or a credential store, never in a tracked file.

For credentials that aren't static — short-lived tokens, SSO, anything that rotates — go a step further and generate auth at connect time. A headers helper is a command Claude Code runs when it connects to the server; its output becomes the request headers, so a fresh token is minted per connection and nothing durable is stored anywhere. Where a server supports OAuth, that's better still: Claude Code discovers the auth endpoints and completes the browser flow, and there's no static secret in any file at all. The progression — env-var reference, then helper, then OAuth — moves steadily away from storing a secret toward proving identity on demand, and each step shrinks what an attacker could find at rest.

## What to avoid

Pasting an API key or bearer token directly into `.mcp.json` and committing it — it's now in history permanently, even if you "remove" it later. Assuming a private repo makes a committed secret safe; access changes, forks happen, history leaks. Hardcoding a long-lived token when the server supports OAuth or short-lived credentials. Committing a `.env` file alongside `.mcp.json` to "keep them together" — that just moves the leak.

## What to do instead

Reference secrets, don't embed them. Use `${VAR}` expansion in `.mcp.json` and provide the value through the environment, so the committed file holds a name, not a key. For credentials that rotate or expire, configure a headers helper that emits fresh auth at connection time. For servers that support OAuth, use it and store no static secret at all. Before every commit, scan `.mcp.json` for literal keys and tokens and replace them with references. The test is simple: nothing in a tracked file should be a secret on its own.

## Example

The anti-pattern — a token baked into committed config:

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://mcp.example.com/mcp?token=sk-live-9c3f...e21a"
    }
  }
}
```

That token is now in git history forever. The fix — reference it, supply the value from the environment:

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://mcp.example.com/mcp?token=${MCP_API_TOKEN}"
    }
  }
}
```

The committed file names the secret; the value comes from `MCP_API_TOKEN` in the environment and never enters the repo. For a rotating credential, drop the static token entirely and let a helper mint headers at connect time:

```bash
claude mcp add --transport http \
  --header "Authorization: Bearer $(mint-short-lived-token)" \
  remote-api https://mcp.example.com/mcp
```

Each connection gets a fresh token; nothing durable is stored. The committed config, in every case, describes how to connect and authorizes nothing on its own — which is exactly the property that keeps a leaked file from becoming a leaked secret.
