# Sample Permissions

Start narrow. Allow the safe commands Claude Code runs often, leave unusual actions to ask, and deny operations that should never happen in this repository.

```json
{
  "permissions": {
    "allow": [
      "Bash(git status*)",
      "Bash(pnpm test*)",
      "Bash(pnpm typecheck)",
      "Bash(pnpm lint*)"
    ],
    "deny": [
      "Bash(git push --force*)",
      "Bash(rm -rf*)",
      "Bash(dropdb*)"
    ]
  }
}
```

Review the allowlist after real usage. A good allowlist is boring: frequent, safe commands stop interrupting the session, while destructive or unusual commands still require deliberate attention.
