# Wiki Freshness Verifier — Agent Design v0.1

**Date:** 2026-04-14
**Status:** draft, initial build complete
**Sibling of:** Floor Janitor (`Git/theLOOP/janitor/`)

---

## What this is

A **read-only detection agent** that verifies wiki source-file freshness and surfaces drift between scheduled wiki build passes. It is the freshness complement to wiki structural lint — lint checks the graph *inside* the wiki; this checks the wiki *against its sources*.

It reuses Janitor's scaffolding patterns (scheduled task + red-flag rules + receipts + read-only detection) but does not share scope, state, or charter.

## What it does

| Capability | Behavior |
|---|---|
| **Source-map parsing** | Reads `wiki_schema/source_map.md` (schema v0.2) for every registered wiki |
| **Drift classification** | SHA256 + mtime compared against stored baseline; rows classified into 7 status codes |
| **Filesystem reconciliation** | Forward (row → live file). Bounded reverse scan (`--reverse-scan`) surfaces untracked source candidates |
| **Queue awareness** | Peeks at `ingest_queue.md` for each wiki and reports staleness in the receipt (non-authoritative) |
| **Red-flag evaluation** | Applies the E.1–E.11 ruleset; returns exit code matching max severity |
| **Revalidation staging** | Writes one request artifact per drifted row to `queue/`; does NOT rewrite wiki pages |
| **Per-run receipts** | Every invocation emits a timestamped receipt with run_id, counts, flags, outputs |

## What it does NOT do

- **Does not rewrite wiki pages.** Canonical mutation is the job of `wiki-build` / `wiki-write-through`, authorized in an interactive session.
- **Does not modify `source_map.md`.** New baselines are written by the ingest/build path, not the detector.
- **Does not touch Janitor state files** (`JANITOR_WrkSps/state/*.yaml`).
- **Does not evaluate blocker/packet/response state** — that is Janitor's exclusive scope.
- **Does not make promotion decisions** (wiki → Container). Promotion gate stays a separate path.
- **Does not overwrite receipts.** Every run produces a new receipt filename.

## Status codes emitted by the classifier

| Status | Meaning | Drives red flag |
|---|---|---|
| `unchanged` | stored hash matches live hash | — |
| `hash_changed` | hashes differ, mtime relationship unknown/unchanged | E.1 |
| `mtime_newer_than_ingest` | hashes differ AND live mtime > stored mtime | E.3 |
| `missing_source` | path does not resolve anywhere | E.2 |
| `unresolved_path` | path resolves but hashing failed (IO error) | E.7 |
| `legacy_no_baseline` | schema v0.2 row but baseline fields empty / pre-upgrade row | E.6 |
| `cluster_reference` | path represents a directory or multi-doc cluster, not a single file | — (logged) |

## Architecture boundary vs Janitor

| Dimension | Janitor | Wiki Freshness |
|---|---|---|
| Primary domain | operational state (blockers, packets, responses) | wiki source integrity |
| State files | `JANITOR_WrkSps/state/*.yaml` (4 files) | `wiki_schema/source_map.md` (read-only) |
| Rule prefix | A / B / C / D (12 rules) | E (11 rules) |
| Mutation | writes to its own state | **none** — read-only |
| Receipts | `janitor/receipts/` | `wiki_freshness/receipts/` |
| Scheduled task | `janitor-sweep-2d` (every 2 days) | `wiki-freshness-weekly` (weekly) |
| Snapshots | pre-mutation SHA256 snapshots | N/A (no mutation to snapshot) |
| Queue | `packet_queue.yaml` (operational) | `wiki_freshness/queue/` (revalidation requests) |

The two systems share no state, no rules, and no scheduler. They may reuse receipt formatting helpers if those are promoted to a shared utility later — but never a shared evaluation loop.

## Run modes

```
python theLOOP/housekeeping/wiki_source_drift.py                    # default sweep
python theLOOP/housekeeping/wiki_source_drift.py --reverse-scan     # + untracked discovery
python theLOOP/housekeeping/wiki_source_drift.py --no-stage         # pure detection, no revalidation requests
```

All modes are read-only with respect to wiki content and source files. `--no-stage` suppresses even the queue writes.

## Files

```
Git/theLOOP/wiki_freshness/
├── README.md
├── STATUS.md
├── architecture/
│   ├── wiki_freshness_agent_design_v0.1__20260414__draft.md   (this file)
│   ├── wiki_freshness_red_flag_rules_v0.1__20260414__draft.md
│   └── wiki_freshness_revalidation_handoff_v0.1__20260414__draft.md
├── automation/
│   ├── wiki_freshness_scheduled_task_spec_v0.1__20260414__draft.md
│   └── test_drift_matrix.py
├── receipts/            # per-run receipts (generated)
├── reports/             # per-run drift reports (generated)
└── queue/               # staged revalidation requests (generated)

theLOOP/housekeeping/
└── wiki_source_drift.py   # the verifier itself

Scheduled/wiki-freshness-weekly/
└── SKILL.md               # scheduled wrapper

wiki_schema/source_map.md            # schema v0.2 (upgraded 2026-04-14)
YASK_WrkSps/wiki_schema/source_map.md  # schema v0.2 (upgraded 2026-04-14)
```

## Ingest/build emission requirement

Future ingests — performed by the `wiki-build` skill — MUST emit baseline metadata:

- compute `SHA256` of each source file at the moment of ingest
- read filesystem mtime at the same moment
- write both into the `Source SHA256 At Ingest` and `Source MTime At Ingest` columns for the row
- set `Baseline Status` to `current`
- append a receipt under `wiki_freshness/receipts/` with `kind: build` summarizing the emission

A skill-side patch to `wiki-build` is the next follow-up (tracked in open items below). Until that lands, new ingests must manually populate the three columns or the row is added with `legacy_no_baseline`.

## Promotion criterion interaction

The wiki → Container promotion gate already requires "source file unchanged since ingest." This detector makes that check **continuously verifiable** instead of promotion-time-only. A page whose source is currently in `hash_changed` or `mtime_newer_than_ingest` status is automatically promotion-blocked.

## Open items

- Skill-side patch for `wiki-build` to emit baseline metadata on every new ingest (see `wiki_freshness_revalidation_handoff_v0.1` for the emission contract).
- Prioritized re-ingest plan for the 62 existing `legacy_no_baseline` rows.
- Integration with `wiki-write-through` for the subset of drifted rows that need claim-level revalidation (YASK wiki use case).

---

*Wiki Freshness Verifier Agent Design v0.1 — 2026-04-14*
