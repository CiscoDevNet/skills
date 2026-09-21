# Apply And Safety Reference

## Render First

Every mode that can mutate live state must render first. Review `coverage-report.json` and `apply-plan.json` before running delegated apply source-repository automation (not bundled).

## Delegated Apply Commands

Use exact child-skill flags:

- Collector Kubernetes: `splunk-observability-otel-collector-setup/source-repository automation (not bundled) --apply-k8s`
- Collector Linux: `splunk-observability-otel-collector-setup/source-repository automation (not bundled) --apply-linux`
- HEC: `splunk-hec-service-setup/source-repository automation (not bundled) --phase apply`
- Log Observer Connect: `splunk-observability-cloud-integration-setup/source-repository automation (not bundled) --apply log_observer_connect`
- Dashboards: `splunk-observability-dashboard-builder/source-repository automation (not bundled) --apply`
- Detectors: `splunk-observability-native-ops/source-repository automation (not bundled) --apply`

## Non-Automated Surfaces

Keep these as `deeplink` or `handoff` unless a documented public API is added and live validation tests exist:

- Observability `Settings > AI Agent Monitoring` connection/index selection.
- Log Observer Connect wizard completion.
- Native APM Agents page, traces, and troubleshooting workflows.
- Product-native AI Infrastructure Monitoring navigators.

## Secret Handling

Reject direct secret flags. File paths are acceptable; secret values are not. The generated commands may pass paths such as `--o11y-token-file /tmp/token`, but must never include token contents.
