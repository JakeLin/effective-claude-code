---
item: 45
theme: mcp-servers
title: "Add each server at the scope that matches who needs it"
tags: [mcp, scope, configuration, collaboration]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [36, 37, 46]
things_to_remember:
  - "MCP servers configure at three scopes: project (.mcp.json, committed, team-shared), user (~/.claude.json, all your projects), and local (private to you on this project)"
  - "Put a server in project scope when the whole team needs it for this repo; user scope when it's your personal tool everywhere; local when it's private to you and this project"
  - "Project-scoped servers travel with the repo — a teammate or a fresh session inherits them automatically"
  - "Choose scope by audience, not convenience — the wrong scope either leaks personal config to the team or hides shared config from them"
agent_steps:
  - "For a server the whole team needs on this repo, define it in .mcp.json at the project root and commit it"
  - "For a personal server you want across all your projects, add it at user scope (~/.claude.json)"
  - "For a server private to you on just this project, use local scope (claude mcp add --scope local)"
  - "Match scope to audience: team+repo → project, you+everywhere → user, you+this-repo → local"
---

## Why this matters

MCP servers, like settings, configure at distinct scopes, and the scope you choose decides *who* gets the server. There are three. **Project scope** lives in `.mcp.json` at the repo root, committed to git — it's the team-shared set, and anyone who clones the repo (or any fresh session that starts in it) inherits those servers. **User scope** lives in your `~/.claude.json` — personal servers that follow you across every project. **Local scope** is private to you *and* scoped to one project — your own servers for this repo that don't leak to teammates and don't follow you elsewhere.

Choosing by audience rather than by whichever command was handiest is what keeps the configuration coherent. A server the whole team relies on for this repo belongs in project scope, so nobody has to set it up by hand and the dependency is documented in the repo itself. A personal tool you want everywhere — your preferred docs server, say — belongs in user scope, so it's there in every project without being imposed on any team. An experimental or credential-bearing server you're trying out belongs in local scope, where it stays yours.

The failure modes are the mirror images of getting scope wrong, and they echo the settings hierarchy exactly. Put a personal server in committed project scope and you've pushed your tooling — and possibly your credentials — onto everyone who clones the repo. Put a team-essential server in your user or local scope and your teammates don't get it; they hit missing-tool errors and have to rediscover the setup you already did. The committed `.mcp.json`, like a committed `settings.json`, doubles as documentation: it tells every collaborator what external systems this project expects to reach. Scope the server to its real audience and that documentation stays accurate.

## What to avoid

Committing a personal or experimental server to project-scope `.mcp.json`, imposing it (and any embedded credentials) on the whole team. Keeping a team-essential server in your user or local scope, so teammates hit missing tools and have to set it up themselves. Defaulting every server to one scope out of habit. Putting a credential-bearing server in committed config at all — that's both a scope error and a secrets error (see the next Item).

## What to do instead

Ask who needs the server before you add it. The whole team, on this repo? Define it in `.mcp.json` and commit it, so it travels with the code. You, across all your projects? User scope. You, on just this repo — or anything experimental or credential-bearing? Local scope, where it stays private. Match the scope to the audience and the configuration stays coherent: shared things are shared, personal things stay personal, and the committed file honestly documents what the project depends on.

## Example

Adding the same kind of server at each scope:

```bash
# Project scope — the whole team needs this on this repo. Commit .mcp.json.
claude mcp add --scope project --transport http \
  team-api https://mcp.internal.example.com/mcp

# User scope — your personal docs server, available in every project.
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp

# Local scope — private to you on this repo; experimental, not shared.
claude mcp add --scope local scratch-db -- npx -y some-experimental-mcp
```

The resulting committed `.mcp.json` is what a teammate inherits on clone:

```json
{
  "mcpServers": {
    "team-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com/mcp"
    }
  }
}
```

Note what's *not* in it: your personal `context7` (user scope) and your experimental `scratch-db` (local scope) stay on your machine. The committed file carries only what the team genuinely shares — which is exactly what makes it trustworthy as a record of the project's external dependencies.
