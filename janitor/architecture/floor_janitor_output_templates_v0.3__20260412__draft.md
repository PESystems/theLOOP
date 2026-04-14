---
tags:
- loop
- janitor
- output
- templates
- v0_3
---
# Floor Janitor Output Templates v0.3
**Version:** v0.3 — draft
**Date:** 2026-04-12
**Status:** DESIGN — no implementation
**Companion to:** `floor_janitor_agent_design_v0.3__20260412__draft.md`

This deliverable contains:
1. Six filled Type 1 dispatch packet templates
2. Type 2 report template + filled example
3. HTML blocker form (Stage 2 and Stage 3 variants)
4. Filled blocker form example
5. Blocker decision YAML submission artifact

---

## Part 1: Type 1 Dispatch Packets (Filled Examples)

### 1.1 Skill Improvement Dispatch

```yaml
# JANITOR_dispatch_20260420_001.yaml
# Type 1 — Skill Improvement Dispatch
dispatch_metadata:
  dispatch_id: "DSP-20260420-001"
  generated_by: "floor-janitor"
  generated_at: "2026-04-20T20:15:00"
  janitor_run_id: "JAN-20260420-001"

target:
  skill: "skill-improvement"
  scope: "global"
  adapter: "cowork_floor"

payload:
  skill_name: "loop-node-hygiene"
  skill_file_path: "LENY_WrkSps/skills/brain/loop-node-hygiene/SKILL.md"
  current_version: "v1.0"
  current_miss_count: 3
  escalation_threshold: 2
  improvement_count: 0
  evidence_entries:
    - date: "2026-04-14T10:30:00"
      event: "miss"
      trigger: "user said 'clean up the system pages'"
      note: "Skill did not fire — trigger phrase not in keyword list"
    - date: "2026-04-16T14:15:00"
      event: "miss"
      trigger: "user said 'tidy the SYSTEM zone'"
      note: "Trigger phrase variant not recognized"
    - date: "2026-04-18T09:00:00"
      event: "miss"
      trigger: "user said 'hygiene audit'"
      note: "Partial keyword match but skill did not activate"

expected_outcome:
  action: "Run improvement pass on loop-node-hygiene"
  proof_of_completion:
    - "Performance log entry: improvement pass for loop-node-hygiene"
    - "Skill file version bumped from v1.0 to v1.1"
    - "Miss count resets in next performance log window"

constraints:
  - "Do NOT dilute the skill's existing aggressive behavior"
  - "Only expand trigger recognition — do not alter core audit logic"
  - "Preserve the 4-bucket classification model exactly"
```

### 1.2 Container Promotion Dispatch

```yaml
# JANITOR_dispatch_20260420_002.yaml
# Type 1 — Container Promotion Dispatch
dispatch_metadata:
  dispatch_id: "DSP-20260420-002"
  generated_by: "floor-janitor"
  generated_at: "2026-04-20T20:18:00"
  janitor_run_id: "JAN-20260420-001"

target:
  skill: "artifact-version-promotion"
  scope: "global"
  adapter: "cowork_floor"

payload:
  artifact_path: "LENY_WrkSps/skills/global/LOOP_Floor_Index_v1.0.md"
  current_version: "v1.0"
  promoted_version: "v1.1"
  target_location: "LENY_WrkSps/skills/global/LOOP_Floor_Index_v1.1.md"
  promotion_reason: "v1.0 references HISTORICAL v2.4 files as active; v3.0 is now live"
  promotion_checklist:
    versioned_filename: false
    header_version_bump: false
    manifest_update: false
    notion_log_entry: false
    prior_version_retained: false

expected_outcome:
  action: "Execute full promotion checklist for Floor Index"
  proof_of_completion:
    - "LOOP_Floor_Index_v1.1.md exists at target path"
    - "MANIFEST.md updated with v1.1 entry"
    - "v1.0 retained as historical"

constraints:
  - "Malik must approve before execution — this is a promotion, not an auto-action"
  - "Retain v1.0 file (do not delete)"
```

### 1.3 Doctrine Update Dispatch

