# Janitor Scheduler Surface Decision
**Date:** 2026-04-13
**Decision:** `migrate_to_claude_scheduler`

---

## 1. Decision

Janitor's recurring cadence layer is standardized on **Claude Scheduled Tasks** as the primary surface. Windows Task Scheduler is retained as fallback only.

---

## 2. Why

### Evidence that drove the decision

| Factor | Finding |
|--------|---------|
| Claude Scheduled Tasks available | YES — `mcp__scheduled-tasks__create_scheduled_task` is live |
| Existing LOOP tasks on this surface | **8 active tasks** — daily and weekly, all running successfully |
| Windows Task Scheduler registered | NO — zero Janitor tasks found on audit |
| Windows Task Scheduler attempted | NO — PowerShell execution policy blocked even the `schtasks` query initially |
| Janitor needs app-independent execution | NO — the Python sweep script defers real ingestion to a Claude Code session anyway |
| Skipped-run replay | Claude Scheduled Tasks replay on wake/app-reopen |

### Why Claude Scheduled Tasks wins

1. **Already the standard** — Malik's environment runs `loop-patch-report`, `memory-staleness-daily`, `session-archive-compactor-daily`, `wiki-ingest-health-daily`, and 4 others on this surface. Janitor should follow the established pattern.
2. **Simpler operator experience** — no Task Scheduler GUI, no Python PATH configuration, no PowerShell execution policy issues.
3. **The sweep prompt runs as a Claude session** — it can directly read Janitor state, run the Python checker, and report findings conversationally. No silent log file that nobody checks.
4. **Skipped runs replay** — a 2-day sweep won't silently miss if the machine was asleep at the scheduled time.
5. **The Python scripts still work** — they're invoked BY the Claude session, not replaced by it.

### Why Windows Task Scheduler is NOT needed as primary

- Janitor's sweep script discovers responses but defers actual ingestion to a Claude Code session. Running offline only produces a log entry that nobody reads until Claude is open.
- The value of Janitor's heartbeat is surfacing findings to the operator (Malik) inside Claude. Windows Task Scheduler would surface them to a text log file.
- PowerShell execution policy already caused friction during the audit.

---

## 3. What Changed

| File | Change |
|------|--------|
| `architecture/janitor_automation_architecture_v0.1__20260412__draft.md` | Layer A mechanism: "External scheduler" → "Claude Scheduled Task (primary)". "Why External Scheduling" section → "Why Claude Scheduled Tasks" with fallback note. |
| `automation/janitor_scheduler_setup_v0.1__20260412__draft.md` | Full rewrite: Claude Scheduled Tasks = recommended default. Windows Task Scheduler moved to "Fallback" section. Task parameters and prompt spec added. |
| `reports/phase2d_automation_dry_run_report_20260412.md` | Post-build clarification note appended (history not rewritten). |
| `logs/phase2d_completion_receipt_20260412.md` | Post-build clarification note appended (history not rewritten). |

**New files:**

| File | Purpose |
|------|---------|
| `reports/janitor_scheduler_surface_decision_20260412.md` | This decision note |
| `automation/janitor_claude_scheduled_task_spec_v0.1__20260412__draft.md` | Exact task spec for creation |

---

## 4. What Stayed Windows-Specific as Fallback Only

- Windows Task Scheduler setup instructions preserved in the scheduler setup guide under "Fallback" heading
- Cron alternative preserved for cross-platform reference
- The Python entrypoint scripts (`run_janitor_scheduled.py`, `check_janitor_red_flags.py`) are unchanged — they work regardless of which scheduler invokes them

---

## 5. Hook Impact

**None.** Hooks were already in draft-only status (deferred pending 3+ real scheduled runs). The scheduler surface migration does not change hook status or design. The 3-run activation threshold now counts Claude Scheduled Task runs.

---

## 6. Remaining Manual Step

**Create the Claude Scheduled Task.** The exact spec is at `automation/janitor_claude_scheduled_task_spec_v0.1__20260412__draft.md`. It can be created via `/schedule` or the `create_scheduled_task` tool.

---

*Janitor Scheduler Surface Decision — 2026-04-13*
