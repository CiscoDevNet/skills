---
name: splunk-cim-data-model-setup
description: >
  Use when the user asks to accelerate a CIM data model, constrain CIM data model indexes, map data to CIM with tags and eventtypes, fix CIM compliance, or manage datamodels.conf for CIM or custom data models. Not for Enterprise Security-specific acceleration, which lives in splunk-enterprise-security-config. Render, validate, and apply Splunk Common Information Model (CIM) data model governance: install handoff for the CIM add-on (Splunk_SA_CIM), data model acceleration settings, allowed-index constraint macros (cim_<model>_indexes), and CIM eventtype/tag mapping to make sourcetypes CIM-compliant, with tstats validation.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-platform
  maturity: draft
---

# Splunk CIM Data Model Setup

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

- Accelerate a CIM data model, constrain CIM data model indexes, map data to CIM with tags and eventtypes, fix CIM
  compliance, or manage datamodels.conf for CIM or custom data models. Not for Enterprise Security-specific
  acceleration, which.
- Preview and review the splunk cim data model setup workflow before any live apply phase.
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

Whenever this workflow installs, configures, or hands off a registry-listed
Splunk app or add-on, follow the
[shared completion gate](#portability-note). Package delivery
alone is not success; capture applicable configuration, data/readiness, and
shipped-view evidence, or explicit package evidence that no dashboards ship.

This skill renders and applies Common Information Model data model governance.
It is render-first because acceleration consumes indexer and storage resources
and index constraints change what searches return.

## Agent Behavior

Never ask for the Splunk admin password; the apply path reads the project
`credentials` file via the shared helper. Acceleration refuses to apply without
`--accept-acceleration`. If `Splunk_SA_CIM` is missing, hand off to
`splunk-app-install` (Splunkbase 1621) before applying.

Read `reference.md` before enabling acceleration on a high-volume model.

## Quick Start

Render acceleration governance for a model:

```bash
bash source-repository automation (not bundled) --datamodel Network_Traffic --acceleration true --earliest-time -7d
```

Apply acceleration live (gated):

```bash
bash source-repository automation (not bundled) --phase apply \
  --datamodel Network_Traffic --acceleration true --accept-acceleration
```

Map a sourcetype into CIM (eventtype + tags) and constrain indexes:

```bash
bash source-repository automation (not bundled) --phase apply \
  --datamodel Authentication \
  --eventtype-name cisco_ise_auth --eventtype-search 'sourcetype=cisco:ise:syslog' \
  --tags authentication --constrain-indexes ise,identity
```

## What It Renders

- `datamodels.conf` - acceleration override (earliest_time, backfill, cron, max_concurrent, manual_rebuilds)
- `macros.conf` - `cim_<model>_indexes` allowed-index constraint
- `eventtypes.conf` + `tags.conf` - CIM compliance mapping
- `validate-tstats.sh` - `| tstats ... from datamodel=<model>` check

## Boundaries

This skill owns CIM-wide data model governance for any app. Enterprise
Security's own data model acceleration and detection wiring stay in
`splunk-enterprise-security-config`. Data readiness scoring stays in
`splunk-data-source-readiness-doctor`.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
