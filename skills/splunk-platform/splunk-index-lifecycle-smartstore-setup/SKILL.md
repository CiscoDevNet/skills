---
name: splunk-index-lifecycle-smartstore-setup
description: >
  Use when the user asks to inventory index age/size/retention, decide whether indexes are unused, change searchable retention, configure SmartStore remote volumes, enable Cloud archive handoffs, restore/thaw archived data, disable indexes, delete indexes, clean standalone index data, configure S3/GCS/Azure object storage for indexes, set indexes.conf lifecycle settings, maxTotalDataSizeMB, maxGlobalDataSizeMB, maxGlobalRawDataSizeMB, frozenTimePeriodInSecs, cache manager settings, limits.conf remote-storage localization settings, cluster-manager bundle deployment, or standalone indexer lifecycle assets. Render, preflight, apply, and validate Splunk index lifecycle and SmartStore workflows.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-platform
  maturity: draft
---

# Splunk Index Lifecycle / SmartStore Setup

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

- Inventory index age/size/retention, decide whether indexes are unused, change searchable retention, configure
  SmartStore remote volumes, enable Cloud archive handoffs, restore/thaw archived data, disable indexes, delete
  indexes, clean.
- Preview and review the splunk index lifecycle smartstore setup workflow before any live apply phase.
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

This skill is the canonical index lifecycle workflow for Splunk Platform. It
renders evidence collection, dependency reports, retention plans, SmartStore
configuration, archive/restore handoffs, and gated apply source-repository automation (not bundled) for selected
high-risk operations.

## Agent Behavior

Never ask for Splunk session keys, ACS tokens, object-store access keys, or
other secrets in chat. Use local files only:

```bash
bash portable local helper /tmp/acs_token
bash portable local helper /tmp/smartstore_s3_access_key
bash portable local helper /tmp/smartstore_s3_secret_key
```

Secret files used by generated live helpers must be regular, non-symlink files,
owned by the executing user, and mode `0600` (or stricter). Generated curl
configuration, ACS request payloads, and ACS response bodies use owner-only,
random temporary paths and are removed on exit. Tokens are never placed in
process arguments.

Start with render or inventory. Do not treat a frozen, stale, or low-volume
index as unused until dependency evidence has been collected and reviewed.

Destructive operations fail closed. `delete-index` and `clean-data` require:

- `--accept-destructive-index-delete`
- `--owner-approval-file`
- `--backup-evidence-file`
- `--evidence-file` marking each target index safe to delete
- `--confirm-token DELETE_INDEX:<index>` for each target index

The skill hard-blocks deletion of internal indexes beginning with `_`. It also
blocks protected default indexes and ES/ITSI/ARI-sensitive indexes unless the
evidence explicitly classifies the index as safe under the documented gates.
Clustered `clean-data` is refused.

Live apply does not report completion from an HTTP or CLI acceptance alone:

- Cloud retention polls ACS `GET` until every requested field matches.
- Cloud deletion polls ACS `GET` until each target returns `404`.
- Standalone Enterprise SmartStore/retention/disable/delete helpers perform a
  post-action `btool` readback.
- Cluster-manager helpers require bundle apply, then require bundle-status
  readback. If bundle apply or a standalone restart is disabled, the generated
  helper exits `2` after staging and identifies the remaining handoff.

Multi-index Cloud mutations stop on the first unverified target, exit nonzero,
and report any earlier targets already verified. They are not transactional.

## Quick Start

Inventory all indexes and render collection searches:

```bash
bash source-repository automation (not bundled) \
  --phase inventory \
  --indexes all
```

Render and optionally run REST export collection with a local session-key file:

```bash
bash source-repository automation (not bundled) \
  --phase inventory \
  --indexes all \
  --session-key-file /tmp/splunk_session_key \
  --splunk-uri https://localhost:8089
```

Render an Enterprise retention overlay:

```bash
bash source-repository automation (not bundled) \
  --operation retention \
  --indexes cisco_asa,network \
  --max-total-data-size-mb 1048576 \
  --frozen-time-period-in-secs 7776000
```

Render per-index SmartStore for an indexer cluster:

```bash
bash source-repository automation (not bundled) \
  --operation smartstore \
  --deployment cluster \
  --remote-provider s3 \
  --remote-path s3://splunk-prod-smartstore/cluster-a \
  --indexes main,summary \
  --max-global-data-size-mb 10485760 \
  --cache-size-mb 262144
```

Render a Splunk Cloud retention payload:

```bash
bash source-repository automation (not bundled) \
  --platform cloud \
  --operation retention \
  --stack my-stack \
  --indexes cisco_asa \
  --searchable-days 90 \
  --max-data-size-mb 512000
```

## What It Renders

The default output directory is `splunk-smartstore-rendered/smartstore/`.

- `index-lifecycle-report.md/json`
- `index-dependency-report.md/json`
- `collection-searches.spl`
- `collect-evidence.sh`
- `retention-change-plan.md`
- `destructive-action-plan.md`
- SmartStore `indexes.conf.template`, `server.conf`, and `limits.conf`
- Enterprise retention/disable overlays and apply helpers
- Cloud ACS retention/delete payload helpers
- DDAA archive and restore/thaw handoffs

Use `splunk-data-source-readiness-doctor` when evidence must prove whether
dashboards, saved searches, ES, ITSI, ARI, CIM, HEC tokens, or macros still
depend on an index. Use `splunk-ddaa-archive-setup` for Splunk Cloud DDAA archive
enable/update and restore auditing.

Read `reference.md` before changing lifecycle safety gates, destructive apply
behavior, or SmartStore retention defaults.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
