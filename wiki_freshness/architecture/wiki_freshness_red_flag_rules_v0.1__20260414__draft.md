# Wiki Freshness Red-Flag Rules v0.1

**Date:** 2026-04-14
**Status:** draft
**Scope:** Floor wiki source-file drift + map integrity. **Not** operational state (that is Janitor's domain).

---

## Purpose

Define conditions that the wiki freshness verifier must surface between scheduled sweeps. The checker is **read-only** — it never mutates wiki pages, source files, or the source map. When a rule fires it stages a revalidation request under `Git/theLOOP/wiki_freshness/queue/` and raises the corresponding exit severity.

Mirrors Janitor's rule-ID-and-severity shape but is an independent ruleset. Janitor's A/B/C/D families cover operational state; this file's E family covers wiki freshness. **The two rulesets never merge.**

---

## Severity levels

| Level | Exit Code | Meaning |
|-------|-----------|---------|
| `none` | 0 | No red flags |
| `low` | 1 | Log-only; next scheduled sweep sufficient |
| `medium` | 1 | Stage revalidation request; human review on next wiki session |
| `high` | 2 | Stage revalidation + surface in next session-open sweep |
| `critical` | 3 | Manual alert — source map or verifier integrity issue |

The verifier returns the highest severity found.

---

## E. Wiki Freshness Rules

### E.1 — Source hash mismatch

| Field | Value |
|-------|-------|
| **condition** | Any row with `Baseline Status: current`, a populated `Source SHA256 At Ingest`, and a live source file whose SHA256 differs from the stored value |
| **severity** | `high` |
| **action** | `stage_revalidation_request` |
| **receipt expectation** | Count in `hash_changed`; one request file per row under `queue/` |
| **rationale** | Source was edited after ingest. Wiki page may now misrepresent the source. |

### E.2 — Source file missing

| Field | Value |
|-------|-------|
| **condition** | Any row whose source path does not resolve to a live file under any candidate base |
| **severity** | `high` |
| **action** | `stage_revalidation_request` |
| **receipt expectation** | Count in `missing_source`; one request file per row |
| **rationale** | Source was moved, renamed, or deleted. Wiki page is now orphaned from its authority. |

### E.3 — Source mtime newer than ingest

| Field | Value |
|-------|-------|
| **condition** | Stored SHA differs from current SHA **and** current filesystem mtime is greater than stored `Source MTime At Ingest` |
| **severity** | `medium` |
| **action** | `stage_revalidation_request` |
| **receipt expectation** | Count in `mtime_newer_than_ingest` |
| **rationale** | Higher-confidence drift signal than hash-alone — confirms the file was written after ingest, not that ingest recorded the wrong hash. |

### E.4 — Orphan source_map row

| Field | Value |
|-------|-------|
| **condition** | Row references a source path that has **never** resolved in the last N sweeps (N=3 by default) and `Baseline Status` is not `source_missing` |
| **severity** | `low` |
| **action** | `log_only` |
| **receipt expectation** | Listed under "Orphan candidates" in the report |
| **rationale** | Row may be stale scaffolding from a superseded source. Needs pruning, not revalidation. |

### E.5 — Queue stale beyond threshold

| Field | Value |
|-------|-------|
| **condition** | `ingest_queue.md` for a wiki has active entries AND mtime older than 168h (7 days) |
| **severity** | `low` |
| **action** | `log_only` |
| **receipt expectation** | Queue awareness block in receipt |
| **rationale** | Pending queued items are aging unprocessed. Coordinate with `wiki_ingest_health.py`. |

### E.6 — Legacy row census above threshold

| Field | Value |
|-------|-------|
| **condition** | Count of rows with `Baseline Status: legacy_no_baseline` ≥ 10 (or configurable) |
| **severity** | `low` |
| **action** | `log_only` + recommend baseline refresh plan |
| **receipt expectation** | Count in `legacy_no_baseline` |
| **rationale** | Legacy rows cannot be diffed — the more of them there are, the larger the detection blind spot. Drives re-ingest prioritization. |

### E.7 — Source path unresolvable (read error)

| Field | Value |
|-------|-------|
| **condition** | Path resolves to a file but hashing fails (permission, IO error, etc.) |
| **severity** | `high` |
| **action** | `stage_revalidation_request` |
| **receipt expectation** | Count in `unresolved_path` |
| **rationale** | Filesystem-level integrity problem. Cannot confirm drift either way. |

### E.8 — Sweep failed / skipped / partial

| Field | Value |
|-------|-------|
| **condition** | Most recent scheduled sweep missing from `receipts/` for more than `2 × sweep_interval`, OR most recent receipt shows `exit_code ≥ 2` with no follow-up resolution |
| **severity** | `medium` |
| **action** | `request_extra_run` + flag on next session open |
| **receipt expectation** | N/A — this rule runs against the receipts directory itself, evaluated by the scheduled skill |
| **rationale** | Silent scheduler failure is the worst outcome for a freshness system. Must be visible. |

### E.9 — Receipt missing

| Field | Value |
|-------|-------|
| **condition** | A report artifact was produced but no receipt exists for the same run_id (or vice versa) |
| **severity** | `medium` |
| **action** | `log_only` + investigate |
| **receipt expectation** | Self-check on sweep start — verify prior-run invariant |
| **rationale** | Receipt/report pair divergence signals an interrupted run. |

### E.10 — Source map schema mismatch

| Field | Value |
|-------|-------|
| **condition** | `source_map.md` lacks `schema_version: 0.2` frontmatter OR its header row does not include the three baseline columns |
| **severity** | `critical` |
| **action** | `manual_alert` |
| **receipt expectation** | Verifier halts before classification |
| **rationale** | Detection is meaningless if schema is wrong. Operator must re-apply the schema upgrade. |

### E.11 — Source map missing or unparseable

| Field | Value |
|-------|-------|
| **condition** | A registered `source_map.md` is missing, empty, or its table cannot be parsed |
| **severity** | `critical` |
| **action** | `manual_alert` |
| **rationale** | Equivalent to Janitor D.3/D.4 for the wiki domain. |

---

## Rule summary table

| Rule | Family | Severity | Action | Exit Code |
|------|--------|----------|--------|-----------|
| E.1  | Drift     | high     | stage_revalidation_request | 2 |
| E.2  | Drift     | high     | stage_revalidation_request | 2 |
| E.3  | Drift     | medium   | stage_revalidation_request | 1 |
| E.4  | Map       | low      | log_only                   | 1 |
| E.5  | Queue     | low      | log_only                   | 1 |
| E.6  | Baseline  | low      | log_only                   | 1 |
| E.7  | Integrity | high     | stage_revalidation_request | 2 |
| E.8  | Scheduler | medium   | request_extra_run          | 1 |
| E.9  | Audit     | medium   | log_only                   | 1 |
| E.10 | Integrity | critical | manual_alert               | 3 |
| E.11 | Integrity | critical | manual_alert               | 3 |

---

## Boundary statement

None of these rules evaluate Janitor state files. None of them run from the Janitor scheduler. None of them write to any Janitor path. Cross-system flags (for example, a blocker that references a drifted wiki page) are routed via the Node tracker, not by either detector silently modifying the other's state.

---

*Wiki Freshness Red-Flag Rules v0.1 — 2026-04-14*
