---
tags:
- loop
- janitor
- implementation
- phases
- v0_3
---
# Floor Janitor Implementation Phases v0.3
**Version:** v0.3 — draft
**Date:** 2026-04-12
**Status:** DESIGN — no implementation
**Companion to:** `floor_janitor_agent_design_v0.3__20260412__draft.md`

---

## Phase Overview

| Phase | Name | Sessions | Hook Dependency | Prereqs |
|-------|------|----------|----------------|---------|
| 1 | Foundation + First Sweep | 1 | None | Design deliverables complete |
| 2 | Dispatch + Forms | 1 | None | Phase 1 complete |
| 3 | Automated Cadence | 1 | None | Phase 2 complete |
| 4 | Hook Infrastructure | 2 | **FUTURE MERGE — Power Automate** | Phase 3 complete + Relay layer built |
| 5 | Notion State Mirror | 1 | **FUTURE MERGE — Power Automate** | Phase 4 complete |

**Total estimated sessions:** 6 (Phases 1–3 are immediately executable; Phases 4–5 are blocked on external infrastructure)

---

## Phase 1: Foundation + First Sweep

**Goal:** Produce the first Janitor sweep from scratch — one session, no hooks, no automation.

**Session count:** 1

**Prereqs:** This design document + state schema + output templates exist in `JANITOR_WrkSps/architecture/`.

### Steps

#### 1.1 Verify Directory Structure
- Confirm `JANITOR_WrkSps/` exists with all 5 subdirectories: `architecture/`, `state/`, `logs/`, `reports/`, `forms/`
- Already created during design run (2026-04-12)
- **Exit criterion:** `ls` confirms all 5 directories exist

#### 1.2 Create Janitor Sweep Prompt
- Write `JANITOR_WrkSps/architecture/janitor_sweep_prompt_v0.3.md`
- Content: the prompt delta that activates Janitor mode when Malik runs it manually
- Includes: responsibility scope, sweep stage sequence (11 stages from Section 4A of design doc), output format pointers, state schema reference
- **Exit criterion:** Prompt file exists, references the correct schema version, contains all 11 sweep stages

#### 1.3 Create Empty State File
- Write `JANITOR_WrkSps/state/janitor_state.yaml` with all fields at defaults (per state schema Section 1 defaults)
- All lists empty, run_metadata fields at default/blank
- **Exit criterion:** `yaml.safe_load()` succeeds on the file; schema_version = "v0.3"

#### 1.4 Create Idea Inbox
- Write `JANITOR_WrkSps/state/idea_inbox.yaml` — empty list with header comment explaining the format
- Write `JANITOR_WrkSps/state/idea_archive.yaml` — empty list with header comment
- **Exit criterion:** Both files exist and parse as valid YAML

#### 1.5 Create Run Log
- Write `JANITOR_WrkSps/logs/janitor_run_log.md` with header and empty table structure
- Columns: `run_id | timestamp | sweep_type | status | trackers_read | blockers_detected | dispatches_sent | duration_s`
- **Exit criterion:** File exists with header row

#### 1.6 Execute First Sweep
- Run the 11-stage sweep sequence manually:
  1. **Mount:** Load state (will be empty/defaults)
  2. **Read:** Fetch all 7 tracker System State blocks via Notion MCP
  3. **Diff:** No previous snapshot — all trackers are new
  4. **Scan:** Read `SKILL_PERFORMANCE_LOG.md` for all entries
  5. **Check:** Read scheduled task data from performance log (last fire dates)
  6. **Detect:** Run blocker detection (from tracker active_blockers fields), promotion candidate check (Doctrine Refresh is PROMOTED — already complete), overlap detection (register known siblings), convergence detection (Ingestion ↔ Write-Through, Dynamic Extraction ↔ Autoresearch), doctrine drift (Floor Index v1.0 stale refs, D3 brain skills citing v2.2)
  7. **Triage:** Idea inbox is empty — skip
  8. **Report:** Generate the first Type 2 report to `JANITOR_WrkSps/reports/JANITOR_report_20260413.md`
  9. **Dispatch:** No Type 1 packets on first run (no threshold crossings, no new promotion candidates)
  10. **State:** Write populated `janitor_state.yaml` with all tracker snapshots, skill snapshots, blockers, siblings
  11. **Log:** Append first entry to `janitor_run_log.md`
- **Exit criterion:** State file populated, Type 2 report exists and is non-empty, run log has 1 entry

