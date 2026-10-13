---
name: cisco-thousandeyes-mcp-setup
description: >
  Use when the user asks to register the ThousandEyes MCP, set up TE in Cursor/Claude/Codex/VS Code/Kiro, configure the Cisco ThousandEyes Cursor plugin, or pair an AI assistant with TE. Render and (optionally) apply Model Context Protocol client configurations for the official ThousandEyes MCP Server (https://api.thousandeyes.com/mcp, GA per docs.thousandeyes.com/.../thousandeyes-mcp-server). Supports Cursor, Claude Code, Codex, VS Code, and AWS Kiro clients with both OAuth Bearer and OAuth2 flows. Claude Code must use the Bearer token path (or a pre-registered OAuth client): zero-config OAuth2 fails because the server rejects dynamic client registration with localhost redirect URIs. Surfaces TE rate limits, the unit-consumption warning for Instant Tests, and gates the write/Instant- Test tool group behind an explicit acknowledgement.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: thousandeyes
  maturity: draft
---

# Cisco ThousandEyes MCP Server Setup

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

- Register the ThousandEyes MCP, set up TE in Cursor/Claude/Codex/VS Code/Kiro, configure the Cisco ThousandEyes
  Cursor plugin, or pair an AI assistant with TE.
- Preview and review the cisco thousandeyes mcp setup workflow before any live apply phase.
- Diagnose failed prerequisites, generated assets, configuration, or validation evidence.

## Scope

Follow the documented read-only or render-first path whenever it is available.
This skill does not imply permission to mutate live systems. Require explicit
apply flags, protected credentials, and operator review for state changes.

## Examples

> **Note:** The helper script referenced below is not bundled with this package
> (see the Portability note), so these commands cannot be run as written. For
> Claude Code, use the manual steps in "Claude Code setup" instead.

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
| Claude Code `/mcp` shows "needs authentication" and Authenticate fails with `Dynamic Client Registration rejected (HTTP 400) ... Invalid redirect_uris: [http://localhost:<port>/callback]` | Claude Code registers an OAuth client dynamically with a random-port localhost callback; the TE MCP server rejects that redirect URI, so zero-config OAuth2 cannot complete | Remove the server (`claude mcp remove thousandeyes -s user`) and use the Bearer token setup in "Claude Code setup", or a pre-registered OAuth client |
| Claude Code shows the server but no tools after registering | Session started before the server or `TE_TOKEN` was added | Restart Claude Code, then check `/mcp` |
| `claude mcp list` shows `Failed to connect ... HTTP 401 ... invalid_token` together with `Missing environment variables: TE_TOKEN` | `${TE_TOKEN}` is empty in the environment of the process running Claude Code, so an invalid Authorization header is sent. The token itself may be fine | Check `echo ${#TE_TOKEN}` is above 0 in the launching shell, `source ~/.zshrc` or open a new terminal, and restart `claude` from it. To test the token directly: `printf 'header = "Authorization: Bearer %s"\n' "$(cat ~/.te_api_token)" \| curl -s -o /dev/null -w '%{http_code}\n' -K - https://api.thousandeyes.com/mcp` (401 = bad token; 405 = token accepted) |
| `claude mcp remove thousandeyes -s user` says no such server, yet `claude mcp list` shows it | The entry is in `local` or `project` scope | Run the remove command with `-s local` or `-s project` |

This skill is **agent-tooling only** — it does not move telemetry. For TE → Splunk Observability Cloud wiring (OpenTelemetry stream, Integrations 2.0 APM connector, full TE asset lifecycle), use `splunk-observability-thousandeyes-integration`. For the Splunk Platform `ta_cisco_thousandeyes` add-on, use `cisco-thousandeyes-setup`.

## Overview

Render per-client MCP configurations for the official **ThousandEyes MCP Server** at `https://api.thousandeyes.com/mcp`. Optionally apply the configurations into the user's actual Cursor / Claude Code / Codex / VS Code / AWS Kiro config locations.

Render-first by default. Automated `--apply` is supported for Codex with OAuth2;
the other clients retain explicit reviewed manual merge handoffs.

## Safety Rules

- Never ask for the ThousandEyes API token in conversation.
- Never pass the token on the command line or as an environment-variable prefix.
- Use `--te-token-file` for the Bearer header path; the renderer never reads the token file.
- Reject direct token flags (`--te-token`, `--access-token`, `--token`, `--bearer-token`, `--api-token`).
- Token files must be `chmod 600`. `--apply` runs a permission preflight and aborts with a `chmod 600 <path>` hint when looser. `--allow-loose-token-perms` overrides with a `WARN`.
- Cursor and VS Code configs use `${input:te-key}` prompt-string patterns or environment variables, never inline tokens. Codex should use OAuth2 browser consent unless a client-side secret store can inject Bearer headers without argv exposure.
- **Claude Code must use the Bearer token path** with the token referenced as `${TE_TOKEN}` in the `Authorization` header, never inline. Do not register the server with plain `claude mcp add --transport http ...` and no credentials: the resulting zero-config OAuth2 flow fails (see Troubleshooting). A pre-registered OAuth client is the only OAuth alternative, and only after verifying that ThousandEyes accepts its callback URL.
- Do not pass the token via `claude mcp add --header "Authorization: Bearer <token>"`; that exposes it in shell history and process arguments.
- `--accept-te-mcp-write-tools` records explicit operator acknowledgement for the write/Instant-Test group (`Create/Update/Delete Synthetic Test`, `Run Instant Test`, `Deploy Template`). It does not silently change client permissions; follow the rendered per-client approval guidance.

## Primary Workflow

1. Decide which clients to register and which auth flow to use:

   - **OAuth Bearer Token**: simplest; one shared token file per client. Counts against the org-wide 240 req/min rate limit. **Required default for Claude Code.**
   - **OAuth2 client**: per-client OAuth2 flow with browser consent. Each OAuth2 client gets its own 240 req/min limit (recommended when multiple AI assistants share an org). Verified for Codex only. Not supported for Claude Code without a pre-registered client, because the server rejects dynamic client registration with localhost redirect URIs.

   When the user selects Claude Code, do not offer "OAuth2 browser consent" as the recommended option and do not register the server without credentials.

2. Render:

   ```bash
   bash source-repository automation (not bundled) \
     --render \
     --client cursor,claude,codex,vscode,kiro \
     --auth bearer \
     --te-token-file /tmp/te_api_token \
     --output-dir cisco-thousandeyes-mcp-rendered
   ```

3. Review `cisco-thousandeyes-mcp-rendered/`:

   - `mcp/cursor.mcp.json`
   - `mcp/claude.mcp.json`
   - `mcp/codex-register-te-mcp.sh`
   - `mcp/vscode.mcp.json`
   - `mcp/kiro.mcp.json`
   - `mcp/README.md` — per-client install instructions, rate-limit notes, unit-consumption warnings
   - `metadata.json`

4. Apply Codex OAuth2 registration only when explicitly requested. Cursor,
   Claude, VS Code, and Kiro remain reviewed manual config merges:

   ```bash
   bash source-repository automation (not bundled) \
     --apply \
     --client codex \
     --auth oauth2
   ```

## Claude Code setup (Bearer token)

Use these manual steps because the render/apply script is not bundled.

1. Create a token file readable only by the user. Do not paste the token into chat:

   ```bash
   install -m 600 /dev/null ~/.te_api_token
   ```

   Have the user add their ThousandEyes API token to it in an editor, and keep it out of version control.

2. Export it for new shells (for example in `~/.zshrc`):

   ```bash
   export TE_TOKEN="$(cat ~/.te_api_token)"
   ```

3. Reference the variable by name only, either in the project `.mcp.json`:

   ```json
   {
     "mcpServers": {
       "thousandeyes": {
         "type": "http",
         "url": "https://api.thousandeyes.com/mcp",
         "headers": { "Authorization": "Bearer ${TE_TOKEN}" }
       }
     }
   }
   ```

   or for user scope with `claude mcp add-json --scope user thousandeyes '<the JSON body above, without the mcpServers wrapper>'`.

   Keep the JSON in single quotes so the shell does not expand `${TE_TOKEN}`. Never use `$(cat ~/.te_api_token)` inside the command: the shell would expand it and write the real token in plaintext into `~/.claude.json` and shell history. After registering, confirm the saved entry still contains the literal text `${TE_TOKEN}` (use `claude mcp list`; do not print the header value).

4. If a zero-config entry already exists, remove it first. Entries can live in more than one scope (`claude mcp add` defaults to `local`), so check `-s user`, `-s local` and `-s project`: `claude mcp remove thousandeyes -s <scope>`.

5. Verify `TE_TOKEN` is set in the shell that will launch Claude Code, without printing it:

   ```bash
   echo ${#TE_TOKEN}   # must be greater than 0
   ```

   Claude Code expands `${TE_TOKEN}` from its own environment at startup. If the variable is empty, the header is invalid and the server answers HTTP 401 `invalid_token`, even when the token is valid. `claude mcp list` also shows `Missing environment variables: TE_TOKEN`. Shells and sessions opened before the `export` was added do not have it, and apps launched from a GUI do not read `~/.zshrc`; open a new terminal (or run `source ~/.zshrc`) and start `claude` from there. For a one-off test: `TE_TOKEN="$(cat ~/.te_api_token)" claude`.

6. Restart Claude Code from that shell, then run `/mcp` and confirm `thousandeyes` shows as connected with a tool count. Test with a read-only request such as listing tests.

### Optional: pre-registered OAuth client (unverified)

If ThousandEyes allows registering `http://localhost:<port>/callback` as a redirect URI for an OAuth client, Claude Code can use it with `claude mcp add --transport http --client-id <id> --client-secret --callback-port <port> thousandeyes https://api.thousandeyes.com/mcp`. Document this path as supported only after testing it against a real tenant.

## Tool Group Gating

The official ThousandEyes MCP Server exposes two tool groups:

- **Read-only tools** (auto-allowed): List/Get Tests, List/Get Events, List/Get Alerts, Search Outages, Get Anomalies, Get Metrics, Get Service Map, Views Explanations, Endpoint Agent Metrics + Connected Device, Cloud/Enterprise Agents, Get Path / Full Path / BGP Test Results / BGP Route Details, Get Account Groups, Search/Deploy Templates (Search only).
- **Write/Instant-Test tools** (require explicit per-client approval; `--accept-te-mcp-write-tools` records operator acknowledgement): Create/Update/Delete Synthetic Test, Run Instant Test, Deploy Template.

**Unit consumption.** Run Instant Test consumes ThousandEyes units identically to scheduled tests. The rendered README always surfaces this warning, and `--apply` refuses to enable write tools without `--accept-te-mcp-write-tools`.

## Hand-offs

- TE → Splunk Observability Cloud wiring → `splunk-observability-thousandeyes-integration` (OpenTelemetry stream, Integrations 2.0 APM connector, full TE asset lifecycle).
- Splunk Platform `ta_cisco_thousandeyes` add-on → `cisco-thousandeyes-setup` (HEC streaming inputs, OAuth device flow, indexes/sourcetypes).

## Validation

```bash
bash source-repository automation (not bundled)
```

Static checks confirm every selected client has a renderable config; verifies no token material was written to any rendered file. Use `--live` after `--apply` to reach `https://api.thousandeyes.com/mcp` from each client config.

For Claude Code, validate manually: `claude mcp get thousandeyes` should show the server, `/mcp` should show it connected after a restart, and a read-only tool call should succeed.

See `reference.md` for option details and `references/clients.md` for the per-client install matrix.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
