# Semantic Selection Evaluation

## Scope

This evaluation covers all 167 migrated skills against the complete canonical
catalog (170 skills, including the three pre-existing skills). Each migrated
skill receives three independent, read-only cases:

1. A direct activation request derived from its frontmatter description.
2. A paraphrased activation request using its title and description.
3. A nearest-sibling negative request that must select the sibling rather than
   the skill under test.

The evaluator creates a temporary `.agents/skills` catalog of symlinks to the
canonical skill directories and invokes Codex without user configuration or
workflow execution. It accepts only a single skill name for each case.

## Result

| Measure | Result |
| --- | ---: |
| Batches | 25 |
| Skills tested | 167 |
| Cases | 501 |
| Passed | 501 |
| Failed | 0 |
| Client | Codex CLI |
| Model | `gpt-5.6-sol` |
| Date | 2026-09-21 |

Two observed collisions were corrected and their batches rerun: the broad
AppDynamics router no longer captures Splunk_TA_AppDynamics controller or
dashboard requests, and the Splunk Platform-to-Observability pairing skill no
longer captures native Observability workflows without a Platform pairing.

## Reproduce

Run from the repository root. The output directory is intentionally outside the
repository because the detailed model responses are test artifacts, not skill
content.

```bash
python3 scripts/run_semantic_selection_evals.py \
  --model gpt-5.6-sol \
  --output-dir "$(mktemp -d /tmp/cisco-semantic-evals.XXXXXX)"
```

The recorded runtime is Codex CLI only. Selection behavior in Claude Code,
GitHub Copilot, Cursor, and Gemini CLI remains untested and should be treated
as a PR limitation.
