# Wiki Freshness Scheduled Task Spec v0.1

**Date:** 2026-04-14
**Status:** draft

---

## Task Definition

| Field | Value |
|-------|-------|
| **taskId** | `wiki-freshness-weekly` |
| **description** | `Wiki source-file drift detection — read-only sweep. Weekly.` |
| **cronExpression** | `0 8 * * 1` |
| **Cadence** | Weekly, Monday 08:00 local time |

Sibling to, **not** submode of, `janitor-sweep-2d`. Runs on its own schedule, produces its own receipts, never shares state with Janitor.

---

## Task Prompt

```
Wiki Freshness Weekly Sweep

Working directory: C:\Users\Malik\Documents\Claude

You are running a scheduled wiki freshness sweep. This is an automated heartbeat — not an interactive session.

## Steps

1. Run the verifier with reverse-scan enabled:
   python theLOOP/housekeeping/wiki_source_drift.py --reverse-scan

2. Read the outputs from the JSON line the script prints:
   - report path (drift report markdown)
   - receipt path
   - exit_code
   - counts by status
   - staged revalidation request count
   - untracked candidate count

3. Summarize findings:
   - Total rows checked, by wiki (LOOP + YASK)
   - Drift detected: hash_changed + mtime_newer_than_ingest + missing_source counts
   - Legacy rows remaining (without baseline)
   - Untracked source candidates (if --reverse-scan ran)
   - Red flags raised with rule IDs

4. If any revalidation requests were staged:
   - List them by source path
   - Note: "Malik should review these in his next wiki session and invoke wiki-build as appropriate"
   - Do NOT invoke wiki-build autonomously
   - Do NOT modify wiki pages
   - Do NOT modify source_map.md

5. If exit_code >= 2 (high severity):
   - Prominently flag the drift
   - Reference the specific rule IDs (E.1 / E.2 / E.7)

6. If exit_code == 3 (critical):
   - Source map is missing or unparseable
   - Prominently flag "Manual investigation required"

## Hard constraints

- Do NOT rewrite wiki pages
- Do NOT modify source_map.md
- Do NOT invoke wiki-build or wiki-write-through autonomously
- Do NOT touch Janitor state files
- Do NOT widen scope into operational state (blockers, packets, responses)
- This is a detection and staging run only
```

---

## Outputs per run

| Artifact | Path |
|---|---|
| Drift report | `Git/theLOOP/wiki_freshness/reports/drift_report_YYYYMMDD_HHMMSS.md` |
| Receipt | `Git/theLOOP/wiki_freshness/receipts/sweep_receipt_YYYYMMDD_HHMMSS.md` |
| Revalidation requests | `Git/theLOOP/wiki_freshness/queue/revalidation_*.md` (zero or more) |

---

## Failure visibility

Rule E.8 (sweep failed / skipped / partial) evaluates the receipts directory at the start of every run. If the most recent receipt is older than `2 × 7 days = 14 days`, the sweep surfaces it to Malik immediately. This closes the "silent scheduler failure" gap.

---

## Interaction with `wiki_ingest_health.py`

Kept separate. The ingest-health script gates `wiki-build` invocations based on queue staleness; the freshness verifier detects source drift. Both can coexist and complement each other — the freshness sweep's receipt reports queue awareness, but does not replace the ingest-health job.

---

*Wiki Freshness Scheduled Task Spec v0.1 — 2026-04-14*
