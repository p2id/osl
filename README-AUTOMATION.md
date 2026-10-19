# Repository Governance Automation

This branch prepares a scheduled, read-only inventory for repositories visible to the configured GitHub token.

## Daily schedule
The workflow contains a GitHub Actions cron of `0 0 * * *` UTC, corresponding to 03:00 in Iraq (Asia/Baghdad, UTC+3). GitHub scheduled workflows are best-effort and may be delayed. The schedule only becomes active after this PR is merged into the repository's default branch.

## Required setup
1. Merge this PR after review.
2. Open Settings → Secrets and variables → Actions.
3. Add `AUDIT_GH_TOKEN` with read-only access to all intended repositories. Never use a write-enabled token for inventory.
4. Open Actions → Repository Governance Audit and run it manually.
5. Download the audit artifact and inspect `inventory.md` and `inventory.json`.
6. Verify all repositories are covered and no access failures are unexplained.

## What runs
- Dynamically discovers repositories visible to the token, plus the explicit configured allowlist.
- Checks repository metadata and selected files/paths.
- Produces JSON and Markdown evidence artifacts with 90-day retention.
- Fails non-zero if any repository is blocked, partially inspected, or not found/visible.

## What does not run
- It does not edit target repositories, create issues or PRs, execute project builds/tests, run security scanners, merge, or deploy.
- A PASS means metadata and the configured path checks succeeded; it does not mean the source code is correct.
- It is not yet an autonomous coding/repair agent.

## Next stage for autonomous development
A coding-agent runner requires an AI provider credential, a GitHub token with branch/PR write access, explicit repository/path allowlists, repository-specific test policies, isolated execution, and a reviewed approval boundary. Those credentials cannot be created by committing files. Do not grant write access to the inventory token.
