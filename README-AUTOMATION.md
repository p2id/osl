# Repository Governance Automation

This branch adds a safe, manual-first inventory system for the configured GitHub repositories.

## Before first run
1. Merge this branch after reviewing it.
2. Open Settings → Secrets and variables → Actions → New repository secret.
3. Add AUDIT_GH_TOKEN with read access to all configured repositories. Do not use a write-enabled token for the read-only inventory stage.
4. Open Actions → Repository Governance Audit → Run workflow.
5. Download the audit artifact and inspect inventory.md and inventory.json.
6. Resolve BLOCKED, PARTIAL, or NOT_FOUND_OR_NOT_VISIBLE results before enabling a schedule.

## Prepared
- Explicit allowlist of 11 currently visible repositories.
- Read-only GitHub API inventory.
- JSON and Markdown reports.
- 90-day artifact retention.
- Manual workflow dispatch, secret validation, syntax/config checks, and honest failure status.

## Intentionally not enabled
- No cron schedule yet.
- No cross-repository writes.
- No automatic code generation, issue/PR creation, merging, publishing, or deployment.
- No claim that project tests have run.

This is an auditable foundation, not yet a full autonomous software engineer. Do not enable scheduling until the manual run and access coverage are verified.
