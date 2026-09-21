---
name: splunk-attack-analyzer-setup
description: >
  Use when a user asks for Attack Analyzer, SAA, phishing and malware analysis data ingestion, the `saa` index, `saa_indexes` macro, or Enterprise Security adaptive response readiness. Install, configure readiness, and validate Splunk Attack Analyzer platform integration using Splunk Add-on for Splunk Attack Analyzer (`Splunk_TA_SAA`, app 6999) and Splunk App for Splunk Attack Analyzer (`Splunk_App_SAA`, app 7000).
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-enterprise-security
  maturity: draft
---

# Splunk Attack Analyzer Setup

## Workflow Overview

```text
┌───────────┐   ┌───────────────┐   ┌───────────────┐   ┌─────────────────┐
│ Preflight │ → │ Render/review │ → │ Apply/handoff │ → │ Validate evidence │
└───────────┘   └───────────────┘   └───────────────┘   └─────────────────┘
```

## When to Activate

- A user asks for Attack Analyzer, SAA, phishing and malware analysis data ingestion, the `saa` index, `saa_indexes`
  macro, or Enterprise Security adaptive response readiness.
- Preview and review the splunk attack analyzer setup workflow before any live apply phase.
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

## TA Completion Gate

For every TA/add-on or dashboard companion run, satisfy the shared
[TA completion gate](#portability-note): configure and enable the
data ingest path owned by this skill or its required companion, validate events
or metrics in the target indexes/source types, and verify any
pre-built/package-shipped dashboards are visible, macro-aligned, and returning
data. If the package ships no dashboards, record that evidence explicitly and
hand off dashboard use to the consuming app, ES/ITSI/ARI content, or readiness
doctor.

Use this skill for the Splunk platform side of Splunk Attack Analyzer.

## Prerequisites

- A Splunk credentials file readable by the shared credential helper. If not
  yet configured, run
  `bash portable local helper`
  or copy `credentials.example` and edit it (`chmod 600 credentials`).
- Both Splunkbase apps come from the
  [`splunk-app-install`](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-platform/splunk-app-install) skill via
  `source-repository automation (not bundled)`. This wrapper handles
  Splunkbase auth, ACS upload, and version pinning so the Attack Analyzer
  setup never embeds those flows.
- Splunkbase lists both packages through platform `10.5`. In this repository,
  that is the current Splunk Cloud target; the self-managed Enterprise default
  remains `10.4.1`. Do not reinterpret the cross-product listing as validation
  of a self-managed Enterprise `10.5` deployment.

## Primary Commands

Preview:

```bash
bash source-repository automation (not bundled) --dry-run --json
```

Install app/add-on, prepare `saa`, configure the dashboard macro, and validate:

```bash
bash source-repository automation (not bundled)
```

Validate only:

```bash
bash source-repository automation (not bundled)
```

## Agent Behavior

- Install both `Splunk_TA_SAA` and `Splunk_App_SAA` by default. The add-on is
  installed first; if it fails the dashboard app is **not** attempted, and if
  the dashboard install fails after the add-on succeeded the script prints a
  rollback hint pointing at
  `source-repository automation (not bundled)`.
- Create or validate the events index, defaulting to `saa`.
- Configure the app macro `saa_indexes` to the selected index.
- Never ask for or pass the Attack Analyzer API key in chat or argv; use
  `--api-key-file` only for readiness checks and operator handoff.
- Treat tenant connection and input creation as a licensed tenant workflow
  unless a supported app REST contract is verified in the target deployment.

Read `reference.md` for source links, app IDs, and handoff notes.

## MCP Tools

This skill includes checked-in, read-only Splunk MCP custom tools generated
from `mcp_tools.source.yaml`.

Validate or regenerate the tool artifact:

```bash
python3 portable local helper validate skills/splunk-attack-analyzer-setup
python3 portable local helper generate skills/splunk-attack-analyzer-setup
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