#### 1.7 Build Skill Registry Snapshot
- Write `JANITOR_WrkSps/reports/skill_registry_current.md` — consolidated table from skill snapshots
- Columns per design Section 2g
- **Exit criterion:** File exists with all 34 skills listed

### Phase 1 Outputs
| Artifact | Path | Type |
|----------|------|------|
| Sweep prompt | `architecture/janitor_sweep_prompt_v0.3.md` | New file |
| Initial state | `state/janitor_state.yaml` | New file (then overwritten by sweep) |
| Idea inbox | `state/idea_inbox.yaml` | New file |
| Idea archive | `state/idea_archive.yaml` | New file |
| Run log | `logs/janitor_run_log.md` | New file |
| First Type 2 report | `reports/JANITOR_report_20260413.md` | New file |
| Skill registry | `reports/skill_registry_current.md` | New file |

### Phase 1 Does NOT Include
- Type 1 dispatch packets (no threshold crossings expected on first run)
- HTML blocker forms (blockers are Stage 1 on first detection — forms start at Stage 2)
- Scheduled automation
- Hook infrastructure
- Notion state mirror

---

## Phase 2: Dispatch + Forms

**Goal:** Implement Type 1 dispatch packets, HTML blocker escalation forms, and idea inbox processing.

**Session count:** 1

**Prereqs:** Phase 1 complete. At least one full sweep has run. State file is populated.

### Steps

#### 2.1 Build Type 1 Dispatch Packet Templates
- Create filled YAML dispatch templates for all 6 packet types (per design Section 5):
  - Skill Improvement Dispatch
  - Container Promotion Dispatch
  - Doctrine Update Dispatch
  - Phase Unblock Action
  - Overlap Remediation
  - New Idea Triage
- Each template lives as a reference in `JANITOR_WrkSps/architecture/dispatch_templates/`
- **Exit criterion:** 6 template files exist, each with all required fields per the design doc, no placeholders

#### 2.2 Implement Dispatch Logic in Sweep Prompt
- Update the sweep prompt to include dispatch generation at Stage 9:
  - Check `pending_skill_dispatches` before sending new skill improvement packets
  - Check `pending_promotion_dispatches` before sending new promotion packets
  - Check `pending_migration_dispatches` before sending new migration packets
  - Write dispatch packets to `JANITOR_WrkSps/reports/dispatches/JANITOR_dispatch_YYYYMMDD_NNN.yaml`
- **Exit criterion:** Sweep prompt Stage 9 contains dispatch logic with double-trigger prevention

#### 2.3 Build HTML Blocker Form Generator
- Create the Stage 2 blocker form template (`forms/blocker_form_template.html`)
- Create the Stage 3 variant with red/high-contrast styling and animated border pulse
- Form fields per design Section 5 HTML blocker form schema
- Decision output writes to `forms/BLK-YYYYMMDD-NNN_decision.yaml`
- **Exit criterion:** Both form variants render correctly in a browser; decision YAML schema matches state schema

#### 2.4 Implement Blocker Escalation in Sweep
- Update sweep prompt to include escalation logic:
  - Stage 1 → 2 transition at 7 days / 2 sweeps
  - Stage 2 → 3 transition at 21 days / 4 sweeps
  - Form generation at Stage 2+
  - Ignored-blocker resurface at count 10
- **Exit criterion:** Escalation thresholds match design doc; ignored-blocker counter logic is present

#### 2.5 Wire Idea Inbox Processing
- Update sweep prompt Stage 7 (Triage):
  - Read `state/idea_inbox.yaml`
  - Run overlap detection against existing trackers and skills
  - Apply triage criteria (5 tests from design Section 2i)
  - Write verdicts to Type 2 report "Idea Triage Results" section
  - Move processed items to `state/idea_archive.yaml` or leave in inbox with "NEEDS CLARIFICATION"
- **Exit criterion:** A test idea deposited in inbox is correctly triaged on next sweep

#### 2.6 Run Second Sweep
- Execute full sweep with dispatch and form capabilities active
- Verify: any blocker from first sweep that is still present has `sweeps_persisted` incremented
- Verify: dispatch logic runs without producing false dispatches
- **Exit criterion:** Second Type 2 report includes change diffs from first report; state reflects 2 runs

