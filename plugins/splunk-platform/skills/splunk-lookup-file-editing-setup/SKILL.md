---
name: splunk-lookup-file-editing-setup
description: >
  Use when the user asks to install, configure, operate, or validate Lookup File Editing. Render and validate Splunk App for Lookup File Editing readiness, including install planning, CSV and KV Store lookup inventory checks, SHC allowRestReplay backup-replication runbook, app health checks, lookup ownership guidance, and handoffs to knowledge-object and KV Store skills.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-platform
  maturity: draft
---

# Splunk Lookup File Editing Setup

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

- Install, configure, operate, or validate Lookup File Editing.
- Preview and review the splunk lookup file editing setup workflow before any live apply phase.
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

## Shared add-on completion gate

Whenever this workflow installs, configures, or hands off the Lookup File
Editing app or a dependency, follow the
[shared completion gate](#portability-note). Package delivery
alone is not success; validate applicable lookup operations and shipped views,
or record explicit evidence that no dashboards ship.

Render-first workflow for the Splunk App for Lookup File Editing. It emits
install readiness, CSV/KV Store lookup inventory SPL, SHC backup-replication
notes, app health checks, and handoffs to knowledge-object and KV Store skills.
It does not edit lookup files or app configuration.

## Workflow

```bash
bash source-repository automation (not bundled) --render \
  --platform auto --lookup-scope both --shc-mode true
```

## Execute

Preview package install and validation:

```bash
bash source-repository automation (not bundled) --all \
  --dry-run --json
```

Install and validate:

```bash
bash source-repository automation (not bundled) --all --live
```

Lookup contents, ACL updates, SHC app config, and KV Store operations remain
delegated to knowledge-object and KV Store workflows.

```bash
bash source-repository automation (not bundled) \
  --rendered-dir splunk-lookup-file-editing-rendered --live
```

See `reference.md` for SHC and lookup-governance guardrails.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
