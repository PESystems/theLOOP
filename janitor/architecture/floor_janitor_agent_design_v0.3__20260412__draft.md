---
tags:
- loop
- janitor
- architecture
- design
- floor
- v0_3
---
# Floor Janitor Agent Design v0.3
**Version:** v0.3 — draft
**Date:** 2026-04-12
**Status:** DESIGN — no implementation
**Author:** Lenny (Floor execution, Claude Code)
**Working directory:** `C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps\`

---

## Pre-Read Summary

### A. Skill Inventory Table

| # | Skill | Version | Scope | Trigger | Purpose | Output Type | Status | Janitor Relationship |
|---|-------|---------|-------|---------|---------|-------------|--------|---------------------|
| 1 | loop-node-hygiene | v1.0 | brain | Scheduled Sun 8:05 AM / "run hygiene" | SYSTEM zone audit — classify and move stale pages | Report + Notion moves | Active, automated | Peer — Janitor reads results, does not duplicate |
| 2 | loop-node-query | v1.1 | brain | "check the Node", "look up [X]" | General-purpose Notion lookup | Formatted query results | Active | Consumed — Janitor uses for tracker reads |
| 3 | loop-tracker-create | v1.0 | brain | "create tracker", "build tracker" | Orchestrator for creating phase trackers | Notion page + receipt | Active (draft) | Independent — Janitor does not create trackers |
| 4 | loop-session-open | v1.2 | brain | Session start (Container-only) | Session open protocol | Context load | Active (Container-only) | Independent — disabled on Floor |
| 5 | loop-session-close | v1.2 | brain | Session end (Container-only) | Session close protocol | Archive + Sketchpad | Active (Container-only) | Independent — disabled on Floor |
| 6 | Task Classification | v1.0 | brain | Every incoming task | Tier 0/1/2 routing | Tier assignment | Active | Independent |
| 7 | Compaction | v1.0 | brain | Context limits, session close | Context reduction | Compacted artifact | Active | Independent |
| 8 | Node Write Back | v1.0 | brain | Node write requests | Clean Notion writes | Notion page updates | Active | Independent |
| 9 | Execution Prompt Design | v1.0 | brain | T2 prompt creation | Designing Floor-facing prompts | Execution packet | Active | Independent |
| 10 | Node Archive Pass | v1.1 | brain | On-demand page routing | 4-layer page routing (any zone) | Routing decisions | Active | Peer — different scope from hygiene |
| 11 | Notion Task Audit | v1.0 | brain | "audit tasks", stale task sweep | Tasks DB hygiene | Sweep report | Active | Peer — Janitor may dispatch |
| 12 | Artifact Version Promotion | v1.1 | global | Promotion requests | Full promotion checklist | Promoted files + receipt | Active | Orchestrated — Janitor detects promotion candidates, dispatches |
| 13 | Container Knowledge Sync | v1.2 | brain | Container sync requests | Container file backup + sync | Sync report | Active | Peer — Janitor detects stale Container state |
| 14 | loop-floor-query | v1.0 | floor | "find [X] on the Floor" | Floor workspace lookup | Search results | Active | Consumed — Janitor uses for Floor reads |
| 15 | loop-patch-sync | — | floor | Session close, "add to patch list" | Write/update patches to Notion | Notion patch list updates | Active | Peer — Janitor reads patch list state |
| 16 | loop-patch-report | v1.0 | floor | Scheduled Fri AM / "patch report" | Weekly patch status + auto-close | Patch report | Active, automated | Peer — Janitor consumes report output |
| 17 | loop-write-through | — | floor | "run write-through", "import clients" | Client/project Notion import | Notion DB writes + receipt | Active | Independent |
| 18 | vendor-docs | v0.2 | floor | "get manuals for [X]" | Vendor doc collection | Downloaded PDFs + log | Active, automated (Sat) | Independent |
| 19 | gdrive-write | — | floor | "upload to drive" | Google Drive write via MCP | Drive file + receipt | Active | Independent |
| 20 | file-query | — | floor | Token-limit errors, "read large file" | Large-file extraction strategies | Extracted content | Active | Independent |
| 21 | bulk-edit-safety | — | floor | Scripts writing >10 files | Seven-step gate for bulk edits | Verification report | Active | Independent |
| 22 | yaml-frontmatter-safe | — | floor | YAML frontmatter parsing | Safe YAML read/write pattern | Code pattern | Active | Independent |
| 23 | canonical-bug-class-correction | v1.0 | floor | Named bug class with CONFIRMED backtest | Bounded factual correction pipeline | Receipted corrections | Active | Independent |
| 24 | Cold Start Context Load | v2.0 | global | Every session start (Floor) | Floor session-open replacement | Context load report | Active | Independent — Janitor has its own startup |
| 25 | Document Review Response | v1.0 | global | Structured review feedback | Triage-before-edit pattern | Review triage | Active | Independent |
| 26 | Workspace Path Migration | v1.0 | global | Folder renames/moves | Sweep stale path references | Migration report | Active | Orchestrated — Janitor detects stale paths |
| 27 | Performance Log Write | v2.1→v3.0 | global | Every skill fire (Floor) | Hyper-aggressive performance logging | Log entries + Notion mirror | Active (merged into Ledger v3.0) | Read — Janitor reads log, does not write |
| 28 | Prebuild Overlap Scan | v1.0 | global | Any build/create/scaffold intent | Pre-build recon for duplicates | Verdict (5 types) | Active | Peer — Janitor's overlap detection is broader |
| 29 | Skill Improvement | v1.1 | global | Threshold crossing in perf log | Evidence-driven skill improvement | Improved skill file | Active | Orchestrated — Janitor coordinates, does not dilute |
| 30 | Skill Performance Ledger | v1.4 (Container) / v3.0 (Floor) | global | Every skill fire | Performance tracking + escalation | Ledger entries | Active (split) | Read — Janitor reads thresholds, never writes |
| 31 | wiki-build | v1.3 | global | Ingest queue items, "run build" | Wiki build pass | Built wiki pages + log | Active, automated (Sun) | Independent |
| 32 | wiki-queue-feeder | — | global | Scheduled Sun 07:00 / gap detection | Wiki gap detection + queue feeding | Queue items | Active, automated | Independent |
| 33 | Node Index | v1.1 | global | Node query lookups | Queryable Node reference map | ID lookups | Active | Consumed — Janitor references for tracker IDs |
| 34 | Floor Index | v1.0 | global | Floor query lookups | Queryable Floor reference map | Path lookups | Active | Consumed — Janitor references for Floor paths |

### B. Tracker State Table

All 7 trackers read **LIVE** via Notion MCP on 2026-04-12.

| # | Tracker | Phase | Status | Last Completed Step | Active Blockers | Next Step | Dependency Links | Read Mode |
|---|---------|-------|--------|--------------------:|----------------|-----------|-----------------|-----------|
| 1 | LOOP Ingestion Process | Pilot Complete / Email Next | ACTIVE | Pilot 003A accepted, v0.3 schema locked | Security abstraction layer design needed | Design secure email-ingestion abstraction layer | Feeds into YAML Write-Through (Phase G) | LIVE |
| 2 | YAML → Notion Write-Through | Phase E complete / Phase F ready | ACTIVE | 3 DB IDs registered, 9 placeholders replaced, vacuous-pass bug fixed | Auth storage decision for Phase F | Phase F — Notion API client, auth, idempotency | Sibling to Ingestion; parallel to Dynamic Extraction | LIVE |
| 3 | Dynamic Extraction Integration | Post-Reviewer Build | GATE B REVIEW SURFACE COMPLETE | Gate B reviewer, CLI, templates, runbook built | None — ready for first manual review cycle | Execute first manual review on GB-20260411-001 | Under YASK Pipeline Family; sibling to Autoresearch | LIVE |
| 4 | YASK Autoresearch Harness | Foundation + all stages pending | ACTIVE | Scaling checkpoint, contract eval v0.3 active, EN3/MULTIPUMP corrections done | Source files not accessible in recent sessions | Load source files, run spine design | Parent of Dynamic Extraction | LIVE |
| 5 | LOOP v3.0 Doctrine Refresh | Phase 5 Complete / Phase 6 Partial | PROMOTED 2026-04-11 | v3.0 promoted under Option E | Manual FUSE upload (Malik action) — notes say "COMPLETE 2026-04-12" | Delete 4 HISTORICAL files from Container, close F1-F4 | None | LIVE |
| 6 | Skill System Refactor (TASK-003) | Post-Inventory / Phase 2 Pending | PHASE 1 COMPLETE | Skill inventory + redundancy/conflict analysis | Malik review + Phase 2 authorization | Phase 2 — defect resolution queue (P0-P3) | None | LIVE |
| 7 | YAML Family Naming & Cohesion | Vocabulary design | PROPOSAL | Naming audit, three-slot pattern drafted | Malik decides path (1/2/3) | Lock convention or defer | Pairs with prebuild-overlap-scan v1.1 | LIVE |

### C. Known Uncertainty List

1. **Missing files at expected paths:**
   - `LOOP_Floor_Index_v1.0.md` — NOT at `architecture/` as the execution packet specified; found at `skills/global/`. The packet's pre-read path A.1 is stale.
   - `LOOP_Node_Index_v1.0.md` — NOT at `architecture/`; found at `skills/global/` (v1.0 and v1.1). Same stale path.

2. **Stale references in Floor state:**
   - Floor Index v1.0 references `LOOP_Architecture_v2_4.md` and `LOOP_Claude_Operating_Doctrine_Addendum_v2_4_1.md` as active Architecture Files — both are now HISTORICAL per v3.0 promotion (2026-04-11). **Floor Index needs v1.1 bump** (also logged as F1 in Doctrine Refresh tracker).
   - D3 defect (Skill Refactor): 4 core brain skills (Task Classification, Compaction, Node Write-Back, Execution Prompt Design) cite stale v2.2 governing reference. Live = v3.0.

3. **Unresolved doctrine conflicts:**
   - Performance logging three-way split (D1 in Skill Refactor): `LOOP_Skill_Performance_Ledger_v1_3.md` is mislabeled — body contains Session Open, not Performance Ledger. Partially resolved via v3.0 merge (Ledger absorbed Log Write), but D1 file-level defect is still live.
   - Container vs User Skills registry — no governing rule exists (P2 item in Skill Refactor Phase 2).

4. **State ambiguities constraining design:**
   - Power Automate / Relay layer: no files found on Floor, no evidence of current implementation. Wiki page "The Relay" exists but no executable infrastructure. **All hook-driven triggers must be marked FUTURE MERGE — Power Automate.**
   - v3.0 FUSE upload status is ambiguous: tracker System State says "STOPPED BEFORE MANUAL FUSE UPLOAD" but Notes field says "FUSE drag-drop COMPLETE (2026-04-12)". Treating as completed but flagging as uncertain.
   - Auto-Research Pilot status: MEMORY.md says "Gate 2 HALTED" but YASK Autoresearch Harness tracker doesn't surface this clearly.

5. **Inaccessible or unexamined:**
   - `.tmp_patch/SKILL.md` — orphan skill directory, content not examined in depth (appears to be a temporary/transient skill).
   - Notion Inbox/Sketchpad content — not read (would inform current cross-session blocker state).
   - No `execution_guardrails.md` or `dispatch_operating_model_v0.2.md` read — referenced in authority hierarchy but not in the pre-read list. Design proceeds without them.

---

## Design Section 1: Agent Identity and Instance Model

### Decision

The Floor Janitor is a **named operational mode of Lenny**, not a separate agent identity. It differs from standard Lenny at startup via a **prompt delta + context package** hybrid approach:

1. **Prompt delta:** A Janitor-mode activation prompt (`JANITOR_WrkSps/architecture/janitor_sweep_prompt_v0.3.md`) that replaces Lenny's standard cold-start context load. This prompt:
   - Sets the Janitor responsibility scope
   - Loads the Janitor state schema
   - Defines the sweep stage sequence
   - Specifies output format requirements

2. **Context package:** Before any sweep, Janitor reads:
   - `JANITOR_WrkSps/state/janitor_state.yaml` (persistent state from last run)
   - `JANITOR_WrkSps/reports/` (last Type 2 report for diff detection)
   - `LENY_WrkSps/architecture/MANIFEST.md` (authority chain)
   - `LENY_WrkSps/logs/SKILL_PERFORMANCE_LOG.md` (skill health)

3. **Runtime profile:** Janitor reads fresh every run:
   - All 7+ Notion trackers (via MCP)
   - Notion Open Patch List
   - Skill files that changed since last run (detected via file modification timestamps in state)

4. **Stable context (mounted, not re-read unless changed):**
   - Architecture v3.0 doctrine
   - Node Index v1.1 (for tracker IDs)
   - Floor Index v1.0 (for path resolution)

### Session Close Difference

Janitor session close differs from standard Lenny:
- **Does NOT** write to the Sketchpad/Inbox
- **Does NOT** create a `sessions/YYYY-MM-DD_*/` archive folder
- **DOES** update `JANITOR_WrkSps/state/janitor_state.yaml` with current snapshot
- **DOES** write a Type 2 report to `JANITOR_WrkSps/reports/`
- **DOES** append a run log entry to `JANITOR_WrkSps/logs/janitor_run_log.md`

### Artifact Naming

All Janitor artifacts use one of these patterns:
- Files in `JANITOR_WrkSps/` — location is sufficient disambiguation
- Reports: `JANITOR_report_YYYYMMDD.md`
- State: `janitor_state.yaml` (single file, overwritten each run)
- Logs: `janitor_run_log.md` (append-only)
- Forms: `JANITOR_blocker_form_YYYYMMDD_NNN.html`
- Execution packets: `JANITOR_dispatch_YYYYMMDD_NNN.yaml`

No `LENY_` prefix collision is possible.

### Container Decision

**Decision:** Janitor does NOT run inside LENY's Container or require its own Container.

**Rationale:** Janitor is a Floor-only execution mode. It needs to read across LENY_WrkSps, YASK_WrkSps, and NRGY_WrkSps — none of which are accessible from inside a Container. The Janitor prompt is loaded at Floor invocation time (Claude Code or Cowork), not baked into a Container's knowledge files. If Container-based Janitor operation is ever needed, a `janitor_brain_skill.md` can be uploaded as a Container knowledge file later — but Phase 1 does not require this.

**Failure mode:** If Janitor is accidentally given a Container-first design, it would be unable to read live tracker state via Notion MCP (Container sessions cannot call MCP tools). This would make the entire cross-tracker synthesis responsibility non-functional.

### Rationale

- Prompt delta (not a separate system prompt) keeps Janitor lightweight and avoids the overhead of a full agent onboarding
- The context package approach aligns with LOOP's JIT retrieval principle — Janitor loads only what it needs
- Separate workspace root (`JANITOR_WrkSps`) prevents state pollution between Janitor and standard Lenny operations
- No Container needed because all Janitor work is T2 Floor execution

### Evidence Used

- LOOP Architecture v3.0: Tier model (Janitor = T2), multi-agent reality (only LENY and YASK are active agents), Layer truth (Floor = execution truth)
- MANIFEST.md: Authority hierarchy — Janitor operates under architecture v3.0 and system prompt v3.0
- Skill Performance Log: Shows Floor-only execution pattern for all operational skills

### Open Questions

1. Should Janitor state eventually be mirrored to a Notion page for visibility when Malik is not at the Floor? (Defer to Phase 2.)
2. Should Janitor produce a Sketchpad/Inbox summary for Container sessions that follow a Janitor run? (Defer — depends on whether Container sessions need Janitor context.)

---

## Design Section 2: Responsibility Model

### 2a. Cross-Tracker State Synthesis

**Trigger:** Every scheduled sweep; also on any hook-driven wake.

**Inputs:**
- All tracker pages via Notion MCP (7 currently; list maintained in `janitor_state.yaml`)
- Node Index v1.1 (for tracker IDs — avoids notion-search calls)

**Process:**
1. Fetch each tracker's System State block (Status, Phase, Last Completed Step, Next Step, Notes)
2. Compare against previous snapshot in `janitor_state.yaml`
3. Detect changes: status transitions, new completed steps, new blockers, new open items
4. Assign priority based on change significance:
   - P0: Status changed to BLOCKED or a new G-level blocker appeared
   - P1: Phase advanced or a phase was completed
   - P2: Open items changed (added/removed)
   - P3: No change (quiet tracker)

**Output class:** Type 2 (Malik-facing report) — system health summary section.

**What Janitor owns:** The cross-tracker snapshot comparison and the health summary. Janitor does NOT own individual tracker updates — those belong to the skill or session that advances the tracker.

**What Janitor routes elsewhere:** If a tracker's status is BLOCKED and the blocker maps to a known skill capability (e.g., "needs Container upload" → `container-knowledge-sync`), Janitor produces a Type 1 dispatch packet.

**Failure mode:** Notion MCP unavailable. Janitor falls back to the last snapshot in state, marks all trackers as `read_mode: proxied_from_state`, and flags the MCP outage in the report. Design does not fail — it degrades to stale data with explicit labeling.

### 2b. Promotion Awareness and Notification

**Trigger:** Cross-tracker synthesis detects a tracker whose phase is marked COMPLETE or whose artifacts are promotion-ready.

**Promotion-candidate criteria (all must be true):**
1. Tracker phase status = COMPLETE for the current phase
2. Associated Floor artifacts exist at the expected paths (verified via Glob)
3. No BLOCKED items remain in the tracker's Open Items section
4. No unresolved G-level decisions pending Malik

**State handling:**
- `pending_promotion`: Criteria met, not yet surfaced to Malik
- `notified`: Surfaced in a Type 2 report, awaiting Malik decision
- `promotion_dispatched`: Malik approved, Type 1 packet sent to `artifact-version-promotion`
- `completed`: Promotion confirmed (next sweep detects version bump)

**Malik-facing presentation:** Dedicated "Upcoming Promotions" section in Type 2 report with:
- What is ready
- What artifacts exist
- What Malik must approve
- One-click dispatch prompt (in the report, not executed automatically)

**Promotion packet structure:** See Output Model (Section 5, Type 1).

**What Janitor owns:** Detection and notification only. **Janitor does NOT promote.** Promotion authority remains with Malik, executed via `artifact-version-promotion` skill.

**Failure mode:** False positive — Janitor flags something as promotion-ready when it isn't. Mitigation: Janitor verifies artifact existence on Floor before flagging. If Floor artifacts are missing, it flags as "promotion candidate — artifacts not verified" instead.

### 2c. G-Level Blocker Detection and Escalation

**Blocker-identification markers (grepped from tracker content):**
- Status contains "BLOCKED"
- Open Items contain "Malik action", "Malik decision", "Malik review"
- Notes contain "waiting on", "pending approval", "gated on Malik"
- Any item tagged with `human_gate_approval` or `G5` or `G-level`

**Clearance form schema:** See Output Model (Section 5, HTML blocker form).

**Escalation stages:**
- **Stage 1 (Informational):** Blocker appears in Type 2 report. No form generated. Blocker is new or < 7 days old.
- **Stage 2 (Attention):** Blocker has persisted across 2+ sweeps (> 7 days). HTML form generated and placed in `JANITOR_WrkSps/forms/`. Form is yellow-highlighted.
- **Stage 3 (Critical):** Blocker has persisted across 4+ sweeps (> 21 days). Form regenerated with red/high-contrast styling. Placed at top of Type 2 report with **UNIGNORABLE** visual treatment.

**Ignored-blocker logic:** If Malik explicitly marks a blocker as "deferred" or "acknowledged-not-acting" in a Janitor form response, the blocker is moved to an `ignored_blockers` register in state with a counter. The counter increments each sweep. At count 10, the blocker resurfaces as Stage 2 regardless of deferral. This prevents permanent burial.

**How cleared blockers are recorded:** When a subsequent sweep detects the blocker is gone (tracker status changed, open item resolved), Janitor:
1. Moves the blocker from `active_blockers` to `cleared_blockers` in state with clearance date
2. Notes it in the Type 2 report "Blockers Cleared This Period" section
3. Removes any outstanding HTML form from `forms/` (or marks it as resolved)

**Failure mode:** Marker grep misses a novel blocker phrasing. Mitigation: Janitor also checks for status = BLOCKED (structural, not text-dependent). Open question: should Janitor also scan for "requires" or "depends on Malik"?

### 2d. Doctrine Drift Detection

**Comparison surfaces:**
- Architecture v3.0 authority hierarchy (9 entries) vs. actual file versions on Floor
- MANIFEST.md file table vs. actual files in `architecture/`
- Skill files referencing superseded doctrine versions (v2.2, v2.4, v2.4.1)
- Container backups (`container/current/`) vs. latest Floor versions

**Stale vs. intentionally superseded logic:**
- A file marked HISTORICAL in MANIFEST is intentionally superseded — not drift
- A file referencing v2.4 doctrine when v3.0 is live IS drift (unless the file itself is HISTORICAL)
- A Container backup that doesn't match the Floor current version IS drift — Container may be behind

**Doctrine update packet structure:** See Output Model (Section 5, Type 1 — doctrine update dispatch).

**What Janitor owns:** Detection and reporting. Janitor does NOT edit doctrine files. It produces a drift report and optionally a dispatch packet for `workspace-path-migration` to sweep stale references.

**Evidence used:** D3 defect in Skill Refactor — 4 skills cite v2.2. Floor Index v1.0 references HISTORICAL files as active (F1 follow-up).

**Failure mode:** Janitor flags HISTORICAL files as drift. Mitigation: check MANIFEST status column before flagging.

**Open question:** Should Janitor scan YASK_WrkSps for doctrine references too, or only LENY_WrkSps? (Start with LENY only — YASK has its own Container.)

### 2e. Skill Lifecycle Coordination

**What Janitor reads from the performance ledger:**
- `SKILL_PERFORMANCE_LOG.md` entries since last Janitor run
- Hit/miss/partial counts per skill
- Escalation threshold status: `min(2 + improvement_count, 5)` per skill
- Improvement pass history (which skills have been improved, how many times)

**What threshold crossings cause:**
- Janitor produces a Type 1 dispatch packet targeting `skill-improvement`
- The packet contains: skill name, current miss count, threshold, evidence entries from the log

**Interface contract with `skill-improvement`:**
- Janitor sends: dispatch packet with evidence
- Janitor expects back: nothing directly — Janitor detects the outcome on next sweep by reading the updated performance log and checking for a new version of the skill file
- Completion is known when: performance log shows an improvement pass entry for the skill AND the miss count resets

**Duplicate-work avoidance:**
- Janitor checks `janitor_state.yaml` for `pending_skill_dispatches` before sending a new one
- If a dispatch was sent in the last sweep and no improvement pass has occurred yet, Janitor does NOT re-dispatch — it reports "dispatch pending, awaiting skill-improvement execution"

**New-skill gap handling:** If Janitor detects a recurring failure pattern that no existing skill covers (e.g., a task type that consistently fails), it logs the gap in the Type 2 report under "Skill Gaps Detected" but does NOT create a new skill. New skill creation requires Malik authorization.

**Hard constraint:** `skill-performance-ledger` and `skill-improvement` preserve their current aggressive behavior exactly. Janitor coordinates around them. Janitor never writes to the performance log. Janitor never executes an improvement pass. Janitor only reads and dispatches.

### 2f. Overlap Detection

**Trigger conditions:**
- Janitor sweep detects two trackers with similar domain keywords (using the YAML Family naming analysis as prior art)
- Janitor detects two skills with overlapping trigger descriptions
- Janitor detects a new skill or tracker that shares >60% of domain keywords with an existing one

**Structural overlap detection method:**
1. Extract domain keywords from each tracker's title, System State notes, and Cross-References section
2. Extract trigger phrases from each skill's YAML frontmatter `description` field
3. Compute keyword overlap ratio per pair
4. Flag pairs where overlap > 60% AND the pair is not already registered as a known sibling relationship in state

**Overlap output format:** Table in Type 2 report:
| Item A | Item B | Overlap Keywords | Overlap % | Known Sibling? | Recommendation |

**Janitor recommendation options:**
- `sibling — no action` (already linked as siblings in tracker cross-references)
- `potential duplicate — investigate` (high overlap, no sibling link)
- `merge candidate` (one subsumes the other)
- `scope boundary needed` (overlapping but distinct — add boundary notes)

**Failure mode:** False positives from generic keywords ("LOOP", "Notion", "skill"). Mitigation: maintain a stop-word list in state (`generic_keywords`) that are excluded from overlap scoring.

### 2g. Feature and Skill Registry Maintenance

**Registry format:** A consolidated table maintained as part of the Type 2 report AND as a standalone file at `JANITOR_WrkSps/reports/skill_registry_current.md`.

Columns: `skill | version | scope | status | last_fired | miss_count | improvement_count | janitor_classification`

**Update method:** Rebuilt from source data each sweep:
- Skill files scanned via Glob for version/status
- Performance log scanned for last fire date and miss/hit counts
- Janitor classification assigned per Section 6 integration map

**Surfacing method:** Included in every Type 2 report. Standalone file updated in-place each sweep (not append-only).

**Decision:** The registry lives both as a section in Type 2 reports AND as a standalone file. Rationale: the standalone file is queryable by `loop-floor-query`; the report section gives Malik the full picture without needing to open a separate file.

### 2h. Cross-Tracker Convergence Flagging

**Convergence signals:**
- Two trackers reference each other in their Cross-References sections
- Two trackers share a Phase that produces/consumes the same artifact format
- A tracker's "Next Step" explicitly mentions bridging to another tracker (e.g., YAML Write-Through Phase G mentions Ingestion Tracker)
- Two trackers' completion criteria overlap (completing one would partially complete the other)

**False-positive avoidance:**
- Generic references ("see also") do not count as convergence signals
- Only active (non-COMPLETE, non-PROPOSAL) trackers are candidates
- Known family relationships (YASK Pipeline Family) are reported as "family convergence" not flagged as novel

**Report format:** "Convergence Opportunities" section in Type 2 report:
| Tracker A | Tracker B | Signal | Evidence | Recommended Action |

**Evidence used:** YAML Write-Through tracker explicitly defines Phase G as the bridge to the Ingestion tracker. Dynamic Extraction tracker and YASK Autoresearch tracker share the YASK Pipeline Family.

### 2i. New Idea Intake and Triage

**Intake source:**
- A designated file at `JANITOR_WrkSps/state/idea_inbox.yaml`
- Malik deposits ideas by adding entries to this file (or by telling Lenny to add them during any session)
- Janitor processes the inbox on each sweep

**Triage criteria:**
1. Does this overlap with an existing tracker? → run overlap detection
2. Does this overlap with an existing skill? → run overlap detection
3. Is this a tracker-level initiative (multi-phase, phased work)? → recommend new tracker
4. Is this a skill-level addition (reusable capability)? → recommend new skill or skill extension
5. Is this a one-off task? → route to Tasks DB, not a tracker

**Output for each verdict:**
- **Greenlight new tracker:** Produce a stub entry with proposed title, domain, lane, artifact type. Flag for `loop-tracker-create` dispatch. Do NOT create the tracker.
- **Merge into existing:** Identify the target tracker. Produce a merge recommendation with the specific section/open-item where the idea fits.
- **Park in archive:** Move the idea from `idea_inbox.yaml` to `idea_archive.yaml` with a dated note explaining why it was parked (duplicate, out of scope, premature).

**Failure mode:** Idea is too vague to triage. Janitor flags it as "NEEDS CLARIFICATION" in the Type 2 report and leaves it in the inbox.

### 2j. Additional Responsibilities Discovered from Real State

**FUSE Upload Tracking**

**Evidence:** The v3.0 Doctrine Refresh tracker has a Phase 6 step that is BLOCKED on a manual FUSE drag-drop upload. The tracker notes say "FUSE drag-drop COMPLETE (2026-04-12)" but the formal Phase 6 checkbox is unchecked. This is a manual-action-required pattern that recurs: Container uploads, file deletions via claude.ai UI, and other operations that Lenny cannot perform.

**What Janitor should do:** Track pending manual actions as a distinct register in state (`pending_manual_actions`). Each entry has: action description, source tracker, date detected, date completed (null until confirmed). The Type 2 report includes a "Pending Manual Actions" section. This prevents manual steps from being forgotten across sessions.

**Scheduled Task Health Monitoring**

**Evidence:** The performance log shows 6 scheduled tasks (`loop-node-hygiene-weekly`, `wiki-queue-feeder-weekly`, `wiki-build-weekly`, `vendor-docs-weekly`, `loop-patch-report`, scheduled for various days/times). Several of these have entries in the log; some have not fired recently.

**What Janitor should do:** On each sweep, check whether each scheduled task has produced a log entry within its expected cadence. If a task has missed its window by >48 hours, flag it in the Type 2 report under "Scheduled Task Health." Do NOT reschedule or re-trigger — just report.

---

## Design Section 3: State Model

### Directory Structure

```
C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps\
  architecture\       # Design docs, Janitor MANIFEST materials
  state\              # Persistent state (janitor_state.yaml, idea_inbox.yaml, idea_archive.yaml)
  logs\               # Run receipts, run log (append-only)
  reports\            # Type 2 reports, skill registry
  forms\              # Generated HTML blocker forms
