---
item: 58
theme: cli-headless
title: "Treat `claude -p` as a Unix utility — pipe in, parse out, compose"
tags: [headless, unix, pipeline, composition, exit-codes]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [57, 59]
things_to_remember:
  - "`claude -p` reads stdin and writes stdout, so it composes with other tools in a pipeline like any Unix command"
  - "Pipe data in (`cat file | claude -p ...`) and pipe results onward (`| jq`, `> out.txt`) — no copy-paste, no TUI scraping"
  - "Use the exit code: a headless run can signal pass/fail so a script or CI step can branch on it"
  - "Keep each invocation focused on one transformation; chain small steps rather than one do-everything prompt"
agent_steps:
  - "Feed input via stdin (`cat data | claude -p \"...\"`) rather than embedding large content in the prompt string"
  - "Pipe the output to the next tool (`| jq`, `| tee`, `> file`) so Claude is one stage in a pipeline"
  - "Have the run signal success/failure through its exit code so callers can branch (`if claude -p ...; then`)"
  - "Compose several small, single-purpose invocations instead of one monolithic prompt when steps are distinct"
---

## Why this matters

Once you see headless Claude as a program (the previous Item), the Unix philosophy applies directly: a good command-line tool reads from standard input, writes to standard output, signals status through its exit code, and composes with other tools. `claude -p` does all of these. You pipe data into it — `cat build.log | claude -p "summarize the failure"` — and it writes its answer to stdout, which you can pipe onward to `jq`, `tee`, a file, or another command. There's no copy-paste, no scraping a terminal UI, no special integration layer. It slots into the same pipelines as `grep`, `sort`, and `curl`, because it speaks the same interface they do.

This matters because composability is leverage. The reason Unix tools are powerful isn't that any one of them does much; it's that they combine, and each new tool multiplies with every existing one. A headless Claude that reads stdin and writes stdout inherits that entire ecosystem for free. You can put it downstream of anything that produces text and upstream of anything that consumes it. Feeding input through stdin rather than stuffing it into the prompt string also keeps the invocation clean and sidesteps shell-quoting pain with large or special-character content — the file's bytes flow in directly, untouched by the shell.

The exit code is the part people forget, and it's what turns Claude from a text generator into a *decision* in a script. A headless run can be asked to exit non-zero when it finds a problem, and then a CI step or shell script can branch on the result: `if claude -p "any critical security issues in this diff?"; then block; fi`. That makes Claude a gate, not just a commentator. And the same Unix instinct says to keep each invocation doing *one* transformation — a small, single-purpose step you can compose — rather than one monolithic prompt that tries to do everything. Small composable steps are easier to test, debug, and recombine, exactly as with any pipeline of well-behaved tools.

## What to avoid

Embedding large file contents directly in the prompt string (and fighting shell quoting) when piping via stdin is cleaner. Scraping the interactive TUI or parsing log output to get a result that stdout would hand you directly. Ignoring the exit code, so a script can't tell whether the headless run found a problem or not. Cramming an entire multi-stage job into one giant prompt when it's really several distinct transformations that would compose better as separate, piped invocations.

## What to do instead

Use the standard streams. Pipe input in through stdin instead of embedding it in the prompt, and pipe output onward to the next tool — `jq`, `tee`, a redirect — so Claude is one well-behaved stage among many. Have the run communicate pass/fail through its exit code so callers can branch on it. And decompose multi-step jobs into small, single-purpose invocations you chain together, rather than one do-everything prompt, so each piece stays testable and recomposable.

## Example

Claude as a stage in real pipelines:

```bash
# stdin in, stdout onward — no copy-paste, no quoting pain
git diff --staged | claude -p "describe this change in one line" | tee msg.txt

# exit code as a gate in a script
if ! git diff --staged | claude -p "reply OK only if no secrets are present; else exit 1"; then
  echo "blocked: possible secret in staged changes" >&2
  exit 1
fi

# composed small steps, each doing one thing
cat errors.log \
  | claude -p "extract just the stack traces" \
  | claude -p "group these by root cause" \
  > triage.txt
```

Each invocation reads stdin, writes stdout, and (in the gate case) returns a meaningful exit code — so it drops into the toolbox alongside every other Unix command. The last example is the philosophy in miniature: two focused transformations chained, not one prompt asked to "read the log, extract traces, and group them," because small composable steps are what make a pipeline robust. Treat `claude -p` like `grep` with judgment, and it composes like `grep` does.
