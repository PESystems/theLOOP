#!/usr/bin/env python3
"""
Floor Janitor — Red-Flag Detection Checker
Version: v0.1
Date: 2026-04-12

Reads Janitor state files and checks for red-flag conditions.
Does NOT mutate any state. Read-only.

Exit codes:
    0 = no red flags
    1 = low/medium priority — extra run requested
    2 = high priority — urgent run requested
    3 = critical — manual alert required (integrity problem)

Usage:
    python check_janitor_red_flags.py
    python check_janitor_red_flags.py --json
    python check_janitor_red_flags.py --output logs/red_flag_report.json
"""

import argparse
import datetime
import hashlib
import json
import os
import sys
import yaml


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

JANITOR_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATE_DIR = os.path.join(JANITOR_ROOT, "state")
FORMS_DIR = os.path.join(JANITOR_ROOT, "forms")
LOGS_DIR = os.path.join(JANITOR_ROOT, "logs")

CORE_STATE_FILES = {
    "janitor_state.yaml": os.path.join(STATE_DIR, "janitor_state.yaml"),
    "packet_queue.yaml": os.path.join(STATE_DIR, "packet_queue.yaml"),
    "response_application_log.yaml": os.path.join(STATE_DIR, "response_application_log.yaml"),
    "blocker_decision_register.yaml": os.path.join(STATE_DIR, "blocker_decision_register.yaml"),
}

# Thresholds
DAYS_UNRESOLVED_THRESHOLD = 14
READY_FOR_REVIEW_THRESHOLD = 3
STILL_BLOCKED_THRESHOLD = 2

# Blocker statuses that are "resolved" (don't trigger aging alerts)
RESOLVED_STATUSES = {"approved_unlocked", "closed", "rejected"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_yaml_safe(path):
    """Load YAML file. Returns (data, error_string)."""
    if not os.path.isfile(path):
        return None, "file_not_found"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            return None, "empty_file"
        return data, None
    except yaml.YAMLError as e:
        return None, f"yaml_parse_error: {e}"
    except Exception as e:
        return None, f"read_error: {e}"


def sha256_file(path):
    if not os.path.isfile(path):
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Finding structure
# ---------------------------------------------------------------------------

class Finding:
    def __init__(self, rule_id, family, severity, action, message, details=None):
        self.rule_id = rule_id
        self.family = family
        self.severity = severity      # none, low, medium, high, critical
        self.action = action           # log_only, request_run, request_run_high_priority, manual_alert
        self.message = message
        self.details = details or {}

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "family": self.family,
            "severity": self.severity,
            "action": self.action,
            "message": self.message,
            "details": self.details,
        }

    def exit_code(self):
        return {"none": 0, "low": 1, "medium": 1, "high": 2, "critical": 3}.get(self.severity, 0)


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_d_integrity():
    """D.3 + D.4 — Missing or corrupt core state files."""
    findings = []
    for name, path in CORE_STATE_FILES.items():
        if not os.path.isfile(path):
            findings.append(Finding(
                "D.3", "integrity", "critical", "manual_alert",
                f"Missing core state file: {name}",
                {"file": name, "path": path}
            ))
        else:
            data, err = load_yaml_safe(path)
            if err:
                findings.append(Finding(
                    "D.4", "integrity", "critical", "manual_alert",
                    f"Core state file unparseable: {name} — {err}",
                    {"file": name, "error": err}
                ))
    return findings


def check_a_aging(state_data):
    """A.1, A.2, A.3 — Blocker aging/escalation."""
    findings = []
    blockers = state_data.get("active_blockers", [])
    if not blockers:
        return findings

    for b in blockers:
        bid = b.get("blocker_id", "?")
        stage = b.get("escalation_stage", 1)
        status = b.get("blocker_status", "")
        days = b.get("days_unresolved", 0)

        if status in RESOLVED_STATUSES:
            continue

        # A.2 — Stage 3
        if stage >= 3:
            findings.append(Finding(
                "A.2", "aging", "high", "request_run_high_priority",
                f"Stage 3 escalation: {bid} (status={status})",
                {"blocker_id": bid, "stage": stage, "status": status}
            ))
        # A.1 — Stage 2
        elif stage >= 2:
            findings.append(Finding(
                "A.1", "aging", "medium", "request_run",
                f"Stage 2 escalation: {bid} (status={status})",
                {"blocker_id": bid, "stage": stage, "status": status}
            ))

        # A.3 — Long unresolved
        if days > DAYS_UNRESOLVED_THRESHOLD:
            findings.append(Finding(
                "A.3", "aging", "low", "log_only",
                f"Blocker unresolved {days} days: {bid}",
                {"blocker_id": bid, "days_unresolved": days, "status": status}
            ))

    return findings