```yaml
# JANITOR_dispatch_20260420_003.yaml
# Type 1 — Doctrine Update Dispatch
dispatch_metadata:
  dispatch_id: "DSP-20260420-003"
  generated_by: "floor-janitor"
  generated_at: "2026-04-20T20:20:00"
  janitor_run_id: "JAN-20260420-001"

target:
  skill: "workspace-path-migration"
  scope: "global"
  adapter: "cowork_floor"

payload:
  drift_type: "stale_doctrine_reference"
  scope: "LENY_WrkSps"
  stale_references:
    - file: "LENY_WrkSps/skills/brain/task-classification/SKILL.md"
      line: 12
      found: "Governing reference: LOOP Architecture v2.2"
      correct: "Governing reference: LOOP Architecture v3.0"
    - file: "LENY_WrkSps/skills/brain/compaction/SKILL.md"
      line: 8
      found: "Governing reference: LOOP Architecture v2.2"
      correct: "Governing reference: LOOP Architecture v3.0"
    - file: "LENY_WrkSps/skills/brain/node-write-back/SKILL.md"
      line: 10
      found: "Governing reference: LOOP Architecture v2.2"
      correct: "Governing reference: LOOP Architecture v3.0"
    - file: "LENY_WrkSps/skills/brain/execution-prompt-design/SKILL.md"
      line: 9
      found: "Governing reference: LOOP Architecture v2.2"
      correct: "Governing reference: LOOP Architecture v3.0"

expected_outcome:
  action: "Sweep stale references and replace with correct version"
  proof_of_completion:
    - "grep for 'v2.2' across brain skills returns zero matches"
    - "All 4 files now reference v3.0"

constraints:
  - "Only update the governing reference line — do not alter skill logic"
  - "This is a D3 defect from Skill System Refactor (TASK-003)"
```

### 1.4 Phase Unblock Action

```yaml
# JANITOR_dispatch_20260420_004.yaml
# Type 1 — Phase Unblock Action
dispatch_metadata:
  dispatch_id: "DSP-20260420-004"
  generated_by: "floor-janitor"
  generated_at: "2026-04-20T20:22:00"
  janitor_run_id: "JAN-20260420-001"

target:
  surface: "malik_decision"
  delivery: "html_form"
  form_path: "JANITOR_WrkSps/forms/JANITOR_blocker_form_20260420_001.html"

payload:
  blocker_id: "BLK-20260413-001"
  source_tracker: "Skill System Refactor TASK-003"
  source_tracker_id: "33fd67199b3381aea666f1cf80c48239"
  blocker_description: "Malik review + Phase 2 authorization required for defect resolution queue"
  detected_date: "2026-04-13T20:01:42"
  escalation_stage: 2
  days_unresolved: 7
  sweeps_persisted: 2
  decision_options:
    - id: "approve_phase2"
      label: "Approve Phase 2 — begin defect resolution queue (P0-P3)"
      consequence: "Lenny will execute Phase 2 in the next available session"
    - id: "defer_phase2"
      label: "Defer Phase 2 — not ready yet"
      consequence: "Blocker moves to ignored register; resurfaces at count 10"
    - id: "modify_scope"
      label: "Approve with modified scope"
      consequence: "Malik specifies which defects to address first"

expected_outcome:
  action: "Malik fills HTML form; decision recorded in YAML submission artifact"
  proof_of_completion:
    - "Decision YAML exists at forms/BLK-20260413-001_decision.yaml"
    - "Next sweep detects decision and updates blocker state"
```

### 1.5 Overlap Remediation

```yaml
# JANITOR_dispatch_20260420_005.yaml
# Type 1 — Overlap Remediation (Report Section)
dispatch_metadata:
  dispatch_id: "DSP-20260420-005"
  generated_by: "floor-janitor"
  generated_at: "2026-04-20T20:24:00"
  janitor_run_id: "JAN-20260420-001"

target:
  surface: "type2_report"
  section: "Overlap Warnings"

payload:
  overlap_pair:
    item_a: "LOOP Ingestion Process"
    item_a_type: "tracker"
    item_b: "YAML → Notion Write-Through Pipeline"
    item_b_type: "tracker"
  overlap_keywords:
    - "YAML"
    - "Notion"
    - "schema"
    - "import"
    - "ingest"
  overlap_percentage: 42
  known_sibling: true
  registered_sibling_date: "2026-04-13T20:02:00"
  recommendation: "sibling — no action"
  rationale: "These trackers are cross-referenced and explicitly designed to converge at Ingestion Phase G. No remediation needed."
```