```

### Persistent State Schema

See Deliverable 3 (`floor_janitor_state_schema_v0.3__20260412__draft.yaml`) for the full schema with types, enums, defaults, and a filled first-run example.

**Key design decisions:**

**Decision:** State is a single YAML file (`janitor_state.yaml`), overwritten in full each run.

**Rationale:** YAML is human-readable, diffable, and aligns with LOOP's existing YAML discipline. A single file avoids the complexity of multi-file state management. Full overwrite (not partial update) ensures state is always consistent — no partial-write corruption.

**Failure mode:** File corruption on write (e.g., crash mid-write). Mitigation: Janitor writes to `janitor_state.yaml.tmp` first, then renames. If `.tmp` exists at startup, the previous write may have failed — Janitor reads the older `janitor_state.yaml` and logs the recovery.

**What gets appended to logs vs overwritten in state:**
- `janitor_state.yaml` — overwritten each run (current snapshot)
- `janitor_run_log.md` — append-only (historical record of all runs)
- `JANITOR_report_YYYYMMDD.md` — new file per run (never overwritten)
- `skill_registry_current.md` — overwritten each run (current snapshot)

**What counts as canonical Janitor state vs report artifact:**
- **Canonical state:** `janitor_state.yaml` — the operational file Janitor reads to orient on next run
- **Report artifact:** everything in `reports/` and `forms/` — for Malik consumption, not Janitor's operational state

### First-Run Initialization

On first run, Janitor:
1. Checks for `state/janitor_state.yaml` — if missing, creates it with the default schema (all fields at defaults, no tracker snapshots, no blocker history)
2. Runs a full sweep to populate the initial snapshot
3. Produces the first Type 2 report
4. Writes the first run log entry

### Recovery on Missing or Malformed State

- **Missing state file:** Treated as first run. Full sweep, fresh state.
- **Malformed YAML:** Janitor attempts `yaml.safe_load()`. If it fails, renames the malformed file to `janitor_state.yaml.malformed.YYYYMMDD` and starts fresh. Logs the recovery in the run log.
- **Missing individual fields:** Janitor fills missing fields with defaults from the schema. This handles schema evolution across versions without requiring migration scripts.

---

## Design Section 4: Wake Cycle and Trigger Model

### A. Scheduled Sweep — Implementable Now

**Recommended cadence:** Weekly, Sunday evening (20:00 ET), to run after the automated Sunday skills (`loop-node-hygiene` at 08:05, `wiki-queue-feeder` at 07:00, `wiki-build` at 08:00) have completed and before the new work week begins.

**Alternative:** Bi-weekly if the system is quiet. Cadence is adjustable via a `sweep_cadence_days` field in state.

**Run stages in order:**
1. **Mount:** Load Janitor state, read last report timestamp
2. **Read:** Fetch all tracker System State blocks via Notion MCP
3. **Diff:** Compare against previous snapshot in state
4. **Scan:** Read `SKILL_PERFORMANCE_LOG.md` for new entries since last run
5. **Check:** Verify scheduled task health (last fire dates)
6. **Detect:** Run blocker detection, promotion candidate detection, overlap detection, convergence detection, doctrine drift detection
7. **Triage:** Process idea inbox if non-empty
8. **Report:** Generate Type 2 report
9. **Dispatch:** Generate any Type 1 packets (skill improvement, promotion, etc.)
10. **State:** Write updated state
11. **Log:** Append run log entry

**Minimum outputs even on a quiet run:**
- Updated `janitor_state.yaml` (even if unchanged — timestamp updates)
- Type 2 report (even if empty — "No changes detected" is a valid report)
- Run log entry

**What gets skipped when no state changes are found:**
- Type 1 dispatch packets (nothing to dispatch)
- HTML blocker forms (no new/escalated blockers)
- Skill registry rebuild (only if no performance log entries since last run)
- Overlap detection (only runs if new skills or trackers appeared)

### B. Hook-Driven Triggers — Design Now, Implement Later

Each hook is marked: **FUTURE MERGE — Power Automate**

#### Hook 1: New file in watched Floor path
- **Event:** New file appears in `LENY_WrkSps/container/pending-upload/`, `LENY_WrkSps/skills/`, or `LENY_WrkSps/architecture/`
- **Priority:** P2 (informational)
- **Behavior:** Queues — does not interrupt. Logged in state as `pending_file_events`. Processed on next sweep.
- **Difference from scheduled wake:** Only the relevant detection stage runs (promotion awareness for pending-upload, skill lifecycle for skills/, doctrine drift for architecture/).
- **Artifact:** Updated state + optional inline note in next Type 2 report

**FUTURE MERGE — Power Automate**

#### Hook 2: Skill-performance-ledger escalation threshold crossed
- **Event:** A skill's miss count crosses its threshold in the performance log
- **Priority:** P1 (action needed)
- **Behavior:** Interrupts — triggers an immediate mini-sweep focused on skill lifecycle coordination. Produces a Type 1 dispatch packet for `skill-improvement`.
- **Difference from scheduled wake:** Only stages 4 (Scan) and 9 (Dispatch) run.
- **Artifact:** Type 1 skill improvement dispatch

**FUTURE MERGE — Power Automate**

#### Hook 3: Phase tracker status changed in Notion
- **Event:** A tracker's System State block changes (detected via Notion webhook or polling)
- **Priority:** P1 (important context)
- **Behavior:** Queues. Logged in state. Processed on next sweep or triggers a mini-sweep if the change is to BLOCKED or COMPLETE.
- **Difference from scheduled wake:** Only stages 2-3 (Read, Diff) and 6 (Detect) run for the affected tracker.
- **Artifact:** Updated state + Type 2 delta report section

**FUTURE MERGE — Power Automate**

#### Hook 4: New idea deposited in intake inbox
- **Event:** `JANITOR_WrkSps/state/idea_inbox.yaml` is modified
- **Priority:** P3 (can wait for next sweep)
- **Behavior:** Queues. Processed during stage 7 (Triage) of the next scheduled sweep.
- **Difference from scheduled wake:** None — triage happens on the normal schedule.
- **Artifact:** Triage result in Type 2 report

**FUTURE MERGE — Power Automate**

#### Hook 5: Version bump in MANIFEST or a skill
- **Event:** `MANIFEST.md` or any `SKILL.md` file is edited
- **Priority:** P2 (tracking)
- **Behavior:** Queues. Logged in state. Triggers registry rebuild on next sweep.
- **Difference from scheduled wake:** Forces skill registry rebuild even if performance log has no new entries.
- **Artifact:** Updated skill registry

**FUTURE MERGE — Power Automate**

#### Hook 6: Uncleared G-level blocker past threshold
- **Event:** A blocker in state has persisted past 7 days (Stage 1→2) or 21 days (Stage 2→3)
- **Priority:** P0 (escalation)
- **Behavior:** Interrupts. Triggers HTML form generation and places form in `forms/`. Updates blocker stage in state.
- **Difference from scheduled wake:** Only the blocker escalation logic runs.
- **Artifact:** HTML blocker form + updated state

**FUTURE MERGE — Power Automate**

### C. Hard Stop Conditions

Janitor MUST halt instead of continuing if:
1. **Notion MCP is completely unavailable AND no prior state exists.** Cannot produce a meaningful report with zero tracker data and zero history. Log the failure and stop.
2. **`JANITOR_WrkSps/state/` directory is inaccessible or unwritable.** Cannot persist state. Log to console and stop.
3. **Architecture v3.0 is not found at `LENY_WrkSps/architecture/LOOP_Architecture_v3.0.md`.** Janitor cannot orient without top-level doctrine. Log the missing file and stop.
4. **More than 3 tracker fetches fail in a single sweep.** Likely a systemic MCP issue, not individual page problems. Stop, report partial results, mark run as `partial`.
5. **State file is locked by another process.** Do not force-break the lock. Report and stop.

---

## Design Section 5: Output Model

### Type 1 — Execution Packets

See Deliverable 4 for filled examples of each packet type.

#### 5.1 Skill Improvement Dispatch
- **Target surface:** `skill-improvement` skill (global)
- **Schema adapter:** LOOP execution packet (Adapter B — cowork_floor)
- **Trigger condition:** Skill miss count crosses threshold in performance log
- **Required inputs:** skill_name, current_miss_count, threshold, evidence_entries (from perf log), skill_file_path
- **Expected recipient action:** Run improvement pass, produce improved skill file
- **Proof-of-completion:** New performance log entry with "improvement pass" event for the skill; skill file version bumped

#### 5.2 Container Promotion Dispatch
- **Target surface:** `artifact-version-promotion` skill (global)
- **Schema adapter:** LOOP execution packet
- **Trigger condition:** Promotion criteria met (Section 2b)
- **Required inputs:** artifact_path, current_version, target_location, promotion_checklist_status
- **Expected recipient action:** Execute promotion checklist (versioned filename, header update, MANIFEST update, Notion log)
- **Proof-of-completion:** Target file exists at promoted path; MANIFEST updated

#### 5.3 Doctrine Update Dispatch
- **Target surface:** `workspace-path-migration` skill (global)
- **Schema adapter:** LOOP execution packet
- **Trigger condition:** Doctrine drift detected (Section 2d)
- **Required inputs:** stale_references (list of file:line:reference), correct_reference, scope (LENY_WrkSps only for Phase 1)
- **Expected recipient action:** Sweep and update stale references
- **Proof-of-completion:** Re-grep for stale references returns zero matches

#### 5.4 Phase Unblock Action
- **Target surface:** Malik (via Type 2 report) or relevant skill
- **Schema adapter:** Blocker clearance form (HTML) + YAML submission
- **Trigger condition:** G-level blocker detected at Stage 2+
- **Required inputs:** blocker_description, source_tracker, detected_date, escalation_stage, decision_options
- **Expected recipient action:** Malik makes a decision, records it in the YAML submission artifact
- **Proof-of-completion:** Janitor detects blocker cleared on next sweep

#### 5.5 Overlap Remediation
- **Target surface:** Malik (via Type 2 report)
- **Schema adapter:** Report section (not a separate dispatch)
- **Trigger condition:** Overlap > 60% between two non-sibling items
- **Required inputs:** item_a, item_b, overlap_keywords, overlap_percentage, recommendation
- **Expected recipient action:** Malik decides: merge, add scope boundary, or acknowledge as siblings
- **Proof-of-completion:** Items registered as siblings in state, or merge/boundary action taken

#### 5.6 New Idea Triage
- **Target surface:** Malik (via Type 2 report) or `loop-tracker-create` (if greenlit)
- **Schema adapter:** Idea triage result in YAML
- **Trigger condition:** New entry in `idea_inbox.yaml`
- **Required inputs:** idea_description, overlap_analysis, triage_verdict, recommended_action
- **Expected recipient action:** Malik confirms verdict; if greenlit, `loop-tracker-create` runs
- **Proof-of-completion:** Idea moved from inbox to either a tracker reference or archive

### Type 2 — Malik-Facing Tracker Report

See Deliverable 4 for the full template and a filled example.

**Report sections:**
1. **Run metadata** — date, run_id, sweep type, duration
2. **System health summary** — overall status (GREEN / YELLOW / RED), tracker count, change count
3. **Tracker state table** — all trackers with current status, changes since last sweep
4. **Feature/skill registry** — consolidated skill table
5. **Blockers dashboard** — all active blockers by stage, with escalation indicators
6. **Dependency map** — which trackers feed into which
7. **Overlap warnings** — any new overlaps detected
8. **Convergence opportunities** — trackers approaching merge points
9. **Upcoming promotions** — promotion candidates with readiness status
10. **Pending manual actions** — FUSE uploads, Container deletes, etc.
11. **Scheduled task health** — last fire dates, missed windows
12. **Skill gaps detected** — recurring failures with no covering skill
13. **Idea triage results** — if inbox had entries
14. **Ignored items** — deferred blockers, parked ideas

### HTML Blocker Form

See Deliverable 4 for the full form schema, visual design, and filled example.

**Form schema fields:**
- `blocker_id` (auto-generated: `BLK-YYYYMMDD-NNN`)
- `source_tracker` (name + Notion URL)
- `blocker_description` (from tracker)
- `detected_date`
- `escalation_stage` (1 / 2 / 3)
- `days_unresolved`
- `decision_options` (list of labeled choices)
- `decision_selected` (Malik fills this)
- `decision_rationale` (Malik fills this)
- `decision_date` (Malik fills this)

**Escalation-stage visual differences:**
- Stage 1: Standard layout, blue accent, informational header
- Stage 2: Yellow/amber background, bold header "DECISION REQUIRED", form appears in reports
- Stage 3: Red background, full-width banner "CRITICAL BLOCKER — ACTION REQUIRED", impossible to miss. Animated border pulse. Placed at TOP of Type 2 report before any other content.

**Output YAML artifact:** When Malik fills out the form, the decision is recorded in a YAML file at `JANITOR_WrkSps/forms/BLK-YYYYMMDD-NNN_decision.yaml`.

---

## Design Section 6: Skill Integration Map

| Skill | Version | Classification | Trigger Owner | Interface Description | Duplicate-Work Risk |
|-------|---------|---------------|---------------|----------------------|-------------------|
| loop-node-hygiene | v1.0 | Peer | Scheduled (own) | Janitor reads hygiene report; does not re-audit SYSTEM | Low — different scope (SYSTEM zone only vs cross-tracker) |
| loop-node-query | v1.1 | Consumed | Janitor | Janitor calls for tracker reads | None |
| loop-tracker-create | v1.0 | Independent | User/skill | Janitor may recommend but never creates | None |
| loop-session-open | v1.2 | Independent | Container session | Disabled on Floor; Janitor has own startup | None |
| loop-session-close | v1.2 | Independent | Container session | Disabled on Floor; Janitor has own close | None |
| Task Classification | v1.0 | Independent | Every task | Janitor is not a task — it's a sweep | None |
| Compaction | v1.0 | Independent | Context limits | Janitor reports are short; no compaction needed | None |
| Node Write Back | v1.0 | Independent | Node write requests | Janitor does not write to Node | None |
| Execution Prompt Design | v1.0 | Independent | T2 prompt creation | Janitor prompt is pre-designed | None |
| Node Archive Pass | v1.1 | Peer | On-demand | Different scope from Janitor; Janitor may note when archive-worthy pages accumulate | Low |
| Notion Task Audit | v1.0 | Peer | On-demand / scheduled | Janitor may detect stale tasks via tracker analysis; could dispatch | Low — Janitor does not audit Tasks DB directly |
| Artifact Version Promotion | v1.1 | Orchestrated | Janitor dispatches | Janitor detects promotion candidates, sends dispatch packet | Medium — must check pending dispatches to avoid re-sending |
| Container Knowledge Sync | v1.2 | Peer | Sync requests | Janitor detects stale Container state; reports but does not sync | Low |
| loop-floor-query | v1.0 | Consumed | Janitor | Janitor uses for Floor file existence checks | None |
| loop-patch-sync | — | Peer | Session close | Janitor reads patch list; does not write patches | None |
| loop-patch-report | v1.0 | Peer | Scheduled Fri | Janitor consumes report data; does not regenerate | Low — different cadence and scope |
| loop-write-through | — | Independent | Import requests | Outside Janitor scope | None |
| vendor-docs | v0.2 | Independent | Scheduled Sat / on-demand | Outside Janitor scope | None |
| gdrive-write | — | Independent | Upload requests | Outside Janitor scope | None |
| file-query | — | Independent | Token-limit errors | Janitor may use internally for large state files | None |
| bulk-edit-safety | — | Independent | Bulk edit requests | Outside Janitor scope | None |
| yaml-frontmatter-safe | — | Independent | YAML parsing | Outside Janitor scope | None |
| canonical-bug-class-correction | v1.0 | Independent | Bug class correction | Outside Janitor scope | None |
| Cold Start Context Load | v2.0 | Independent | Session start | Janitor has own startup; does not use cold-start | None |
| Document Review Response | v1.0 | Independent | Review feedback | Outside Janitor scope | None |
| Workspace Path Migration | v1.0 | Orchestrated | Janitor dispatches | Janitor detects stale paths via doctrine drift; sends dispatch | Medium — must check pending dispatches |
| Performance Log Write | v3.0 | Read | Every skill fire | Janitor reads; never writes | None |
| Prebuild Overlap Scan | v1.0 | Peer | Build/create intent | Janitor's overlap detection is broader (cross-tracker + cross-skill); prebuild is per-artifact | Low — complementary scopes |
| Skill Improvement | v1.1 | Orchestrated | Threshold crossing | Janitor dispatches; skill-improvement executes. Janitor must NOT dilute aggressive behavior. | Medium — must check pending dispatches |
| Skill Performance Ledger | v3.0 | Read | Every skill fire | Janitor reads thresholds; never writes to ledger | None — Janitor is read-only on this surface |
| wiki-build | v1.3 | Independent | Scheduled Sun / queue items | Outside Janitor scope | None |
| wiki-queue-feeder | — | Independent | Scheduled Sun / gap detection | Janitor monitors scheduled health only | None |
| Node Index | v1.1 | Consumed | Lookups | Janitor references for tracker IDs | None |
| Floor Index | v1.0 | Consumed | Lookups | Janitor references for path resolution | None |

### Orchestrated Skill Details

**Artifact Version Promotion (Orchestrated):**
- Janitor sends: promotion dispatch packet (artifact path, version, target location, checklist status)
- Janitor expects back: promoted file at target path, MANIFEST updated
- Completion known: next sweep detects version change in MANIFEST or file path
- Double-triggering prevention: `pending_promotion_dispatches` list in state; cleared when promotion detected

**Workspace Path Migration (Orchestrated):**
- Janitor sends: doctrine update dispatch (stale references list, correct reference, scope)
- Janitor expects back: stale references replaced
- Completion known: next sweep re-greps for stale references, expects zero matches
- Double-triggering prevention: `pending_migration_dispatches` list in state

**Skill Improvement (Orchestrated):**
- Janitor sends: skill improvement dispatch (skill name, miss count, threshold, evidence)
- Janitor expects back: improved skill file, performance log entry
- Completion known: performance log shows improvement pass for the skill
- Double-triggering prevention: `pending_skill_dispatches` list in state

**Hard constraint restated:** `skill-performance-ledger` and `skill-improvement` must preserve their current aggressive behavior exactly. Janitor may coordinate around them, not dilute them. Janitor never intercepts a threshold crossing — it only reads the crossing and dispatches.

### Janitor's Own Future Skill Description (for MANIFEST)

```yaml
name: floor-janitor
version: v0.3
scope: floor
owner: LENY
status: draft
description: >
  Cross-workstream state coordinator and system health reporter. Runs as a
  named operational mode of Lenny. Reads all phase trackers, the skill
  performance log, the patch list, and Floor file state to produce two
  output classes: (1) bounded execution dispatch packets for skill-improvement,
  artifact-version-promotion, and workspace-path-migration; (2) Malik-facing
  tracker reports with blocker escalation, promotion awareness, overlap
  detection, convergence flagging, and scheduled task health monitoring.
  Does not promote, does not write to the performance log, does not create
  trackers. Promotion authority remains with Malik.
  Trigger on: "run janitor", "janitor sweep", "system health check",
  "what's blocked", "what needs my attention", "cross-tracker status",
  "what's ready to promote".
