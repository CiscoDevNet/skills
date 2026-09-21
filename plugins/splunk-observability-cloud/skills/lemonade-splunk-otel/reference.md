# Lemonade Splunk OpenTelemetry Reference

| Need | Load |
|---|---|
| Debian/Ryzen AI discovery, upgrade, rollback | `references/debian-runbook.md` |
| macOS Keychain to protected runtime file | `references/keychain.md` |
| Source-to-backend validation ladder | `references/validation.md` |

Packaged assets:

- `assets/lemonade-trixie-backports.sources`: example Debian backports source.
- `assets/splunk-otel-collector.list`: example Splunk collector APT source.
- `source-repository automation (not bundled)`: deterministic full-config renderer.
- `source-repository automation (not bundled)`: strict static validation and optional exact-binary
  production validation.
- `source-repository automation (not bundled)`: privacy-safe OpenInference/GenAI canary.
- `source-repository automation (not bundled)`: exact-realm and organization-bound Splunk
  APM trace readback with all-segment validation and sanitized evidence.
- `source-repository automation (not bundled)`: sanitized loopback health/counter snapshots
  and before/after deltas for exact v0.156 metrics.
- `source-repository automation (not bundled)`: value-free semantic YAML change paths for
  reviewing normalized generated configs without exposing literal values.
- `source-repository automation (not bundled)`: Linux/root-only schema-v2 transaction with
  current-generation ownership, durable phase recovery, host/package/binary/
  unit provenance, exact systemd-state proof, config-only recovery on runtime
  drift, exact metadata preservation, and resumable restore.
- `source-repository automation (not bundled)`: root-only Splunk ingest-token
  cutover preflight that permits only one environment-file value to change,
  requires private files and protected ancestry, and delegates to the
  crash-durable apply/restore transaction with an exact live-file hash.

Source baseline researched on 2026-07-11: Lemonade v10.10.0. Re-run source
and installed-version discovery before acting because package and telemetry
behavior can change.
