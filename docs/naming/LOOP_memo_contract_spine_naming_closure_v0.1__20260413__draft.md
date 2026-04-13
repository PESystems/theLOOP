# LOOP Memo — Contract Spine Naming Closure v0.1

> Status: `draft` — awaiting THEO canonical sign-off
> Author: LENY
> Date: 2026-04-13
> Type: Naming governance / system function

---

## 1. What Changed

The umbrella name for the LOOP contract-layer system has been renamed from **YAML Family** to **LOOP Contract Spine**.

This is not a cosmetic rename. It is a system-function change that redefines how all agents, documents, issue stacks, and execution surfaces refer to the contract-layer system.

### Active naming lock (effective 2026-04-13)

| Concept | Active Name |
|---------|-------------|
| Umbrella system | **LOOP Contract Spine** |
| Source intake + normalization | **Ingress Lane** |
| Reduction into structured meaning | **Distillation Lane** |
| Checks, conflicts, provisional/block rules | **Validation Layer** |
| Surface-specific wrappers | **Adapter Layer** |
| Promotion boundary into Node | **Compile Boundary** |
| Audit trail + mutation records | **Receipt Layer** |

### Retired umbrella names

These terms are retired as **active umbrella names**. They may still appear in historical artifacts and should be preserved there with deprecation markers where needed.

| Retired Name | Replaced By |
|-------------|-------------|
| YAML Family | LOOP Contract Spine |
| Ingestion Layer | Ingress Lane |
| Distillation (standalone) | Distillation Lane |

## 2. Why the Rename Happened

Three reasons:

1. **"YAML Family" confused implementation with architecture.** YAML is a serialization format. The contract system is a governance layer. Naming the system after its format locked the wrong concept at the top.

2. **"Ingestion Layer" was too narrow.** It implied one-directional intake. The actual system handles bidirectional flow — ingress, distillation, validation, compilation, and receipt emission.

3. **"Distillation" as a standalone umbrella was ambiguous.** It could mean the lane, the process, or the output. "Distillation Lane" is precise. Standalone "Distillation" is not.

## 3. What This Changes for Ongoing Work

### For LENY (Floor execution)
- All new artifacts, plans, receipts, and schemas must use Contract Spine naming.
- The ontology document (`docs/ontology/yaml_family_ontology.md`) was built under the old name and requires a forward pointer. Its content is valid; its framing needs a deprecation header.
- The LENY status board (`leny/STATUS.md`) must update its section header from "YAML Family v0.3" to "Contract Spine v0.3".
- Issue 01 plan (`leny/plans/01_lock_yaml_family_ontology_plan.md`) is a historical artifact — preserve as-is with no rewrite.

### For THEO (architecture / Notion)
- The active Notion page ("LOOP Contract Spine Spec + Issue Pack v0.3") is already using correct naming.
- The active GitHub issue stack (`docs/issues/contract_spine_v0_3/`) is already using correct naming.
- The old issue stack (`docs/issues/yaml_family_v0_3/`) should remain as a historical reference with a deprecation README.

### For the repo
- No folder deletions. The old `yaml_family_v0_3/` folder stays but gets a deprecation header on its README.
- No broad string replacement. Only active-facing references in LENY's operational files get updated.
- The naming lock document (`docs/naming/LOOP_contract_spine_nomenclature_v0.1.md`) is the single source of truth for naming.

## 4. What Cannot Be Signed Off Until Closure Is Complete

- **Issue 01 ontology** (`docs/ontology/yaml_family_ontology.md`) — cannot be promoted to canonical while its title and authority line still use "YAML Family" without at minimum a deprecation/forward header.
- **Issue 01 decision log** (`docs/ontology/ontology_decision_log.md`) — same: needs a forward header before canonical promotion.
- **LENY STATUS.md** — currently shows "YAML Family v0.3" as the active issue stack header. Must be updated before any canonical issue work is signed off.

## 5. Scope of This Closure Pass

This memo authorizes:
- deprecation markers on legacy-named active surfaces
- forward pointers from old naming to new naming
- operational reference updates in LENY's active files
- a structured audit of all legacy references

This memo does NOT authorize:
- folder deletions
- historical document rewrites
- broad string replacement
- canonical sign-off changes
- new umbrella term creation

---

## 6. Proposed Operating Rule for Future Naming/Doctrine Updates

**Advisory only — not canonical until THEO approves.**

When a system-level naming or doctrine change is made, the following structured update pattern should be followed:

| Step | Artifact | Purpose |
|------|----------|---------|
| 1 | **Naming lock document** | Single source of truth for active + retired names |
| 2 | **Retired names list** | Explicit list of what is no longer active |
| 3 | **Migration audit** | Structured inventory of all legacy references |
| 4 | **Cleanup packet** | Exact moves, grouped by safety level |
| 5 | **Execution receipt** | What was changed, what was preserved, rollback paths |
| 6 | **Sign-off gate** | THEO reviews closed loop before anything becomes canonical |

This pattern keeps naming changes governed and auditable without requiring a full doctrine rewrite every time.

---

*— LENY, 2026-04-13*
