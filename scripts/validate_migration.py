#!/usr/bin/env python3
"""Supplemental validation for the 167-skill CiscoDevNet migration."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MIGRATION_MANIFEST.json"
EXPECTED_NAMESPACES = {
    "splunk-platform": 87,
    "splunk-observability-cloud": 36,
    "splunk-enterprise-security": 18,
    "appdynamics": 20,
    "thousandeyes": 3,
    "splunk-itsi": 2,
    "isovalent": 1,
}
COMPATIBILITY = "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_under(path: Path) -> set[str]:
    return {str(item.relative_to(path)) for item in path.rglob("*") if item.is_file()}


def frontmatter(text: str) -> str:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return ""
    return text.split("---\n", 2)[1]


def check_local_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for target in re.findall(r"\]\(([^)\s]+)", text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0].strip("<>")
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: dangling local link {target}")


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = manifest.get("records", [])
    if len(records) != 167:
        errors.append(f"manifest contains {len(records)} records, expected 167")
    counts: dict[str, int] = {}
    names: set[str] = set()
    for record in records:
        name = record["name"]
        product = record["namespace"]
        names.add(name)
        counts[product] = counts.get(product, 0) + 1
        canonical_dir = ROOT / "skills" / product / name
        mirror_dir = ROOT / "plugins" / product / "skills" / name
        if not (canonical_dir / "SKILL.md").exists():
            errors.append(f"missing canonical SKILL.md: {canonical_dir.relative_to(ROOT)}")
            continue
        if not (mirror_dir / "SKILL.md").exists():
            errors.append(f"missing plugin mirror: {mirror_dir.relative_to(ROOT)}")
        canonical_files = files_under(canonical_dir)
        mirror_files = files_under(mirror_dir)
        if canonical_files != mirror_files:
            errors.append(f"mirror file set differs for {product}/{name}")
        for relative in sorted(canonical_files & mirror_files):
            if (canonical_dir / relative).read_bytes() != (mirror_dir / relative).read_bytes():
                errors.append(f"mirror bytes differ for {product}/{name}/{relative}")
        for skill_file in sorted(canonical_dir.rglob("SKILL.md")):
            block = frontmatter(skill_file.read_text(encoding="utf-8"))
            required = {
                f"name: {name}",
                "license: Apache-2.0",
                f"compatibility: \"{COMPATIBILITY}\"",
                f"  product: {product}",
                "  maturity: draft",
            }
            for value in required:
                if value not in block:
                    errors.append(f"{skill_file.relative_to(ROOT)}: missing frontmatter {value}")
            description_match = re.search(r"^description:\s*>\n((?:\s+.*\n?)+)", block, re.MULTILINE)
            if not description_match or len(" ".join(description_match.group(1).split())) > 1024:
                errors.append(f"{skill_file.relative_to(ROOT)}: invalid description")
            if "## Portability note" not in skill_file.read_text(encoding="utf-8"):
                errors.append(f"{skill_file.relative_to(ROOT)}: missing portability note")
            check_local_links(skill_file, errors)
        for item in canonical_dir.rglob("*"):
            if item.is_file() and item.suffix.lower() in {".md", ".markdown"}:
                text = item.read_text(encoding="utf-8", errors="ignore")
                if len(text.splitlines()) > 100 and item.name != "SKILL.md" and "table of contents" not in text.lower() and "## contents" not in text.lower():
                    errors.append(f"{item.relative_to(ROOT)}: long reference lacks table of contents")
                check_local_links(item, errors)
        if list(canonical_dir.rglob("agents/openai.yaml")) or list(canonical_dir.rglob("scripts")):
            errors.append(f"{canonical_dir.relative_to(ROOT)}: source automation/agent metadata was not omitted")
        for item in canonical_dir.rglob("*"):
            if item.is_file():
                text = item.read_text(encoding="utf-8", errors="ignore")
                if "skills/shared" in text or "splunk-cisco-skills" in text:
                    errors.append(f"{item.relative_to(ROOT)}: source-repository dependency remains")
    if counts != EXPECTED_NAMESPACES:
        errors.append(f"namespace counts {counts} do not equal {EXPECTED_NAMESPACES}")
    if len(names) != 167:
        errors.append(f"duplicate or missing skill names: {len(names)} unique")
    for path in (ROOT / ".claude-plugin/marketplace.json", ROOT / ".agents/plugins/marketplace.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid marketplace JSON {path.relative_to(ROOT)}: {exc}")
    print(f"Validated migration records: {len(records)}")
    print(f"Namespace counts: {counts}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("Migration validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
