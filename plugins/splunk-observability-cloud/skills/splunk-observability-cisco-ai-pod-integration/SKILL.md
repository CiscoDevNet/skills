---
name: splunk-observability-cisco-ai-pod-integration
description: >
  Use when deploying Splunk Observability Cloud for a Cisco AI Pod with UCS, Nexus, NVIDIA GPUs, NIM/vLLM inference, and storage telemetry. Hand off base collector, HEC, dashboards, and detectors to the owning skills. Compose Cisco Nexus, Cisco Intersight, and NVIDIA GPU Observability skills into a Cisco AI Pod overlay, then add NIM, vLLM, Milvus, NetApp Trident, Pure Portworx, Redfish exporter, OpenShift SCC, workshop tenancy, RBAC, receiver naming, DCGM discovery, dual-pipeline filtering, NIM model-name extraction, and existing-collector cleanup patterns.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-observability-cloud
  maturity: draft
---

# Splunk Observability Cisco AI Pod Integration (Umbrella)

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

- Deploying Splunk Observability Cloud for a Cisco AI Pod with UCS, Nexus, NVIDIA GPUs, NIM/vLLM inference, and
  storage telemetry. Hand off base collector, HEC, dashboards, and detectors to the owning skills.
- Preview and review the splunk observability cisco ai pod integration workflow before any live apply phase.
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

This is the **AI Pod umbrella** that ties together every component skill needed for end-to-end Cisco AI Pod observability in Splunk Observability Cloud. It composes:

1. [splunk-observability-cisco-nexus-integration](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-observability-cloud/splunk-observability-cisco-nexus-integration) for Cisco Nexus 9000 fabric metrics (cisco_os receiver).
2. [splunk-observability-cisco-intersight-integration](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-observability-cloud/splunk-observability-cisco-intersight-integration) for Cisco UCS metrics via Intersight OTel deployment.
3. [splunk-observability-nvidia-gpu-integration](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-observability-cloud/splunk-observability-nvidia-gpu-integration) for NVIDIA GPU telemetry via DCGM Exporter.

And adds **AI-Pod-specific bits** documented in the configuration guide and production-validated by an OpenShift deployment:

- NIM scrapes (multi-job: llm/embedqa/rerankqa, port 8000 `/v1/metrics`).
- vLLM scrape (port 8000 `/metrics`).
- Milvus vector DB scrape (port 9091).
- NetApp Trident storage scrape (port 8001 `/metrics`).
- Pure Portworx storage scrape (ports 17001 + 17018).
- Redfish exporter (user-supplied) on port 9210.
- Cisco AI PODs Splunk Observability dashboard pipeline (`metrics/cisco-ai-pods`, unfiltered).
- NIM dashboard pipeline (`metrics/nvidianim-metrics`, unfiltered).
- `k8s_attributes/nim` processor for `app -> model_name` extraction.
- OpenShift SCC helper, `workshop/multi-tenant.sh`, and dual-pipeline filtering pattern.

## Critical production lessons encoded

These are the **silent failure traps** the umbrella prevents:

1. **RBAC gap**: base chart's ClusterRole grants only `pods` and `services`. Any `kubernetes_sd_configs.role: endpoints` scrape (e.g. NIM in endpoint mode) silently fails with `endpoints is forbidden`. The umbrella emits the `rbac.customRules` block with `endpoints` + `discovery.k8s.io/endpointslices` get/list/watch when needed.
2. **receiver_creator naming**: `receiver_creator/dcgm-cisco`, NOT `receiver_creator/nvidia` (collision with chart autodetect). Inherited from the GPU child skill.
3. **DCGM dual-label discovery**: matches both `app` and `app.kubernetes.io/name`. Inherited from the GPU child skill.
4. **Dual-pipeline filtering**: filtered standard pipeline + unfiltered specialized pipelines for AI Pod dashboards. Smarter than the canonical single-pipeline pattern.
5. **OpenShift defaults**: `kubeletstats.insecure_skip_verify: true` (REQUIRED), `certmanager.enabled: false`, `cloudProvider: ""`.
6. **Existing collector apply**: use `--apply-existing-collector` when a Splunk OTel Collector is already running. This path renders the overlay, reads current Helm values without persisting the token, removes stale `receiver_creator/nvidia`, wires `otlp` into the metrics pipeline for Intersight, applies via Helm, restarts the existing collector agent, restarts Intersight, and runs live validation.
7. **Helm token pattern**: apply source-repository automation (not bundled) use a file-backed token (`--set-file splunkObservability.accessToken=...`) so the token is never written to a tracked values file or temporary values file.

## Composition model

When you run `--render`, the umbrella:

1. Invokes each child skill's renderer to produce its overlay under a sub-directory.
2. Merges the child overlays into a unified `splunk-otel-overlay/values.overlay.yaml` with the renderer's deterministic Python deep-merge. The rendered base-collector handoff uses `yq` later to merge that reviewed overlay with base collector values.
3. Adds AI-Pod-specific blocks on top of the merged overlay.
4. Renders unified handoff source-repository automation (not bundled).

When you run `--apply-existing-collector`, the umbrella applies its rendered overlay to the already running Splunk OTel Collector Helm release instead of standing up a second collector.

## What it renders (composed + AI-Pod-specific)