### 1.6 New Idea Triage

```yaml
# JANITOR_dispatch_20260420_006.yaml
# Type 1 — Idea Triage Result
dispatch_metadata:
  dispatch_id: "DSP-20260420-006"
  generated_by: "floor-janitor"
  generated_at: "2026-04-20T20:26:00"
  janitor_run_id: "JAN-20260420-001"

target:
  surface: "type2_report"
  section: "Idea Triage Results"

payload:
  idea:
    title: "Auto-close Notion tasks when tracker phase completes"
    submitted_by: "Malik"
    submitted_date: "2026-04-19T15:00:00"
    description: "When a tracker phase is marked COMPLETE, automatically close all Notion tasks linked to that phase."
  triage_result:
    overlap_with_trackers: []
    overlap_with_skills:
      - skill: "notion-task-audit"
        overlap_keywords: ["Notion", "task", "close"]
        overlap_percentage: 55
    verdict: "merge_into_existing"
    target: "notion-task-audit"
    target_section: "Phase completion trigger — currently only manual/scheduled. Add phase-complete as trigger source."
    recommendation: "Extend notion-task-audit to accept phase-completion events as a trigger. Do NOT create a new skill."
  action_taken: "moved_to_archive"
  archive_note: "Triaged 2026-04-20. Merge candidate with notion-task-audit. Awaiting Malik confirmation."
```

---

## Part 2: Type 2 Report Template

### Template

