---
item: 53
theme: orchestration-workflows
title: "Close every workflow with a verification loop Claude runs itself"
tags: [verification, testing, iteration, quality]
claude_code_version: "2.1.150"
stability: stable
status: current
related_items: [32, 50, 54]
things_to_remember:
  - "The iteration loop — generate, verify, fix — is what separates plausible output from working output"
  - "Give Claude a way to check its own work: run the tests, type-check, take a screenshot, hit the endpoint"
  - "Verification only counts if Claude actually observes the result and acts on it — 'I added a test' is not 'the test passed'"
  - "A failing check Claude can see and re-run is worth more than any amount of careful prose about correctness"
agent_steps:
  - "After implementing, have Claude run the relevant verification — test suite, type-checker, linter, build, or a live check — and read the output"
  - "Loop on failures: Claude fixes, re-runs, and repeats until the check actually passes, rather than declaring done after the edit"
  - "For UI or runtime behavior, verify by observation (screenshot, endpoint response, log) not by inspection of the code alone"
  - "Make the verification command explicit and runnable so Claude can close the loop without asking how to check"
---

## Why this matters

A model is very good at producing code that *looks* correct and only sometimes good at producing code that *is* correct, and from the inside those two are indistinguishable — the plausible-but-wrong version reads exactly as confidently as the right one. What collapses the difference is the iteration loop: generate, verify, fix, repeat. Output quality on real work is a function of that loop as much as of the model; without it you get a first draft, and a first draft of code is a hypothesis, not a result. The single most reliable upgrade to any Claude Code workflow is to end it with a check Claude runs and observes for itself.

The reason self-verification beats careful review is that it grounds the work in something external to the model's own judgment. Tests, type-checkers, linters, builds, a live HTTP response, a screenshot of the rendered page — these report facts the model can't talk itself out of. When Claude runs the suite and sees a red failure, that failure is real in a way that no amount of "this should work" prose is, and it gives the loop something concrete to close against. The verification has to be *observed*, though: the failure mode to watch for is Claude declaring victory after writing a test without running it, or after an edit without rebuilding. "I added a test" is a claim; "the test passed, here's the output" is evidence. Only the second one closes the loop.

This also pairs with the planning Item at the front of the chapter: a phased plan gives you natural verification points — a check at the end of each phase rather than only at the very end, so a regression is caught while the cause is still fresh. And it pairs with hooks (Chapter 5): a `Stop` hook that blocks until the tests pass turns "please verify" from a request the model might skip into a guarantee the harness enforces. The principle is constant across all of these: don't trust generated code until something other than the generator has confirmed it works, and make sure Claude actually watched that confirmation happen.

## What to avoid

Accepting code as done because it looks right, with no execution behind the claim. Letting Claude report "added tests" or "fixed the bug" without running anything to confirm it. Verifying UI or runtime behavior by reading the source instead of observing the actual output. Ending a long, multi-phase implementation with a single check at the very end, so a phase-two regression only surfaces after phase four is built on top of it.

## What to do instead

End every implementation with a verification Claude executes and reads — the test suite, the type-checker, the linter, the build, or a live check against the running thing. Loop on failure: fix, re-run, repeat until the check genuinely passes, rather than stopping at the edit. For anything visual or runtime, verify by observation — a screenshot, an endpoint response, a log line — not by inspecting code. Make the check explicit and runnable so closing the loop is frictionless, and put checks at phase boundaries on larger work so regressions surface early. Where the guarantee must hold, enforce it with a `Stop` hook.

## Example

The loop, closed against a real signal:

```text
1. Claude implements the rate limiter.
2. Claude runs:  npm test -- limiter
   Output:       1 failing — "allows 11th request in the same window"
3. Claude reads the failure, sees an off-by-one in the window reset,
   fixes it.
4. Claude re-runs:  npm test -- limiter
   Output:          all passing
5. Only now: "Done — limiter implemented, 8 tests passing."
```

Step 2's red result is the whole value: the first draft was plausible and wrong, and the test said so. Contrast the open loop — "I've implemented the limiter and added tests for it" with nothing run — which sounds identical to step 5 but rests on a hypothesis no one checked. For behavior you can't unit-test, swap the signal but keep the shape:

```text
UI change → take a screenshot, look at it, compare to intent
API change → curl the endpoint, read the actual response
Build concern → run the build, read the output
```

In every case Claude does the observing and acts on what it sees. That observe-and-act step is the difference between code that looks done and code that is.