- `splunk-otel-overlay/values.overlay.yaml` — composed overlay (Nexus + Intersight + GPU children + AI-Pod additions).
- `child-renders/<skill>/` — each child skill's full rendered output (preserved for debugging the merge).
- `intersight-integration/` — from the Intersight child.
- `secrets/cisco-nexus-ssh-secret.yaml` — from the Nexus child.
- `dcgm-pod-labels-patch/` — from the GPU child when `--enable-dcgm-pod-labels`.
- NIM, vLLM, Milvus, Trident, Portworx, and Redfish scrape configuration embedded in `splunk-otel-overlay/values.overlay.yaml`.
- `openshift/scc.sh` — OpenShift SCC helper script.
- `workshop/multi-tenant.sh` — Workshop multi-tenant deploy script (when `--workshop-mode`).
- `dashboards/` — AI-Pod-specific dashboards for NIM/vLLM inference, Milvus, and Trident/Portworx storage.
- `detectors/` — AI-Pod-specific detectors (vLLM error rate, NIM TTFT regression, Milvus query latency, Portworx node offline, Trident volume allocation).
- `source-repository automation (not bundled)` — emits the base collector + merge command with `--distribution openshift` (default).
- `source-repository automation (not bundled)` — for K8s container log shipping to Splunk Platform.
- `source-repository automation (not bundled)`, `handoff-detectors.sh` — emit reviewed dashboard and detector commands across all four skills.
- `source-repository automation (not bundled)` — prints the per-child contribution summary.
- `metadata.json`.

## Safety Rules

- File-backed token flags only:
  - `--o11y-token-file` (Splunk Observability Org access token; passed through to all child skills + base collector).
  - `--platform-hec-token-file` (optional; for K8s container logs to Splunk Platform).
  - `--intersight-key-id-file` and `--intersight-key-file` (passed through to the Intersight child).
- Reject every direct token / key flag.
- Token files must be `chmod 600`; `--allow-loose-token-perms` overrides with WARN.
- Cisco Nexus SSH credentials handled by the Nexus child (K8s Secret stub; user creates the Secret out-of-band).

## Primary Workflow

1. Confirm prerequisites are installed: NVIDIA GPU Operator (or standalone DCGM Exporter), NIM/vLLM with the standard pod labels, Milvus, NetApp Trident, Pure Portworx, Redfish exporter, Cisco Intersight account + API key.

2. Render the composed overlay:

   ```bash
   bash source-repository automation (not bundled) \
     --render --validate \
     --realm us0 \
     --cluster-name atl-ai-pod \
     --distribution openshift \
     --nim-scrape-mode endpoints \
     --enable-dcgm-pod-labels \
     --output-dir splunk-observability-cisco-ai-pod-rendered
   ```

3. If a Splunk OTel Collector is already running, apply the overlay in place and run live validation:

   ```bash
   bash source-repository automation (not bundled) \
     --render --apply-existing-collector --validate --live \
     --realm us0 \
     --cluster-name atl-ai-pod \
     --distribution openshift \
     --collector-release splunk-otel-collector \
     --collector-namespace splunk-otel \
     --o11y-token-file /path/to/o11y-token \
     --output-dir splunk-observability-cisco-ai-pod-rendered
   ```

4. For greenfield installs, apply child manifests (Intersight, optional DCGM patch) + merge overlay + apply via base collector:

   ```bash
   bash splunk-observability-cisco-ai-pod-rendered/source-repository automation (not bundled)
   bash splunk-observability-cisco-ai-pod-rendered/source-repository automation (not bundled)
   bash splunk-observability-cisco-ai-pod-rendered/source-repository automation (not bundled)
   ```

## Hand-offs

- Splunk OTel Collector base install: [splunk-observability-otel-collector-setup](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-observability-cloud/splunk-observability-otel-collector-setup) with `--distribution openshift` (default; configurable).
- HEC for K8s container logs: [splunk-hec-service-setup](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-platform/splunk-hec-service-setup).
- Dashboards: [splunk-observability-dashboard-builder](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-observability-cloud/splunk-observability-dashboard-builder).
- Detectors: [splunk-observability-native-ops](https://github.com/CiscoDevNet/skills/tree/main/skills/splunk-observability-cloud/splunk-observability-native-ops).
- Component skills (composed): Nexus / Intersight / GPU child skills.

## Out of scope

- All children's out-of-scope items (NVIDIA GPU Operator install, DCGM Exporter install, NIM/vLLM/Milvus/Trident/Portworx/Redfish exporter deployment, OpenShift cluster bootstrap, Cisco Intersight account creation).

## Validation

```bash
bash source-repository automation (not bundled)
```

Runs each child skill's `validate.sh` recursively, then checks the composed overlay, endpoint-discovery RBAC, OpenShift kubelet settings, and rendered secret safety. With `--live`, it probes collector and Intersight resources and logs plus the live collector ConfigMap. The umbrella validator does not make direct SignalFlow API probes for NIM, Milvus, or vLLM metrics.

With `--live`, validation prefers `oc`, falls back to `kubectl`, passes `--live` through to child validators, and fails on Intersight OTLP export errors such as `unknown service opentelemetry.proto.collector.metrics.v1.MetricsService`.

See `reference.md` and `references/composition-and-overlay-merge.md`, `nim-vllm-scrape-catalog.md`, `milvus-storage-redfish.md`, `openshift-scc.md`, `workshop-multi-tenant.md`, `ai-pod-dashboards-catalog.md`, `endpoints-rbac-patch.md`, `dual-pipeline-filtering.md`, `nim-scrape-modes.md`, `production-troubleshooting-reference.md`, `troubleshooting.md` for the full annexes.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
