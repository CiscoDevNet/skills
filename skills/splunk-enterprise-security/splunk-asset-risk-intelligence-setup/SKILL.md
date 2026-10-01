---
name: splunk-asset-risk-intelligence-setup
description: >
  Use when a user asks to set up ARI, Splunk Asset and Risk Intelligence, asset/identity risk inventory, or ARI-backed ES Exposure Analytics readiness. Install, prepare, validate, and plan Splunk Asset and Risk Intelligence (`SplunkAssetRiskIntelligence`, Splunkbase app 7180), including ARI indexes, KV Store, roles/capabilities, app readiness, data visibility, Enterprise Security integration, ES 8.5+ Exposure Analytics, ARI Technical Add-ons, ARI Echo, upgrade, and uninstall prerequisite handoffs.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-enterprise-security
  maturity: draft
---

# Splunk Asset and Risk Intelligence Setup

## Workflow Overview

```text
┌───────────┐   ┌───────────────┐   ┌───────────────┐   ┌─────────────────┐
│ Preflight │ → │ Render/review │ → │ Apply/handoff │ → │ Validate evidence │
└───────────┘   └───────────────┘   └───────────────┘   └─────────────────┘
```

## When to Activate

- A user asks to set up ARI, Splunk Asset and Risk Intelligence, asset/identity risk inventory, or ARI-backed ES
  Exposure Analytics readiness.
- Preview and review the splunk asset risk intelligence setup workflow before any live apply phase.
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

Use this skill for Splunk Asset and Risk Intelligence (ARI). It is
setup-plus-handoff coverage, not ARI config-as-code.

## Prerequisites

- A Splunk credentials file readable by the shared credential helper. If not
  yet configured, run
  `bash portable local helper`
  or copy `credentials.example` and edit it (`chmod 600 credentials`).
- App delivery uses the
  [`splunk-app-install`](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-platform/splunk-app-install) wrapper
  (`source-repository automation (not bundled)`) so Splunkbase auth and
  ACS upload paths stay in one place. ARI is currently a restricted-entitlement
  app on Splunkbase; pass `--file <path-to-tgz>` when Splunkbase pulls fail.
- For SHC deployments, run the install/setup against the deployer/captain
  (the search-tier role placement is `required`); this skill does not split
  per-member work.
- Treat Splunk platform compatibility carefully: Splunkbase lists ARI `1.2.2`
  for Splunk `9.3` through `10.5`, while ARI docs signal `9.1.3+` for current
  ARI releases. In this repository, `10.5` is the current Splunk Cloud target;
  the self-managed Enterprise default remains `10.4.1`. Do not use the
  cross-product Splunkbase listing as evidence for a self-managed Enterprise
  `10.5` deployment. Warn below `9.1.3`; do not hard-fail only on that conflict.

## Primary Commands

Preview:

```bash
bash source-repository automation (not bundled) --dry-run --json
```

Full read-only handoff plan:

```bash
bash source-repository automation (not bundled) --full-handoff
```

Install, create ARI indexes, and validate:

```bash
bash source-repository automation (not bundled) --file /path/to/splunk-asset-and-risk-intelligence.tgz
```

Validate only:

```bash
bash source-repository automation (not bundled)
```

## Handoff Flags

Use these flags for read-only planning without modifying Splunk unless combined
with `--install`:

- `--preflight-only`
- `--full-handoff`
- `--post-install-handoff`
- `--admin-handoff`
- `--risk-handoff`
- `--response-audit-handoff`
- `--investigation-handoff`
- `--es-integration-handoff`
- `--exposure-analytics-handoff`
- `--addon-handoff`
- `--echo-handoff`
- `--upgrade-handoff`
- `--uninstall-handoff`

## Agent Behavior

- Prefer `--file` when Splunkbase access is restricted for app `7180`.
- Create and validate `ari_staging`, `ari_asset`, `ari_internal`, and `ari_ta`.
- Validate KV Store, ARI roles, ARI capabilities, app-owned saved-search
  visibility, `ari_ta` data visibility, ES presence/version hints, and
  related-product evidence where observable.
- Do not automate ARI app-specific UI/API configuration, role assignment,
  secret-bearing Echo connections, Universal Forwarder rollout details,
  destructive data cleanup, index removal, app removal, or ES integration
  changes by default.
- Route Enterprise Security 8.5+ Exposure Analytics implementation detail to
  `splunk-enterprise-security-config`; only ARI Asset, IP, Mac, and User entity
  discovery sources belong in that mode.
- Keep normal ARI-to-ES integration separate from ES 8.5+ Exposure Analytics:
  normal mode covers asset/identity sync, swim lanes, workflow actions,
  `ari_lookup_host()`, `ari_lookup_ip()`, ES field mapping, `ari_risk_score`,
  and ES risk factors.
- Include related-product handoffs for ARI Technical Add-ons (Windows `7214`,
  Linux `7416`, macOS `7417`) and ARI Echo. Do not automate Echo installation
  until the Splunkbase ID/package name is locally verified.

Read `reference.md` for the official coverage map, app IDs, lifecycle surfaces,
and source links.

## MCP Tools

This skill includes checked-in, read-only Splunk MCP custom tools generated
from `mcp_tools.source.yaml`.

Validate or regenerate the tool artifact:

```bash
python3 portable local helper validate skills/splunk-asset-risk-intelligence-setup
python3 portable local helper generate skills/splunk-asset-risk-intelligence-setup
```

Load the tools into Splunk MCP Server:

```bash
bash source-repository automation (not bundled)
```

The loader uses the supported `/mcp_tools` REST batch endpoint by default. Use
`--allow-legacy-kv` only for older MCP Server app versions that lack that
endpoint.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