def check_b_responses(log_data):
    """B.1, B.2 — New or changed response files."""
    findings = []

    # Build lookup of applied responses
    entries = []
    if log_data:
        entries = log_data.get("response_entries", [])

    applied_by_path = {}
    applied_hashes = set()
    for e in entries:
        if e.get("ingestion_status") == "applied":
            p = e.get("response_file_path", "")
            h = e.get("content_hash", "")
            if p:
                applied_by_path[p] = h
            if h:
                applied_hashes.add(h)

    # Scan response files
    if not os.path.isdir(FORMS_DIR):
        return findings

    for fname in sorted(os.listdir(FORMS_DIR)):
        if not fname.endswith("_response.yaml"):
            continue
        if "template" in fname.lower() or "example" in fname.lower():
            continue

        fpath = os.path.join(FORMS_DIR, fname)
        data, err = load_yaml_safe(fpath)

        if err:
            # D.1 — Malformed response file
            findings.append(Finding(
                "D.1", "integrity", "high", "request_run_high_priority",
                f"Malformed response file: {fname} — {err}",
                {"file": fname, "error": err}
            ))
            continue

        if data is None:
            continue

        decision_status = str(data.get("decision_status", "")).strip()
        if not decision_status:
            continue  # Unfilled — not a red flag

        # Check required fields exist
        blocker_id = data.get("blocker_id", "")
        if not blocker_id or not decision_status:
            findings.append(Finding(
                "D.1", "integrity", "high", "request_run_high_priority",
                f"Response file missing required fields: {fname}",
                {"file": fname, "blocker_id": blocker_id, "decision_status": decision_status}
            ))
            continue

        current_hash = sha256_file(fpath)
        rel_path = f"forms/{fname}"

        # B.1 — New completed response
        if current_hash not in applied_hashes and rel_path not in applied_by_path:
            findings.append(Finding(
                "B.1", "response", "medium", "request_run",
                f"New completed response: {fname} (blocker={blocker_id}, decision={decision_status})",
                {"file": fname, "blocker_id": blocker_id, "decision_status": decision_status,
                 "hash": current_hash}
            ))

        # B.2 — Changed after application
        if rel_path in applied_by_path:
            old_hash = applied_by_path[rel_path]
            if old_hash and current_hash != old_hash:
                findings.append(Finding(
                    "B.2", "response", "high", "request_run_high_priority",
                    f"Response changed after application: {fname}",
                    {"file": fname, "old_hash": old_hash, "new_hash": current_hash}
                ))

        # D.2 — Duplicate (already applied, same hash)
        if current_hash in applied_hashes:
            findings.append(Finding(
                "D.2", "integrity", "low", "log_only",
                f"Response already applied (idempotent): {fname}",
                {"file": fname, "hash": current_hash}
            ))

    return findings


def check_b_conflicts():
    """C.3 — Conflicting responses for same blocker."""
    findings = []
    if not os.path.isdir(FORMS_DIR):
        return findings

    blocker_decisions = {}  # blocker_id -> list of (file, decision_status)
    for fname in sorted(os.listdir(FORMS_DIR)):
        if not fname.endswith("_response.yaml"):
            continue
        if "template" in fname.lower() or "example" in fname.lower():
            continue

        fpath = os.path.join(FORMS_DIR, fname)
        data, err = load_yaml_safe(fpath)
        if err or data is None:
            continue

        ds = str(data.get("decision_status", "")).strip()
        bid = str(data.get("blocker_id", "")).strip()
        if ds and bid:
            blocker_decisions.setdefault(bid, []).append((fname, ds))

    for bid, pairs in blocker_decisions.items():
        if len(pairs) > 1:
            statuses = set(ds for _, ds in pairs)
            if len(statuses) > 1:
                findings.append(Finding(
                    "C.3", "queue", "high", "request_run_high_priority",
                    f"Conflicting responses for {bid}: {pairs}",
                    {"blocker_id": bid, "responses": [{"file": f, "decision": d} for f, d in pairs]}
                ))

    return findings


