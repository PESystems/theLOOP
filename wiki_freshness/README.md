# Wiki Freshness Verifier

**A read-only detector that surfaces drift between ingested wiki pages and their source files on the Floor.**

Sibling of Floor Janitor (`Git/theLOOP/janitor/`). Same scaffolding pattern, entirely separate scope and state.

---

## What this closes

Before this existed the wiki had:

- no idle-time source drift detection
- no changed-source detection after ingest
- no source-map vs live-filesystem reconciliation
- no wiki-grade per-run receipts
- no scheduled passive sweep for silent source changes

This verifier addresses all five.

## What it does

| Capability | Behavior |
|---|---|
| **Source-map parsing** | Reads `wiki_schema/source_map.md` (schema v0.2) for LOOP and YASK wikis |
| **Drift classification** | SHA256 + mtime vs stored baseline → 7 status codes |
| **Forward reconciliation** | Every source_map row resolved against the live filesystem |
| **Reverse reconciliation** | `--reverse-scan` surfaces untracked source candidates under bounded roots |
| **Red-flag rules** | E.1–E.11 — mirrors Janitor's rule-and-severity style, disjoint scope |
| **Revalidation staging** | One request artifact per drifted row, written to `queue/` |
| **Per-run receipts** | `sweep_receipt_YYYYMMDD_HHMMSS.md` under `receipts/` |

## What it does NOT do

- Does not rewrite wiki pages — canonical mutation belongs to `wiki-build` / `wiki-write-through`
- Does not modify `source_map.md` — new baselines are emitted by the ingest path
- Does not touch Janitor state — `JANITOR_WrkSps/` is off-limits
- Does not evaluate blocker / packet / response state
- Does not auto-invoke downstream skills

## Package contents

```
wiki_freshness/
├── README.md                                                      ← you are here
├── architecture/
│   ├── wiki_freshness_agent_design_v0.1__20260414__draft.md
│   ├── wiki_freshness_red_flag_rules_v0.1__20260414__draft.md     ← 11 rules (E.1–E.11)
│   └── wiki_freshness_revalidation_handoff_v0.1__20260414__draft.md
├── automation/
│   ├── wiki_freshness_scheduled_task_spec_v0.1__20260414__draft.md
│   └── test_drift_matrix.py                                       ← self-test
├── receipts/            ← generated per run
├── reports/             ← generated per run
└── queue/               ← staged revalidation requests
```

The verifier script itself lives at `theLOOP/housekeeping/wiki_source_drift.py` (alongside `wiki_ingest_health.py`, per existing repo convention).

## How to run

```
# default sweep (reads both source maps, stages requests, writes receipt+report)
python theLOOP/housekeeping/wiki_source_drift.py

# + reverse discovery of untracked candidate sources
python theLOOP/housekeeping/wiki_source_drift.py --reverse-scan

# pure detection, no queue writes
python theLOOP/housekeeping/wiki_source_drift.py --no-stage

# self-test (fixture harness, no real files touched)
python Git/theLOOP/wiki_freshness/automation/test_drift_matrix.py
```

Exit codes:
- `0` clean (only legacy rows, no drift)
- `1` low/medium red flags
- `2` high red flags (`hash_changed`, `missing_source`, `unresolved_path`)
- `3` critical — source map missing or unparseable

## Scheduled automation

`Scheduled/wiki-freshness-weekly/SKILL.md` runs the verifier on a weekly cadence (Mon 08:00 local). Sibling to Janitor's `janitor-sweep-2d`, not a submode.

## Schema v0.2 source_map

Upgraded 2026-04-14 for both LOOP (`wiki_schema/source_map.md`) and YASK (`YASK_WrkSps/wiki_schema/source_map.md`). Added columns:

- `Source SHA256 At Ingest`
- `Source MTime At Ingest`
- `Baseline Status` ∈ {`legacy_no_baseline`, `current`, `reingest_pending`, `source_missing`}

All pre-upgrade rows carry `legacy_no_baseline` — they are **not** silently upgraded. They must be re-ingested through `wiki-build` to establish a trusted baseline.

## Ingest emission contract (follow-up)

`wiki-build` skill must be patched to emit baseline metadata (hash + mtime + `current` status) on every new ingest. The emission contract lives in `architecture/wiki_freshness_revalidation_handoff_v0.1__20260414__draft.md`. Until that patch lands, new ingests must manually populate the three columns.

## Boundary vs Janitor

See `architecture/wiki_freshness_agent_design_v0.1__20260414__draft.md` § "Architecture boundary vs Janitor" for the full table. Short form: no shared state, no shared rules, no shared scheduler.

---

*Wiki Freshness Verifier — packaged 2026-04-14*
