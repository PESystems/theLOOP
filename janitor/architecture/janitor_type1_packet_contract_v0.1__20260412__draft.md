---
tags:
- janitor
- packet
- contract
- v0_1_1
---
# Janitor Type 1 Packet Contract v0.1.1

Defines the implemented packet shapes for each Type 1 dispatch type. Every generated packet must conform to the shape defined here.

**Patch:** Phase 2A.1 — packet model normalization

## Packet Model — Normalized Field Definitions

Every packet uses these distinct taxonomy fields:

| Field | Purpose | Values |
|-------|---------|--------|
| `packet_class` | Packet generation tier | `type1` |
| `packet_type` | Specific packet kind | `skill_improvement_dispatch`, `container_promotion_dispatch`, `doctrine_update_dispatch`, `phase_unblock_action`, `overlap_remediation`, `new_idea_triage` |
| `target_surface` | Where the packet is executed | `dispatch`, `claude_code`, `cowork`, `lenny`, `manual` |
| `artifact_format` | File format of the packet artifact | `markdown`, `yaml`, `html` |
| `routing_mode` | How the packet enters the execution pipeline | `direct_execution`, `manual_decision`, `dispatch_ready`, `watch_only` |

---

## 1. skill_improvement_dispatch

**Purpose:** Route a skill that has crossed its miss threshold to the `skill-improvement` skill for an evidence-driven improvement pass.

**Trigger condition:** Skill `miss_count >= escalation_threshold` in `janitor_state.yaml` skill_snapshots.

**Required fields:**
- `packet_id` — format `PKT-YYYYMMDD-NNN`
- `packet_class` — literal `type1`
- `packet_type` — literal `skill_improvement_dispatch`
- `source_blocker_id` — blocker ID or threshold-crossing evidence reference
- `target_skill` — literal `skill-improvement`
- `target_surface` — `dispatch`
- `artifact_format` — `yaml`
- `routing_mode` — `dispatch_ready`
- `skill_name` — the skill needing improvement
- `skill_file_path` — Floor path to SKILL.md
- `current_version` — current skill version
- `miss_count` — current miss count
- `escalation_threshold` — threshold that was crossed
- `evidence_entries` — list of {date, event, trigger, note} objects from performance log

**What Janitor fills automatically:** All fields. Evidence entries are extracted verbatim from the performance log.

**What must remain unresolved:** Nothing — this packet is fully self-contained. The `skill-improvement` skill handles all judgment about what to change.

**Proof-of-completion:** Performance log contains an improvement pass entry for the skill AND the miss count resets in the next performance log window.

---

## 2. container_promotion_dispatch

**Purpose:** Route a Floor artifact that is promotion-ready to the `artifact-version-promotion` skill for the full promotion checklist.

**Trigger condition:** Janitor detects a promotion candidate via tracker analysis: phase COMPLETE, artifacts exist at expected paths, no unresolved blockers.

**Required fields:**
- `packet_id`
- `packet_class` — literal `type1`
- `packet_type` — literal `container_promotion_dispatch`
- `source_blocker_id` — promotion candidate ID or tracker reference
- `target_skill` — literal `artifact-version-promotion`
- `target_surface` — `dispatch`
- `artifact_format` — `yaml`
- `routing_mode` — `dispatch_ready`
- `artifact_path` — Floor path to the artifact to promote
- `current_version` — version being promoted from
- `promoted_version` — target version
- `target_location` — where the promoted artifact lands
- `promotion_reason` — why this is ready now
- `checklist_items` — list: versioned_filename, header_bump, manifest_update, notion_log, prior_retained

**What Janitor fills automatically:** artifact_path, current_version, promotion_reason, checklist_items (all false — they are the promotion TODO).

**What must remain unresolved:** `promoted_version` — Malik may override. The promotion skill handles the actual rename and metadata update.

**Proof-of-completion:** Promoted file exists at target_location. MANIFEST.md shows updated version entry.

---

## 3. doctrine_update_dispatch

**Purpose:** Route detected stale doctrine references to `workspace-path-migration` for a bounded sweep-and-fix.

**Trigger condition:** Janitor's doctrine drift register (`doctrine_drift_items` in state) contains items with `status: detected`.

**Required fields:**
- `packet_id`
- `packet_class` — literal `type1`
- `packet_type` — literal `doctrine_update_dispatch`
- `source_blocker_id` — drift ID from `DFT-YYYYMMDD-NNN`
- `target_skill` — literal `workspace-path-migration`
- `target_surface` — `claude_code`
- `artifact_format` — `markdown`
- `routing_mode` — `direct_execution`
- `stale_references` — list of {file_path, stale_reference, correct_reference} objects
- `scope` — which workspace(s) to sweep (e.g., `LENY_WrkSps`)
- `verification_command` — grep pattern that should return zero matches after fix