```markdown
# JANITOR Report — {{YYYY-MM-DD}}

## Run Metadata
| Field | Value |
|-------|-------|
| Run ID | {{run_id}} |
| Timestamp | {{run_timestamp}} |
| Sweep Type | {{sweep_type}} |
| Duration | {{sweep_duration_seconds}}s |
| Previous Run | {{previous_run_id}} ({{previous_run_timestamp}}) |
| MCP Available | {{mcp_available}} |
| Schema Version | {{schema_version}} |

---

## System Health Summary

**Overall Status: {{GREEN / YELLOW / RED}}**

| Metric | Value |
|--------|-------|
| Trackers monitored | {{count}} |
| Trackers changed since last sweep | {{count}} |
| Active blockers | {{count}} ({{count}} at Stage 2+) |
| Pending dispatches | {{count}} |
| Pending manual actions | {{count}} |
| Scheduled tasks on track | {{on_track}} / {{total}} |

**Status criteria:**
- GREEN: 0 Stage 2+ blockers, 0 missed scheduled tasks, all dispatches confirmed or pending < 2 sweeps
- YELLOW: any Stage 2 blocker, OR any missed scheduled task, OR any dispatch pending >= 2 sweeps
- RED: any Stage 3 blocker, OR 3+ consecutive missed scheduled tasks, OR MCP unavailable

---

## Tracker State

| # | Tracker | Status | Phase | Change Priority | Changes Since Last Sweep | Active Blockers | Read Mode |
|---|---------|--------|-------|----------------|--------------------------|----------------|-----------|
| {{n}} | {{tracker_name}} | {{status}} | {{phase}} | {{P0-P3}} | {{change_summary}} | {{blocker_count}} | {{live/proxied}} |

### Tracker Change Details
{{For each tracker with change_priority < P3:}}

**{{tracker_name}}** ({{change_priority}})
- Previous: {{previous_status}} / {{previous_phase}}
- Current: {{current_status}} / {{current_phase}}
- What changed: {{change_description}}
- Impact: {{impact_assessment}}

---

## Feature / Skill Registry

| Skill | Version | Scope | Status | Last Fired | Misses | Improvements | Classification |
|-------|---------|-------|--------|-----------|--------|-------------|---------------|
| {{skill_name}} | {{version}} | {{scope}} | {{status}} | {{last_fired}} | {{miss_count}} | {{improvement_count}} | {{janitor_classification}} |

---

## Blockers Dashboard

### Active Blockers ({{count}})

| ID | Source Tracker | Description | Type | Stage | Days Unresolved | Sweeps | Form? |
|----|--------------|-------------|------|-------|----------------|--------|-------|
| {{blocker_id}} | {{source_tracker}} | {{description}} | {{blocker_type}} | {{stage}} | {{days}} | {{sweeps}} | {{yes/no}} |

### Blockers Cleared This Period ({{count}})

| ID | Source Tracker | Description | Detected | Cleared | Method | Max Stage |
|----|--------------|-------------|----------|---------|--------|-----------|
| {{blocker_id}} | {{tracker}} | {{description}} | {{detected_date}} | {{cleared_date}} | {{method}} | {{max_stage}} |

### Ignored Blockers ({{count}})

| ID | Source Tracker | Description | Deferred | Reason | Sweep Count | Resurfaces At |
|----|--------------|-------------|----------|--------|-------------|--------------|
| {{blocker_id}} | {{tracker}} | {{description}} | {{deferred_date}} | {{reason}} | {{count}} | {{resurface_at}} |

---

## Dependency Map

| Tracker A | Tracker B | Relationship | Evidence |
|-----------|-----------|-------------|----------|
| {{tracker_a}} | {{tracker_b}} | {{type}} | {{cross_reference / shared_artifact / family}} |

---

## Overlap Warnings

| Item A | Item B | Type | Overlap Keywords | Overlap % | Known Sibling? | Recommendation |
|--------|--------|------|-----------------|-----------|---------------|---------------|
| {{item_a}} | {{item_b}} | {{tracker/skill}} | {{keywords}} | {{pct}} | {{yes/no}} | {{recommendation}} |

---

## Convergence Opportunities

| Tracker A | Tracker B | Signal | Evidence | Recommended Action |
|-----------|-----------|--------|---------|-------------------|
| {{tracker_a}} | {{tracker_b}} | {{signal_type}} | {{evidence}} | {{action}} |

---

## Upcoming Promotions

| Candidate | Source Tracker | Artifact | Current Version | Status | Artifact Verified? |
|-----------|--------------|----------|----------------|--------|-------------------|
| {{candidate_id}} | {{tracker}} | {{artifact_path}} | {{version}} | {{promotion_status}} | {{yes/no}} |

**Action required:** Malik must approve before any promotion is dispatched.

---

## Pending Manual Actions

| ID | Description | Source Tracker | Detected | Completed? |
|----|-------------|--------------|----------|-----------|
| {{action_id}} | {{description}} | {{tracker}} | {{detected_date}} | {{yes/no}} |

---

## Scheduled Task Health

| Task | Expected | Last Fired | Missed Window? | Consecutive Misses |
|------|----------|-----------|---------------|-------------------|
| {{task_name}} | {{day}} {{time}} | {{last_fire_date}} | {{yes/no}} | {{count}} |

---

## Skill Gaps Detected

| Pattern | Occurrences | Covering Skill | Gap Description |
|---------|------------|---------------|-----------------|
| {{failure_pattern}} | {{count}} | None | {{what_is_missing}} |

---

## Idea Triage Results

| Idea | Verdict | Target | Recommendation | Action Taken |
|------|---------|--------|---------------|-------------|
| {{idea_title}} | {{verdict}} | {{target}} | {{recommendation}} | {{moved_to_archive / left_in_inbox}} |

---

## Ignored Items

| Type | ID | Description | Reason | Since |
|------|-----|-------------|--------|-------|
| {{blocker/idea}} | {{id}} | {{description}} | {{reason}} | {{date}} |

---

*Generated by Floor Janitor {{schema_version}} — Run {{run_id}}*
```

---

### Filled Type 2 Report Example (First Run)

