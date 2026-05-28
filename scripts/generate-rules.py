#!/usr/bin/env python3
"""
Generate a compact CLAUDE.md rule set from Effective Claude Code items.

Reads every item-NN.md file in book/, extracts things_to_remember (and
optionally agent_steps), and outputs a CLAUDE.md-ready rule set grouped
by chapter.

Usage:
  python scripts/generate-rules.py [OPTIONS]

Options:
  --chapters 1,2,3      Include only these chapter numbers (1-12)
  --themes memory,hooks  Include only these theme slugs
  --items 1,5,10-20     Include only these item numbers (ranges ok)
  --include-beta        Include beta/experimental items (default: stable only)
  --agent-steps         Include agent_steps sections after each item's rules
  --output FILE         Write to FILE instead of stdout

Examples:
  # Compact stable rules for any project
  python scripts/generate-rules.py > rules.md

  # Chapters 1-3 only (memory, commands, subagents)
  python scripts/generate-rules.py --chapters 1,2,3

  # Everything including beta, with agent steps
  python scripts/generate-rules.py --include-beta --agent-steps --output CLAUDE-rules.md

  # Pick specific items
  python scripts/generate-rules.py --items 1,5,15-21,29-35
"""

import argparse
import datetime
import os
import re
import sys

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "book")

CHAPTERS = {
    "01": ("Memory & CLAUDE.md", "memory"),
    "02": ("Commands", "commands"),
    "03": ("Subagents", "subagents"),
    "04": ("Skills", "skills"),
    "05": ("Hooks", "hooks"),
    "06": ("Settings & Permissions", "settings-permissions"),
    "07": ("MCP Servers", "mcp-servers"),
    "08": ("Orchestration & Workflows", "orchestration-workflows"),
    "09": ("CLI & Headless Mode", "cli-headless"),
    "10": ("Git Worktrees", "git-worktrees"),
    "11": ("Agent Teams", "agent-teams"),
    "12": ("Scheduled Tasks & Routines", "scheduled-tasks"),
}


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_scalar(lines, key):
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            return unquote(line[len(prefix):])
    return ""


def parse_list(lines, key):
    values = []
    in_key = False
    for line in lines:
        if line.startswith(f"{key}:"):
            in_key = True
            continue
        if in_key:
            if line and not line.startswith(" "):
                break
            stripped = line.strip()
            if stripped.startswith("- "):
                values.append(unquote(stripped[2:]))
    return values


def parse_ecc_meta(lines):
    """Parse the ecc_meta block into a dict with target, action, check keys."""
    result = {}
    in_block = False
    for line in lines:
        if line.startswith("ecc_meta:"):
            in_block = True
            continue
        if in_block:
            if line and not line.startswith(" "):
                break
            stripped = line.strip()
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                result[k.strip()] = unquote(v)
    return result


def split_frontmatter(content):
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None, content
    for i, line in enumerate(lines[1:], start=1):
        if line == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    return None, content


def parse_item_range(spec):
    """Parse '1,5,10-20' into a set of ints."""
    result = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            result.update(range(int(lo), int(hi) + 1))
        else:
            result.add(int(part))
    return result