def check_c_queue(queue_data):
    """C.1, C.2 — Queue stress."""
    findings = []
    if not queue_data:
        return findings

    queue_items = queue_data.get("queue_items", [])
    form_items = queue_data.get("form_items", [])
    all_items = queue_items + form_items

    ready_count = sum(1 for i in all_items if i.get("status") == "ready_for_review")
    blocked_count = sum(1 for i in all_items if i.get("status") == "still_blocked")

    if ready_count > READY_FOR_REVIEW_THRESHOLD:
        findings.append(Finding(
            "C.1", "queue", "low", "log_only",
            f"Ready-for-review items exceed threshold: {ready_count} > {READY_FOR_REVIEW_THRESHOLD}",
            {"count": ready_count, "threshold": READY_FOR_REVIEW_THRESHOLD}
        ))

    if blocked_count > STILL_BLOCKED_THRESHOLD:
        findings.append(Finding(
            "C.2", "queue", "medium", "request_run",
            f"Still-blocked items accumulating: {blocked_count} > {STILL_BLOCKED_THRESHOLD}",
            {"count": blocked_count, "threshold": STILL_BLOCKED_THRESHOLD}
        ))

    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_all_checks():
    """Run all red-flag checks. Returns (findings_list, max_exit_code)."""
    all_findings = []

    # D — Integrity first (if state is missing, other checks are meaningless)
    integrity = check_d_integrity()
    all_findings.extend(integrity)

    # If critical integrity failure, skip data-dependent checks
    critical_failures = [f for f in integrity if f.severity == "critical"]
    if critical_failures:
        return all_findings, max(f.exit_code() for f in all_findings)

    # Load data
    state_data, _ = load_yaml_safe(CORE_STATE_FILES["janitor_state.yaml"])
    queue_data, _ = load_yaml_safe(CORE_STATE_FILES["packet_queue.yaml"])
    log_data, _ = load_yaml_safe(CORE_STATE_FILES["response_application_log.yaml"])

    # A — Aging
    if state_data:
        all_findings.extend(check_a_aging(state_data))

    # B — Response-ready
    if log_data:
        all_findings.extend(check_b_responses(log_data))

    # C.3 — Conflicts
    all_findings.extend(check_b_conflicts())

    # C — Queue stress
    if queue_data:
        all_findings.extend(check_c_queue(queue_data))

    max_exit = max((f.exit_code() for f in all_findings), default=0)
    return all_findings, max_exit


def print_summary(findings, max_exit):
    """Print human-readable summary to stdout."""
    severity_labels = {0: "CLEAR", 1: "LOW/MEDIUM", 2: "HIGH", 3: "CRITICAL"}

    print("=" * 60)
    print(f"  JANITOR RED-FLAG CHECK")
    print(f"  {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"  Overall: {severity_labels.get(max_exit, '?')} (exit code {max_exit})")
    print("=" * 60)

    if not findings:
        print("\n  No red flags detected.\n")
        return

    print(f"\n  {len(findings)} finding(s):\n")

    for i, f in enumerate(findings, 1):
        icon = {"low": ".", "medium": "!", "high": "!!", "critical": "XXX"}.get(f.severity, "?")
        print(f"  [{icon}] {f.rule_id} ({f.family}/{f.severity}) — {f.message}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Floor Janitor Red-Flag Checker")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--output", type=str, help="Write JSON report to file")
    args = parser.parse_args()

    findings, max_exit = run_all_checks()

    # Always print summary to console
    if not args.json:
        print_summary(findings, max_exit)

    # JSON output
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "exit_code": max_exit,
        "finding_count": len(findings),
        "findings": [f.to_dict() for f in findings],
    }

    if args.json:
        print(json.dumps(report, indent=2))

    if args.output:
        out_path = args.output
        if not os.path.isabs(out_path):
            out_path = os.path.join(JANITOR_ROOT, out_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        if not args.json:
            print(f"  JSON report written to: {out_path}")

    sys.exit(max_exit)


if __name__ == "__main__":
    main()
