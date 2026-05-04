#!/usr/bin/env python3
"""Package the context-packet skill as a distributable .skill file."""

from __future__ import annotations

import fnmatch
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "context-packet" / "skills" / "context-packet"
DIST_DIR = ROOT / "dist"

EXCLUDE_DIRS = {"__pycache__", "node_modules"}
ROOT_EXCLUDE_DIRS = {"evals"}
EXCLUDE_FILES = {".DS_Store"}
EXCLUDE_GLOBS = {"*.pyc"}
ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def parse_frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")

    end = content.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter closing marker not found")

    frontmatter = content[4:end].splitlines()
    parsed: dict[str, str] = {}
    current_key: str | None = None
    block_indent: int | None = None
    block_lines: list[str] = []

    def flush_block() -> None:
        nonlocal current_key, block_indent, block_lines
        if current_key is not None and block_lines:
            parsed[current_key] = "\n".join(line[block_indent or 0 :] for line in block_lines).strip()
        current_key = None
        block_indent = None
        block_lines = []

    for line in frontmatter:
        if not line.strip():
            if current_key is not None:
                block_lines.append(line)
            continue

        key_match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if key_match and not line.startswith(" "):
            flush_block()
            key, value = key_match.groups()
            value = value or ""
            if value in {">", "|"}:
                current_key = key
                block_indent = None
                block_lines = []
            else:
                parsed[key] = value.strip().strip('"').strip("'")
            continue

        if current_key is not None:
            if block_indent is None and line.strip():
                block_indent = len(line) - len(line.lstrip(" "))
            block_lines.append(line)

    flush_block()
    return parsed


def validate_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"Missing {skill_md}")

    frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        raise ValueError(f"Unexpected SKILL.md frontmatter keys: {', '.join(sorted(unexpected))}")

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()
    compatibility = frontmatter.get("compatibility", "").strip()

    if not name:
        raise ValueError("SKILL.md frontmatter must include name")
    if not description:
        raise ValueError("SKILL.md frontmatter must include description")
    if name != skill_dir.name:
        raise ValueError(f"Skill name {name!r} must match folder name {skill_dir.name!r}")
    if not re.match(r"^[a-z0-9-]+$", name):
        raise ValueError("Skill name must be kebab-case lowercase letters, digits, and hyphens")
    if len(name) > 64:
        raise ValueError("Skill name must be 64 characters or fewer")
    if len(description) > 1024:
        raise ValueError("Skill description must be 1024 characters or fewer")
    if "<" in description or ">" in description:
        raise ValueError("Skill description cannot contain angle brackets")
    if compatibility and len(compatibility) > 500:
        raise ValueError("Compatibility must be 500 characters or fewer")


def should_exclude(rel_path: Path) -> bool:
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    if rel_path.name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(rel_path.name, pattern) for pattern in EXCLUDE_GLOBS)


def package_skill() -> Path:
    validate_skill(SKILL_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    output = DIST_DIR / "context-packet.skill"

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(SKILL_DIR.rglob("*")):
            if not file_path.is_file():
                continue
            archive_name = file_path.relative_to(SKILL_DIR.parent)
            if should_exclude(archive_name):
                continue
            archive.write(file_path, archive_name)

    return output


def main() -> int:
    try:
        output = package_skill()
    except ValueError as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1

    print(f"Packaged context-packet skill: {output}")
    print("Install or share this .skill artifact as the distributable skill package.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