**What Janitor fills automatically:** All fields. stale_references come directly from state. verification_command is constructed from the stale_reference pattern.

**What must remain unresolved:** Nothing structurally — but the executing agent must verify each file exists before editing. File paths in state may be stale.

**Proof-of-completion:** Re-grep for the stale reference pattern returns zero matches across the specified scope.

---

## 4. phase_unblock_action

**Purpose:** Package a bounded execution task that unblocks a tracker phase. The blocker is actionable (not a Malik decision) and maps to concrete Floor work.

**Trigger condition:** Blocker typed `actionable` in the blocker register, AND the work can be scoped to a single session, AND no Malik decision is required.

**Required fields:**
- `packet_id`
- `packet_class` — literal `type1`
- `packet_type` — literal `phase_unblock_action`
- `source_blocker_id`
- `source_tracker` — tracker name
- `source_tracker_id` — Notion ID
- `target_surface` — `claude_code` | `cowork` | `dispatch`
- `artifact_format` — `markdown`
- `routing_mode` — `direct_execution` | `dispatch_ready`
- `task_description` — what the execution session must accomplish
- `scope_boundary` — what the session must NOT touch
- `inputs` — files/data the session needs to read
- `expected_outputs` — what files/artifacts the session must produce
- `verification` — how to confirm the blocker is resolved

**What Janitor fills automatically:** source fields, task_description (from blocker + tracker context), scope_boundary (from architectural constraints).

**What must remain unresolved:** Detailed implementation choices within the execution session. Janitor defines the box; the session fills it.

**Proof-of-completion:** Next Janitor sweep detects the tracker's active_blockers field no longer contains this blocker.

---

## 5. overlap_remediation

**Purpose:** Surface a detected overlap between two trackers or skills for Malik's review. This is a report-embedded packet, not a standalone dispatch.

**Trigger condition:** Overlap detection finds >60% keyword overlap between two non-sibling items.

**Required fields:**
- `packet_id`
- `packet_class` — literal `type1`
- `packet_type` — literal `overlap_remediation`
- `source_blocker_id` — `OVL-YYYYMMDD-NNN` (overlap items are not blockers; they use their own ID series)
- `target_surface` — `manual` (Malik reviews in report)
- `artifact_format` — `markdown`
- `routing_mode` — `manual_decision`
- `item_a` — name and type (tracker/skill)
- `item_b` — name and type
- `overlap_keywords` — shared keywords after stop-word exclusion
- `overlap_percentage` — computed overlap ratio
- `recommendation` — one of: `sibling_no_action`, `potential_duplicate`, `merge_candidate`, `scope_boundary_needed`

**What Janitor fills automatically:** All fields. Overlap computation is deterministic.

**What must remain unresolved:** Malik's verdict — Janitor recommends but does not act.

**Proof-of-completion:** Malik confirms the recommendation (pair added to known_siblings, or merge/boundary action taken), detected on next sweep.

---

## 6. new_idea_triage

**Purpose:** Present a triaged idea from the idea inbox for Malik's confirmation before any tracker or skill is created.

**Trigger condition:** New entry found in `state/idea_inbox.yaml` during sweep.

**Required fields:**
- `packet_id`
- `packet_class` — literal `type1`
- `packet_type` — literal `new_idea_triage`
- `source_blocker_id` — `IDEA-YYYYMMDD-NNN`
- `target_surface` — `manual` (Malik reviews in report)
- `artifact_format` — `markdown`
- `routing_mode` — `manual_decision`
- `idea_title` — from inbox
- `idea_description` — from inbox
- `overlap_analysis` — list of overlapping trackers/skills with percentages
- `triage_verdict` — one of: `greenlight_tracker`, `merge_into_existing`, `new_skill`, `one_off_task`, `park`
- `recommended_target` — if merge, which tracker/skill; if greenlight, proposed tracker stub
- `recommended_action` — plain-language next step

**What Janitor fills automatically:** All fields. Overlap analysis runs against current tracker and skill registries.

**What must remain unresolved:** Malik's confirmation of the verdict. Janitor does not create trackers or skills.

**Proof-of-completion:** Idea moved from inbox to archive with a resolution note, OR a new tracker/skill is detected on next sweep.

---

## Common Packet Header

Every packet file starts with this header block:

```
# Janitor Type 1 Packet — [packet_type]
# Packet ID: [packet_id]
# Packet Class: type1
# Generated: [timestamp]
# Source: [source_blocker_id] via [source_tracker]
# Target Surface: [target_surface]
# Artifact Format: [artifact_format]
# Routing Mode: [routing_mode]
# Status: generated — requires human review before execution
```

---

*Janitor Type 1 Packet Contract v0.1.1 -- 2026-04-12*
