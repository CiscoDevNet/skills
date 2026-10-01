---
name: splunk-amazon-kinesis-firehose-setup
description: >
  Use when the user asks to send AWS Firehose data to Splunk. Render and validate Amazon Kinesis Firehose to Splunk HEC onboarding for CloudTrail, VPC Flow Logs, CloudWatch events, and raw or JSON data, including HEC token/index handoffs, delivery stream settings, buffering, retry, S3 backup, IAM policy stubs, CloudWatch delivery metrics, ACK guidance, and strict source/sourcetype readiness evidence.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  product: splunk-platform
  maturity: draft
---

# Amazon Kinesis Firehose Setup

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

- Send AWS Firehose data to Splunk.
- Preview and review the splunk amazon kinesis firehose setup workflow before any live apply phase.
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

Render-first workflow for Amazon Kinesis Firehose delivery into Splunk HEC.
The skill emits HEC handoffs, Firehose destination settings, IAM and backup
stubs, delivery metric checks, validation SPL, and readiness evidence. It does
not create HEC tokens, AWS resources, or Splunk indexes directly.

## Workflow

```bash
bash source-repository automation (not bundled) --render \
  --index aws --hec-token-name aws_firehose_hec --source-profile cloudtrail \
  --s3-backup-bucket s3://example-firehose-backup --use-ack true
```

Review rendered `firehose-destination-settings.json.template`,
`iam-policy.stub.json`, and `install-commands.sh`, then delegate HEC token work
to `splunk-hec-service-setup` and AWS resource creation to the AWS owner.

## Execute

Preview the executable Splunk-side plan:

```bash
bash source-repository automation (not bundled) --all \
  --platform enterprise --token-file /path/to/hec-token-file --dry-run --json
```

Apply the Splunk-side HEC/index setup and run local validation:

```bash
bash source-repository automation (not bundled) --all \
  --platform enterprise --token-file /path/to/hec-token-file
```

Use `--platform cloud --write-token-file /path/to/output-token-file` for the
Cloud HEC token workflow. AWS Firehose delivery-stream creation remains an AWS
owner handoff from the rendered templates.

```bash
bash source-repository automation (not bundled) \
  --rendered-dir splunk-amazon-kinesis-firehose-rendered --live
```

See `reference.md` for the strict Firehose source/sourcetype matching contract.


## Portability note

This Cisco DevNet package preserves the source skill's operational guidance, references, templates, and assets. Source-repository `agents/openai.yaml` files and repository-coupled scripts/shared helpers are intentionally not bundled. Any omitted automation must be recreated with the target product's supported tools after read-only discovery, exact-target review, explicit approval, rollback preparation, and post-change validation. Keep secrets in local mode-0600 files and never paste them into chat, commands, or logs.
