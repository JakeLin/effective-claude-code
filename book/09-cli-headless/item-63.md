---
item: 63
theme: cli-headless
title: "Graduate to the Agent SDK when the script becomes a product"
tags: [headless, sdk, automation, production]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [57, 60]
things_to_remember:
  - "The Agent SDK (TypeScript and Python) is the same harness as the CLI, exposed programmatically via a `query()` primitive"
  - "Shelling out to `claude -p` is right for scripts and glue; the SDK is right when automation becomes an application"
  - "The SDK gives you typed message streams, programmatic hooks, permission callbacks, and real error handling — things shell parsing fakes badly"
  - "Don't reach for the SDK prematurely — a shell pipeline is simpler until you need the control the SDK provides"
agent_steps:
  - "Use `claude -p` for one-off automation, glue scripts, CI steps, and pipelines"
  - "Move to the Agent SDK (`@anthropic-ai/claude-agent-sdk` or `claude-agent-sdk`) when building an application that embeds Claude as a component"
  - "Choose the SDK when you need to iterate over message events, handle permissions in code, register hooks programmatically, or do structured error handling and retries"
  - "Stay with the CLI when a shell pipeline already does the job cleanly — adopt the SDK for control, not by default"
---

## Why this matters

Headless `claude -p` and the Agent SDK run the *same harness* — the same context assembly, tool loop, subagents, hooks, and permissions. The difference is the interface: the CLI is a command you shell out to and parse, while the SDK exposes that harness programmatically through a `query()` primitive (in both TypeScript, `@anthropic-ai/claude-agent-sdk`, and Python, `claude-agent-sdk`). Because the engine is identical, choosing between them isn't about capability — it's about whether you're writing a *script* that calls Claude or an *application* that embeds it.

For scripts, glue, CI steps, and pipelines, the CLI is what fits, and this whole chapter applies. Shelling out is simple, composable, and language-agnostic; a `claude -p` in a bash script or a Makefile is exactly enough. The SDK starts to pay off when the automation grows into something with a lifecycle of its own — a service, an internal tool, a product feature — where you're no longer just capturing stdout but reacting to what happens *during* the run. At that point the seams of shelling out start to show: you find yourself parsing JSON to reconstruct state the SDK would hand you as typed objects, or wishing you could make a decision mid-run that the command line can't express.

Concretely, the SDK gives you what shell parsing can only fake. You iterate over a stream of typed message events as they happen, rather than waiting for a final blob and dissecting it. You handle permission requests with a callback in code — real logic, not a pre-set flag. You register hooks programmatically and wire them to your application's own state. And you get genuine error handling: structured exceptions, retries, fallbacks, integrated with the rest of your system. Those capabilities are the signal to graduate. The caution is the mirror image: don't reach for the SDK *prematurely*. If a shell pipeline already does the job cleanly, the SDK is added complexity for control you don't need yet. Adopt it when the script has become a product — not before, and not never.

## What to avoid

Building an entire application around scraping `claude -p` output — reconstructing state from JSON, faking mid-run control with clever flags — when the SDK exposes all of it natively. Conversely, pulling in the SDK and a build toolchain for what is really a three-line shell script. Assuming the SDK is more *capable* than the CLI and reaching for it to unlock features — it's the same harness, so the choice is about interface, not power. Staying on brittle shell glue long after the automation has clearly become a product that needs real error handling.

## What to do instead

Match the interface to what you're building. Use `claude -p` for one-off automation, glue, CI steps, and pipelines — the simple, composable default. Move to the Agent SDK when you're building an application that embeds Claude as a component and you need its programmatic control: iterating over typed message events, handling permissions in code, registering hooks programmatically, structured error handling and retries. Let the need for that control — not habit or assumed capability — be the trigger, and stay on the CLI as long as a shell pipeline does the job cleanly.

## Example

The CLI — right for a script:

```bash
# A CI step. Shelling out is exactly enough.
git diff origin/main... | claude -p "review for regressions; exit 1 on any blocker" \
  --max-turns 20 --max-budget-usd 1.00
```

The SDK — right when it's an application embedding Claude:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const msg of query({
  prompt: "triage this incoming issue and label it",
  options: {
    canUseTool: async (tool, input) => approvals.decide(tool, input), // permission logic in code
    hooks: { PreToolUse: [auditEveryToolCall] },                      // wired to app state
  },
})) {
  if (msg.type === "tool_use") dashboard.record(msg);                 // react mid-run
  if (msg.type === "result")   store.save(msg.result, msg.total_cost_usd);
}
```

The bash version captures a final result and an exit code — all a CI gate needs. The SDK version reacts to events *as they happen*, decides permissions with real logic, and integrates with the application's own state and storage — things you'd be faking badly by parsing CLI output. Same harness underneath; the SDK is simply the interface you graduate to when the automation has become a product. Until then, the shell pipeline wins on simplicity, and simplicity is the right default.
