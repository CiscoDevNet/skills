---
name: splunk-appdynamics-dual-agent-setup
description: >
  Use when the user asks for AppDynamics Java dual-agent, Java Dual Signal mode, AGENT_DEPLOYMENT_MODE=dual, -Dagent.deployment.mode=dual, Java OTLP export to a local collector, or coordinated collector-first then Java restart rollout on local or SSH hosts. Render, validate, preflight, apply, and rollback production Java Dual Signal AppDynamics agent configuration.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: appdynamics
  maturity: draft
---

# Splunk AppDynamics Dual Agent Setup

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

- The user asks for AppDynamics Java dual-agent, Java Dual Signal mode, AGENT_DEPLOYMENT_MODE=dual,
  -Dagent.deployment.mode=dual, Java OTLP export to a local collector, or coordinated collector-first then Java
  restart rollout on local or SSH.
- Preview and review the splunk appdynamics dual agent setup workflow before any live apply phase.
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

Owns production Java Dual Signal host configuration. The supported apply order
is collector first, Java second: configure and validate the local collector, then
write persistent Java startup settings and restart only approved app services.

```bash
bash source-repository automation (not bundled) --render
bash source-repository automation (not bundled) --apply preflight --spec dual-agent.yaml
bash source-repository automation (not bundled) --apply all --spec dual-agent.yaml --accept-host-mutation --accept-app-restart
bash source-repository automation (not bundled) --output-dir splunk-appdynamics-dual-agent-setup-rendered
```

## What This Skill Covers

- Java Dual Signal startup configuration using `AGENT_DEPLOYMENT_MODE=dual`
  or equivalent system properties.
- OTLP trace export to a local collector, defaulting to
  `http://127.0.0.1:4318` and `http/protobuf`.
- Resource attributes for application, tier, node, and deployment environment.
- Linux systemd drop-ins, process env files or wrappers, Docker env files, and
  Windows service environment guidance.
- Gated apply and rollback for local or SSH targets with backup manifests,
  checksum verification, redacted reports, and generated rollback plans.

## Guardrails

- `--accept-host-mutation` is required before writing files or restarting
  services.
- `--accept-remote-execution` is required for SSH targets.
- `--accept-app-restart` is required for Java service or container restarts.
- `--accept-full-restart` is required when `restart_strategy: full`.
- Direct token, access-token, and API key flags are refused; use file-backed
  fields in the spec.
- Referenced collector secret files must be non-empty and mode 600. Collector
  apply writes a target-side mode-600 environment file; Docker and Windows
  targets need an explicit `collector_credentials_ready_command`.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
