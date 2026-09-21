---
name: widefield-saviynt-integration-setup
description: >
  Use when the user asks to connect WideField Security to Saviynt, map WideField detections to Saviynt remediation policies, or collect Saviynt evidence while failing closed for unsupported live Saviynt mutation. Render and validate Saviynt Identity Cloud remediation mappings for WideField Security findings, including access revocation, password reset, and micro-certification handoffs.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-enterprise-security
  maturity: draft
---

# WideField Saviynt Integration Setup

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

- Connect WideField Security to Saviynt, map WideField detections to Saviynt remediation policies, or collect
  Saviynt evidence while failing closed for unsupported live Saviynt mutation.
- Preview and review the widefield saviynt integration setup workflow before any live apply phase.
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

Render Saviynt remediation maps for WideField findings. Live Saviynt mutation
is disabled until official Saviynt or customer-provided API documentation is
added to `reference.md`.

## Workflow

```bash
bash source-repository automation (not bundled) --render \
  --saviynt-tenant-url https://example.saviyntcloud.com
```

Validate customer-supplied remediation evidence:

```bash
bash source-repository automation (not bundled) \
  --evidence-file ./widefield-saviynt-evidence.local.json
```

Validation fails closed when the evidence file is omitted, is not valid JSON,
or lacks a revoke, password-reset, micro-certification, or remediation outcome
marker. `--dry-run` is the only validation mode that does not require evidence.

## Remediation Map

- Compromised identity: revoke access.
- Weak or stale credential: password reset.
- Anomalous entitlement/session: micro-certification.

Do not infer or call Saviynt write APIs from examples or assumptions.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
