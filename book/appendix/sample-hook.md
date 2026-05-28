# Sample Hook

Use hooks for mechanical guarantees, not taste. This example blocks force-pushing from Claude Code.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git push --force*)",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-force-push.sh"
          }
        ]
      }
    ]
  }
}
```

```sh
#!/usr/bin/env sh
echo "Force-push is blocked in this repository." >&2
exit 2
```

Keep the matcher narrow. If the hook fires constantly but rarely acts, the matcher is carrying unnecessary latency.
