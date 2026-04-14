# Janitor Red-Flag Detection Rules v0.1

---

## Purpose

Define conditions that should trigger an additional Janitor run or surface an alert between scheduled sweeps. The red-flag checker reads Janitor state files and emits findings. It never mutates state.

---

## Severity Levels

| Level | Exit Code | Meaning |
|-------|-----------|---------|
| `none` | 0 | No red flags detected |
| `low` | 1 | Informational — log only, next scheduled sweep is sufficient |
| `medium` | 1 | Request an extra Janitor run at normal priority |
| `high` | 2 | Request an extra Janitor run at high priority |
| `critical` | 3 | Manual alert required — possible integrity problem |

The checker returns the highest severity exit code found across all rules.

---

## A. Aging Blockers

### A.1 — Stage 2 Escalation Detected

| Field | Value |
|-------|-------|
| **condition** | Any blocker has `escalation_stage >= 2` and `blocker_status` is not `approved_unlocked`, `closed`, or `rejected` |
| **severity** | `medium` |
| **action** | `request_run` |
| **rationale** | Stage 2 means the blocker has persisted across multiple sweeps. An extra run ensures it gets attention. |

### A.2 — Stage 3 Escalation Detected

| Field | Value |
|-------|-------|
| **condition** | Any blocker has `escalation_stage >= 3` and `blocker_status` is not `approved_unlocked`, `closed`, or `rejected` |
| **severity** | `high` |
| **action** | `request_run_high_priority` |
| **rationale** | Stage 3 is the maximum escalation. Malik needs to see this promptly. |

### A.3 — Blocker Unresolved Beyond Threshold

| Field | Value |
|-------|-------|
| **condition** | Any blocker has `days_unresolved > 14` and `blocker_status` in (`pending_decision`, `active`, `externally_blocked`) |
| **severity** | `low` |
| **action** | `log_only` |
| **rationale** | Long-lived blockers are not emergencies but should be visible. Logged for sweep review. |

---

## B. Response-Ready Events

### B.1 — New Completed Response File

| Field | Value |
|-------|-------|
| **condition** | A response YAML file in `forms/` has non-empty `decision_status` AND its `content_hash` is not found in `response_application_log.yaml` |
| **severity** | `medium` |
| **action** | `request_run` |
| **rationale** | Malik has filled a response. An extra run should process it promptly rather than waiting up to 2 days. |

### B.2 — Response File Changed After Application

| Field | Value |
|-------|-------|
| **condition** | A response YAML file has non-empty `decision_status`, its file path IS in `response_application_log.yaml` with `ingestion_status: "applied"`, but current file hash differs from the logged `content_hash` |
| **severity** | `high` |
| **action** | `request_run_high_priority` |
| **rationale** | Malik may have updated a decision. Needs re-evaluation. Could also indicate corruption. |

---

## C. Queue Stress

### C.1 — Ready-for-Review Items Exceed Threshold

| Field | Value |
|-------|-------|
| **condition** | Count of queue items with `status: "ready_for_review"` > 3 |
| **severity** | `low` |
| **action** | `log_only` |
| **rationale** | Accumulating review items suggest work is unlocked but not being acted on. Informational only. |

### C.2 — Still-Blocked Items Accumulate

| Field | Value |
|-------|-------|
| **condition** | Count of queue items with `status: "still_blocked"` > 2 |
| **severity** | `medium` |
| **action** | `request_run` |
| **rationale** | Multiple deferred items suggest a systemic block worth reviewing. |

### C.3 — Conflicting Responses for Same Blocker

| Field | Value |
|-------|-------|
| **condition** | Two or more response files exist for the same `blocker_id` with different `decision_status` values and both have non-empty `decision_status` |
| **severity** | `high` |
| **action** | `request_run_high_priority` |
| **rationale** | Contradictory decisions for the same blocker cannot both be correct. Needs human review. |

---

## D. Integrity Problems

### D.1 — Malformed Response File

| Field | Value |
|-------|-------|
| **condition** | A `*_response.yaml` file in `forms/` fails YAML parsing or is missing required top-level fields (`blocker_id`, `decision_status`) |
| **severity** | `high` |
| **action** | `request_run_high_priority` |
| **rationale** | A broken response file could indicate a copy-paste error. Janitor should surface it immediately. |

### D.2 — Duplicate Accepted Response Attempt

| Field | Value |
|-------|-------|
| **condition** | A response file's `content_hash` matches an entry in `response_application_log.yaml` with `ingestion_status: "applied"` |
| **severity** | `low` |
| **action** | `log_only` |
| **rationale** | Not harmful — idempotency rule prevents re-application. Logged for awareness. |

### D.3 — Missing Core State File

| Field | Value |
|-------|-------|
| **condition** | Any of the 4 core state files (`janitor_state.yaml`, `packet_queue.yaml`, `response_application_log.yaml`, `blocker_decision_register.yaml`) does not exist |
| **severity** | `critical` |
| **action** | `manual_alert` |
| **rationale** | Missing state files mean Janitor cannot operate. Requires immediate human intervention. |

### D.4 — State File Empty or Unparseable

| Field | Value |
|-------|-------|
| **condition** | Any core state file exists but fails YAML parsing or has zero content |
| **severity** | `critical` |
| **action** | `manual_alert` |
| **rationale** | Corrupt state is as bad as missing state. |

---

## Rule Summary Table

| Rule | Family | Severity | Action | Exit Code |
|------|--------|----------|--------|-----------|
| A.1 | Aging | medium | request_run | 1 |
| A.2 | Aging | high | request_run_high_priority | 2 |
| A.3 | Aging | low | log_only | 1 |
| B.1 | Response | medium | request_run | 1 |
| B.2 | Response | high | request_run_high_priority | 2 |
| C.1 | Queue | low | log_only | 1 |
| C.2 | Queue | medium | request_run | 1 |
| C.3 | Queue | high | request_run_high_priority | 2 |
| D.1 | Integrity | high | request_run_high_priority | 2 |
| D.2 | Integrity | low | log_only | 1 |
| D.3 | Integrity | critical | manual_alert | 3 |
| D.4 | Integrity | critical | manual_alert | 3 |

---

*Janitor Red-Flag Rules v0.1 — 2026-04-12*
