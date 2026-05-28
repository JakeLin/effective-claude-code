# Choose the Right Claude Code Primitive

Claude Code gives you a ladder of mechanisms. The effective move is to use the lowest rung that solves the problem, then add bounds and verification when autonomy increases. This table is the fast path through that choice.

| Need | Reach for | Avoid |
|---|---|---|
| One-off direction in the current conversation | A prompt | Permanent config for temporary intent |
| Persistent project convention | `CLAUDE.md` | Repeating the same chat instruction every session |
| Path-specific convention | `.claude/rules/` | A global rule that only applies to one directory |
| Reusable knowledge or workflow | A skill | Long pasted prompts or a custom agent for one procedure |
| Harness-level operation | A slash command | Asking Claude to guess state the harness can measure |
| Hard guarantee before or after tool use | A hook or permission rule | "Please always..." instructions |
| Isolated research or planning | A subagent | Polluting the main context with side-quest output |
| External system access | An MCP server | Copy-pasting live system data into chat |
| Repeatable non-interactive work | Headless mode | An interactive session nobody is watching |
| Parallel work in one repository | Git worktrees | Multiple sessions fighting over one checkout |
| Many independent agents with coordination needs | An agent team | A team when one session plus subagents is enough |
| Recurring unattended work | A scheduled routine | Manual reminders or an immortal chat session |

The decision is not about which primitive is most powerful. It is about which property the step needs: memory, reuse, enforcement, isolation, external access, unattended execution, or coordination. When the primitive matches the property, the workflow stays small enough to understand and strong enough to trust.
