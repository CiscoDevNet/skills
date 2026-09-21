# Dashboards catalog

## Table of contents

- [Per-test-type chart sets](#per-test-type-chart-sets)
- [`agent-to-server` / `agent-to-agent`](#agent-to-server-agent-to-agent)
- [`http-server`](#http-server)
- [`page-load`](#page-load)
- [`web-transactions`](#web-transactions)
- [`api` / `api-step`](#api-api-step)
- [`bgp`](#bgp)
- [`dns-server` / `dns-trace`](#dns-server-dns-trace)
- [`dnssec`](#dnssec)
- [`voice` (RTP-stream)](#voice-rtp-stream)
- [`sip-server`](#sip-server)
- [`ftp-server`](#ftp-server)
- [Adding test-type entries](#adding-test-type-entries)
- [Cross-referencing TE test ID](#cross-referencing-te-test-id)

The skill renders one starter SignalFlow dashboard spec per selected test type under `dashboards/<test_type>.signalflow.yaml`. Each spec is consumable by `splunk-observability-dashboard-builder` and follows that skill's chart-spec shape.

## Per-test-type chart sets

The chart program text is parameterized over `${ACCOUNT_GROUP_ID}` (your TE account group ID) and `${TEST_ID}` (the specific test you're filtering on). The dashboard-builder skill substitutes these per dashboard.

### `agent-to-server` / `agent-to-agent`

| Chart | Metric | Program text (templated) |
|-------|--------|--------------------------|
| Latency | `network.latency` | `data('network.latency', filter=filter('thousandeyes.account.id', '${ACCOUNT_GROUP_ID}') and filter('thousandeyes.test.id', '${TEST_ID}')).publish(label='network.latency')` |
| Loss | `network.loss` | `data('network.loss', ...)` |
| Jitter | `network.jitter` | `data('network.jitter', ...)` |

### `http-server`

| Chart | Metric |
|-------|--------|
| Availability | `http.server.request.availability` |
| Throughput | `http.server.throughput` |
| Client request duration | `http.client.request.duration` |

### `page-load`

| Chart | Metric |
|-------|--------|
| Page load duration | `web.page_load.duration` |
| Completion | `web.page_load.completion` |

### `web-transactions`

| Chart | Metric |
|-------|--------|
| Transaction duration | `web.transaction.duration` |
| Errors count | `web.transaction.errors.count` |
| Completion | `web.transaction.completion` |

### `api` / `api-step`

| Chart | Metric |
|-------|--------|
| Duration | `api.duration` |
| Completion | `api.completion` |
| Step duration | `api.step.duration` (api-step only) |
| Step completion | `api.step.completion` (api-step only) |

### `bgp`

| Chart | Metric |
|-------|--------|
| Path changes | `bgp.path_changes.count` |
| Reachability | `bgp.reachability` |
| Updates | `bgp.updates.count` |

### `dns-server` / `dns-trace`

| Chart | Metric |
|-------|--------|
| Availability | `dns.lookup.availability` |
| Duration | `dns.lookup.duration` |

### `dnssec`

| Chart | Metric |
|-------|--------|
| Validity | `dns.lookup.validity` |

### `voice` (RTP-stream)

| Chart | Metric |
|-------|--------|
| MOS | `rtp.client.request.mos` |
| Loss | `rtp.client.request.loss` |
| Discards | `rtp.client.request.discards` |
| Duration | `rtp.client.request.duration` |
| PDV | `rtp.client.request.pdv` |

### `sip-server`

| Chart | Metric |
|-------|--------|
| Availability | `sip.server.request.availability` |
| Duration | `sip.client.request.duration` |
| Total time | `sip.client.request.total_time` |

### `ftp-server`

| Chart | Metric |
|-------|--------|
| Availability | `ftp.server.request.availability` |
| Client request duration | `ftp.client.request.duration` |
| Throughput | `ftp.server.throughput` |

## Adding test-type entries

When ThousandEyes adds a new metric to an existing test type, update `PER_TYPE_METRICS` in `source-repository automation (not bundled)` and the matching table here. The test inventory itself is in `references/test-types-catalog.md`.

When ThousandEyes adds a brand-new test type:

1. Add the type to `VALID_TEST_TYPES` in `source-repository automation (not bundled)`.
2. Add a `PER_TYPE_METRICS[<new_type>]` entry with the canonical metric list.
3. Optionally add a `DEFAULT_DETECTORS[<new_type>]` entry for starter detectors.
4. Update `references/test-types-catalog.md` and this file.

## Cross-referencing TE test ID

Every TE test ID is reachable via `bash source-repository automation (not bundled)`. The dashboard-builder skill needs `${TEST_ID}` substituted per dashboard; if you want a single dashboard that aggregates across all tests of a type, drop the `thousandeyes.test.id` filter from the SignalFlow program and keep only the `thousandeyes.account.id` filter.
