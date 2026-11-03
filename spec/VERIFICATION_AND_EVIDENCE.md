# Verification and Evidence Rules

- Every run must identify its run ID, timestamp, branch and commit SHA.
- The JSON report is the machine-readable source for that run; Markdown is a human-readable rendering.
- Never infer a passing build/test from a README, badge, old log, or previous commit.
- A missing file is not the same as a missing repository.
- Distinguish HTTP 404 from 401/403 and rate limiting; 404 may mean absent or not visible.
- State exactly which checks ran and which did not.
- Never include tokens, secret values, environment dumps, source files, or user data.
- An artifact proves only what happened in that workflow run; it does not prove a schedule is enabled.

The initial implementation checks repository metadata and selected path presence only. It does not run builds/tests, security scans, mutate target repositories, open PRs, or deploy.
