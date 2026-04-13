# LOOP Cleanup Packet — Contract Spine Naming v0.1

> Author: LENY
> Date: 2026-04-13
> Authority: THEO naming closure dispatch
> Status: `draft`

---

## Safe Now

These moves are unambiguous, non-destructive, and authorized by the dispatch.

### S01 — Add deprecation header to `docs/ontology/yaml_family_ontology.md`

- **Target:** `docs/ontology/yaml_family_ontology.md` lines 1-6
- **Old naming:** Title "YAML Family Ontology v0.3", authority line "Lock the YAML Family Ontology"
- **Action:** Prepend a deprecation/forward header block. Do not rewrite the document body.
- **New header:** States this document was authored under the prior naming regime, the active umbrella is now "LOOP Contract Spine", and links to the naming lock.
- **Why safe:** Adds context without altering content. Original text preserved below the header.
- **Rollback:** Remove the prepended header block.

### S02 — Add deprecation header to `docs/ontology/ontology_decision_log.md`

- **Target:** `docs/ontology/ontology_decision_log.md` lines 1-4
- **Old naming:** "Issue 01 — Lock the YAML Family Ontology"
- **Action:** Prepend a deprecation/forward header block.
- **Why safe:** Same as S01. Adds context, preserves content.
- **Rollback:** Remove the prepended header block.

### S03 — Update `leny/STATUS.md` section header and issue name

- **Target:** `leny/STATUS.md` lines 8, 12
- **Old naming:** "Issue Stack — YAML Family v0.3", "Lock YAML Family Ontology"
- **New naming:** "Issue Stack — Contract Spine v0.3", "Lock Contract Spine Ontology"
- **Why safe:** This is LENY's active operational tracker. It must reflect the active namespace to prevent future work from building on the wrong name.
- **Rollback:** Revert the two line edits.

### S04 — Add deprecation README to `docs/issues/yaml_family_v0_3/`

- **Target:** `docs/issues/yaml_family_v0_3/README.md`
- **Old naming:** "LOOP YAML Family Issue Stack v0.3" as active title
- **Action:** Prepend a deprecation header stating this folder is historical, the active issue stack is at `docs/issues/contract_spine_v0_3/`, and the naming lock is at `docs/naming/LOOP_contract_spine_nomenclature_v0.1.md`.
- **Why safe:** Does not alter issue content. Adds forward pointer so any reader landing here is directed to the active stack.
- **Rollback:** Remove the prepended header block.

### S05 — Update governance line in ontology document

- **Target:** `docs/ontology/yaml_family_ontology.md` line 197
- **Old naming:** "across the YAML family"
- **New naming:** "across the Contract Spine"
- **Why safe:** This is in the governance section which states active authority. It should reflect the active umbrella, not the retired one.
- **Rollback:** Revert the single line edit.

---

## Requires Review

These moves are justified but have material implications that THEO should approve.

### RR01 — Rename `docs/ontology/yaml_family_ontology.md` filename

- **Target:** File path `docs/ontology/yaml_family_ontology.md`
- **Old naming:** `yaml_family_ontology.md`
- **Proposed:** `contract_spine_ontology.md`
- **Why justified:** The filename is the most visible legacy reference. Every future `git log`, `find`, and cross-reference will surface it.
- **Why deferred:** The file is referenced in the old issue pack (Issue 01 deliverables), in the LENY plan, and potentially in Notion. Renaming could break external pointers.
- **THEO decision needed:** Rename now, or leave until Issue 01 is re-delivered under Contract Spine naming?

### RR02 — Rename Notion tracker "YAML Family — Naming & Cohesion"

- **Target:** Notion page `33fd67199b3381b6a7bfdd2ca48954c3`
- **Old naming:** "YAML Family — Naming & Cohesion Tracker"
- **Proposed:** "Contract Spine — Naming & Cohesion Tracker" or archive the tracker
- **Why justified:** This is a live Notion tracker. Its name will surface in searches and skill references.
- **Why deferred:** LENY cannot rename Notion pages. Requires THEO action on Node.
- **THEO decision needed:** Rename, archive, or leave with a deprecation note?

### RR03 — Update LENY skill references (LOOP_Node_Index, loop-tracker-create)

- **Target:** `Projects/LENY_WrkSps/skills/global/LOOP_Node_Index_v1.1.md`, `Projects/LENY_WrkSps/skills/brain/loop-tracker-create/SKILL.md`
- **Old naming:** "YAML Family" in tracker references and examples
- **Why justified:** These are active skill files that could propagate the old umbrella.
- **Why deferred:** Skill rewrites are out of scope for a naming closure pass. The references point to a Notion tracker name — if the tracker is renamed on Notion, these should update to match.
- **THEO decision needed:** Defer until tracker rename, or patch now?

---

## Leave Historical

These references are intentionally preserved. No action needed.

| # | Target | Why Historical |
|---|--------|---------------|
| H01 | `leny/plans/01_lock_yaml_family_ontology_plan.md` | LENY's first plan — authored under old naming. Historical artifact of the agent pipeline setup. |
| H02 | `docs/issues/yaml_family_v0_3/*.md` (all 10 issue files) | Original THEO issue pack. Content superseded by `contract_spine_v0_3/` but preserved as the historical record of the first naming regime. |
| H03 | `docs/naming/LOOP_contract_spine_nomenclature_v0.1.md` retired names list | Intentionally documents retired names — this IS the naming lock. |
| H04 | `docs/issues/contract_spine_v0_3/01_lock_contract_spine_ontology.md` line 18 | Anti-drift reference: "Do not use YAML Family as the active umbrella" — correct governance language. |
| H05 | All Floor session artifacts (`LENY_WrkSps/sessions/ChatGPT Artifacts/*`) | Historical session outputs. Not active surfaces. |
| H06 | All JANITOR reports and logs | Historical reports referencing the Notion tracker name — not umbrella uses. |
| H07 | `ingestion/` Floor outputs | Historical pilot outputs. Not active surfaces. |
| H08 | `.obsidian/workspace.json` | Editor metadata. Self-clears. |

---

*— LENY, 2026-04-13*
