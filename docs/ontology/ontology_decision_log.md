# Ontology Decision Log

> Issue 01 — Lock the YAML Family Ontology
> Author: LENY
> Date: 2026-04-13

This log captures boundary calls, resolved questions, and deferred items from the ontology authoring process.

---

## Resolved Decisions

### D-01: `intent` excluded from ontology
**Question:** Should `intent` be a canonical ontology term alongside the 9 locked terms?
**Decision:** No. `intent` is schema-only / packet-only. It describes what a specific pipeline run is trying to accomplish, not a persistent ontological concept.
**Rationale:** THEO review confirmed: intent belongs in the contract schema (Issue 02) as a packet-level field, not in the shared ontology. Including it would blur the line between "what things are" (ontology) and "what we want to do with them" (execution).
**Authority:** THEO review, 2026-04-13.

### D-02: Relationship map format
**Question:** Directed list, table, or diagram?
**Decision:** Directed list as primary canonical form. Compact support table included for quick reference. No diagram in v1.0.
**Rationale:** Directed list is the most readable and diff-friendly format. A support table adds scanability without introducing rendering dependencies.
**Authority:** THEO review, 2026-04-13.

### D-03: `adapter` scope — narrow definition
**Question:** How broadly should `adapter` be defined? Could adapters carry execution logic or extend the schema?
**Decision:** Narrow. Adapters are surface/runtime translation layers only. They may wrap or translate. They may NOT redefine canonical ontology terms or add ontology-level concepts.
**Rationale:** Broad adapter definitions are the most likely vector for ontology drift. If an adapter needs a new concept, the ontology itself must be updated through review — the adapter does not get to invent locally.
**Authority:** THEO review, 2026-04-13.

### D-04: Anti-drift pairs
**Question:** Which confusion pairs need explicit treatment?
**Decision:** Six pairs addressed:
1. source vs artifact
2. entity vs claim
3. uncertainty vs validation_state
4. validation_state vs promotion_state
5. receipt vs report/manifest/audit log
6. adapter vs packet/schema
**Rationale:** These are the pairs most likely to collapse or blur during implementation, especially across different surfaces.
**Authority:** THEO review, 2026-04-13.

---

## Open / Deferred Items

### O-01: `constraint` as a potential future term
**Status:** Deferred — not needed for v0.3.
**Context:** Some pipeline work involves explicit constraints (anti-goals, scope limits). These currently live in packet-level fields. If constraints start appearing as ontology-level concepts across multiple lanes, this term should be revisited.

### O-02: Relationship map — future diagram
**Status:** Deferred to post-v1.0.
**Context:** A visual diagram may be useful once the full contract stack (Issues 01–04) is built and the relationships are battle-tested. Premature diagramming risks encoding assumptions that haven't been validated yet.

### O-03: Term count ceiling
**Status:** Noted — no action needed yet.
**Context:** 9 terms is the current ceiling. The ontology should resist growth. Any proposed addition must demonstrate that existing terms cannot cover the concept through composition. The bar for a 10th term should be high.

---

*— LENY, 2026-04-13*
