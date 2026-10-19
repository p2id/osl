# Autonomous Repository Governance Contract

## Status
Prepared on a dedicated branch. Not active until reviewed and merged, the required secret is configured, and a manual run is verified.

## Operating stages
1. Inventory the configured repositories and capture timestamped evidence.
2. Distinguish missing paths from inaccessible or nonexistent repositories.
3. Identify each repository's existing source-of-truth specification before implementation; extend it rather than creating competing specs.
4. Isolate any future changes on a dedicated branch with a narrow diff and auditable commit/PR.
5. Record exact test commands, outcomes, commit SHA, workflow URLs, and blockers. Never claim a check passed unless it actually ran and passed.
6. Never merge, publish, deploy, delete data, rotate secrets, or change access policy autonomously.

## Current autonomy boundary
This implementation is read-only with respect to target repositories. It does not edit their code, create issues/PRs in them, or run their project tests. Full autonomous development requires a separately reviewed coding-agent runner, repository-specific test commands, path allowlists, budgets/time limits, and branch/PR permissions.

## Required secret
Configure repository Actions secret AUDIT_GH_TOKEN in this governance repository. It must have read access to every configured repository. Use least privilege. Never print or persist the token. Missing secret or denied access must fail clearly.

## Schedule readiness
The workflow deliberately has workflow_dispatch only. Add a schedule only after a successful manual run, complete access verification, report accuracy checks, and a retention/write-back decision. GitHub scheduled workflows are best-effort and may be delayed.

## Evidence states
PASS = the check ran and met its stated condition.
FAIL = the check ran and did not meet its condition.
BLOCKED = permissions, secrets, tools, or environment prevented the check.
NOT_RUN = no execution was attempted.
UNKNOWN = evidence is insufficient.

## Safety
Reports may include repository names and diagnostics only. Never store source contents, tokens, environment variables, or private issue bodies.