def collect_items(include_beta, chapter_filter, theme_filter, item_filter):
    """Yield dicts for each matching item, in chapter/item order."""
    book_dir = os.path.realpath(BOOK_DIR)
    if not os.path.isdir(book_dir):
        sys.exit(f"error: book dir not found: {book_dir}")

    for ch_num, (ch_title, ch_theme) in sorted(CHAPTERS.items()):
        # Chapter filter
        if chapter_filter and int(ch_num) not in chapter_filter:
            continue
        if theme_filter and ch_theme not in theme_filter:
            continue

        ch_dir = None
        for entry in os.listdir(book_dir):
            if entry.startswith(ch_num + "-") and os.path.isdir(os.path.join(book_dir, entry)):
                ch_dir = os.path.join(book_dir, entry)
                break
        if not ch_dir:
            continue

        item_files = sorted(
            f for f in os.listdir(ch_dir)
            if re.match(r"item-\d+\.md$", f)
        )

        chapter_items = []
        for fname in item_files:
            path = os.path.join(ch_dir, fname)
            with open(path, encoding="utf-8") as fh:
                content = fh.read()

            fm, _ = split_frontmatter(content)
            if fm is None:
                continue

            item_num = int(parse_scalar(fm, "item") or "0")
            stability = parse_scalar(fm, "stability")
            is_beta = stability.lower() == "beta"

            if not include_beta and is_beta:
                continue
            if item_filter and item_num not in item_filter:
                continue

            chapter_items.append({
                "num": item_num,
                "title": parse_scalar(fm, "title"),
                "stability": stability,
                "things": parse_list(fm, "things_to_remember"),
                "steps": parse_list(fm, "agent_steps"),
                "ecc_meta": parse_ecc_meta(fm),
                "chapter_num": int(ch_num),
                "chapter_title": ch_title,
                "chapter_theme": ch_theme,
            })

        if chapter_items:
            yield from chapter_items


def render(items, with_steps, args_summary):
    today = datetime.date.today().isoformat()
    lines = [
        "# Claude Code Principles",
        f"<!-- From: Effective Claude Code (https://github.com/JakeLin/effective-claude-code) -->",
        f"<!-- Generated: {today} | {args_summary} -->",
        f"<!-- Re-generate: python scripts/generate-rules.py {sys.argv[1:] and ' '.join(sys.argv[1:]) or ''} -->",
        "",
    ]

    current_chapter = None
    for item in items:
        if item["chapter_title"] != current_chapter:
            current_chapter = item["chapter_title"]
            beta_note = " *(beta)*" if item["stability"] == "beta" else ""
            lines.append(f"## {current_chapter}{beta_note}")
            lines.append("")

        badge = f"[#{item['num']}]"
        lines.append(f"### {item['title']} {badge}")
        meta = item.get("ecc_meta", {})
        if meta.get("target") and meta.get("action"):
            parts = [f'target="{meta["target"]}"', f'action="{meta["action"]}"']
            if meta.get("check"):
                parts.append(f'check="{meta["check"]}"')
            lines.append(f"<!-- ecc-meta: {' '.join(parts)} -->")
        for rule in item["things"]:
            lines.append(f"- {rule}")

        if with_steps and item["steps"]:
            lines.append("")
            lines.append("**Agent steps:**")
            for i, step in enumerate(item["steps"], 1):
                lines.append(f"{i}. {step}")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a CLAUDE.md rule set from Effective Claude Code items.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--chapters", help="Chapter numbers to include (e.g. 1,2,3)")
    parser.add_argument("--themes", help="Theme slugs to include (e.g. memory,hooks)")
    parser.add_argument("--items", help="Item numbers to include (e.g. 1,5,10-20)")
    parser.add_argument("--include-beta", action="store_true", help="Include beta items")
    parser.add_argument("--agent-steps", action="store_true", help="Include agent_steps sections")
    parser.add_argument("--output", metavar="FILE", help="Write to FILE instead of stdout")
    args = parser.parse_args()

    chapter_filter = set(int(n) for n in args.chapters.split(",")) if args.chapters else None
    theme_filter = set(t.strip() for t in args.themes.split(",")) if args.themes else None
    item_filter = parse_item_range(args.items) if args.items else None

    parts = []
    if args.include_beta:
        parts.append("stable + beta")
    else:
        parts.append("stable only")
    if chapter_filter:
        parts.append(f"chapters {args.chapters}")
    if theme_filter:
        parts.append(f"themes {args.themes}")
    if item_filter:
        parts.append(f"items {args.items}")
    args_summary = "; ".join(parts)

    items = list(collect_items(args.include_beta, chapter_filter, theme_filter, item_filter))
    if not items:
        sys.exit("error: no items matched the given filters")

    output = render(items, args.agent_steps, args_summary)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output + "\n")
        print(f"Wrote {len(items)} items to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
