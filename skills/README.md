# Cisco Agent Skills catalog

Skills are grouped by Cisco, Splunk, AppDynamics, and partner-product
namespace. The migrated namespaces contain 167 self-contained skills:

- `appdynamics/` — AppDynamics (20)
- `isovalent/` — Isovalent (1)
- `splunk-enterprise-security/` — Splunk Enterprise Security and WideField (18)
- `splunk-itsi/` — Splunk IT Service Intelligence (2)
- `splunk-observability-cloud/` — Splunk Observability Cloud and Galileo (36)
- `splunk-platform/` — Splunk Platform, Enterprise, Cloud, and integrations (87)
- `thousandeyes/` — Cisco ThousandEyes integrations (3)

Existing Cisco namespaces remain available: `aci/`, `cloud-security/`, `cml/`,
`intersight/`, `ios/`, `ise/`, `meraki/`, and `sccfm/`.

Each installable child directory contains a `SKILL.md`. Category `README.md`
files reserve and explain product scope; they are not skills and are not loaded
by agents.

Start new content from
[`template/skill-template`](../template/skill-template/SKILL.md) and follow the
[`spec/authoring-guide.md`](../spec/authoring-guide.md).
