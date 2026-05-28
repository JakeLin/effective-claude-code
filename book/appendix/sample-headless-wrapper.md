# Sample Headless Wrapper

Use headless mode when no human will participate in the loop. Fence the run before it starts.

```sh
#!/usr/bin/env sh
set -eu

prompt_file="${1:?usage: ./run-claude-check.sh prompt.md}"

claude -p "$(cat "$prompt_file")" \
  --append-system-prompt "Return JSON with keys: summary, changed_files, checks_run, risks." \
  --max-turns 8 \
  --max-budget-usd 3 \
  --allowedTools "Read,Grep,Glob,Bash(pnpm test*),Bash(pnpm typecheck)" \
  --disallowedTools "Bash(git push*),Bash(rm -rf*)"
```

The wrapper should make three things explicit: what output the caller expects, what tools the run may use, and when the run must stop.
