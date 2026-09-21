---
name: splunk-appdynamics-infrastructure-visibility-setup
description: >
  Use when the user asks for AppDynamics Machine Agent, Server Visibility, Network Visibility, Docker or container visibility, service availability, server tags, host metrics, or infrastructure health rules, NVIDIA GPU monitoring, DCGM, NVIDIA-SMI, or Prometheus exporter monitoring through Machine Agent. Render and validate Splunk AppDynamics Infrastructure Visibility workflows, including Machine Agent, Server Visibility, Network Visibility, Docker and container visibility, service availability, server tags, GPU Monitoring, Prometheus extension coverage, and infrastructure health rules.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: appdynamics
  maturity: draft
---

# Splunk AppDynamics Infrastructure Visibility Setup

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

- The user asks for AppDynamics Machine Agent, Server Visibility, Network Visibility, Docker or container
  visibility, service availability, server tags, host metrics, or infrastructure health rules, NVIDIA GPU
  monitoring, DCGM, NVIDIA-SMI,.
- Preview and review the splunk appdynamics infrastructure visibility setup workflow before any live apply phase.
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

Owns Machine Agent and infrastructure visibility plans. Privileged host or
network-agent changes are rendered for review.
The generated command plan is non-mutating and `--apply` fails closed; operators
must execute the reviewed host/API runbook or delegate collector configuration
to `splunk-appdynamics-machine-agent-otel-collector-setup`.

```bash
bash source-repository automation (not bundled) --render
bash source-repository automation (not bundled)
```


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
