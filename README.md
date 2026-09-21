# Cisco Agent Skills

Reusable [Agent Skills](https://agentskills.io) for Cisco products, Splunk
platforms, AppDynamics, Observability, and adjacent operational workflows.
Each skill is a self-contained folder with a `SKILL.md` file that compatible
coding agents load only when a request matches its description.

The migrated catalog adds 167 skills in seven namespaces:

- `splunk-platform/` — Splunk Platform, Cloud Platform, Enterprise, collectors,
  applications, Cisco integrations, and data-source add-ons (87).
- `splunk-observability-cloud/` — Splunk Observability Cloud, Galileo, Lemonade,
  and telemetry integrations (36).
- `splunk-enterprise-security/` — Enterprise Security, security portfolio, and
  WideField workflows (18).
- `appdynamics/` — AppDynamics administration, agents, monitoring, and
  integrations (20).
- `thousandeyes/` — ThousandEyes and cross-product integrations (3).
- `splunk-itsi/` — ITSI lifecycle and configuration (2).
- `isovalent/` — Isovalent platform installation (1).

The existing Cisco namespaces remain available alongside the migrated catalog.
The migration manifest and source attribution are recorded in
[`MIGRATION_MANIFEST.json`](MIGRATION_MANIFEST.json) and [`SOURCES.md`](SOURCES.md).

## Installation

The remote for this project is
[`CiscoDevNet/skills`](https://github.com/CiscoDevNet/skills). The `npx` and
marketplace options require that repository to be published and accessible.

### Option 1: `npx skills`

Use the community installer with any Agent Skills-compatible client:

```bash
# Preview discovered skills
npx skills add CiscoDevNet/skills --list

# Install one skill
npx skills add CiscoDevNet/skills --skill cisco-ios-patterns

# Install all skills
npx skills add CiscoDevNet/skills --all
```

### Option 2: Claude Code Marketplace

```text
/plugin marketplace add CiscoDevNet/skills
/plugin install ios@cisco-skills
/plugin install sccfm@cisco-skills
/plugin install splunk-platform@cisco-skills
/plugin install splunk-observability-cloud@cisco-skills
/plugin install appdynamics@cisco-skills
```

Other product plugins can be installed with
`/plugin install <product>@cisco-skills` after that product contains a reviewed
skill.

### Option 3: Clone and copy manually

```bash
git clone https://github.com/CiscoDevNet/skills.git cisco-agent-skills

# Copy one product catalog into a project-level skills directory
cp -R cisco-agent-skills/skills/ios/* .agents/skills/

# Or copy one skill
cp -R cisco-agent-skills/skills/sccfm/sccfm-cli .agents/skills/
```

Use the equivalent directory for your client, such as `.claude/skills/`,
`.cursor/skills/`, or `.github/skills/`.

## Repository layout

```text
.
├── .agents/plugins/marketplace.json    # cross-agent marketplace catalog
├── .claude-plugin/marketplace.json     # Claude Code marketplace catalog
├── plugins/<product>/                  # installable product plugin packages
│   ├── .claude-plugin/plugin.json
│   └── skills/<skill>/SKILL.md
├── skills/<product>/<skill>/SKILL.md   # portable canonical catalog
├── spec/authoring-guide.md
├── template/skill-template/SKILL.md
└── scripts/validate_skills.py
```

The `skills/` tree is optimized for open-standard discovery and manual
installation. The `plugins/` tree packages the same reviewed content for
marketplace clients. Run the repository validation before opening a pull
request to ensure mirrored copies have not drifted.

## Authoring and security

Read [the authoring guide](spec/authoring-guide.md) before adding a skill.
Examples must use placeholders instead of real credentials, default to
read-only discovery, and require explicit review before potentially disruptive
changes.

This repository follows the open
[Agent Skills specification](https://github.com/agentskills/agentskills).
Security guidance should also be checked against
[CoSAI Project CodeGuard](https://github.com/cosai-oasis/project-codeguard).
CodeGuard is linked as an upstream reference; vendoring or running its MCP
server is optional and is not required to use these skills.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Imported material and source commits
are recorded in [SOURCES.md](SOURCES.md).

## License

Licensed under Apache 2.0. See [Apache License 2.0. LICENSE](LICENSE). Third-party source attribution is
recorded in [SOURCES.md](SOURCES.md).
