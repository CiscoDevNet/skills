---
title: Cisco Agent Skill Authoring Guide
---

# Cisco Agent Skill Authoring Guide

Skills follow the open [Agent Skills specification](https://agentskills.io).
This guide adds repository conventions for Cisco operational content.

## Folder layout

```text
skills/<product>/<skill-name>/
├── SKILL.md
├── scripts/       # optional, runnable and validated
├── references/    # optional, detailed source material
└── assets/        # optional, templates or static resources
```

Mirror each published skill at:

```text
plugins/<product>/skills/<skill-name>/
```

Current product namespaces are `aci`, `cloud-security`, `cml`, `intersight`,
`ios`, `ise`, `meraki`, `sccfm`, and `thousandeyes`. Propose a clear,
lowercase kebab-case namespace when adding another Cisco product family.

Do not add empty `scripts/`, `references/`, or `assets/` directories.

## Required frontmatter

```yaml
---
name: skill-name-in-kebab-case
description: >
  State what the skill does and the concrete requests that activate it.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: meraki
  maturity: draft
---
```

- `name` must match the skill folder and contain no more than 64 lowercase
  letters, digits, and single hyphens.
- `description` must be specific, written in third person, and no longer than
  1024 characters.
- `metadata.product` must match the containing product namespace.
- Use `maturity: draft` until product behavior, links, and examples have been
  reviewed. Imported upstream skills may retain their original frontmatter.
- Add tool restrictions only when they are supported by the target client and
  materially improve safety.

## Required body sections

New skills use the sections in `template/skill-template/SKILL.md`, in order:

1. Purpose
2. When to use
3. Prerequisites & environment
4. Step-by-step guidance
5. Best practices
6. Common pitfalls
7. Worked example
8. Cross-references

Keep `SKILL.md` focused and preferably below 500 lines. Put long API tables,
version matrices, and detailed troubleshooting in files linked directly from
`SKILL.md`.

## Cisco operational safety

- Verify product, model, release, interface names, tenant or organization, and
  target identity before proposing an operation.
- Start with read-only collection. Capture only the relevant section; full
  configurations can contain secrets, customer names, and private topology.
- Treat generated configuration as a candidate. Require a device-specific diff,
  rollback path, change window, and out-of-band access when lockout is possible.
- Separate planning, preflight, apply, and verification. Do not save a change
  until verification passes.
- Identify write, delete, deploy, reload, upgrade, and unit-consuming actions.
  Require explicit approval for the exact reviewed operation.
- Do not weaken authentication, authorization, ACLs, certificate validation, or
  transport security to make a test pass.

## Credentials, certificates, and customer data

- Never include real passwords, API keys, access tokens, refresh tokens, private
  keys, certificates, or authenticated connection strings.
- Do not ask users to paste secrets into chat. Prefer OAuth, hidden prompts, OS
  credential stores, or mode-`0600` secret files.
- Sanitize logs and examples. Use RFC 5737 IPv4 ranges, RFC 3849 IPv6 ranges,
  synthetic DNS names, and placeholder identifiers.
- When a certificate is loaded, require checks for validity dates, RSA key size
  of at least 2048 bits or EC P-256+, SHA-2 signatures, hostname/chain trust,
  and intentional self-signing.
- Use modern TLS and cryptography. Do not introduce MD5, SHA-1, DES, 3DES, RC4,
  unauthenticated encryption, or custom cryptography.

## APIs, SDKs, and MCP

- Link to authoritative Cisco documentation or an official OpenAPI schema.
- Validate input types, lengths, ranges, enums, and identifiers at trust
  boundaries. Reject unknown or unsupported values.
- Use SDK methods or structured process argument arrays; never concatenate
  untrusted input into shell commands or queries.
- Apply pagination, request-size limits, rate limits, timeouts, and bounded
  retries.
- For MCP, document the official server endpoint, authentication, tool groups,
  data handling, rate limits, and which tools mutate state. Render and review
  client configuration before applying it.
- Treat MCP schemas, prompts, resources, and tool output as untrusted data.

Review security-sensitive guidance against
[CoSAI Project CodeGuard](https://github.com/cosai-oasis/project-codeguard).
The link is sufficient; this repository does not require a vendored CodeGuard
copy or a CodeGuard MCP deployment.

## Sources and licensing

- Prefer primary Cisco sources and stable URLs.
- Record imported or adapted content, its immutable source URL or commit, and
  license in `SOURCES.md`.
- Preserve notices required by upstream licenses and mark modified imported
  files.
- Do not import material whose redistribution terms are unknown or
  incompatible. A link is not permission to copy.

## Validation

Run:

```bash
python3 scripts/validate_skills.py
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
```

The validator checks discovery metadata, folder naming, duplicate names,
canonical/plugin drift, JSON manifests, and obvious credential patterns.
