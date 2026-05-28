---
paths:
  - "book/**"
---

# Writing rules for Items

Loaded only when Claude touches files under `book/`. The canonical schema lives in `book/_item-template.md` — copy that file to start a new Item. This file explains the field semantics, prose structure, and theme-level workflow.

## Item count per theme

Variable per theme based on available material. Target ~5–6 Items per theme on average (medium density). Let the topic dictate depth — do not pad thin themes or truncate rich ones.

## Frontmatter field semantics

- `item`: Global integer, unique across all themes. Stable forever — never renumbered, retired numbers never reused.
- `title`: Imperative or principle statement — the advice in one line. A reader scanning titles alone should learn something.
- `claude_code_version`: Version when the Item was **last verified** to still be accurate. Update lazily when you re-verify; the real staleness signal is `status: needs-review`.
- `status`: Set to `needs-review` when a Claude Code release may have changed the specifics.
- `things_to_remember`: 2–4 bullets. The first bullet is the one-line takeaway an agent extracts. This field is the **single source of truth** — rendered onto the page by the mdBook build, not duplicated in the body.
- `agent_steps`: Concrete, ordered, executable steps — written so Claude can follow them without reading the prose.

## Item body structure

After the frontmatter, every Item follows: `## Why this matters` → `## What to avoid` → `## What to do instead` → `## Example`. The "Things to Remember" list comes from the `things_to_remember` frontmatter field and is rendered onto the page by the mdBook build — do not write it into the body.

**Length:** 1–2 rendered pages. Long enough to explain the *why*, short enough to read in 3 minutes.

## Writing principles

- **Prose is principle-based, not syntax-based.** The *why* is durable; specific field names and file paths go in examples only. When Claude Code changes a field name, update one code block, not the whole Item.
- **Title is the advice.** A reader scanning titles alone should learn something.
- **No comments in code examples** unless the why is non-obvious.
- **agent_steps are imperative and concrete.** They should work without reading the prose.
- **`things_to_remember` lives only in frontmatter.** Do not transcribe it into the body.

## Staleness handling

- Write prose as durable principles (rarely needs updating).
- Code examples and frontmatter samples carry `claude_code_version`.
- Set `status: needs-review` on Items when a Claude Code release changes their specifics.
- Beta-theme chapters (10–12) carry an explicit "subject to change" note at the chapter intro.

## Contribution model

- Author writes initial Items for each theme.
- Community submits corrections and new Items via PR.
- New Items start by copying `book/_item-template.md`.
- Each PR must follow the frontmatter schema, match the body structure, include a real `claude_code_version`, and pass a review for principle-level writing (not just syntax documentation).

## Per-theme building workflow

Repeat for each of the 12 chapters in order:

1. **Research**: Delegate to the `Explore` subagent rather than reading inline — the raw doc/reference dump belongs in the child, not the main thread (see Item 15). Ask the agent to read the relevant files in `references/claude-code-best-practice/` AND fetch the official docs page for the theme from `https://code.claude.com/docs`, and return under ~400 words covering: frontmatter fields and behavior, anti-patterns called out in the sources, and any version-specific notes worth flagging.
2. **Propose titles**: Draft 5–7 candidate Item titles. Present them to the user for approval, cuts, reordering, or additions.
3. **Calibrate (chapter 1 only)**: Write the intro `README.md` + the first `item-NN.md` in full and wait for user review on voice, structure, and length. From chapter 2 onward, the title-approval gate in step 2 is the only checkpoint — proceed straight to bulk writing unless a deliberate style shift is needed.
4. **Bulk write**: Write all remaining Items for the theme in one pass.
5. **Commit**: One commit per completed theme. Message names the chapter and lists Item titles.

## Cross-references

Write `related_items` opportunistically as you go — at the time of writing chapter N, link backward to any relevant Items in chapters 1..N-1. After all 12 themes are complete, do a single **forward-link** pass to add references that point from earlier Items to later ones.

## Chapter folder structure

Each `book/NN-theme/` folder contains:
- `README.md` — chapter intro: what the feature is (beginner-friendly, ~150 words), why it matters, how Items build on each other. Beta chapters (10–12) include an explicit "subject to change" note.
- `item-NN.md` — one file per Item, global item numbering across the whole book.
