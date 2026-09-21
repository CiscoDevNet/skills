---
name: splunk-observability-browser-rum-setup
description: >
  Use when the user asks for Splunk Browser RUM, JavaScript RUM, @splunk/otel-web, source maps, frontend Session Replay, DXA prerequisites, or non-Kubernetes browser instrumentation. Render, validate, apply, and hand off generic Splunk Observability Cloud Browser RUM and Session Replay setup for web applications outside the Kubernetes injection path, including CDN snippets, npm/TypeScript initialization, Next.js/Vite/ Webpack source-map upload helpers, CSP headers, Session Replay privacy controls, RUM-to-APM Server-Timing trace linking validation, and dashboard or detector handoffs.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-observability-cloud
  maturity: draft
---

# Splunk Observability Browser RUM Setup

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

- The user asks for Splunk Browser RUM, JavaScript RUM, @splunk/otel-web, source maps, frontend Session Replay, DXA
  prerequisites, or non-Kubernetes browser instrumentation.
- Preview and review the splunk observability browser rum setup workflow before any live apply phase.
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

Use this skill for Browser RUM instrumentation that belongs in the web app
source tree, build pipeline, CDN HTML template, or server-rendered frontend. For
Kubernetes pod-side, ingress, or initContainer injection, use
`splunk-observability-k8s-frontend-rum-setup`.

The workflow is render-first. It does not embed RUM token values. Rendered
snippets reference a build-time variable or placeholder and keep the
server-to-server Observability API token for source-map upload in
`SPLUNK_O11Y_TOKEN_FILE`.

## Workflow

1. Render snippets for the framework or deployment path:

```bash
bash source-repository automation (not bundled) --render \
  --application-name checkout-web \
  --environment prod \
  --realm us1 \
  --version "${APP_VERSION:?set application version}" \
  --framework vite \
  --enable-session-replay
```

2. Review `browser-rum-plan.md`, `cdn-snippet.html`,
   `npm-init.ts`, `source-map-upload.sh`, and `csp-header.txt`.

3. Add the selected snippet to the application build or HTML template. Keep the
   same `applicationName` and `version` values in source-map uploads.

4. Validate the deployed site and endpoint reachability:

```bash
bash source-repository automation (not bundled) \
  --rendered-dir splunk-observability-browser-rum-rendered \
  --check-url https://shop.example.com
```

5. After reviewing the rendered helper, inject and upload source maps from a
   completed frontend build:

```bash
chmod 600 /path/to/o11y-token
bash source-repository automation (not bundled) \
  --upload-source-maps \
  --output-dir splunk-observability-browser-rum-rendered \
  --assets-dir /path/to/app/dist \
  --token-file /path/to/o11y-token
```

6. Hand off dashboards to `splunk-observability-dashboard-builder`, detectors to
   `splunk-observability-native-ops`, and missing backend trace headers to the
   appropriate APM or auto-instrumentation skill.

## Guardrails

- Never paste RUM tokens or Observability API tokens into chat or argv.
- Session Replay requires explicit privacy review before enablement.
- Source maps are server-to-server uploads; use an org/API token file, not the
  browser-embedded RUM token.
- `--upload-source-maps` requires an existing rendered helper, an existing build
  directory, and a token file with mode `0600` or `0400`; it never accepts a
  token value on argv.
- Keep CSP `script-src` and `connect-src` aligned with the selected CDN and
  `rum-ingest.<realm>.observability.splunkcloud.com`.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