```markdown
# JANITOR Report — 2026-04-13

## Run Metadata
| Field | Value |
|-------|-------|
| Run ID | JAN-20260413-001 |
| Timestamp | 2026-04-13T20:00:00 |
| Sweep Type | scheduled |
| Duration | 142s |
| Previous Run | (none — first run) |
| MCP Available | yes |
| Schema Version | v0.3 |

---

## System Health Summary

**Overall Status: YELLOW**

| Metric | Value |
|--------|-------|
| Trackers monitored | 7 |
| Trackers changed since last sweep | 7 (all new — first run) |
| Active blockers | 4 (0 at Stage 2+) |
| Pending dispatches | 0 |
| Pending manual actions | 1 |
| Scheduled tasks on track | 0 / 5 |

**YELLOW because:** All 5 scheduled tasks show missed windows (last fire dates are 7+ days ago). Blockers are all Stage 1 (new). No Stage 2+ escalations yet.

---

## Tracker State

| # | Tracker | Status | Phase | Change Priority | Changes Since Last Sweep | Active Blockers | Read Mode |
|---|---------|--------|-------|----------------|--------------------------|----------------|-----------|
| 1 | LOOP Ingestion Process | ACTIVE | Pilot Complete / Email Next | P3 | First snapshot (baseline) | 1 | live |
| 2 | YAML → Notion Write-Through | ACTIVE | Phase E / F ready | P3 | First snapshot (baseline) | 1 | live |
| 3 | Dynamic Extraction Integration | ACTIVE | Post-Reviewer Build | P3 | First snapshot (baseline) | 0 | live |
| 4 | YASK Autoresearch Harness | ACTIVE | Foundation | P3 | First snapshot (baseline) | 1 | live |
| 5 | LOOP v3.0 Doctrine Refresh | PROMOTED | Phase 5 Complete | P3 | First snapshot (baseline) | 0 | live |
| 6 | Skill System Refactor TASK-003 | ACTIVE | Phase 2 Pending | P3 | First snapshot (baseline) | 1 | live |
| 7 | YAML Family Naming & Cohesion | PROPOSAL | Vocabulary design | P3 | First snapshot (baseline) | 1 | live |

### Tracker Change Details
No changes to report — all trackers are new baselines on first run.

---

## Feature / Skill Registry

| Skill | Version | Scope | Status | Last Fired | Misses | Improvements | Classification |
|-------|---------|-------|--------|-----------|--------|-------------|---------------|
| loop-node-hygiene | v1.0 | brain | active | 2026-04-06 | 0 | 0 | peer |
| loop-node-query | v1.1 | brain | active | 2026-04-12 | 0 | 0 | consumed |
| loop-tracker-create | v1.0 | brain | active | 2026-04-10 | 0 | 0 | independent |
| artifact-version-promotion | v1.1 | global | active | 2026-04-11 | 0 | 0 | orchestrated |
| workspace-path-migration | v1.0 | global | active | — | 0 | 0 | orchestrated |
| skill-improvement | v1.1 | global | active | 2026-04-09 | 0 | 0 | orchestrated |
| skill-performance-ledger | v3.0 | global | active | 2026-04-12 | 0 | 0 | read |
| loop-floor-query | v1.0 | floor | active | 2026-04-12 | 0 | 0 | consumed |
| loop-patch-sync | — | floor | active | 2026-04-11 | 0 | 0 | peer |
| loop-patch-report | v1.0 | floor | active | 2026-04-04 | 0 | 0 | peer |
| (24 additional skills) | — | — | active | — | 0 | 0 | independent |

---

## Blockers Dashboard

### Active Blockers (4)

| ID | Source Tracker | Description | Type | Stage | Days | Sweeps | Form? |
|----|--------------|-------------|------|-------|------|--------|-------|
| BLK-20260413-001 | Skill System Refactor | Malik review + Phase 2 auth | malik_decision | 1 | 0 | 1 | no |
| BLK-20260413-002 | YAML Family Naming | Malik decides path (1/2/3) | malik_decision | 1 | 0 | 1 | no |
| BLK-20260413-003 | Write-Through Pipeline | Auth storage decision for Phase F | malik_decision | 1 | 0 | 1 | no |
| BLK-20260413-004 | YASK Autoresearch | Source files not accessible | tracker_blocked | 1 | 0 | 1 | no |

### Blockers Cleared This Period (0)
None.

### Ignored Blockers (0)
None.

---

## Dependency Map

| Tracker A | Tracker B | Relationship | Evidence |
|-----------|-----------|-------------|----------|
| LOOP Ingestion Process | YAML Write-Through | sibling | Cross-referenced; Ingestion Phase G feeds into Write-Through |
| Dynamic Extraction | YASK Autoresearch | family | YASK Pipeline Family — parent/child |

---

## Overlap Warnings

No new overlaps detected. Known siblings registered:
- Ingestion ↔ Write-Through (sibling)
- Dynamic Extraction ↔ Autoresearch (family)

---

## Convergence Opportunities

| Tracker A | Tracker B | Signal | Evidence | Recommended Action |
|-----------|-----------|--------|---------|-------------------|
| Ingestion Process | Write-Through Pipeline | Phase bridge | Ingestion Phase G explicitly bridges to Write-Through | Monitor — convergence is intentional and designed |
| Dynamic Extraction | Autoresearch Harness | Shared family | Both under YASK Pipeline Family | Monitor — family relationship is documented |

---

## Upcoming Promotions

No new promotion candidates. Doctrine Refresh is PROMOTED (already complete).

---

## Pending Manual Actions

| ID | Description | Source Tracker | Detected | Completed? |
|----|-------------|--------------|----------|-----------|
| MAN-20260413-001 | Delete 4 HISTORICAL files from Container | Doctrine Refresh | 2026-04-13 | no |

---

## Scheduled Task Health

| Task | Expected | Last Fired | Missed Window? | Consecutive Misses |
|------|----------|-----------|---------------|-------------------|
| loop-node-hygiene-weekly | Sun 08:05 | 2026-04-06 | yes | 1 |
| wiki-queue-feeder-weekly | Sun 07:00 | 2026-04-06 | yes | 1 |
| wiki-build-weekly | Sun 08:00 | 2026-04-06 | yes | 1 |
| vendor-docs-weekly | Sat 09:00 | 2026-04-05 | yes | 1 |
| loop-patch-report-weekly | Fri 08:00 | 2026-04-04 | yes | 1 |

**Note:** All scheduled tasks show missed windows. This may indicate the scheduled task infrastructure needs attention, or the tasks fired but did not produce performance log entries.

---

## Skill Gaps Detected

No recurring failure patterns detected on first run.

---

## Idea Triage Results

Idea inbox is empty — no items to triage.

---

## Ignored Items

None.

---

*Generated by Floor Janitor v0.3 — Run JAN-20260413-001*
```

