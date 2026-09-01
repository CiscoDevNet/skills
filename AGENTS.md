# Agent guidance for Cisco Agent Skills

This repository contains portable Agent Skills, not a product SDK or a
collection of paste-ready production configurations. Keep guidance grounded in
current Cisco documentation and safe for operators to review before use.

## Repository model

- Canonical portable content lives at `skills/<product>/<skill>/SKILL.md`.
- Marketplace packages live at `plugins/<product>/skills/<skill>/SKILL.md`.
- Canonical and packaged copies of a skill must remain byte-identical.
- Every skill directory must contain `SKILL.md`; add `scripts/`, `references/`,
  or `assets/` only when they contain material the skill actually uses.
- Product and skill names use lowercase kebab-case. The frontmatter `name` must
  exactly match the skill directory name.
- Start new work from `template/skill-template/SKILL.md` and follow
  `spec/authoring-guide.md`.

## Authoritative documentation

Prefer primary, current sources:

- Cisco documentation: https://www.cisco.com/c/en/us/support/index.html
- Cisco developer documentation: https://developer.cisco.com/docs/
- Cisco API catalog: https://developer.cisco.com/docs/apis/
- Cisco DevNet Sandboxes: https://devnetsandbox.cisco.com/DevNet
- Agent Skills specification: https://agentskills.io
- Agent Skills reference implementation:
  https://github.com/agentskills/agentskills
- CoSAI Project CodeGuard:
  https://github.com/cosai-oasis/project-codeguard

For Cisco Secure Access authorization examples, use the current published API
specification:

https://pubhub.devnetcloud.com/media/cloud-security-apis-in-eft/docs/secure-access/reference/auth/cisco_secure_access_token_authorization_api_2_0_0.yaml

Do not infer an endpoint, option, model identifier, or supported version when a
schema, installed CLI help, SDK reference, or product documentation can verify
it. Record source URLs and version constraints in the skill.

## MCP and external tools

MCP servers are optional unless a skill explicitly declares one as a
prerequisite. Prefer official Cisco-hosted MCP servers and document:

1. the official endpoint and documentation;
2. supported authentication flows;
3. read-only versus mutating tool groups;
4. rate limits and usage impact;
5. a render/review step before editing client configuration.

Never ask users to paste tokens, passwords, private keys, or session material
into chat. Use hidden prompts, OS credential stores, or permission-restricted
secret files. Do not commit generated client configuration containing secrets.

## Skill authoring rules

- Write a specific third-person description containing both capability and
  activation triggers.
- Keep the main `SKILL.md` concise; move detailed material into directly linked
  reference files.
- Start operational workflows with read-only discovery and current-state
  capture.
- Treat generated device configuration as a candidate, not as approved
  production configuration.
- For changes, require exact targets, rollback steps, out-of-band access where
  relevant, and before/after verification.
- Do not save, commit, deploy, or apply a change merely because a command was
  accepted.
- Use placeholders such as `YOUR_ORG_ID` and `${TOKEN_FILE}`. Never include real
  customer names, addresses, topology, credentials, or certificates.
- Validate untrusted input and use structured process execution. Never build
  shell commands by concatenating untrusted values.
- If certificate files are referenced, require verification of validity dates,
  key strength, signature algorithm, hostname/chain trust, and whether
  self-signing is intentional.

## Validation

Run from the repository root:

```bash
python3 scripts/validate_skills.py
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
```

If Claude Code tooling is installed, also run:

```bash
claude plugin validate .
```

For a product workflow, use a suitable
[Cisco DevNet Sandbox](https://devnetsandbox.cisco.com/DevNet) when one exists.
Do not test mutating instructions against production.

## Pull requests

- Keep one product or coherent workflow per pull request.
- Explain source documentation, tested versions, validation performed, and any
  live-testing gaps.
- Update both canonical and plugin copies.
- Preserve upstream attribution in `SOURCES.md`.
- Do not commit credentials, tokens, generated customer data, local reference
  repositories, or private topology.
- Preserve backward compatibility unless fixing unsafe or incorrect guidance;
  document behavior changes.
