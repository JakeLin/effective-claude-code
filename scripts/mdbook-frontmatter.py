#!/usr/bin/env python3
import json
import sys
import codecs


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
        if "\\" in value:
            return codecs.decode(value, "unicode_escape")
        return value
    return value


def escape_markdown_text(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


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


def parse_scalar(lines, key):
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            return unquote(line[len(prefix) :])
    return ""


def split_frontmatter(content):
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None, content

    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            frontmatter = lines[1:index]
            body = "\n".join(lines[index + 1 :]).lstrip("\n")
            return frontmatter, body

    return None, content


def render_item(frontmatter, body):
    item = parse_scalar(frontmatter, "item")
    title = parse_scalar(frontmatter, "title")
    claude_code_version = parse_scalar(frontmatter, "claude_code_version")
    stability = parse_scalar(frontmatter, "stability")
    status = parse_scalar(frontmatter, "status")
    things_to_remember = parse_list(frontmatter, "things_to_remember")

    parts = []
    if item and title:
        parts.append(f"# Item {escape_markdown_text(item)}: {escape_markdown_text(title)}")
    elif title:
        parts.append(f"# {escape_markdown_text(title)}")

    metadata = []
    if claude_code_version:
        metadata.append(f"Verified with Claude Code {escape_markdown_text(claude_code_version)}")
    if stability:
        metadata.append(f"Stability: {escape_markdown_text(stability)}")
    if status:
        metadata.append(f"Status: {escape_markdown_text(status)}")

    if metadata:
        parts.append("> " + "  \n> ".join(metadata))

    parts.append(body)

    if things_to_remember:
        bullets = "\n".join(f"- {escape_markdown_text(item)}" for item in things_to_remember)
        parts.append(f"## Things to Remember\n\n{bullets}")

    return "\n\n".join(part for part in parts if part).rstrip() + "\n"


def process_chapter(chapter):
    frontmatter, body = split_frontmatter(chapter.get("content", ""))
    if frontmatter is not None:
        chapter["content"] = render_item(frontmatter, body)

    for section in chapter.get("sub_items", []):
        process_section(section)


def process_section(section):
    chapter = section.get("Chapter")
    if chapter:
        process_chapter(chapter)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        sys.exit(0)

    _, book = json.load(sys.stdin)
    for section in book.get("sections", book.get("items", [])):
        process_section(section)
    json.dump(book, sys.stdout)


if __name__ == "__main__":
    main()
