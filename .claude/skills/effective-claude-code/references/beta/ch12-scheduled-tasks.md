# Claude Code Principles
<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->
<!-- Generated: 2026-05-30 | stable + beta; chapters 12 -->
<!-- Re-generate: python scripts/generate-rules.py --chapters 12 --include-beta --agent-steps -->

## Scheduled Tasks & Routines *(beta)*

### Reach for `/loop` to repeat work within a conversation — and know it pauses with Claude Code [#71]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- `/loop <interval> <prompt-or-command>` repeats work inside the current conversation — built in, no setup
- Loop tasks are conversation-bound: they pause when Claude Code closes and resume only if you resume that conversation before expiry
- Tasks auto-expire after three days; a forgotten loop does not run forever
- Manage tasks in natural language or through the underlying CronCreate, CronList, and CronDelete tools

**Agent steps:**
1. Schedule recurring in-session work with `/loop <interval> \"<prompt>\"` or `/loop <interval> /<command>`
2. Use it for things worth checking repeatedly while you work — deploy status, a watch-and-report, a periodic cleanup command
3. Remember the task pauses when Claude Code closes and only resumes if the same conversation is resumed before expiry; for durable work, use a routine instead (Item 73)
4. List and cancel scheduled tasks in natural language or with the cron tools rather than leaving stale loops running

### Match the scheduler to how long the work must outlive your conversation [#72]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- The schedulers differ by lifetime: `/loop` is conversation-bound, a routine is cloud-persistent, OS cron / CI is machine- or infra-bound
- Use `/loop` for work that only needs to run while you're in the conversation; it pauses when Claude Code closes
- Use a routine (or OS cron / GitHub Actions) for work that must run unattended, on a schedule, whether or not your machine is on
- The failure mode is mismatching: a conversation-bound loop pauses the moment you close Claude Code

**Agent steps:**
1. Before scheduling, ask how long the work must keep running: just this conversation, or independently of it?
2. For conversation-only cadence, use `/loop` (Item 71)
3. For work that must survive the conversation and run unattended, use a cloud routine (Item 73), OS cron, or GitHub Actions
4. Never rely on a conversation-bound loop for production or always-on automation

### Promote work that must run unattended to a routine [#73]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- Create persistent routines with `/schedule`; they run on managed cloud infrastructure whether or not your machine or session is running
- Routines can start from schedules, external webhooks, GitHub events, or email triggers
- They run with the integrations you explicitly connect, so a routine can act on real systems unattended
- Routines are plan- and platform-gated; confirm your account, platform, triggers, and limits before depending on them

**Agent steps:**
1. When work must run unattended and survive the conversation, create a routine with `/schedule` rather than stretching `/loop`
2. Pick the trigger that fits: a schedule for time-based work, a webhook for external systems, a GitHub trigger for repo events, or email for incoming messages
3. Connect only the integrations the routine needs, and scope those deliberately
4. Verify plan availability, platform support, triggers, and limits against current docs before depending on a routine

### Fence every recurring autonomous run — cost and risk repeat with each iteration [#74]
<!-- ecc-meta: target="conversation" action="suggest" check="always" -->
- A scheduled task multiplies the unattended-run risk by every iteration — cost, permissions, and mistakes all repeat on a timer
- Bound each run the way you'd bound any headless job (turn and budget limits, scoped tools) — then it's bounded per tick
- Give the task a clear exit or escalation condition so it doesn't run pointlessly or compound a failure forever
- Route each iteration's outcome through notification hooks so a silent loop doesn't drift unwatched

**Agent steps:**
1. Apply the headless guardrails (Item 60) to each scheduled run: turn limit, budget cap, and a scoped, pre-approved toolset
2. Define an exit or escalation condition so the task stops or pings you instead of looping uselessly or repeating a failure
3. Use the per-iteration hooks (UserPromptSubmit/Stop) to notify on meaningful results, not on every tick
4. Periodically review active scheduled tasks and routines, and cancel any that have outlived their purpose

