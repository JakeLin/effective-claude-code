---
item: 59
theme: cli-headless
title: "Ask for structured output when a program reads the result"
tags: [headless, json, structured-output, parsing, observability]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [58, 61]
things_to_remember:
  - "Use `--output-format json` when a program consumes the result — you get a stable envelope with the result, session id, and cost, not prose to scrape"
  - "Use `--json-schema` when you need the model's answer itself to be validated structured data, not just wrapped in metadata"
  - "Parse fields (`jq -r '.result'`, `.session_id`, `.total_cost_usd`) instead of regex-ing free text"
  - "Plain text output is for humans and simple pipes; structured output is for machines that branch on the result"
agent_steps:
  - "When a script will parse the result, pass `--output-format json` and read fields with `jq` rather than scraping text"
  - "Capture `.session_id` from the JSON envelope to chain follow-up turns, and `.total_cost_usd` for cost tracking"
  - "When the answer must be machine-validated structured data, pass `--json-schema` so output conforms to your schema"
  - "Reserve default text output for human-read results and simple file/pipe redirection"
---

## Why this matters

The previous Item put Claude in a pipeline; this one is about making its output safe for a *program* to consume. Default output is prose — fine when a human reads it or when you're piping to a file, but treacherous when a script has to extract a decision from it. Prose varies: the same answer might come back as "Yes, there's a bug" one run and "I found an issue" the next, and any regex you write to parse it is a guess that breaks the first time the phrasing shifts. The moment a program branches on Claude's output, you want a contract, not a paragraph.

`--output-format json` provides that contract. Instead of prose, you get a stable envelope: the `result` field carries Claude's answer, alongside metadata the run produced — `session_id` for chaining the next turn, `total_cost_usd` and token counts for tracking spend, `num_turns`, and more. A script reads exactly the field it needs with `jq -r '.result'` and never touches the rest. The structure is stable across runs even as the wording inside `result` varies, so the parsing logic stays correct. This is also where headless observability comes from: cost and usage are right there in the envelope, no dashboard lookup required, which makes per-invocation budgeting and logging trivial.

There's a second, stronger level. Sometimes it's not enough for the *envelope* to be structured — you need the model's actual answer to be machine-validated data, like a classification, a list of extracted fields, or a triage verdict with a fixed shape. `--json-schema` enforces exactly that: you supply a JSON Schema and the output is validated against it, so a downstream program can rely on the answer having the fields and types it expects, not just being wrapped in JSON. The rule of thumb across both levels is about the consumer: text for humans and simple redirection, the JSON envelope when a program needs the result plus metadata, and a JSON schema when the answer itself must be structured data the program can trust without defensive parsing.

## What to avoid

Scraping prose with regexes to pull a yes/no or a value out of default text output — it works until the phrasing changes, then fails silently. Discarding the JSON envelope's metadata and re-deriving cost or session continuity some harder way. Asking for free text and then writing brittle string-matching to impose structure after the fact, when `--json-schema` would have guaranteed it. Using JSON output for results a human simply reads, adding parsing ceremony for no consumer.

## What to do instead

Match the output format to who reads it. When a program will branch on the result, use `--output-format json` and read the fields you need with `jq` — `.result` for the answer, `.session_id` to chain, `.total_cost_usd` for spend tracking. When the answer itself must be structured, pass `--json-schema` so it's validated against your shape and downstream code can trust it. Keep plain text for human-read output and simple file or pipe redirection, where structure would just be overhead.

## Example

Scraping prose (fragile) versus reading a field (stable):

```bash
# Fragile — breaks when the wording changes
claude -p "is the build broken?" | grep -qi "yes" && echo broken

# Stable — branch on a parsed field
verdict=$(claude -p "is the build broken? answer yes or no" \
            --output-format json | jq -r '.result')
```

Using the envelope's metadata — chain the session and track cost in one read:

```bash
out=$(claude -p "start the migration plan" --output-format json)
sid=$(echo "$out"  | jq -r '.session_id')
cost=$(echo "$out" | jq -r '.total_cost_usd')
echo "spent \$$cost so far"
claude -p "now execute phase 1" --resume "$sid"
```

When the answer itself must be structured data a program can rely on:

```bash
claude -p "classify this ticket" \
  --json-schema '{"type":"object","properties":{
      "severity":{"enum":["low","medium","high"]},
      "team":{"type":"string"}},
      "required":["severity","team"]}'
```

The downstream code can read `.severity` and `.team` without defensive parsing, because the schema guaranteed they're there. In every case the principle is the same: the format follows the consumer — a human gets prose, a program gets a contract.
