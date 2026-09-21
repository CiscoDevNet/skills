---
name: splunk-data-source-readiness-doctor
description: >
  Use when the user asks for data-source readiness, ES/ITSI/ARI readiness scoring, CIM or OCSF validation, data-model acceleration checks, dashboard population checks, ingest pipeline health, knowledge-object enrichment, federated data usability, ITSI summary health, or fix handoffs after app/input setup. Diagnose whether onboarded Splunk data sources are usable by Enterprise Security, ITSI, Asset and Risk Intelligence, CIM, OCSF, and dashboards.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-platform
  maturity: draft
---

# Splunk Data Source Readiness Doctor

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

- The user asks for data-source readiness, ES/ITSI/ARI readiness scoring, CIM or OCSF validation, data-model
  acceleration checks, dashboard population checks, ingest pipeline health, knowledge-object enrichment, federated
  data usability,.
- Preview and review the splunk data source readiness doctor workflow before any live apply phase.
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

Whenever this workflow validates or hands off a registry-listed Splunk app or
add-on, use the [shared completion gate](#portability-note).
Package presence alone is not readiness; require applicable ingest and
dashboard evidence, or explicit package evidence that no dashboards ship.

This skill proves that already-onboarded data is usable by the consumers that
matter after installation: **ES**, **ITSI**, **ARI**, **CIM**, **OCSF**, and
dashboards. It does not install apps or mutate Splunk. It consumes evidence from
live searches, the shared app registry, expected index/sourcetype/macro
contracts, sample-event summaries, CIM tags/eventtypes, data model acceleration
state, OCSF transform status, and product-specific readiness signals.
It also applies bundled source-specific packs for common sources such as AWS
CloudTrail, Amazon Security Lake OCSF, Cisco ASA, Cisco Secure Firewall, Cisco
Secure Access, Kubernetes Audit, Linux secure/auditd, Microsoft 365 management
activity, Windows Security events, Okta, Microsoft Entra ID, Google Workspace,
CrowdStrike, Palo Alto Networks, Zscaler, AWS VPC Flow Logs, AWS Security
Hub/GuardDuty, Duo, GitHub audit logs, and Fortinet FortiGate.
Those readiness signals include ES correlation/content activation, SSE data
inventory and CIM compliance outputs, ITSI KPI threshold/entity-split/runtime
state, ITSI Event Analytics, metrics/mstats readiness, ES risk/threat/ESCU
readiness, Dashboard Studio data-source health, ARI
relevant-event/key-field/event-search evidence, ingest pipeline and latency
evidence, lookup/field-alias/calculated-field enrichment, federated/remote
dataset usability, ITSI summary-index health, scheduled content execution, and
retention/lookback coverage. Live collection can now synthesize source evidence
and a dashboard/content dependency graph from read-only REST export results.

## Agent Behavior

Never ask for passwords, session keys, API keys, HEC tokens, or bearer tokens in
chat. Keep all credentials in local files and pass only file paths to the
underlying collection workflows.

Live REST collection requires a credential-free HTTPS origin and never follows
redirects. Plaintext HTTP is refused unless an operator explicitly sets
`SPLUNK_ALLOW_INSECURE_HTTP=true` for an isolated, short-lived lab;
`--no-verify-tls` does not authorize HTTP.

Use this doctor after an input/app setup skill says ingestion is configured, or
when dashboards, ES detections, ITSI services, ARI inventories, or CIM/OCSF
content are not producing useful results.

Safety model:

- `doctor`, `fix-plan`, `validate`, `status`, `source-packs`, `collect`, and
  `synthesize` are read-only.
- `collect` renders a collector manifest and can optionally run read-only
  Splunk REST export searches when given `--splunk-uri` and a local
  `--session-key-file`.
- `synthesize` consumes `live-collector-results.redacted.json` or
  `--collector-results-file`, writes synthesized evidence, and reruns scoring
  without querying Splunk.
- `apply` renders local handoff/support packets for selected finding IDs only.
- The doctor does not create indexes, alter macros, enable searches, rebuild
  data models, install apps, activate ARI data sources, import ITSI objects, or
  change ES configuration.
- Remediation routes to mature skills such as `splunk-enterprise-security-config`,
  `splunk-itsi-config`, `splunk-asset-risk-intelligence-setup`,
  `splunk-hec-service-setup`, `splunk-app-install`, and product setup skills.

## Quick Start

Validate catalog coverage:

```bash
bash source-repository automation (not bundled)
```

Render a readiness report from evidence:

```bash
bash source-repository automation (not bundled) \
  --phase doctor \
  --evidence-file skills/splunk-data-source-readiness-doctor/fixtures/comprehensive_unready.json
```

List source-specific packs:

```bash
bash source-repository automation (not bundled) \
  --phase source-packs \
  --json
```

Render a source-specific collection manifest without live credentials:

```bash
bash source-repository automation (not bundled) \
  --phase collect \
  --source-pack aws_cloudtrail \
  --evidence-file evidence.json
```

Synthesize live collector rows into evidence and refreshed scoring:

```bash
bash source-repository automation (not bundled) \
  --phase synthesize \
  --evidence-file evidence.json \
  --collector-results-file splunk-data-source-readiness-doctor-rendered/live-collector-results.redacted.json \
  --json
```

Preview selected handoff packets:

```bash
bash source-repository automation (not bundled) \
  --phase apply \
  --evidence-file skills/splunk-data-source-readiness-doctor/fixtures/comprehensive_unready.json \
  --fixes DSRD-CIM-TAG-EVENTTYPE-GAP,DSRD-DM-ACCELERATION-GAP \
  --dry-run \
  --json
```

## Outputs

The default output directory is `splunk-data-source-readiness-doctor-rendered/`:

- `readiness-report.md` and `readiness-report.json`
- `fix-plan.md` and `fix-plan.json`
- `coverage-report.json`
- `registry-projection.json`
- `source-pack-catalog.json`
- `source-pack-report.json`
- `collector-manifest.json`
- `collection-searches.spl`
- `live-collector-results.redacted.json` from `collect`
- `evidence/live-evidence.synthesized.json` from `collect` or `synthesize`
- `dashboard-dependency-graph.json`
- `synthesis-report.json`
- `evidence/input-evidence.redacted.json`
- `handoffs/*.md` for delegated or direct fix packets
- `support-tickets/*.md` for manual/support packets

Read `reference.md` before changing rule coverage, target scoring, evidence
shape, registry consumption, or apply behavior.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
