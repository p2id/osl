# Autonomous Repository Governance Contract

## Status
Scheduled read-only inventory is implemented on a dedicated branch. It becomes active only after merge and secret setup. No code-repair agent is active.

## Operating stages
1. Discover all repositories visible to the token and union them with the explicit allowlist.
2. Capture timestamped metadata/path evidence and upload JSON/Markdown reports.
3. Distinguish missing paths from inaccessible or nonexistent repositories.
4. Before any implementation, identify and extend the repository's existing source-of-truth specification.
5. Isolate future code changes on dedicated branches and open auditable PRs.
6. Record exact test commands, outcomes, commit SHA, workflow URLs, and blockers. Never claim checks passed unless they ran and passed.
7. Never merge, publish, deploy, delete data, rotate secrets, or change access policy autonomously.

## Current capability boundary
The current workflow performs read-only repository metadata and selected path checks. It does not edit target repositories, run their builds/tests/security scans, or create PRs. Do not describe this implementation as a full autonomous software engineer.

## Secrets
- `AUDIT_GH_TOKEN`: read-only access to all intended repositories. Do not print or persist it.
- A future coding agent must use a separate write-limited credential and an AI provider key, stored only as Actions secrets. The inventory token must not be granted write access.

## Schedule
Workflow cron: `0 0 * * *` UTC (03:00 Asia/Baghdad, UTC+3). The schedule activates only when the workflow exists on the default branch. GitHub scheduled workflows are best-effort and may be delayed. Verify a manual run and inspect the artifact after merge.

## Evidence states
PASS = the check ran and met its stated condition.
FAIL = the check ran and did not meet its condition.
BLOCKED = permissions, secrets, tools, or environment prevented the check.
NOT_RUN = no execution was attempted.
UNKNOWN = evidence is insufficient.

## Safety
Reports may include repository names and diagnostics only. Never store source contents, tokens, environment variables, or user data. Never run untrusted build/test scripts while credentials are available in the environment.
