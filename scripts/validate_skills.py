#!/usr/bin/env python3
# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""Validate Cisco Agent Skills and marketplace packaging with stdlib only."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_RE = re.compile(r"^(name|description|license):\s*(.*)$")
SECRET_PATTERNS = (
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "literal password",
        re.compile(r"""(?i)\bpassword\s*[:=]\s*["'][^"'${}<]{8,}["']"""),
    ),
)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        errors.append(f"{path.relative_to(ROOT)}: malformed YAML frontmatter")
        return {}

    fields: dict[str, str] = {}
    active_field: str | None = None
    for line in block.splitlines():
        match = FIELD_RE.match(line)
        if match:
            active_field = match.group(1)
            value = match.group(2).strip().strip("\"'")
            fields[active_field] = "" if value in {">", "|"} else value
        elif active_field == "description" and line.startswith((" ", "\t")):
            value = line.strip()
            if value and not re.match(r"^[a-z0-9_-]+:", value):
                fields["description"] = (
                    f"{fields['description']} {value}".strip()
                )
    return fields


def validate_skill(path: Path, errors: list[str], warnings: list[str]) -> str | None:
    relative = path.relative_to(ROOT)
    folder_name = path.parent.name
    fields = parse_frontmatter(path, errors)
    name = fields.get("name")
    description = fields.get("description", "").strip()

    if not name:
        errors.append(f"{relative}: missing frontmatter name")
    elif name != folder_name:
        errors.append(f"{relative}: name '{name}' does not match '{folder_name}'")
    elif len(name) > 64 or not NAME_RE.fullmatch(name):
        errors.append(f"{relative}: name must be kebab-case and at most 64 characters")

    if not description:
        errors.append(f"{relative}: missing frontmatter description")
    elif len(description) > 1024:
        errors.append(f"{relative}: description exceeds 1024 characters")

    if not fields.get("license"):
        warnings.append(f"{relative}: no license field; verify SOURCES.md covers it")

    text = path.read_text(encoding="utf-8")
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{relative}: possible hardcoded {label}")
    return name


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    canonical = sorted((ROOT / "skills").glob("*/*/SKILL.md"))
    packaged = sorted((ROOT / "plugins").glob("*/skills/*/SKILL.md"))

    if not canonical:
        errors.append("No canonical skills found under skills/<product>/<skill>/SKILL.md")

    seen: dict[str, Path] = {}
    for path in canonical:
        name = validate_skill(path, errors, warnings)
        if name and name in seen:
            errors.append(
                f"{path.relative_to(ROOT)}: duplicate name also used by "
                f"{seen[name].relative_to(ROOT)}"
            )
        elif name:
            seen[name] = path

        product = path.parent.parent.name
        mirror = ROOT / "plugins" / product / "skills" / path.parent.name / "SKILL.md"
        if not mirror.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing plugin mirror {mirror.relative_to(ROOT)}")
        elif path.read_bytes() != mirror.read_bytes():
            errors.append(f"{path.relative_to(ROOT)}: plugin mirror differs")

    canonical_paths = {
        (path.parent.parent.name, path.parent.name) for path in canonical
    }
    for path in packaged:
        key = (path.parent.parent.parent.name, path.parent.name)
        if key not in canonical_paths:
            errors.append(f"{path.relative_to(ROOT)}: missing canonical copy")

    claude = load_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    agents = load_json(ROOT / ".agents" / "plugins" / "marketplace.json", errors)
    for label, manifest in (("Claude", claude), ("Agents", agents)):
        if not isinstance(manifest, dict) or not isinstance(manifest.get("plugins"), list):
            errors.append(f"{label} marketplace: missing plugins array")
            continue
        for plugin in manifest["plugins"]:
            if not isinstance(plugin, dict) or not NAME_RE.fullmatch(str(plugin.get("name", ""))):
                errors.append(f"{label} marketplace: invalid plugin name")

    for path in sorted((ROOT / "plugins").glob("*/.claude-plugin/plugin.json")):
        manifest = load_json(path, errors)
        expected_name = path.parent.parent.name
        if isinstance(manifest, dict) and manifest.get("name") != expected_name:
            errors.append(
                f"{path.relative_to(ROOT)}: plugin name must be '{expected_name}'"
            )

    print(f"Validated {len(canonical)} canonical and {len(packaged)} packaged skills.")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        print("Validation failed.")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