```

---

## Design Section 7: Implementation Phases

See Deliverable 2 (`floor_janitor_implementation_phases_v0.3__20260412__draft.md`) for the full phased build plan.

**Summary:**

| Phase | Name | Scope | Session Count | Hook Dependency |
|-------|------|-------|--------------|----------------|
| 1 | Foundation + First Sweep | Directory setup, state schema, manual sweep prompt, first Type 2 report | 1 session | None |
| 2 | Dispatch + Forms | Type 1 packets, HTML blocker forms, idea inbox | 1 session | None |
| 3 | Automated Cadence | Scheduled task via Claude Code scheduled tasks | 1 session | None |
| 4 | Hook Infrastructure | Power Automate triggers for file watches, threshold alerts | 2 sessions | **FUTURE MERGE — Power Automate** |
| 5 | Notion State Mirror | Optional Notion page mirroring Janitor state for mobile visibility | 1 session | **FUTURE MERGE — Power Automate** |

Phase 1 is executable now, in one session, with no hooks, no automation dependency, and no Power Automate requirement.

---

## Design Section 8: Overlap Analysis

### Janitor Functions vs Existing Skills

| Janitor Function | Existing Skill | Overlap Type | Recommendation |
|-----------------|---------------|-------------|----------------|
| Cross-tracker state synthesis | None | No overlap | New capability — no existing skill reads across all trackers |
| Promotion awareness | `artifact-version-promotion` | Interface only | Janitor detects; skill executes. No duplication. |
| G-level blocker detection | `loop-patch-report` | Partial overlap | Patch report covers patch-level blockers; Janitor covers tracker-level blockers. **Extend:** Janitor reads patch report output for patch-level blocker integration rather than re-scanning the patch list independently. |
| Doctrine drift detection | `workspace-path-migration` | Interface only | Janitor detects; skill sweeps. No duplication. |
| Skill lifecycle coordination | `skill-performance-ledger` + `skill-improvement` | Coordination layer | Janitor reads ledger output and dispatches to improvement. **No duplication.** Janitor never writes to the ledger or executes improvement passes. |
| Overlap detection | `prebuild-overlap-scan` | Complementary scopes | Prebuild scans per-artifact at build time; Janitor scans cross-system periodically. **Extend:** Janitor could feed its overlap findings into prebuild's keyword expansion list (v1.1 proposed improvement). |
| Registry maintenance | None | No overlap | New capability — no existing skill maintains a consolidated registry |
| Cross-tracker convergence | None | No overlap | New capability |
| New idea intake | None | No overlap | New capability — no existing skill triages ideas |
| Scheduled task health | None | No overlap | New capability — no existing skill monitors scheduled task cadence |

### Trackers Janitor Would Make Redundant

**None.** Janitor does not replace any tracker. It reads trackers as input. No tracker becomes unnecessary because Janitor exists.

### Missing Capabilities That Truly Require New Skills

1. **No new skills required for Phase 1.** Janitor is designed to compose existing skills via dispatch packets, not to create new skills.

2. **Phase 4 (hooks) will require Power Automate flows**, which are infrastructure, not skills. The Relay/Power Automate layer is not yet built. When it is, each hook becomes a Power Automate flow that triggers a Janitor mini-sweep.

### Explicit Attention to Named Skills

**`loop-node-hygiene`:** Janitor scope is cross-tracker synthesis across all zones and workstreams. Hygiene scope is SYSTEM zone page classification and cleanup. They share the "read Notion pages" pattern but never the same pages. **No conflict.** Janitor reads hygiene results as a data point for scheduled task health monitoring.

**`prebuild-overlap-scan`:** Janitor's overlap detection is periodic and cross-system. Prebuild is synchronous and per-artifact at build time. They are complementary. **Interface opportunity:** Janitor could maintain an `overlap_known_siblings` list that prebuild consults to reduce false negatives.

**`skill-performance-ledger`:** Janitor reads the ledger. Janitor never writes to it. The ledger's aggressive real-time logging behavior is preserved exactly. **No conflict.**

**`skill-improvement`:** Janitor dispatches to it when thresholds cross. Janitor never executes improvement passes. The improvement skill's ceiling detection and diminishing-returns logic is preserved exactly. **No conflict.**

**`container-knowledge-sync`:** Janitor detects stale Container state (Container backup != Floor current) and reports it. Janitor does not sync. Container-knowledge-sync does the actual work. **No conflict.** Janitor may eventually dispatch to it, but Phase 1 only reports the drift.

---

*Floor Janitor Agent Design v0.3 -- Draft -- 2026-04-12*
