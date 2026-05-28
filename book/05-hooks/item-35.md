---
item: 35
theme: hooks
title: "Route notifications through hooks; stop watching the spinner"
tags: [hooks, notifications, async, observability]
claude_code_version: "2.1.153"
stability: stable
status: current
related_items: []
things_to_remember:
  - "Hooks turn lifecycle events into out-of-band signals — Slack pings, sounds, webhook calls — so you don't have to watch the terminal"
  - "Common patterns: `PermissionRequest` to Slack (Claude needs you), `SubagentStop`/`Stop` to a sound or webhook (work is done), `Notification` for harness alerts"
  - "Use `async: true` on notification hooks so they don't block Claude's loop"
  - "Scope what you get pinged about — getting paged on every event teaches you to ignore them"
agent_steps:
  - "When the user wants to be notified when Claude needs attention or finishes, set up a hook on `PermissionRequest`, `Stop`, or `SubagentStop` that posts to their notification channel"
  - "Use HTTP hook handlers for webhook destinations (Slack, Pushover, ntfy.sh) — these are first-class hook types"
  - "Set `async: true` on notification hooks so the Claude session doesn't wait for the network round-trip"
  - "Narrow the matcher or add a script-side filter so notifications only fire for events worth acting on"
---

## Why this matters

A long Claude session is unfriendly to attention. If the user has to watch the terminal to know when Claude needs a permission decision or when a long task finishes, they either babysit (wasteful) or wander off and come back to find the session has been waiting on them for fifteen minutes (also wasteful). Hooks solve this by turning lifecycle events into signals — out-of-band pings the user can receive without being at the keyboard. That's the original reason hooks exist: users were getting coffee while Claude waited on a permission prompt, and the feature was built to route those prompts somewhere the user would actually see them.

The high-leverage events for notifications are small and specific. `PermissionRequest` fires when Claude is asking for permission to run a tool — the right place to ping the user when their attention is needed. `Stop` and `SubagentStop` fire when work finishes — the right place to ping when the task is done. `Notification` covers harness-initiated alerts. For each, the hook payload includes enough context (tool name, agent name, reason) to compose a meaningful notification rather than a generic "Claude wants you."

The shape that works has three properties. First, `async: true` — the notification round-trip shouldn't block Claude's loop; the network call to Slack or Pushover happens in the background while the session continues. Second, the matcher (or a script-side filter) narrows what produces notifications — getting pinged for every `Read` tool call trains you to ignore the channel within an hour. Third, the message content is specific: "Claude is asking for `Bash(npm publish)` permission" is actionable; "Claude needs attention" is not. The HTTP hook type is built for exactly this — point it at a webhook URL, configure headers, and the harness handles the call.

The risk is over-notification. A hook on `PostToolUse` with no matcher will fire on every tool call and produce a useless firehose. A `Stop` hook pinging Slack on every turn will train the user to mute the channel. Notifications earn their keep when they fire only when something genuinely needs attention — escalate the signal-to-noise ratio carefully.

## What to avoid

Pinging on every event. Notifications without context — "Claude needs you" with no detail. Synchronous notification hooks that block Claude waiting on the webhook to respond. Spamming the same channel from many sessions without a way to tell them apart.

## What to do instead

Decide what events genuinely warrant interrupting the user: permission requests during long tasks, task completion when they're away, specific failure modes. Configure hooks on exactly those events with matchers narrowed to the cases that matter. Use the HTTP hook type pointing at a webhook (Slack incoming webhook, Pushover endpoint, ntfy.sh topic) — keep secrets in env vars allowed for the hook. Set `async: true`. Compose messages with enough context to be actionable.

## Example

Notify on permission requests so the user can approve from anywhere:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "https://hooks.slack.com/services/T.../B.../...",
            "headers": { "Content-Type": "application/json" },
            "async": true,
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

The harness POSTs the event JSON to the webhook; Slack receives the payload and posts a message. Because `async: true`, the Claude session continues while the round-trip happens in the background.

For a richer notification, use a `command` hook that composes the message:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/ping-on-done.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

```bash
#!/usr/bin/env bash
input=$(cat)
session_id=$(echo "$input" | jq -r '.session_id')
title=$(echo "$input" | jq -r '.session_title // "Claude session"')

curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg t "$title" --arg s "$session_id" \
        '{text: "✅ \($t) finished (session \($s))"}')" \
  >/dev/null
```

The user gets a clean Slack message when work completes — no spinner-watching, no return to find the terminal idle for an hour. The hook fires once per stop, sends one message, and the session continues. The point is that the user's attention is the bottleneck; hooks are how you stop spending it on watching the terminal.