### Phase 2 Outputs
| Artifact | Path | Type |
|----------|------|------|
| Dispatch templates (6) | `architecture/dispatch_templates/*.yaml` | New files |
| Blocker form template (Stage 2) | `forms/blocker_form_template.html` | New file |
| Blocker form template (Stage 3) | `forms/blocker_form_template_critical.html` | New file |
| Decision YAML schema | `architecture/blocker_decision_schema.yaml` | New file |
| Updated sweep prompt | `architecture/janitor_sweep_prompt_v0.3.md` | Updated |
| Second Type 2 report | `reports/JANITOR_report_YYYYMMDD.md` | New file |

---

## Phase 3: Automated Cadence

**Goal:** Register the Janitor sweep as a Claude Code scheduled task for weekly automated runs.

**Session count:** 1

**Prereqs:** Phase 2 complete. Manual sweeps have been validated at least twice.

### Steps

#### 3.1 Register Scheduled Task
- Use Claude Code's scheduled task system to register a weekly Janitor sweep
- Schedule: Sunday 20:00 ET (after all other Sunday automated skills have completed)
- Task definition:
  - Name: `janitor-weekly-sweep`
  - Command: Run the Janitor sweep prompt against the JANITOR_WrkSps workspace
  - Cadence: Weekly, Sunday 20:00
- **Exit criterion:** `list_scheduled_tasks` shows `janitor-weekly-sweep` registered

#### 3.2 Update State Schema for Automation
- Add `automation_config` section to state schema:
  - `scheduled_task_id`: the registered task ID
  - `auto_sweep_enabled`: bool (default true, killswitch)
  - `last_auto_run`: iso8601
  - `auto_run_failures`: int (counter for consecutive auto-run failures)
- **Exit criterion:** State schema updated; field added to state file

#### 3.3 Add Automation Guard to Sweep Prompt
- Add startup check: if `auto_run_failures >= 3`, halt and require manual intervention
- Add startup check: if `auto_sweep_enabled == false`, halt with "Automation disabled" message
- **Exit criterion:** Guards present in sweep prompt; tested by temporarily setting flag

#### 3.4 First Automated Run
- Let the scheduled task fire on the next Sunday
- Verify: report generated, state updated, run log appended
- Compare output quality against manual runs
- **Exit criterion:** Automated run produces identical output structure to manual runs

### Phase 3 Outputs
| Artifact | Path | Type |
|----------|------|------|
| Scheduled task registration | Claude Code scheduled tasks | System config |
| Updated state schema | `state/janitor_state.yaml` | Updated |
| Updated sweep prompt | `architecture/janitor_sweep_prompt_v0.3.md` | Updated |
| First automated report | `reports/JANITOR_report_YYYYMMDD.md` | New file |

---

## Phase 4: Hook Infrastructure

**Status:** FUTURE MERGE — Power Automate

**Goal:** Connect Janitor to real-time triggers via Power Automate flows.

**Session count:** 2

**Prereqs:** Phase 3 complete. Power Automate / Relay layer is built and operational. This phase cannot begin until the Relay infrastructure exists on the Floor.

### Steps (Design-Level — Not Execution-Ready)

#### 4.1 File Watch Hook (Hook 1 + Hook 5)
- Power Automate flow monitors `LENY_WrkSps/skills/`, `LENY_WrkSps/architecture/`, `LENY_WrkSps/container/pending-upload/`
- On new/modified file: writes event to `JANITOR_WrkSps/state/pending_file_events` in janitor_state.yaml
- Janitor processes queued events on next sweep (does not interrupt)

#### 4.2 Threshold Alert Hook (Hook 2)
- Power Automate flow monitors `LENY_WrkSps/logs/SKILL_PERFORMANCE_LOG.md` for new entries
- On threshold crossing detected: triggers immediate Janitor mini-sweep (Stages 4 + 9 only)
- Produces skill improvement dispatch packet

#### 4.3 Tracker Status Hook (Hook 3)
- Notion webhook (via Power Automate) monitors tracker page updates
- On status change to BLOCKED or COMPLETE: triggers mini-sweep (Stages 2-3 + 6)
- Updates affected tracker snapshot in state

#### 4.4 Idea Deposit Hook (Hook 4)
- Power Automate flow monitors `JANITOR_WrkSps/state/idea_inbox.yaml` for modifications
- On change: queues for next scheduled sweep (no interrupt)

#### 4.5 Blocker Escalation Timer (Hook 6)
- Power Automate scheduled flow checks blocker ages daily
- When a blocker crosses the 7-day or 21-day threshold: triggers form generation mini-sweep
- Independent of the weekly sweep cadence

