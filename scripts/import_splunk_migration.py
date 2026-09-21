#!/usr/bin/env python3
"""Import the pinned Splunk/Cisco skill snapshot into CiscoDevNet packaging.

The importer intentionally keeps the migration deterministic and conservative:
documentation, references, templates, and assets are copied; source-repository
agent metadata and repository-coupled automation are not.  Every decision is
recorded in MIGRATION_MANIFEST.json and SOURCES.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


SOURCE_COMMIT = "c74a619301bca7ebcdc8323308402ca9d857966a"
COMPATIBILITY = "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
SOURCE_URL = "https://github.com/chambear2809/splunk-cisco-skills"
DEST_URL = "https://github.com/CiscoDevNet/skills"

EXCLUDED = {"cisco-product-setup", "cisco-defenseclaw-deskside-setup"}
SECURITY_PORTFOLIO = {
    "splunk-asset-risk-intelligence-setup",
    "splunk-attack-analyzer-setup",
    "splunk-fraud-analytics-setup",
    "splunk-infosec-app-setup",
    "splunk-pci-compliance-setup",
    "splunk-uba-setup",
}


def namespace(name: str) -> str:
    if name in EXCLUDED:
        return "excluded"
    if name.startswith("splunk-appdynamics-"):
        return "appdynamics"
    if name in {
        "splunk-observability-thousandeyes-integration",
        "cisco-meraki-aam-thousandeyes-setup",
        "cisco-thousandeyes-mcp-setup",
    }:
        return "thousandeyes"
    if name == "cisco-isovalent-platform-setup":
        return "isovalent"
    if name.startswith("splunk-itsi-"):
        return "splunk-itsi"
    if (
        name.startswith("splunk-enterprise-security-")
        or name.startswith("splunk-security-")
        or name.startswith("widefield-")
        or name in SECURITY_PORTFOLIO
    ):
        return "splunk-enterprise-security"
    if name.startswith("splunk-observability-") or name.startswith("galileo-") or name == "lemonade-splunk-otel":
        return "splunk-observability-cloud"
    return "splunk-platform"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_description(text: str, fallback: str) -> str:
    """Read a simple YAML description without depending on PyYAML."""
    if not text.startswith("---\n"):
        return fallback
    block = text.split("---\n", 2)[1]
    lines = block.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("description:"):
            continue
        value = line.split(":", 1)[1].strip()
        values: list[str] = []
        if value not in {">", "|", ">-", "|-", ">+", "|+"} and value:
            values.append(value)
        for continuation in lines[index + 1 :]:
            if continuation.startswith((" ", "\t")):
                values.append(continuation.strip())
            else:
                break
        description = " ".join(values).strip().strip("\"'")
        description = re.sub(r"\s+", " ", description)
        if description:
            return description[:1021].rstrip() + ("..." if len(description) > 1021 else "")
    return fallback


def canonical_link(name: str, target_names: set[str]) -> str:
    if name in target_names:
        return f"{DEST_URL}/tree/main/skills/{namespace(name)}/{name}"
    return f"{DEST_URL}/tree/main"


def sanitize_markdown(text: str, target_names: set[str]) -> str:
    """Remove local source-repository paths while retaining operational prose."""
    # Relative links to another migrated skill become stable canonical links.
    nested_skill = re.compile(
        r"\((?:[^)]*?/)?skills/([a-z0-9][a-z0-9-]*)/SKILL\.md\)"
    )
    text = nested_skill.sub(
        lambda match: f"({canonical_link(match.group(1), target_names)})",
        text,
    )
    relative_skill = re.compile(
        r"\((?:\.\./|\./)+([a-z0-9][a-z0-9-]*)/SKILL\.md\)"
    )
    text = relative_skill.sub(
        lambda match: f"({canonical_link(match.group(1), target_names)})",
        text,
    )
    # Shared completion references cannot point outside an installed skill.
    text = re.sub(r"\]\((?:\.\./)+shared/[^)]+\)", "](#portability-note)", text)
    text = re.sub(r"(?:\.\./)+shared/[A-Za-z0-9_./-]+", "portable local reference", text)
    text = re.sub(r"skills/shared(?:/[A-Za-z0-9_./-]+)?", "portable local helper", text)
    # Commands and links to omitted scripts are deliberately non-executable.
    text = re.sub(r"(?:\.\./)+scripts(?:/[A-Za-z0-9_./-]+)?", "source-repository automation (not bundled)", text)
    text = re.sub(r"skills/[a-z0-9][a-z0-9-]*/scripts(?:/[A-Za-z0-9_./-]+)?", "source-repository automation (not bundled)", text)
    text = re.sub(r"scripts(?:/[A-Za-z0-9_./-]+)?", "source-repository automation (not bundled)", text)
    text = re.sub(r"\]\([^)]*(?:source-repository automation|portable local helper|products\.json|agent/)[^)]*\)", "](#portability-note)", text)
    text = text.replace("splunk-cisco-skills", "the source repository")
    return text


def add_reference_toc(text: str) -> str:
    """Add a compact TOC to long reference Markdown files."""
    if len(text.splitlines()) <= 100 or re.search(r"(?im)^## (?:table of contents|contents)\s*$", text):
        return text
    headings = re.findall(r"^##+\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if len(headings) < 2:
        toc = "## Table of contents\n\nThis reference is intentionally linear; use in-file search and the headings below.\n\n"
        first_heading = re.search(r"^#\s+.+$", text, flags=re.MULTILINE)
        if first_heading:
            end = first_heading.end()
            return text[:end] + "\n\n" + toc + text[end:].lstrip("\n")
        return toc + text
    entries: list[str] = []
    for heading in headings:
        anchor = re.sub(r"[^a-z0-9 -]", "", heading.lower()).strip().replace(" ", "-")
        anchor = re.sub(r"-+", "-", anchor)
        entries.append(f"- [{heading}](#{anchor})")
    toc = "## Table of contents\n\n" + "\n".join(entries) + "\n\n"
    first_heading = re.search(r"^#\s+.+$", text, flags=re.MULTILINE)
    if first_heading:
        end = first_heading.end()
        return text[:end] + "\n\n" + toc + text[end:].lstrip("\n")
    return toc + text


def rewrite_skill(source: Path, name: str, product: str, target_names: set[str]) -> str:
    original = source.read_text(encoding="utf-8")
    description = source_description(
        original,
        f"Use when working with {name.replace('-', ' ')} and its documented operational workflow.",
    )
    body = original
    if original.startswith("---\n") and "\n---\n" in original[4:]:
        body = original.split("---\n", 2)[2]
    body = sanitize_markdown(body.lstrip("\n"), target_names)
    if not body.startswith("# "):
        body = f"# {name.replace('-', ' ').title()}\n\n{body}"
    portability = (
        "\n\n## Portability note\n\n"
        "This Cisco DevNet package preserves the source skill's operational guidance, "
        "references, templates, and assets. Source-repository `agents/openai.yaml` "
        "files and repository-coupled scripts/shared helpers are intentionally not "
        "bundled. Any omitted automation must be recreated with the target product's "
        "supported tools after read-only discovery, exact-target review, explicit "
        "approval, rollback preparation, and post-change validation. Keep secrets in "
        "local mode-0600 files and never paste them into chat, commands, or logs.\n"
    )
    if "## Portability note" not in body:
        body += portability
    return (
        "---\n"
        f"name: {name}\n"
        "description: >\n"
        f"  {description}\n"
        "license: Apache-2.0\n"
        f'compatibility: "{COMPATIBILITY}"\n'
        "metadata:\n"
        f"  product: {product}\n"
        "  maturity: draft\n"
        "---\n\n"
        + body.lstrip()
    )


def docs_urls(root: Path) -> list[str]:
    urls: list[str] = []
    for path in root.rglob("*.md"):
        urls.extend(re.findall(r"https?://[^)\s>]+", path.read_text(encoding="utf-8", errors="ignore")))
    result: list[str] = []
    for url in urls:
        url = url.rstrip(".,;\"")
        if url not in result and "example.com" not in url:
            result.append(url)
    return result[:8]


def batch_for(product: str, index: int) -> str:
    counts = {
        "splunk-platform": 10,
        "splunk-observability-cloud": 4,
        "thousandeyes": 2,
        "appdynamics": 3,
        "splunk-itsi": 1,
        "splunk-enterprise-security": 4,
        "isovalent": 1,
    }
    total = counts[product]
    # Deterministic contiguous batches: 1-based skill index divided evenly.
    return f"{product}-{min(total, (index * total // max(index, 1)) if False else 1):02d}"


def assign_batches(names_by_product: dict[str, list[str]]) -> dict[str, str]:
    counts = {
        "splunk-platform": 10,
        "splunk-observability-cloud": 4,
        "thousandeyes": 2,
        "appdynamics": 3,
        "splunk-itsi": 1,
        "splunk-enterprise-security": 4,
        "isovalent": 1,
    }
    result: dict[str, str] = {}
    for product, names in names_by_product.items():
        batch_count = counts[product]
        for index, name in enumerate(sorted(names)):
            batch = min(batch_count - 1, index * batch_count // len(names)) + 1
            result[name] = f"{product}-{batch:02d}"
    return result


def source_dependencies(text: str, target_names: set[str], self_name: str) -> list[str]:
    found = sorted(name for name in target_names if name != self_name and name in text)
    return [f"{name} ({canonical_link(name, target_names)})" for name in found]


def plugin_metadata(product: str) -> dict[str, object]:
    display = {
        "splunk-platform": "Splunk Platform",
        "splunk-observability-cloud": "Splunk Observability Cloud",
        "splunk-enterprise-security": "Splunk Enterprise Security",
        "appdynamics": "AppDynamics",
        "splunk-itsi": "Splunk IT Service Intelligence",
        "isovalent": "Isovalent",
        "thousandeyes": "Cisco ThousandEyes",
    }[product]
    description = {
        "splunk-platform": "Operational skills for Splunk Platform, Splunk Cloud Platform, Splunk Enterprise, collectors, and data-source integrations.",
        "splunk-observability-cloud": "Operational skills for Splunk Observability Cloud, Galileo, Lemonade, and telemetry integrations.",
        "splunk-enterprise-security": "Operational skills for Splunk Enterprise Security, security portfolio products, and WideField integrations.",
        "appdynamics": "Operational skills for AppDynamics platform administration, agents, monitoring, and integrations.",
        "splunk-itsi": "Operational skills for Splunk IT Service Intelligence installation, configuration, and service operations.",
        "isovalent": "Operational skills for Isovalent platform installation and lifecycle management.",
        "thousandeyes": "Operational skills for Cisco ThousandEyes, Meraki Assurance, and Observability Cloud integrations.",
    }[product]
    category = "security" if product == "splunk-enterprise-security" else "infrastructure" if product == "isovalent" else "observability"
    keywords = ["splunk", product, "agent-skills"]
    return {
        "name": product,
        "displayName": display,
        "description": description,
        "version": "0.1.0",
        "author": {"name": "Cisco DevNet", "url": "https://developer.cisco.com/"},
        "homepage": f"{DEST_URL}/tree/main/skills/{product}",
        "repository": DEST_URL,
        "license": "Apache-2.0",
        "keywords": keywords + [category],
        "category": category,
    }


def update_marketplaces(root: Path, products: list[str]) -> None:
    claude_path = root / ".claude-plugin/marketplace.json"
    agents_path = root / ".agents/plugins/marketplace.json"
    claude = json.loads(claude_path.read_text(encoding="utf-8"))
    agents = json.loads(agents_path.read_text(encoding="utf-8"))
    descriptions = {
        product: plugin_metadata(product) for product in products
    }
    for product in products:
        meta = descriptions[product]
        if not any(item.get("name") == product for item in claude["plugins"]):
            claude["plugins"].append({
                "name": product,
                "source": f"./plugins/{product}",
                "description": meta["description"],
                "category": meta["category"],
                "keywords": meta["keywords"],
            })
        if not any(item.get("name") == product for item in agents["plugins"]):
            agents["plugins"].append({
                "name": product,
                "source": {"source": "local", "path": f"./plugins/{product}"},
                "description": meta["description"],
                "policy": {"installation": "AVAILABLE", "authentication": "ON_DEMAND"},
                "category": str(meta["category"]).title(),
            })
    claude_path.write_text(json.dumps(claude, indent=2) + "\n", encoding="utf-8")
    agents_path.write_text(json.dumps(agents, indent=2) + "\n", encoding="utf-8")


def write_readmes(root: Path, products: list[str]) -> None:
    titles = {
        "splunk-platform": "Splunk Platform",
        "splunk-observability-cloud": "Splunk Observability Cloud",
        "splunk-enterprise-security": "Splunk Enterprise Security",
        "appdynamics": "AppDynamics",
        "splunk-itsi": "Splunk IT Service Intelligence",
        "isovalent": "Isovalent",
        "thousandeyes": "Cisco ThousandEyes",
    }
    descriptions = {
        "splunk-platform": "Splunk Cloud Platform, Splunk Enterprise, data collection, applications, administration, and Cisco integrations.",
        "splunk-observability-cloud": "Splunk Observability Cloud, Galileo, Lemonade, and telemetry integrations.",
        "splunk-enterprise-security": "Splunk Enterprise Security, security portfolio workflows, and WideField integrations.",
        "appdynamics": "AppDynamics platform, agents, application monitoring, content, and integrations.",
        "splunk-itsi": "Splunk IT Service Intelligence lifecycle, service modeling, KPIs, and configuration.",
        "isovalent": "Isovalent platform installation, configuration, and lifecycle operations.",
        "thousandeyes": "Cisco ThousandEyes, Meraki Assurance, and Observability Cloud integrations.",
    }
    for product in products:
        text = (
            f"# {titles[product]} skills\n\n"
            f"Scope: {descriptions[product]}\n\n"
            "Each child directory is a self-contained Agent Skill with its own "
            "`SKILL.md` and any included references, templates, or assets.\n"
        )
        for base in (root / "skills" / product, root / "plugins" / product):
            base.mkdir(parents=True, exist_ok=True)
            (base / "README.md").write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_snapshot", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    source_skills = args.source_snapshot / "skills"
    root = args.root.resolve()
    source_names = sorted(path.name for path in source_skills.iterdir() if path.is_dir())
    names = [name for name in source_names if name not in EXCLUDED and name != "shared"]
    target_names = set(names)
    products = sorted({namespace(name) for name in names})
    names_by_product = {product: sorted(name for name in names if namespace(name) == product) for product in products}
    batches = assign_batches(names_by_product)

    records: list[dict[str, object]] = []
    for name in names:
        product = namespace(name)
        source_dir = source_skills / name
        source_files = sorted(path for path in source_dir.rglob("*") if path.is_file())
        included = [str(path.relative_to(source_dir)) for path in source_files if "agents" not in path.parts and "scripts" not in path.parts]
        excluded = [str(path.relative_to(source_dir)) for path in source_files if str(path.relative_to(source_dir)) not in included]
        source_skill = source_dir / "SKILL.md"
        source_text = source_skill.read_text(encoding="utf-8")
        docs = docs_urls(source_dir)
        records.append({
            "name": name,
            "source_hash": sha256(source_skill),
            "source_path": f"skills/{name}",
            "source_commit": SOURCE_COMMIT,
            "destination": f"skills/{product}/{name}",
            "plugin_mirror": f"plugins/{product}/skills/{name}",
            "namespace": product,
            "batch": batches[name],
            "port_mode": "adapted-copy",
            "dependencies": source_dependencies(source_text, target_names, name),
            "included_files": included,
            "excluded_files": excluded,
            "provenance": {
                "source_repository": SOURCE_URL,
                "source_commit": SOURCE_COMMIT,
                "license": "Apache-2.0 (source repository); external documentation remains linked, not vendored",
                "adaptation": "Frontmatter normalized; source-repository automation and agent metadata omitted; local paths rewritten.",
            },
            "authoritative_documentation": docs or ["https://docs.splunk.com/", "https://developer.cisco.com/docs/"],
            "validation_commands": [
                "python3 scripts/validate_skills.py",
                "python3 scripts/validate_migration.py",
                "git diff --check",
                "python3 -m json.tool .claude-plugin/marketplace.json",
                "python3 -m json.tool .agents/plugins/marketplace.json",
            ],
        })

        for relative in included:
            source_path = source_dir / relative
            canonical = root / "skills" / product / name / relative
            canonical.parent.mkdir(parents=True, exist_ok=True)
            if relative == "SKILL.md":
                canonical.write_text(rewrite_skill(source_path, name, product, target_names), encoding="utf-8")
            else:
                try:
                    content = source_path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    shutil.copy2(source_path, canonical)
                else:
                    content = sanitize_markdown(content, target_names)
                    if canonical.suffix.lower() in {".md", ".markdown"}:
                        content = add_reference_toc(content)
                    canonical.write_text(content, encoding="utf-8")

        mirror = root / "plugins" / product / "skills" / name
        if mirror.exists():
            shutil.rmtree(mirror)
        shutil.copytree(root / "skills" / product / name, mirror)

    # Remove the old placeholder now that ThousandEyes has real skills.
    placeholder = root / "plugins/thousandeyes/skills/.gitkeep"
    if placeholder.exists():
        placeholder.unlink()

    for product in products:
        manifest_dir = root / "plugins" / product / ".claude-plugin"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        (manifest_dir / "plugin.json").write_text(
            json.dumps({k: v for k, v in plugin_metadata(product).items() if k != "category"}, indent=2) + "\n",
            encoding="utf-8",
        )
    update_marketplaces(root, products)
    write_readmes(root, products)

    records.sort(key=lambda record: str(record["name"]))
    manifest = {
        "schema_version": 1,
        "source_repository": SOURCE_URL,
        "source_commit": SOURCE_COMMIT,
        "destination_baseline": "16ca54d351f793984f6768952e2c6c75b43007c7",
        "scope": {"selected_skill_count": len(records), "excluded": sorted(EXCLUDED), "namespaces": {product: len(names_by_product[product]) for product in products}},
        "records": records,
    }
    (root / "MIGRATION_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (root / "MIGRATION_MANIFEST.md").write_text(
        "# CiscoDevNet skill migration manifest\n\n"
        f"Pinned source: `{SOURCE_URL}@{SOURCE_COMMIT}`. Destination baseline: `16ca54d…`.\n\n"
        "The complete machine-readable manifest is in `MIGRATION_MANIFEST.json`; "
        "each record includes source hash/path, destination, batch, dependencies, "
        "included/excluded files, provenance, authoritative documentation, and validation commands.\n\n"
        "| Namespace | Skills | Batches |\n| --- | ---: | --- |\n"
        + "\n".join(
            f"| `{product}` | {len(names_by_product[product])} | "
            + ", ".join(sorted({batches[name] for name in names_by_product[product]}))
            + " |"
            for product in products
        )
        + "\n",
        encoding="utf-8",
    )
    source_lines = [
        "# Imported and adapted sources",
        "",
        "The migrated skills below are adapted from the immutable source snapshot. "
        "The source repository's Apache-2.0 license is recorded here; external "
        "documentation is linked rather than copied. Source-repository automation "
        "and agent metadata were excluded where they depended on the original repository.",
        "",
        "## Existing Cisco skills",
        "",
        "The pre-existing CiscoDevNet skills remain attributed here for continuity:",
        "",
        "- SCC Firewall Manager skills: imported from [CiscoDevNet/sccfm-devkit](https://github.com/CiscoDevNet/sccfm-devkit) at commit `0d1fe58e59a2b4dc112b2d206dd1e116805eb349`, Apache-2.0.",
        "- Cisco IOS patterns: imported from [affaan-m/ECC](https://github.com/affaan-m/ECC) at commit `ca185ef5f7667078a1e70a763bd3a9c71c48acf0`, MIT; see `THIRD_PARTY_LICENSES/ECC-MIT.txt`.",
        "",
        "The Agent Skills specification and CoSAI Project CodeGuard remain reference-only projects and are not vendored.",
        "",
        f"- Source: [{SOURCE_URL}]({SOURCE_URL})",
        f"- Commit: [`{SOURCE_COMMIT}`]({SOURCE_URL}/commit/{SOURCE_COMMIT})",
        "- License: Apache-2.0",
        "- Adaptation: normalized CiscoDevNet frontmatter, product namespace, path references, and portability notes.",
        "",
        "## Per-skill provenance",
        "",
        "See `MIGRATION_MANIFEST.json` for the complete 167-record file-level inventory. "
        "Every record contains original paths, SHA-256 hash, included/excluded files, "
        "dependencies, documentation URLs, and validation commands.",
        "",
    ]
    source_lines.extend(
        f"- `{record['name']}` → `{record['destination']}`; source `skills/{record['name']}`; "
        f"source SKILL.md SHA-256 `{record['source_hash']}`; status: adapted-copy."
        for record in records
    )
    (root / "SOURCES.md").write_text("\n".join(source_lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