---

## Part 3: HTML Blocker Form

### Stage 2 Form (Attention — Yellow)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JANITOR — Decision Required</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #1a1a2e;
    color: #e0e0e0;
    padding: 2rem;
    min-height: 100vh;
  }
  .form-container {
    max-width: 800px;
    margin: 0 auto;
    background: #16213e;
    border: 3px solid #e2b714;
    border-radius: 12px;
    overflow: hidden;
  }
  .header {
    background: #e2b714;
    color: #1a1a2e;
    padding: 1.5rem 2rem;
    text-align: center;
  }
  .header h1 {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .header .subtitle {
    font-size: 0.9rem;
    margin-top: 0.3rem;
    font-weight: 600;
  }
  .body { padding: 2rem; }
  .field {
    margin-bottom: 1.5rem;
  }
  .field label {
    display: block;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #888;
    margin-bottom: 0.4rem;
  }
  .field .value {
    font-size: 1rem;
    color: #f0f0f0;
    background: #0f3460;
    padding: 0.8rem 1rem;
    border-radius: 6px;
    border-left: 4px solid #e2b714;
  }
  .field .value.urgent {
    border-left-color: #e94560;
  }
  .metadata-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  .decision-section {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 2px solid #e2b714;
  }
  .decision-section h2 {
    font-size: 1.1rem;
    color: #e2b714;
    margin-bottom: 1rem;
  }
  .option {
    background: #0f3460;
    border: 2px solid #333;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    cursor: pointer;
    transition: border-color 0.2s;
  }
  .option:hover {
    border-color: #e2b714;
  }
  .option input[type="radio"] {
    margin-right: 0.8rem;
    accent-color: #e2b714;
  }
  .option .option-label {
    font-weight: 600;
    color: #f0f0f0;
  }
  .option .option-consequence {
    font-size: 0.85rem;
    color: #999;
    margin-top: 0.3rem;
    margin-left: 1.8rem;
  }
  textarea {
    width: 100%;
    min-height: 100px;
    background: #0f3460;
    border: 2px solid #333;
    border-radius: 8px;
    color: #f0f0f0;
    padding: 0.8rem;
    font-family: inherit;
    font-size: 0.95rem;
    resize: vertical;
  }
  textarea:focus {
    outline: none;
    border-color: #e2b714;
  }
  input[type="date"] {
    background: #0f3460;
    border: 2px solid #333;
    border-radius: 8px;
    color: #f0f0f0;
    padding: 0.6rem 0.8rem;
    font-family: inherit;
    font-size: 0.95rem;
  }
  .submit-btn {
    display: block;
    width: 100%;
    padding: 1rem;
    margin-top: 1.5rem;
    background: #e2b714;
    color: #1a1a2e;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: background 0.2s;
  }
  .submit-btn:hover { background: #c9a012; }
  .footer {
    text-align: center;
    padding: 1rem;
    font-size: 0.75rem;
    color: #666;
  }
</style>
</head>
<body>
<div class="form-container">
  <div class="header">
    <h1>Decision Required</h1>
    <div class="subtitle">Floor Janitor — Blocker Escalation Stage 2</div>
  </div>
  <div class="body">
    <div class="metadata-grid">
      <div class="field">
        <label>Blocker ID</label>
        <div class="value">{{blocker_id}}</div>
      </div>
      <div class="field">
        <label>Escalation Stage</label>
        <div class="value">Stage 2 — Attention</div>
      </div>
      <div class="field">
        <label>Days Unresolved</label>
        <div class="value">{{days_unresolved}}</div>
      </div>
      <div class="field">
        <label>Sweeps Persisted</label>
        <div class="value">{{sweeps_persisted}}</div>
      </div>
    </div>

    <div class="field">
      <label>Source Tracker</label>
      <div class="value">{{source_tracker}}</div>
    </div>

    <div class="field">
      <label>Blocker Description</label>
      <div class="value urgent">{{blocker_description}}</div>
    </div>

    <div class="field">
      <label>First Detected</label>
      <div class="value">{{detected_date}}</div>
    </div>

    <div class="decision-section">
      <h2>Your Decision</h2>

      {{#each decision_options}}
      <div class="option">
        <label>
          <input type="radio" name="decision" value="{{id}}">
          <span class="option-label">{{label}}</span>
          <div class="option-consequence">{{consequence}}</div>
        </label>
      </div>
      {{/each}}

      <div class="field" style="margin-top: 1.5rem;">
        <label>Rationale (optional but recommended)</label>
        <textarea name="rationale" placeholder="Why this decision? Any constraints or context for future reference..."></textarea>
      </div>

      <div class="field">
        <label>Decision Date</label>
        <input type="date" name="decision_date">
      </div>

      <button class="submit-btn" onclick="generateYAML()">Record Decision</button>
    </div>
  </div>
  <div class="footer">
    Floor Janitor v0.3 — Save the generated YAML to JANITOR_WrkSps/forms/{{blocker_id}}_decision.yaml
  </div>
</div>

<script>
function generateYAML() {
  const selected = document.querySelector('input[name="decision"]:checked');
  const rationale = document.querySelector('textarea[name="rationale"]').value;
  const date = document.querySelector('input[name="decision_date"]').value;

  if (!selected) { alert('Select a decision option.'); return; }
  if (!date) { alert('Enter a decision date.'); return; }

  const yaml = `# Blocker Decision — {{blocker_id}}
blocker_id: "{{blocker_id}}"
decision_selected: "${selected.value}"
decision_rationale: "${rationale.replace(/"/g, '\\"')}"
decision_date: "${date}"
recorded_at: "${new Date().toISOString()}"
source_tracker: "{{source_tracker}}"
escalation_stage_at_decision: 2
`;

  const blob = new Blob([yaml], {type: 'text/yaml'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = '{{blocker_id}}_decision.yaml';
  a.click();
}
</script>
</div>
</body>
</html>
```

### Stage 3 Form (Critical — Red, Unignorable)

The Stage 3 form uses the same structure as Stage 2 with these visual overrides:

```css
/* Stage 3 overrides — replace Stage 2 styles */
.form-container {
  border: 4px solid #e94560;
  box-shadow: 0 0 30px rgba(233, 69, 96, 0.3);
  animation: pulse-border 2s ease-in-out infinite;
}
@keyframes pulse-border {
  0%, 100% { box-shadow: 0 0 20px rgba(233, 69, 96, 0.3); }
  50% { box-shadow: 0 0 40px rgba(233, 69, 96, 0.6); }
}
.header {
  background: #e94560;
  color: #fff;
}
.header h1 {
  font-size: 1.8rem;
}
/* Add full-width banner before .form-container */
.critical-banner {
  background: #e94560;
  color: #fff;
  text-align: center;
  padding: 1rem;
  font-size: 1.4rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  animation: flash-bg 1.5s ease-in-out infinite;
  margin-bottom: 1rem;
  border-radius: 8px;
}
@keyframes flash-bg {
  0%, 100% { background: #e94560; }
  50% { background: #c0392b; }
}
.submit-btn {
  background: #e94560;
}
.submit-btn:hover { background: #c0392b; }
.decision-section h2 { color: #e94560; }
.field .value { border-left-color: #e94560; }
```

Add before `.form-container`:
```html
<div class="critical-banner">
  CRITICAL BLOCKER — ACTION REQUIRED — {{days_unresolved}} DAYS UNRESOLVED
</div>
```

Header changes:
```html
<div class="header">
  <h1>Critical Blocker — Immediate Action Required</h1>
  <div class="subtitle">Floor Janitor — Blocker Escalation Stage 3 — This item has been unresolved for {{days_unresolved}} days</div>
</div>
```

---

## Part 4: Filled Blocker Form Example

Below is the Stage 2 form filled with real data from the Skill System Refactor blocker:

```
Blocker ID:           BLK-20260413-001
Escalation Stage:     Stage 2 — Attention
Days Unresolved:      7
Sweeps Persisted:     2
Source Tracker:        Skill System Refactor TASK-003
Blocker Description:  Malik review + Phase 2 authorization required for defect resolution queue (D1 mislabeled file, D2 missing sections, D3 stale references)
First Detected:       2026-04-13T20:01:42

Decision Options:
  [1] Approve Phase 2 — begin defect resolution queue (P0-P3)
      -> Lenny will execute Phase 2 in the next available session

  [2] Defer Phase 2 — not ready yet
      -> Blocker moves to ignored register; resurfaces at count 10

  [3] Approve with modified scope
      -> Malik specifies which defects to address first
```

---

## Part 5: Blocker Decision YAML Submission Artifact

```yaml
# Blocker Decision — BLK-20260413-001
# Generated by Floor Janitor HTML form
# Save to: JANITOR_WrkSps/forms/BLK-20260413-001_decision.yaml
blocker_id: "BLK-20260413-001"
decision_selected: "modify_scope"
decision_rationale: "Start with D3 (stale v2.2 references) only — these are low-risk and immediately verifiable. D1 and D2 require more investigation before acting."
decision_date: "2026-04-20"
recorded_at: "2026-04-20T16:30:00"
source_tracker: "Skill System Refactor TASK-003"
source_tracker_id: "33fd67199b3381aea666f1cf80c48239"
escalation_stage_at_decision: 2
modified_scope:
  include:
    - "D3 — stale v2.2 governing references in 4 brain skills"
  exclude:
    - "D1 — mislabeled Performance Ledger file (needs investigation)"
    - "D2 — missing sections in core skills (needs scope definition)"
  notes: "Run D3 first. Report back before touching D1 or D2."
```

---

*Floor Janitor Output Templates v0.3 -- Draft -- 2026-04-12*
