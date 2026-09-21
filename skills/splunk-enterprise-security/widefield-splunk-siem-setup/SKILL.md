---
name: widefield-splunk-siem-setup
description: >
  Use when the user asks to send WideField Security events to Splunk, create WideField HEC/index plumbing, validate WideField ingest, or prepare SIEM searches and dashboard readiness for identity threat detections. Render, apply, and validate Splunk SIEM readiness for WideField Security events using a WideField index, HEC token, schema-light spath searches, saved searches, macros, and starter dashboard assets.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-enterprise-security
  maturity: draft
---

# WideField Splunk SIEM Setup

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

- Send WideField Security events to Splunk, create WideField HEC/index plumbing, validate WideField ingest, or
  prepare SIEM searches and dashboard readiness for identity threat detections.
- Preview and review the widefield splunk siem setup workflow before any live apply phase.
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

Prepare Splunk Platform to receive and search WideField Security events.

## Workflow

Render reviewable assets:

```bash
bash source-repository automation (not bundled) --render
```

Apply in Splunk Enterprise with a file-backed HEC token value:

```bash
bash source-repository automation (not bundled) --apply --accept-apply \
  --splunk-platform enterprise \
  --hec-token-file /secure/splunk/widefield_hec_token
```

For Splunk Cloud, let ACS create the token and write the returned value to a
local-only file:

```bash
bash source-repository automation (not bundled) --apply --accept-apply \
  --splunk-platform cloud \
  --write-hec-token-file /secure/splunk/widefield_hec_token
```

## Defaults

- Index: `widefield`
- Sourcetype: `widefield:security`
- Source: `widefield`
- HEC token name: `widefield_security_hec`

The skill delegates token lifecycle to `splunk-hec-service-setup` and uses
schema-light `spath` searches so WideField event shapes can evolve safely.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
