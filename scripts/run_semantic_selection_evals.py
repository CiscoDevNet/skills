#!/usr/bin/env python3
"""Run reproducible implicit-skill-selection evaluations with Codex CLI.

The evaluator builds an isolated temporary `.agents/skills` catalog from the
canonical tree, asks Codex to identify the most specific skill for direct,
paraphrased, and nearby-sibling-negative requests, and writes JSON artifacts.
It never gives the model the expected answer or permits workflow execution.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "MIGRATION_MANIFEST.json"
DEFAULT_MODEL = "gpt-5.6-sol"


def frontmatter_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    block = text.split("---\n", 2)[1]
    match = re.search(r"(?m)^description:\s*>\n((?:^[ \t]+[^\n]*(?:\n|$))+)", block)
    if not match:
        raise ValueError(f"missing folded description: {path}")
    return " ".join(match.group(1).split())


def title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return path.parent.name.replace("-", " ").title()


def paraphrase(skill_title: str, description: str) -> str:
    terms = description.removeprefix("Use when").removeprefix("the user asks for").strip()
    return f"I need the most specific operational guidance for {skill_title}: {terms}"


def cases_for_batch(records: list[dict[str, object]]) -> list[dict[str, str]]:
    cases: list[dict[str, str]] = []
    for index, record in enumerate(records):
        skill = str(record["name"])
        description = str(record["description"])
        skill_title = str(record["title"])
        sibling = records[(index + 1) % len(records)]
        sibling_name = str(sibling["name"])
        sibling_description = str(sibling["description"])
        cases.extend(
            [
                {
                    "id": f"direct-{skill}",
                    "expected": skill,
                    "kind": "direct",
                    "request": description,
                },
                {
                    "id": f"paraphrase-{skill}",
                    "expected": skill,
                    "kind": "paraphrase",
                    "request": paraphrase(skill_title, description),
                },
                {
                    "id": f"negative-{skill}",
                    "expected": sibling_name,
                    "kind": "nearby-sibling-negative",
                    "request": sibling_description,
                },
            ]
        )
    return cases


def prompt_for_cases(cases: list[dict[str, str]]) -> str:
    return (
        "Each numbered case below is an independent user request. For every case, "
        "select exactly one installed skill that is the most specific fit. Do not "
        "execute commands, do not modify files, and do not explain your reasoning. "
        "Return JSON only as an array of objects with exactly `id` and `skill` keys.\n\n"
        + "\n".join(f"{case['id']}: {case['request']}" for case in cases)
    )


def install_catalog(temp_root: Path) -> None:
    """Expose the complete installed catalog, including pre-existing skills."""
    skills_dir = temp_root / ".agents" / "skills"
    skills_dir.mkdir(parents=True)
    targets = sorted(path.parent for path in (ROOT / "skills").glob("*/*/SKILL.md"))
    for target in targets:
        link = skills_dir / target.name
        if link.exists() or link.is_symlink():
            raise ValueError(f"duplicate installed skill name: {target.name}")
        link.symlink_to(target, target_is_directory=True)


def run_case_chunk(
    temp_root: Path,
    cases: list[dict[str, str]],
    model: str,
    chunk_number: int,
) -> dict[str, object]:
    response_path = temp_root / f"response-{chunk_number}.json"
    completed = subprocess.run(
        [
            "codex",
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "-C",
            str(temp_root),
            "-s",
            "read-only",
            "-m",
            model,
            "--output-last-message",
            str(response_path),
            prompt_for_cases(cases),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    raw_response = response_path.read_text(encoding="utf-8") if response_path.exists() else ""
    try:
        parsed = json.loads(raw_response)
        selections = parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        selections = []
    return {
        "chunk": chunk_number,
        "exit_code": completed.returncode,
        "raw_response": raw_response,
        "cli_output": completed.stdout,
        "selections": selections,
    }


def run_batch(
    batch: str,
    records: list[dict[str, object]],
    model: str,
    output_dir: Path,
    cases_per_call: int,
    workers: int,
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="cisco-skills-semantic-") as raw_temp:
        temp_root = Path(raw_temp)
        install_catalog(temp_root)
        cases = cases_for_batch(records)
        chunks = [cases[index : index + cases_per_call] for index in range(0, len(cases), cases_per_call)]
        with ThreadPoolExecutor(max_workers=workers) as executor:
            runs = list(
                executor.map(
                    lambda item: run_case_chunk(temp_root, item[1], model, item[0]),
                    enumerate(chunks, start=1),
                )
            )
    selections = [selection for run in runs for selection in run["selections"] if isinstance(selection, dict)]
    by_id = {str(item.get("id")): str(item.get("skill")) for item in selections if isinstance(item, dict)}
    outcomes = [
        {
            **case,
            "selected": by_id.get(case["id"], ""),
            "passed": by_id.get(case["id"]) == case["expected"],
        }
        for case in cases
    ]
    result = {
        "batch": batch,
        "model": model,
        "exit_code": max(int(run["exit_code"]) for run in runs),
        "passed": all(case["passed"] for case in outcomes),
        "cases": outcomes,
        "runs": runs,
    }
    (output_dir / f"{batch}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="append", help="Batch name from MIGRATION_MANIFEST.json; repeatable.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--cases-per-call", type=int, default=3)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "evals" / "semantic-selection")
    args = parser.parse_args()
    if args.cases_per_call < 1 or args.workers < 1:
        parser.error("--cases-per-call and --workers must be positive")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in manifest["records"]:
        skill_path = ROOT / str(record["destination"]) / "SKILL.md"
        grouped[str(record["batch"])].append(
            {
                "name": record["name"],
                "destination": record["destination"],
                "description": frontmatter_description(skill_path),
                "title": title(skill_path),
            }
        )
    requested = args.batch or sorted(grouped)
    missing = sorted(set(requested) - set(grouped))
    if missing:
        parser.error(f"unknown batches: {', '.join(missing)}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = [
        run_batch(batch, grouped[batch], args.model, args.output_dir, args.cases_per_call, args.workers)
        for batch in requested
    ]
    summary = {
        "created_at": datetime.now(UTC).isoformat(),
        "client": "Codex CLI",
        "model": args.model,
        "batches": requested,
        "case_count": sum(len(result["cases"]) for result in results),
        "passed_case_count": sum(sum(case["passed"] for case in result["cases"]) for result in results),
        "failed_cases": [
            {"batch": result["batch"], **case}
            for result in results
            for case in result["cases"]
            if not case["passed"]
        ],
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("client", "model", "case_count", "passed_case_count")}, indent=2))
    return 0 if not summary["failed_cases"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
