# LOOP Blockers — Contract Spine Final Naming Closure v0.1

> Author: LENY
> Date: 2026-04-13
> Status: `open`

---

## Blocker 1 — Notion Tracker Title (Node-side)

**Page:** "YAML Family — Naming & Cohesion Tracker" (`33fd67199b3381b6a7bfdd2ca48954c3`)
**Location:** Runtime & Phase Artifacts, under STACKS > Reference
**Issue:** Page title still uses retired "YAML Family" umbrella name.
**Impact:** Floor skill files (Node Index, tracker-create skill) reference it by current title. Cannot clean those references until the source is renamed.
**Required action:** THEO renames or archives the tracker on Node.
**Follow-up after rename:** Run `workspace-path-migration` or manual sweep to update Floor references that quoted the old title.

## Blocker 2 — Notion-Wide Legacy Scan (Node-side)

**Issue:** Notion workspace has not been exhaustively searched for other pages using "YAML Family" as an active umbrella label (beyond the known tracker).
**Impact:** Unknown. May be zero additional pages, may be several.
**Required action:** THEO runs a Notion-side search for "YAML Family" and triages results as active vs historical.

## Blocker 3 — Ontology Filename (THEO Decision)

**File:** `docs/ontology/yaml_family_ontology.md`
**Issue:** Filename uses retired umbrella. Content is forward-pointed with deprecation header, but the filename itself surfaces in `git log`, `find`, and cross-references.
**Impact:** Low — does not block issue execution. The deprecation header handles discoverability.
**Required action:** THEO decides: rename to `contract_spine_ontology.md` now, or defer to Issue 01 re-delivery.

---

**None of these blockers prevent Contract Spine issue execution from proceeding.** They prevent *final naming closure sign-off* only.

---

*— LENY, 2026-04-13*
