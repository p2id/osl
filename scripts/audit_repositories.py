#!/usr/bin/env python3
"""Read-only inventory of configured GitHub repositories; no source-code writes."""
import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "repositories.json"
OUT = pathlib.Path(os.environ.get("AUDIT_OUTPUT_DIR", "audit-output"))
API = os.environ.get("GH_API_URL", "https://api.github.com").rstrip("/")
TOKEN = os.environ.get("AUDIT_GH_TOKEN", "").strip()
KEY_PATHS = ["README.md", "pyproject.toml", "package.json", "Cargo.toml", "go.mod",
             "requirements.txt", "Dockerfile", "docker-compose.yml",
             ".github/workflows", "docs/spec/MASTER_SPEC.md", "SPEC.md", "spec/MASTER_SPEC.md"]

def request(path):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + TOKEN,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "repository-governance-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            body = response.read()
            return response.status, json.loads(body.decode("utf-8")) if body else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code == 404:
            return 404, {"message": "Not found or not visible to this token"}
        if exc.code == 403 and exc.headers.get("X-RateLimit-Remaining") == "0":
            return 429, {"message": "GitHub API rate limit exhausted"}
        return exc.code, {"message": body[:400]}
    except (urllib.error.URLError, TimeoutError) as exc:
        return 0, {"message": str(exc)[:250]}

def check_path(repo, path, branch):
    encoded = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    status, data = request("/repos/" + repo + "/contents/" + encoded + "?ref=" + urllib.parse.quote(branch, safe=""))
    if status == 200:
        return {"path": path, "status": "PRESENT", "kind": data.get("type", "unknown") if isinstance(data, dict) else "unknown"}
    if status == 404:
        return {"path": path, "status": "ABSENT_OR_NOT_VISIBLE"}
    return {"path": path, "status": "BLOCKED", "http_status": status,
            "detail": data.get("message", "request failed") if isinstance(data, dict) else "request failed"}

def audit(repo):
    status, meta = request("/repos/" + repo)
    if status != 200 or not isinstance(meta, dict):
        state = "BLOCKED" if status in (0, 401, 403, 429, 500, 502, 503) else "NOT_FOUND_OR_NOT_VISIBLE"
        return {"repository": repo, "status": state, "http_status": status,
                "evidence": meta.get("message", "metadata request failed") if isinstance(meta, dict) else "metadata request failed"}
    branch = meta.get("default_branch") or ""
    result = {"repository": repo, "status": "PASS", "http_status": 200,
              "full_name": meta.get("full_name"), "description": meta.get("description"),
              "visibility": meta.get("visibility", "unknown"), "archived": bool(meta.get("archived", False)),
              "disabled": bool(meta.get("disabled", False)), "default_branch": branch or None,
              "pushed_at": meta.get("pushed_at"), "html_url": meta.get("html_url"), "key_paths": [],
              "limitations": ["Metadata/path inventory only; source correctness and production readiness are not assessed."]}
    if not branch:
        result["status"] = "BLOCKED"
        result["limitations"].append("No default branch was returned.")
        return result
    for path in KEY_PATHS:
        item = check_path(repo, path, branch)
        result["key_paths"].append(item)
        if item["status"] == "BLOCKED":
            result["status"] = "PARTIAL"
    if not any(x["path"] == "README.md" and x["status"] == "PRESENT" for x in result["key_paths"]):
        result["findings"] = ["README.md is absent or not visible at the default branch."]
    if result["archived"]:
        result["findings"] = result.get("findings", []) + ["Repository is archived; automatic repairs must be skipped."]
    return result

def main():
    if not TOKEN:
        print("ERROR: AUDIT_GH_TOKEN is missing; no audit was run.", file=sys.stderr)
        return 2
    try:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        repos = config["repositories"]
        if not isinstance(repos, list) or not repos or any(not isinstance(x, str) or "/" not in x for x in repos):
            raise ValueError("repositories must be a non-empty list of owner/name strings")
    except Exception as exc:
        print("ERROR: invalid config: " + str(exc), file=sys.stderr)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for i, repo in enumerate(repos):
        if i:
            time.sleep(0.15)
        try:
            records.append(audit(repo))
        except Exception as exc:
            records.append({"repository": repo, "status": "BLOCKED",
                            "evidence": "Unhandled audit error: " + type(exc).__name__ + ": " + str(exc)[:200]})
    summary = {s: sum(1 for r in records if r.get("status") == s)
               for s in ("PASS", "PARTIAL", "BLOCKED", "NOT_FOUND_OR_NOT_VISIBLE")}
    report = {"schema_version": 1, "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "scope": "configured repository allowlist", "repository_count": len(records),
              "summary": summary, "records": records,
              "verification_limits": ["No source code was changed.", "No builds, tests, security scans, or deployments were run.",
                                      "ABSENT_OR_NOT_VISIBLE means a path may be absent or inaccessible."]}
    (OUT / "inventory.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Repository Inventory", "", "- Generated (UTC): " + report["generated_at_utc"],
             "- Repositories: " + str(len(records)), "- Scope: read-only metadata and selected path checks", "",
             "| Repository | Status | Default branch | Archived | Findings |",
             "|---|---|---|---:|---|"]
    for r in records:
        findings = "; ".join(r.get("findings", [])) or r.get("evidence", "")
        findings = findings.replace("|", "\\|")
        lines.append("| " + str(r.get("repository", "?")) + " | **" + str(r.get("status", "UNKNOWN")) +
                     "** | " + str(r.get("default_branch") or "—") + " | " + str(r.get("archived", "—")) +
                     " | " + findings + " |")
    lines += ["", "PASS means metadata was retrieved, not that code is correct.",
              "Missing paths are not proof that the repository is missing.",
              "Builds, tests, security scans, repairs, and deployments were not run.", ""]
    (OUT / "inventory.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 1 if any(r.get("status") in ("BLOCKED", "PARTIAL", "NOT_FOUND_OR_NOT_VISIBLE") for r in records) else 0

if __name__ == "__main__":
    raise SystemExit(main())
