---
name: splunk-sysmon-ta-setup
description: >
  Use when the user asks to onboard, configure, render, or validate Microsoft Sysmon data in Splunk. Install, render, configure, and validate the Splunk Add-on for Microsoft Sysmon (Splunk_TA_microsoft_sysmon, Splunkbase 5709). Renders package-backed endpoint or Windows Event Collector WinEventLog inputs from extracted defaults, prevents duplicate direct-plus-WEC ingestion, hands off Universal Forwarder rollout, constrains readiness to the Sysmon source, and validates XmlWinEventLog Sysmon data. Use for Sysmon, WEC Sysmon, Microsoft Sysinternals Sysmon, or Splunk_TA_microsoft_sysmon onboarding.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-platform
  maturity: draft
---

# Splunk Add-on for Microsoft Sysmon Setup

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

- Onboard, configure, render, or validate Microsoft Sysmon data in Splunk.
- Preview and review the splunk sysmon ta setup workflow before any live apply phase.
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

Render-first automation for `Splunk_TA_microsoft_sysmon` (Splunkbase `5709`,
verified `5.0.1`). The renderer emits one collection mode at a time:
endpoint direct collection or Windows Event Collector. It does not install
Sysmon on endpoints.

## Workflow

Endpoint mode:

```bash
bash source-repository automation (not bundled) --render --mode endpoint --index sysmon
```

WEC mode:

```bash
bash source-repository automation (not bundled) --render --mode wec --index sysmon
```

Install and create the index:

```bash
bash source-repository automation (not bundled) --install --create-index --index sysmon
```

Roll out the rendered deployment app through `splunk-universal-forwarder-setup`
or `splunk-agent-management-setup`, then validate:

```bash
bash source-repository automation (not bundled) --index sysmon
```

Readiness handoff:

```bash
bash source-repository automation (not bundled) \
  --phase collect --source-pack sysmon
```


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