### Phase 4 Outputs
| Artifact | Type |
|----------|------|
| 5 Power Automate flow definitions | PA flows |
| Mini-sweep prompt variants | Janitor prompt updates |
| Hook test suite | Validation runs |

### Phase 4 Blockers
- **No Power Automate infrastructure exists on the Floor today.** The wiki page "The Relay" documents the concept, but no executable flows have been built.
- This phase is entirely gated on the Relay layer being operational.
- **Do not attempt Phase 4 until Malik confirms Relay readiness.**

---

## Phase 5: Notion State Mirror

**Status:** FUTURE MERGE — Power Automate

**Goal:** Mirror Janitor state and reports to a Notion page for mobile visibility.

**Session count:** 1

**Prereqs:** Phase 4 complete. Notion write capability proven via `loop-write-through` skill.

### Steps (Design-Level — Not Execution-Ready)

#### 5.1 Create Janitor Dashboard Page in Notion
- Parent: Runtime & Phase Artifacts zone (33dd67199b338176bd28f993d56ca4e8)
- Page structure:
  - System Health Status (GREEN/YELLOW/RED badge)
  - Active Blockers summary table
  - Tracker State summary table
  - Last Sweep metadata
  - Link to full Floor report

#### 5.2 Add Notion Write to Sweep Prompt
- After Stage 10 (State write), add Stage 10b: Notion mirror write
- Uses `loop-write-through` or direct Notion MCP to update the dashboard page
- Idempotent — overwrites the same page each sweep

#### 5.3 Mobile Notification (Stretch)
- If Power Automate can send push notifications: trigger notification on RED status or Stage 3 blockers
- This is a stretch goal, not a Phase 5 requirement

### Phase 5 Outputs
| Artifact | Type |
|----------|------|
| Notion dashboard page | Notion page |
| Updated sweep prompt | Janitor prompt update |
| Notification flow (stretch) | PA flow |

### Phase 5 Blockers
- Depends on Phase 4 (Power Automate infrastructure)
- Depends on Notion write permissions being proven safe for this use case
- **Do not attempt Phase 5 until Phase 4 is validated.**

---

## Cross-Phase Dependencies

```
Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4 ──→ Phase 5
  (manual)    (dispatch)   (auto)     (hooks)     (mirror)
                                        ↑
                                   BLOCKED ON
                                 Power Automate
                                  / Relay layer
```

- Phases 1–3 form a self-contained, immediately executable chain
- Phase 4 is hard-gated on external infrastructure
- Phase 5 depends on Phase 4

---

## Risk Register

| Risk | Phase | Impact | Mitigation |
|------|-------|--------|-----------|
| Notion MCP outage during first sweep | 1 | Cannot populate tracker snapshots | Design includes proxied_from_state fallback; first run with zero MCP = empty tracker section, not failure |
| State file corruption | 1–3 | Lost previous snapshot | Write-to-tmp-then-rename pattern; malformed-file recovery in design |
| Scheduled task fails silently | 3 | Missed sweep with no report | auto_run_failures counter; consecutive failures = halt + manual review |
| Power Automate never materializes | 4–5 | Phases 4–5 permanently deferred | Phases 1–3 provide full Janitor capability via scheduled weekly sweep; hooks are optimization, not requirement |
| Blocker escalation false positives | 2 | Malik receives unnecessary forms | Stage 1 is report-only (no forms); forms start at Stage 2 (7 days), giving time to clear naturally |
| Dispatch double-triggering | 2 | Same skill improvement sent twice | pending_*_dispatches registers prevent re-dispatch until confirmed or expired |

---

## Success Criteria per Phase

| Phase | Success = |
|-------|-----------|
| 1 | First Type 2 report exists, is non-empty, covers all 14 report sections (even if empty), state file is populated with all 7 trackers, run log has 1 entry |
| 2 | Dispatch packet generated for at least one test case; HTML form renders correctly; idea inbox processes a test entry; second report shows diffs from first |
| 3 | Automated sweep fires on schedule; output matches manual sweep structure; auto_run_failures stays at 0 |
| 4 | At least one hook triggers a mini-sweep; queued events are correctly processed on next full sweep |
| 5 | Notion dashboard page exists and is updated by automated sweep; mobile view shows current system health |

---

*Floor Janitor Implementation Phases v0.3 -- Draft -- 2026-04-12*
