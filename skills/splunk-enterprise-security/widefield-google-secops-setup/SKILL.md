---
name: widefield-google-secops-setup
description: >
  Use when the user asks to ingest WideField Security into Google Security Operations, verify the WideField default parser, prepare feed handoffs, or collect parser evidence while failing closed for undocumented Google SecOps live feed mutation. Render and validate Google SecOps ingestion, webhook/feed, parser, and evidence assets for WideField Security log type WIDEFIELD_SECURITY.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-enterprise-security
  maturity: draft
---

# WideField Google SecOps Setup

## Prerequisites

| Tool or access | Purpose | Verify |
|---|---|---|
| Bash and Python 3 | Run bundled setup and validation helpers | `bash --version && python3 --version` |
| Required product/platform access | Inspect or configure the selected target | Complete the documented preflight |
| Credential files for live modes | Keep secrets out of chat | Verify paths only |

## Workflow Overview

```text
┌───────────┐   ┌───────────────┐   ┌───────────────┐   ┌─────────────────┐
│ Preflight │ → │ Render/review │ → │ Apply/handoff │ → │ Validate evidence │
└───────────┘   └───────────────┘   └───────────────┘   └─────────────────┘
```

## When to Activate

- Ingest WideField Security into Google Security Operations, verify the WideField default parser, prepare feed
  handoffs, or collect parser evidence while failing closed for undocumented Google SecOps live feed mutation.
- Preview and review the widefield google secops setup workflow before any live apply phase.
- Diagnose failed prerequisites, generated assets, configuration, or validation evidence.

## Scope

Follow the documented read-only or render-first path whenever it is available.
This skill does not imply permission to mutate live systems. Require explicit
apply flags, protected credentials, and operator review for state changes.

## Examples

Inspect the supported setup modes before selecting one:

```bash
bash source-repository automation (not bundled) --help
```

Expected output: usage, supported modes, and required arguments are displayed
without changing the target environment.

Inspect validation modes before running completion checks:

```bash
bash source-repository automation (not bundled) --help
```

Expected output: offline, live, and completion options are displayed when the
skill supports them; help exits without mutation.

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Preflight fails | A required tool or access path is missing | Resolve it before rendering or applying |
| Rendered assets are incomplete | Required non-secret inputs are absent | Complete intake and render again |
| Apply is blocked | Review, credentials, or explicit acceptance is missing | Use the documented handoff |
| Validation is incomplete | Live evidence is unavailable | Record the gap and keep completion open |

Render Google SecOps assets for the public `WIDEFIELD_SECURITY` parser entry.
Live feed creation is disabled until a documented Google SecOps API path is
added to `reference.md`.

## Workflow

```bash
bash source-repository automation (not bundled) --render \
  --google-secops-project example-project \
  --google-secops-region us \
  --feed-name widefield-security
```

Validate supplied evidence:

```bash
bash source-repository automation (not bundled) \
  --evidence-file ./widefield-google-secops-evidence.local.json
```

Evidence should show the feed name, log type `WIDEFIELD_SECURITY`, parser
visibility, and sample events. Validation fails closed when `--evidence-file`
is omitted, is not valid JSON, or does not contain `WIDEFIELD_SECURITY`.
`--dry-run` is the only validation mode that does not require evidence.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
