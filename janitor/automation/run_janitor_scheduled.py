#!/usr/bin/env python3
"""
Floor Janitor — Scheduled Run Entrypoint
Version: v0.1
Date: 2026-04-12

Invokes a Janitor sweep with pre-run snapshotting and run logging.
Designed to be called by Windows Task Scheduler, cron, or manually.

Usage:
    python run_janitor_scheduled.py --mode sweep
    python run_janitor_scheduled.py --mode dry-run
    python run_janitor_scheduled.py --mode red-flag-only

Exit codes:
    0 = success
    1 = partial (e.g., no responses to process)
    2 = error
"""

import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys
import yaml


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

JANITOR_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATE_FILES = [
    os.path.join(JANITOR_ROOT, "state", "janitor_state.yaml"),
    os.path.join(JANITOR_ROOT, "state", "packet_queue.yaml"),
    os.path.join(JANITOR_ROOT, "state", "response_application_log.yaml"),
    os.path.join(JANITOR_ROOT, "state", "blocker_decision_register.yaml"),
]

FORMS_DIR = os.path.join(JANITOR_ROOT, "forms")
LOGS_DIR = os.path.join(JANITOR_ROOT, "logs")
SNAPSHOTS_DIR = os.path.join(JANITOR_ROOT, "state", "snapshots")
RUN_LOG_PATH = os.path.join(LOGS_DIR, "janitor_automation_run_log.md")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def timestamp_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def date_stamp():
    return datetime.datetime.now().strftime("%Y%m%d")


def run_id():
    ts = datetime.datetime.now(datetime.timezone.utc)
    return f"JAUTO-{ts.strftime('%Y%m%d-%H%M%S')}"


def sha256_file(path):
    """Compute SHA-256 of a file. Returns empty string if file missing."""
    if not os.path.isfile(path):
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_yaml(path):
    """Load a YAML file safely. Returns None on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------------------
# Step 1 — Pre-run snapshot
# ---------------------------------------------------------------------------

def create_snapshot(rid):
    """Copy all 4 core state files to a snapshot folder. Returns snapshot path and hashes."""
    snap_dir = os.path.join(SNAPSHOTS_DIR, rid)
    ensure_dir(snap_dir)

    hashes = {}
    missing = []
    for sf in STATE_FILES:
        fname = os.path.basename(sf)
        if os.path.isfile(sf):
            shutil.copy2(sf, os.path.join(snap_dir, fname))
            hashes[fname] = sha256_file(sf)
        else:
            missing.append(fname)
            hashes[fname] = "MISSING"

    return snap_dir, hashes, missing


# ---------------------------------------------------------------------------
# Step 2 — Response discovery (read-only scan)
# ---------------------------------------------------------------------------

def discover_responses():
    """Scan forms/ for response YAMLs. Returns list of dicts with file info."""
    results = []
    if not os.path.isdir(FORMS_DIR):
        return results

    for fname in sorted(os.listdir(FORMS_DIR)):
        if not fname.endswith("_response.yaml"):
            continue
        # Skip templates and examples
        if "template" in fname.lower() or "example" in fname.lower():
            continue

        fpath = os.path.join(FORMS_DIR, fname)
        data = load_yaml(fpath)
        if data is None:
            results.append({
                "file": fname,
                "path": fpath,
                "status": "malformed",
                "decision_status": "",
                "blocker_id": "",
                "hash": sha256_file(fpath),
            })
            continue

        decision_status = data.get("decision_status", "")
        blocker_id = data.get("blocker_id", "")

        if not decision_status or decision_status.strip() == "":
            status = "unfilled"
        else:
            status = "filled"

        results.append({
            "file": fname,
            "path": fpath,
            "status": status,
            "decision_status": str(decision_status),
            "blocker_id": str(blocker_id),
            "hash": sha256_file(fpath),
        })

    return results


def check_already_applied(responses, log_path):
    """Mark responses that have already been applied (idempotency check)."""
    log_data = load_yaml(log_path)
    if not log_data:
        return responses

    entries = log_data.get("response_entries", [])
    applied_hashes = set()
    applied_paths = set()
    for e in entries:
        if e.get("ingestion_status") == "applied":
            h = e.get("content_hash", "")
            p = e.get("response_file_path", "")
            if h:
                applied_hashes.add(h)
            if p:
                applied_paths.add(p)

    for r in responses:
        rel_path = os.path.relpath(r["path"], JANITOR_ROOT).replace("\\", "/")
        if r["hash"] in applied_hashes or rel_path in applied_paths:
            r["already_applied"] = True
        else:
            r["already_applied"] = False

    return responses


# ---------------------------------------------------------------------------
# Step 3 — Sweep summary (what would happen)
# ---------------------------------------------------------------------------

def build_sweep_summary(responses):
    """Analyze discovered responses and produce a summary."""
    summary = {
        "total_scanned": len(responses),
        "unfilled": 0,
        "filled_new": 0,
        "filled_already_applied": 0,
        "malformed": 0,
        "eligible_for_processing": [],
    }

    for r in responses:
        if r["status"] == "unfilled":
            summary["unfilled"] += 1
        elif r["status"] == "malformed":
            summary["malformed"] += 1
        elif r["status"] == "filled":
            if r.get("already_applied", False):
                summary["filled_already_applied"] += 1
            else:
                summary["filled_new"] += 1
                summary["eligible_for_processing"].append(r["file"])

    return summary


# ---------------------------------------------------------------------------
# Step 4 — Run log entry
# ---------------------------------------------------------------------------

def append_run_log(rid, trigger_source, trigger_reason, mode, outcome, artifacts, follow_up):
    """Append an entry to the automation run log."""
    ensure_dir(LOGS_DIR)

    entry = f"""
