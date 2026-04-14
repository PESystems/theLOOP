---
tags:
- janitor
- response-ingestion
- contract
- v0_1
---
# Janitor Response Ingestion Contract v0.1

Defines how Janitor discovers, validates, applies, and logs blocker decision responses.

---

## A. Valid Response Shape

Every blocker decision response YAML must include these top-level fields:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `blocker_id` | str | always | Must match an active/pending blocker in janitor_state.yaml |
| `source_tracker` | str | always | Must match the blocker's source_tracker |
| `escalation_stage_at_decision` | int | always | 1, 2, or 3 |
| `decision_status` | enum | always | `approve` / `defer` / `reject` / `need_more_info` |
| `selected_option_id` | str | on approve | Machine-readable option key from form |
| `selected_option_label` | str | on approve | Human-readable label |
| `decision_payload` | object | on approve | Blocker-family-specific structured fields |
| `urgency` | enum | always | `low` / `normal` / `high` / `critical` |
| `signoff_name` | str | always (stage 3 required, 1-2 optional) | Name of decision-maker |
| `decision_date` | str | always | YYYY-MM-DD |
| `recorded_at` | str | always | ISO 8601 timestamp |

---

## B. Validation Rules

### B.1 — Identity validation
- `blocker_id` must map to a known blocker in `janitor_state.yaml` active_blockers or a form_item in `packet_queue.yaml`
- `source_tracker` must match the expected tracker for that blocker ID
- If either fails: reject response as `rejected_invalid`, reason: `identity_mismatch`

### B.2 — Decision status validation
- `decision_status` must be one of: `approve`, `defer`, `reject`, `need_more_info`
- Any other value: reject as `rejected_invalid`, reason: `invalid_decision_status`

### B.3 — Approve-specific validation
When `decision_status = approve`:
- `selected_option_id` must be non-empty
- `selected_option_label` must be non-empty
- `decision_payload` must be present and match the blocker-family schema
- If any of these fail: reject as `rejected_invalid`, reason: `incomplete_approval`

### B.4 — Blocker-family payload validation

| Blocker | Required payload fields | Valid `selected_option_id` values |
|---------|------------------------|----------------------------------|
| BLK-20260412-002 | `auth_storage_choice`, `notes` | `env_var`, `local_secrets_file`, `os_keychain` |
| BLK-20260412-004 | `phase2_scope_choice`, `authorized_defects`, `notes` | `full_phase2`, `d3_only`, `hold_phase2` |
| BLK-20260412-005 | `naming_path_choice`, `notes` | `batch_rename`, `new_only`, `notion_property_bridge` |
| BLK-20260412-006 | `cleanup_choice`, `approved_targets`, `notes` | `delete_listed_files`, `archive_only`, `hold_cleanup` |

### B.5 — Stage validation
- `escalation_stage_at_decision` must be 1, 2, or 3
- At stage 3: `signoff_name` must be non-empty, notes within `decision_payload` must be non-empty

### B.6 — Structural validation
- Response must parse as valid YAML
- All required fields must be present (not just empty strings for required-on-approve fields)
- Malformed or partial responses are rejected entirely — never half-applied

---

## C. Idempotency Rule

A response file must not be applied twice. Janitor tracks applied responses by:

| Check | Field | Purpose |
|-------|-------|---------|
| File path | `response_file_path` | Primary dedup key |
| Blocker ID | `blocker_id` | Prevents multiple decisions for same blocker |
| Timestamp | `recorded_at` | Distinguishes updated responses from duplicates |
| Content fingerprint | `content_hash` | SHA-256 of the raw YAML file content |

### Dedup logic
1. Check `response_application_log.yaml` for existing entry with same `response_file_path`
2. If found AND `content_hash` matches: skip as `ignored_duplicate`
3. If found AND `content_hash` differs: this is an updated response — apply as new (supersedes prior)
4. If not found: proceed with validation and application
5. After applying, a blocker's decision is final until explicitly reopened by a new response

---

## D. Decision Consequences

### D.1 — `approve`

| Target | Effect |
|--------|--------|
| Blocker state | `blocker_status` → `approved_unlocked` |
| Form item | `status` → `answered_approved` |
| Packet queue | Packets in `unlocks_packets` → `ready_for_review`. Packets with `decision_source` pointing to this form: update `blocked_by_decision: false` |
| Follow-up | Generate scoped follow-up artifact based on `selected_option_id` and `decision_payload` |
| Decision register | Record full decision with `state_effect: approved`, `unlocked_items` populated |

### D.2 — `defer`

| Target | Effect |
|--------|--------|
| Blocker state | `blocker_status` → `deferred` |
| Form item | `status` → `answered_deferred` |
| Packet queue | No advancement. Dependent packets remain at current status |
| Follow-up | None |
| Decision register | Record with `state_effect: deferred`, `still_blocked_items` populated |

### D.3 — `reject`

| Target | Effect |
|--------|--------|
| Blocker state | `blocker_status` → `rejected` → then `closed` |
| Form item | `status` → `answered_rejected` |
| Packet queue | Dependent packets → `closed_no_action` |
| Follow-up | None |
| Decision register | Record with `state_effect: rejected` |

### D.4 — `need_more_info`

| Target | Effect |
|--------|--------|
| Blocker state | `blocker_status` → `needs_more_info` |
| Form item | `status` → `answered_need_more_info` |
| Packet queue | No advancement. Blocker stays active for next sweep |
| Follow-up | None — Janitor gathers more context on next sweep |
| Decision register | Record with `state_effect: needs_more_info`, `still_blocked_items` populated |

---

## E. Response Discovery Rules

### E.1 — Scan path
Scan `forms/` directory for files matching pattern:
- `JANITOR_blocker_BLK-*_response.yaml`

### E.2 — Exclusion rules
Ignore:
- `janitor_blocker_form_response_template_*.yaml` (generic template)
- `janitor_blocker_response_filled_example_*.yaml` (documentation example — unless test mode)
- `*.html` files
- Files not matching the response naming pattern

### E.3 — Empty detection
A response file is considered unfilled if:
- `decision_status` is empty string `""`
- `selected_option_id` is empty string `""` AND `decision_status` is `approve`
- `recorded_at` is empty string `""`

Unfilled templates are skipped silently — they are not invalid, just not yet completed.

---

## F. Test Mode vs Real Mode

### Real mode
- Applies only to real response files (not examples/templates)
- Mutates `janitor_state.yaml`, `packet_queue.yaml`, `blocker_decision_register.yaml`
- Logs to `response_application_log.yaml` with `ingestion_status: applied`

### Test mode
- Uses the filled example: `janitor_blocker_response_filled_example_v0.1__20260412__draft.yaml`
- All log entries marked with `ingestion_status: test_only`
- Does NOT mutate production blocker state
- Writes test results to `reports/phase2b_test_mode_report_20260412.md`
- Generates test follow-up artifacts with `_test_` in filename

---

*Janitor Response Ingestion Contract v0.1 -- 2026-04-12*
