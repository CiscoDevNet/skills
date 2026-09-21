# Submission notes

This migration is prepared against source commit
`c74a619301bca7ebcdc8323308402ca9d857966a` and CiscoDevNet baseline
`16ca54d351f793984f6768952e2c6c75b43007c7`.

The destination fork is `chambear2809/skills`, with `CiscoDevNet/skills` as
`upstream`. GitHub Issues are disabled on the fork, so the planned coordination
issue could not be opened; the complete manifest is retained in
`MIGRATION_MANIFEST.json` for maintainers to review.

The proposed 25-batch split is recorded per skill in the manifest: 10 Splunk
Platform, 1 Isovalent, 4 Splunk Observability, 2 ThousandEyes, 3 AppDynamics,
1 ITSI, and 4 Enterprise Security batches. New plugin manifests use `0.1.0`;
the existing ThousandEyes manifest remains on its current `0.1.0` version.

Validation completed locally:

- `python3 scripts/validate_skills.py`
- `python3 scripts/validate_migration.py`
- both marketplace files parse as JSON
- canonical/plugin skill trees are byte-identical
- selected skills contain no `agents/openai.yaml`, `scripts/`, or source-repository shared-helper paths

Semantic discovery against installed client/model runtimes and remote
`npx skills add CiscoDevNet/skills --list` discovery remain post-merge checks;
the fork is not the upstream repository and therefore cannot verify the final
remote discovery path before maintainers merge the contribution.
