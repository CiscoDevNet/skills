---
name: splunk-appdynamics-k8s-cluster-agent-setup
description: >
  Use when the user asks for AppDynamics Cluster Agent, Kubernetes monitoring, AppDynamics Kubernetes auto-instrumentation, Splunk OTel Collector through Cluster Agent, O11y export, or workload rollout validation. Render, validate, and gate Splunk AppDynamics Kubernetes Cluster Agent, Kubernetes auto- instrumentation, and Splunk OpenTelemetry Collector setup through the Cluster Agent, including dual- signal combined-agent plans for Java, .NET Core Linux, Node.js, Machine Agent handoff, and Splunk Observability Cloud export validation.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: appdynamics
  maturity: draft
---

# Splunk AppDynamics Kubernetes Cluster Agent Setup

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

- The user asks for AppDynamics Cluster Agent, Kubernetes monitoring, AppDynamics Kubernetes auto-instrumentation,
  Splunk OTel Collector through Cluster Agent, O11y export, or workload rollout validation.
- Preview and review the splunk appdynamics k8s cluster agent setup workflow before any live apply phase.
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

Kubernetes mutations require `--accept-k8s-rollout`. Render mode writes Helm
values, O11y collector values, secret templates, combined-agent workload
patches, and validation runbooks without touching the active cluster.

```bash
bash source-repository automation (not bundled) --render
bash source-repository automation (not bundled)
```

Read-only Controller API validation for Cluster Agent availability can be run
with file-backed credentials:

```bash
bash source-repository automation (not bundled) \
  --application 'Server & Infrastructure Monitoring' \
  --duration-mins 5
```

The probe defaults to
`Application Infrastructure Performance|Root|Individual Nodes|*|Cluster Agent|Availability`
so it can read every visible Cluster Agent under Server Visibility. Pass
`--metric-path` only when you want to pin validation to a copied full path for
one Cluster Agent.

A disabled Server Visibility health rule for Cluster Agent availability can be
rendered first, then applied after the API client has Server health-rule
permissions:

```bash
bash source-repository automation (not bundled)

bash source-repository automation (not bundled) \
  --apply
```

Typical flow:

1. Edit `template.example` or pass `--spec <file>` with Controller, cluster,
   Splunk Observability realm, token file path, and workload targets.
2. Render first and review `cluster-agent-values.yaml`,
   `splunk-otel-collector-values.yaml`, `dual-signal-workload-env.yaml`, and
   `cluster-agent-rollout-plan.sh`.
3. Keep O11y tokens, the Controller password, and the Controller access key
   file-backed. The rollout plan uses `--set-file`; it does not render values.
4. Execute the reviewed rollout only after explicit approval:

```bash
bash source-repository automation (not bundled) \
  --apply rollout --accept-k8s-rollout --spec path/to/spec.yaml
```

The wrapper renders and then executes `cluster-agent-rollout-plan.sh` with the
mutation gate enabled. Running that rendered script directly remains dry-run by
default and requires `K8S_APPLY=1` before it mutates Kubernetes.

Controller URLs default to HTTPS. Plain HTTP requires the explicit
`accept_insecure_controller_http: true` exception. The O11y validation API is
restricted to `https://api.<realm>.signalfx.com`; a reviewed proxy additionally
requires `splunk_otel_collector.accept_custom_api_url: true`. Live O11y
validation fails when its chmod-600 token file, Helm-release pods, readiness, or
collector log access is unavailable; it never reports a skipped probe as a pass.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