| {rid} | {timestamp_now()} | {trigger_source} | {trigger_reason} | {mode} | {outcome} | {artifacts} | {follow_up} |"""

    # Create file with header if it doesn't exist
    if not os.path.isfile(RUN_LOG_PATH):
        header = """# Floor Janitor — Automation Run Log

| run_id | timestamp | trigger_source | trigger_reason | mode | outcome | artifacts_written | follow_up_required |
|--------|-----------|----------------|----------------|------|---------|-------------------|-------------------|"""
        with open(RUN_LOG_PATH, "w", encoding="utf-8") as f:
            f.write(header + entry + "\n")
    else:
        with open(RUN_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(entry + "\n")


# ---------------------------------------------------------------------------
# Main modes
# ---------------------------------------------------------------------------

def mode_sweep(rid, dry_run=False):
    """Full Janitor sweep."""
    label = "dry_run" if dry_run else "real"
    print(f"[Janitor] Starting {label} sweep: {rid}")

    # Step 1 — Snapshot
    snap_dir, hashes, missing = create_snapshot(rid)
    print(f"[Janitor] Snapshot created: {snap_dir}")

    if missing:
        print(f"[Janitor] WARNING: Missing state files: {missing}")
        append_run_log(rid, "scheduled", "periodic sweep", label,
                       f"FAILED — missing state files: {missing}", "snapshot only", "manual fix required")
        return 2

    # Step 2 — Discover responses
    responses = discover_responses()
    log_path = os.path.join(JANITOR_ROOT, "state", "response_application_log.yaml")
    responses = check_already_applied(responses, log_path)

    # Step 3 — Analyze
    summary = build_sweep_summary(responses)
    print(f"[Janitor] Scan: {summary['total_scanned']} files, "
          f"{summary['filled_new']} new eligible, "
          f"{summary['unfilled']} unfilled, "
          f"{summary['filled_already_applied']} already applied, "
          f"{summary['malformed']} malformed")

    if dry_run:
        outcome = f"dry_run complete — {summary['filled_new']} would be processed"
        artifacts = "snapshot"
        follow_up = "none (dry run)"
        append_run_log(rid, "scheduled", "periodic sweep (dry-run)", "dry_run",
                       outcome, artifacts, follow_up)
        # Write dry-run JSON summary
        json_path = os.path.join(LOGS_DIR, f"janitor_dry_run_{date_stamp()}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "run_id": rid,
                "mode": "dry_run",
                "timestamp": timestamp_now(),
                "snapshot_path": snap_dir,
                "hashes": hashes,
                "discovery": summary,
                "responses": [{k: v for k, v in r.items() if k != "path"} for r in responses],
            }, f, indent=2)
        print(f"[Janitor] Dry-run summary: {json_path}")
        print(f"[Janitor] Dry-run complete. No state mutated.")
        return 0

    # Real sweep — if eligible responses exist, this is where Claude Code
    # would be invoked to run the ingestion pipeline. In the automation
    # entrypoint, we document what was found and defer to the next
    # Claude Code session for actual ingestion (no autonomous execution).
    if summary["filled_new"] > 0:
        outcome = f"responses found — {summary['filled_new']} new eligible: {summary['eligible_for_processing']}"
        follow_up = "run Phase 2C ingestion in next Claude Code session"
    elif summary["malformed"] > 0:
        outcome = f"malformed responses detected — {summary['malformed']} files need review"
        follow_up = "review malformed files"
    else:
        outcome = "no new responses — all unfilled or already applied"
        follow_up = "none"

    artifacts = "snapshot + run log"
    append_run_log(rid, "scheduled", "periodic sweep", "real", outcome, artifacts, follow_up)

    print(f"[Janitor] Sweep complete: {outcome}")
    return 0 if summary["filled_new"] == 0 and summary["malformed"] == 0 else 1


def mode_red_flag_only(rid):
    """Run red-flag check only, no sweep."""
    print(f"[Janitor] Running red-flag check: {rid}")

    # Import and run the checker
    checker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_janitor_red_flags.py")
    if not os.path.isfile(checker_path):
        print("[Janitor] ERROR: check_janitor_red_flags.py not found")
        return 2

    # Run as subprocess to get exit code
    import subprocess
    result = subprocess.run(
        [sys.executable, checker_path],
        capture_output=True, text=True, cwd=JANITOR_ROOT
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    append_run_log(rid, "red_flag", "on-demand check", "red_flag_only",
                   f"exit_code={result.returncode}", "none",
                   "run requested" if result.returncode > 0 else "none")

    return result.returncode


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Floor Janitor Scheduled Run")
    parser.add_argument("--mode", choices=["sweep", "dry-run", "red-flag-only"],
                        default="sweep", help="Run mode")
    args = parser.parse_args()

    rid = run_id()

    if args.mode == "sweep":
        sys.exit(mode_sweep(rid, dry_run=False))
    elif args.mode == "dry-run":
        sys.exit(mode_sweep(rid, dry_run=True))
    elif args.mode == "red-flag-only":
        sys.exit(mode_red_flag_only(rid))


if __name__ == "__main__":
    main()
