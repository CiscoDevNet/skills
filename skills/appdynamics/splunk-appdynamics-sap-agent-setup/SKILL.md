---
name: splunk-appdynamics-sap-agent-setup
description: >
  Use when the user asks for AppDynamics SAP Agent, ABAP Agent, HTTP SDK, SNP CrystalBridge Monitoring, BiQ Collector, SAP NetWeaver transports, SAP authorization runbooks, local or gateway HTTP SDK deployment, or SAP release or metric validation. Render, validate, and hand off Splunk AppDynamics SAP Agent workflows, including SAP Agent, ABAP Agent, HTTP SDK, SNP CrystalBridge Monitoring, BiQ Collector, local and gateway HTTP SDK deployment, SAP NetWeaver transports, SAP authorization checks, Controller node registration, SAP Agent release notes, and SAP metric validation.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: appdynamics
  maturity: draft
---

# Splunk AppDynamics SAP Agent Setup

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

- The user asks for AppDynamics SAP Agent, ABAP Agent, HTTP SDK, SNP CrystalBridge Monitoring, BiQ Collector, SAP
  NetWeaver transports, SAP authorization runbooks, local or gateway HTTP SDK deployment, or SAP release or metric
  validation.
- Preview and review the splunk appdynamics sap agent setup workflow before any live apply phase.
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

SAP transports and authorization changes are runbook-only. Agent command
snippets are rendered for SAP Basis/application teams to execute.

```bash
bash source-repository automation (not bundled) --render
bash source-repository automation (not bundled)
```


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
