# Floor Janitor — Status Tracker

> Last updated: 2026-04-13
> Package version: v0.1
> Runtime location: `C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps` (outside this repo)

---

## Current State

**Live.** Scheduler registered, Phase 2D complete, first real scheduled run due 2026-04-14 at 9:00 AM local.

---

## Phase History

| Phase | Scope | Status | Receipt |
|-------|-------|--------|---------|
| **1** | Initial agent design + first manual sweep | complete | `receipts/phase1_completion_receipt_20260412.md` (in WrkSps) |
| **2A** | Blocker form generation + state schema v0.3 | complete | |
| **2A.1** | Corrective patch — structured payloads, packet normalization, dependency-aware queue, hardened YAML output | complete | |
| **2B** | Response ingestion layer — contract, validation B.1-B.6, test-mode proof pass | complete | |
| **2C** | First real-response operational pass (zero eligible, partial) | complete | |
| **2C-R1** | Rerun after BLK-004 filled — first successful real ingestion | complete | |
| **D3 Execution** | Bounded v2.2 → v3.0 stale-ref fix in 4 brain skills | complete | `receipts/d3_execution_receipt_20260412.md` |
| **2D** | Automation scaffolding — scheduler, red-flag checker, hook scaffolding, dry-run proof | complete | `receipts/phase2d_completion_receipt_20260412.md` |
| **Scheduler migration** | Windows Task Scheduler → Claude Scheduled Tasks (primary) | complete | `receipts/janitor_scheduler_surface_decision_20260412.md` |

---

## Live Components

| Component | Status | Detail |
|-----------|--------|--------|
| Scheduled sweep entrypoint | LIVE | `automation/run_janitor_scheduled.py` — tested dry-run passes |
| Red-flag checker | LIVE | `automation/check_janitor_red_flags.py` — 12 rules, exit codes 0-3 |
| Claude Scheduled Task | REGISTERED | `janitor-sweep-2d`, cron `0 9 */2 * *`, next run 2026-04-14 09:00 local |
| Hook scaffolding | DEFERRED | Draft only. Activation after 3+ successful scheduled runs |
| Snapshot protocol | LIVE | SHA-256-verified backups before every mutation |

---

## Active Blockers (reference — lives in `JANITOR_WrkSps/state/janitor_state.yaml`)

| Blocker | Status | Stage | Notes |
|---------|--------|-------|-------|
| BLK-20260412-001 | active | 1 | Security abstraction layer design |
| BLK-20260412-002 | pending_decision | 1 | Auth storage for Phase F |
| BLK-20260412-003 | externally_blocked | 1 | YASK source file access |
| BLK-20260412-004 | **approved_unlocked** | 1 | D3 completed 2026-04-12 |
| BLK-20260412-005 | pending_decision | 1 | YAML family naming path |
| BLK-20260412-006 | pending_decision | 1 | Container HISTORICAL file cleanup |

---

## Next Actions

| Priority | Action | Owner |
|----------|--------|-------|
| P1 | First real scheduled sweep fires 2026-04-14 09:00 — observe output | automated |
| P2 | Malik fills responses for BLK-002, BLK-005, BLK-006 when ready | Malik |
| P3 | After 3 successful scheduled runs, activate hook scaffolding | LENY |
| P4 | D1 + D2 defects remain deferred — reassess after D3 verified in live use | Malik |

---

## Design Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-12 | Pre-mutation snapshot is mandatory, not optional | Rollback must always exist |
| 2026-04-12 | Real follow-up artifacts use `__draft.md`, test artifacts use `__test.md` | No silent overwrite of test proofs |
| 2026-04-12 | Hook activation deferred until 3+ real scheduled runs | Don't build the layer before the foundation |
| 2026-04-13 | Scheduler surface = Claude Scheduled Tasks (primary) | Already 8 LOOP tasks on this surface; Windows not needed |
| 2026-04-13 | Package Janitor into theLOOP git repo | Version history, diff visibility, remote backup |

---

*Floor Janitor Tracker — maintained by LENY — cross-check against `leny/STATUS.md` for overall repo state*
