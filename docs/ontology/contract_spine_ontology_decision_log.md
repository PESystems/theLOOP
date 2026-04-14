# Contract Spine Ontology — Decision Log

> Authority: `docs/issues/contract_spine_v0_3/01_lock_contract_spine_ontology.md`
> Author: LENY
> Date: 2026-04-13
> Status: `draft` — awaiting THEO canonical review

This log captures boundary calls, resolved questions, and deferred items for the Contract Spine Ontology v0.3.

---

## Resolved Decisions

### D-01: `intent` excluded from ontology
**Question:** Should `intent` be a canonical ontology term alongside the 9 locked terms?
**Decision:** No. `intent` is schema-only / packet-only. It describes what a specific pipeline run is trying to accomplish, not a persistent ontological concept.
**Rationale:** THEO review confirmed: intent belongs in the core contract schema (Issue 02) as a packet-level field. Including it in the ontology would blur the line between "what things are" (ontology) and "what we want to do with them" (execution packet).
**Authority:** THEO review, 2026-04-13.

### D-02: Relationship map format
**Question:** Directed list, table, or diagram?
**Decision:** Directed list as primary canonical form. Compact support table included for quick reference. No diagram in v1.0.
**Rationale:** Directed list is the most readable and diff-friendly format. A support table adds scanability without introducing rendering dependencies. Diagram deferred until contract stack (Issues 01–04) is battle-tested.
**Authority:** THEO review, 2026-04-13.

### D-03: `adapter` scope — narrow definition
**Question:** How broadly should `adapter` be defined? Could adapters carry execution logic or extend the schema?
**Decision:** Narrow. Adapters are surface/runtime translation layers only. They may wrap or translate. They may NOT redefine canonical ontology terms or add ontology-level concepts.
**Rationale:** Broad adapter definitions are the most likely vector for ontology drift. If an adapter needs a new concept, the ontology must be updated through THEO review — the adapter cannot invent locally.
**Authority:** THEO review, 2026-04-13.

### D-04: Anti-drift pairs
**Question:** Which confusion pairs need explicit treatment in the Forbidden Drift Patterns section?
**Decision:** Six pairs addressed:
1. source vs artifact
2. entity vs claim
3. uncertainty vs validation_state
4. validation_state vs promotion_state
5. receipt vs report/manifest/audit log
6. adapter vs packet/schema
**Rationale:** These are the pairs most likely to collapse or blur during implementation, particularly across Claude.ai and Floor surfaces.
**Authority:** THEO review, 2026-04-13.

---

## Open / Deferred Items

### O-01: `constraint` as a potential future term
**Status:** Deferred — not needed for v0.3.
**Context:** Explicit constraints (anti-goals, scope limits) currently live in packet-level fields. If constraints appear as ontology-level concepts across multiple lanes, this should be revisited. Bar for addition: cannot be covered by existing terms through composition.

### O-02: Relationship map — future diagram
**Status:** Deferred to post-v1.0.
**Context:** Visual diagram may be valuable once the full contract stack (Issues 01–04) is built and term relationships are stable. Premature diagramming risks encoding assumptions before they're proven.

### O-03: Term count ceiling
**Status:** Noted — no action needed yet.
**Context:** 9 terms is the current ceiling. The ontology should resist growth. The bar for a 10th term is: it cannot be expressed through composition of the existing 9, and it appears as a first-class concept in multiple lanes.

---

*— LENY, 2026-04-13*
