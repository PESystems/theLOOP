# Wiki Freshness Verifier — Build Status

## Phase tracker

| Phase | Status | Date | Notes |
|---|---|---|---|
| D1 — Source map schema upgrade | ✅ complete | 2026-04-14 | LOOP + YASK maps at schema v0.2; 62 legacy rows marked |
| D2 — Ingest/build emission patch | 🟡 contract-only | 2026-04-14 | Contract defined in revalidation_handoff_v0.1; `wiki-build` skill patch is the follow-up |
| D3 — Freshness verifier script | ✅ complete | 2026-04-14 | `theLOOP/housekeeping/wiki_source_drift.py` v0.1 |
| D4 — Red-flag rules | ✅ complete | 2026-04-14 | E.1–E.11, draft |
| D5 — Scheduled sweep | ✅ complete | 2026-04-14 | `Scheduled/wiki-freshness-weekly/SKILL.md` |
| D6 — Receipt layer | ✅ complete | 2026-04-14 | sweep receipts emitted; build receipts pending D2 follow-up |
| D7 — Revalidation handoff | ✅ complete | 2026-04-14 | queue/ pattern + hard interlock `canonical_write_authorized: false` |
| D8 — Janitor boundary preservation | ✅ verified | 2026-04-14 | no janitor files modified; rule families disjoint (A/B/C/D vs E) |

## Test matrix

| Case | Result |
|---|---|
| unchanged tracked source | PASS |
| edited tracked source (hash_changed) | PASS |
| edited tracked source (mtime_newer_than_ingest) | PASS |
| missing tracked source | PASS |
| legacy row with no baseline | PASS |
| unresolved path | PASS |
| receipt generation | PASS (real run 2026-04-14T08:43) |
| drift report generation | PASS (real run 2026-04-14T08:43) |
| revalidation request staging | PASS (9 requests staged from real run) |
| reverse scan untracked discovery | PASS (62 candidates surfaced) |

## Open items

- **OPEN-1**: `wiki-build` skill-side patch to emit SHA256 + mtime + `Baseline Status: current` on new ingests. Contract ready; skill edit is follow-up work (cowork-side, not this task's scope).
- **OPEN-2**: Prioritized re-ingest plan for the 62 `legacy_no_baseline` rows. Recommend batching by doctrine-criticality (LOOP_Architecture + System_Prompt first; YASK dossiers next).
- **OPEN-3**: Integration with `wiki-write-through` for YASK claim-level drift — flagged in revalidation_handoff_v0.1 but not wired.
- **OPEN-4**: NRGY wiki has no `wiki_schema/source_map.md` yet; verifier currently skips it. Either stand one up or document the exclusion formally.
- **OPEN-5**: Receipt directory is unbounded; add rotation/compaction when receipt count exceeds a threshold.
