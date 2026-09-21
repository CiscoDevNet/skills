---
name: widefield-okta-integration-setup
description: >
  Use when the user asks to connect WideField Security to Okta, configure Okta event hooks for WideField, validate shared-signal risk events, or build Okta evidence for WideField detect-and-remediate workflows. Render, validate, and safely apply the Okta side of a WideField Security integration, including OIN handoffs, Shared Signals receiver evidence, and documented Okta event hook creation, update, verification, or deactivation.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-enterprise-security
  maturity: draft
---

# WideField Okta Integration Setup

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

- Connect WideField Security to Okta, configure Okta event hooks for WideField, validate shared-signal risk events,
  or build Okta evidence for WideField detect-and-remediate workflows.
- Preview and review the widefield okta integration setup workflow before any live apply phase.
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

Prepare Okta integration assets for WideField Security. Live apply is limited
to documented Okta Event Hooks Management API operations.

## Workflow

1. Read `reference.md` before any live action.
2. Render the Okta packet:

```bash
bash source-repository automation (not bundled) --render \
  --okta-org-url https://example.okta.com \
  --receiver-url https://widefield.example.com/okta/events
```

3. Apply only documented event hook actions with file-backed credentials:

```bash
bash source-repository automation (not bundled) --apply --accept-apply \
  --okta-org-url https://example.okta.com \
  --okta-token-file /secure/okta/api_token \
  --receiver-url https://widefield.example.com/okta/events
```

4. Validate event hook and System Log reachability:

```bash
bash source-repository automation (not bundled) \
  --okta-org-url https://example.okta.com \
  --okta-token-file /secure/okta/api_token
```

The renderer emits `okta-oin-coverage.md` for the full OIN feature surface.
OIN assignment, shared-signal provider setup, federation, logout, workflow,
and provisioning features remain UI/provider handoffs unless public API
coverage is added to `reference.md`.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
