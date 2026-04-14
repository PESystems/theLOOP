# Contract Spine Ontology v0.3

> Status: `draft` — awaiting THEO canonical review
> Author: LENY
> Date: 2026-04-13
> Authority: `docs/issues/contract_spine_v0_3/01_lock_contract_spine_ontology.md`
> Naming lock: `docs/naming/LOOP_contract_spine_nomenclature_v0.1.md`

This document defines the shared ontology for the LOOP Contract Spine. All lanes, adapters, schemas, and receipts must use these terms with the meanings defined here. Lane-specific language must map back to these canonical terms — never invent parallel concepts.

---

## Canonical Terms

### source

**Definition:** The original material entering the system — a document, file, URL, pasted text, or other raw input that has not yet been normalized.

**Role in pipeline:** Entry point. Every pipeline run begins with a source. Sources are referenced but never mutated by the system.

**What it is NOT:** Not an artifact. A source becomes an artifact only after normalization. A source is not a claim — it may contain claims, but the source itself is unstructured input.

---

### artifact

**Definition:** A normalized, structured representation produced by the system from one or more sources. Artifacts are the working objects that move through the pipeline.

**Role in pipeline:** Artifacts are what lanes operate on. Extraction, validation, and promotion all act on artifacts, not on raw sources.

**What it is NOT:** Not the source itself. A PDF is a source; the structured contract extracted from it is an artifact. An artifact is not a receipt — artifacts carry content and structure, receipts carry operational outcomes.

---

### entity

**Definition:** A discrete, named thing identified within an artifact — a product, a person, a parameter, a component. Entities are factual identifiers, not assertions.

**Role in pipeline:** Entities anchor claims. Claims are always *about* one or more entities. Entity extraction produces the structured backbone of an artifact.

**What it is NOT:** Not a claim. "Yaskawa A1000" is an entity. "The A1000 supports sensorless vector control" is a claim about that entity. Entities do not carry truth values — claims do.

---

### claim

**Definition:** A specific assertion extracted from a source, attached to one or more entities. Claims carry meaning that can be validated as true, false, uncertain, or conflicting.

**Role in pipeline:** Claims are the atomic units of validation. The validation contract evaluates claims, not entities or artifacts as wholes.

**What it is NOT:** Not an entity. Not a fact — a claim is an *assertion* that requires validation before it can be treated as fact. Not a summary or interpretation — claims are extracted, not generated.

---

### uncertainty

**Definition:** A structured marker indicating that a claim's truth value is not yet resolved. Uncertainty records *why* a claim cannot be confirmed — missing source, conflicting data, ambiguous language, or insufficient evidence.

**Role in pipeline:** Uncertainty is attached to claims. It prevents premature promotion by making unknowns explicit. Validation rules use uncertainty to determine whether a claim can pass, must be blocked, or is provisional.

**What it is NOT:** Not the same as `validation_state`. Uncertainty describes *the nature of the doubt*. Validation state describes *the system's decision about that doubt*. A claim can have uncertainty and still receive a `provisional` validation state.

---

### validation_state

**Definition:** The system's judgment on a claim after applying validation rules. One of: `pass`, `fail`, `provisional`, `blocked`, `conflict`.

**Role in pipeline:** Validation state is the gate between extraction and promotion. Only claims with appropriate validation states can advance. Validation state is set by the Validation Layer contract, not by individual lanes or adapters.

**What it is NOT:** Not uncertainty. Uncertainty is the input to validation; validation state is the output. Not promotion state — validation says "this claim has been evaluated," promotion says "this claim has been approved for canonical use."

---

### promotion_state

**Definition:** The status of a validated artifact or claim's advancement toward canonical truth. One of: `staged`, `promoted`, `rejected`, `reverted`.

**Role in pipeline:** Promotion state governs what crosses the Compile Boundary into the Node. Only `promoted` material becomes coordination truth. `staged` means ready for review. `rejected` means reviewed and denied. `reverted` means previously promoted but withdrawn.

**What it is NOT:** Not validation state. Validation determines quality; promotion determines destination. A claim can `pass` validation but remain `staged` if human review is required before Node promotion.

---

### receipt

**Definition:** A structured record of a pipeline operation's outcome — what was attempted, on what surface, with what result. Receipts are emitted by every mutating or potentially mutating action.

**Role in pipeline:** Receipts make the Contract Spine auditable. They connect a contract run to its outcome, surface, and any blockers or conflicts encountered. Dry runs emit receipts. Failures emit receipts. The Receipt Layer manages receipt emission and structure.

**What it is NOT:** Not a report, manifest, or audit log. A receipt records one operation's outcome in a structured format. It does not narrate, summarize, or aggregate. It does not contain the full artifact — it references it.

---

### adapter

**Definition:** A surface-specific translation layer that wraps the core contract for consumption or emission on a particular runtime. Adapters specify *how* a surface interacts with the contract — read order, field mapping, preflight rules, receipt emission format.

**Role in pipeline:** Adapters sit between the core contract and execution surfaces (Claude.ai, Floor/Cowork, Node/Notion). Each surface gets one adapter via the Adapter Layer. The adapter translates without redefining.

**What it is NOT:** Not a packet or schema. A packet is a bounded unit of work. A schema defines structure. An adapter defines *how a surface uses* the schema and packets. Adapters may NOT redefine canonical ontology terms — they translate surface-specific concerns only. An adapter that changes what "claim" means is a broken adapter.

---

## Relationship Map

Primary canonical form — directed list:

```
source → artifact
artifact → entity + claim
claim → uncertainty
claim + uncertainty → validation_state
validation_state → promotion_state
promotion_state → receipt
adapter wraps [source, artifact, receipt] per surface
```

| From | To | Relationship |
|------|----|-------------|
| source | artifact | normalization produces |
| artifact | entity | extraction identifies |
| artifact | claim | extraction asserts |
| claim | uncertainty | evaluation may attach |
| claim + uncertainty | validation_state | Validation Layer decides |
| validation_state | promotion_state | Compile Boundary advances |
| promotion_state | receipt | Receipt Layer emits |
| adapter | source, artifact, receipt | Adapter Layer translates per surface |

---

## Worked Examples

### Ingress Lane — Google Doc enters the system

1. **source** — a Google Doc URL shared in Claude.ai chat
2. **artifact** — LENY normalizes the doc content into a structured contract
3. **entity** — extraction identifies: `Yaskawa A1000`, `sensorless vector control`, `heavy-duty rating`
4. **claim** — extraction asserts: "The A1000 supports sensorless vector control up to 150% torque at 0.3 Hz"
5. **uncertainty** — the 0.3 Hz figure appears in one source only; flagged `single_source`
6. **validation_state** — Validation Layer sets claim to `provisional` (single-source uncertainty)
7. **promotion_state** — artifact is `staged`, awaiting human review before Node promotion
8. **receipt** — dry-run receipt emitted: surface=`claude_chat_cloud`, mode=`dry_run`, outcome=`staged`, blockers=`none`, notes=`1 provisional claim flagged`
9. **adapter** — Claude.ai adapter handled source fetch (URL paste), inline normalization, and cloud receipt emission

### Distillation Lane — wiki article refined

1. **source** — raw wiki draft on Floor at `LENY_WrkSps/wiki/VFD_Sensorless_Vector.md`
2. **artifact** — structured claim set extracted from the draft
3. **entity** — extraction identifies: `sensorless vector control`, `open-loop V/f`, `encoder feedback`
4. **claim** — extraction asserts: "Sensorless vector provides torque control without encoder hardware"
5. **uncertainty** — none; claim is well-sourced across multiple datasheets
6. **validation_state** — `pass` (multi-source, no conflicts)
7. **promotion_state** — `promoted` after LENY review; crosses Compile Boundary
8. **receipt** — write receipt emitted: surface=`floor_execution`, mode=`live_write`, outcome=`promoted`, emitted_artifacts=`[wiki_vfd_sensorless_v1.yaml]`
9. **adapter** — Floor adapter handled local file read, heavy normalization, and floor receipt emission. Node receives a compiled pointer — not the full artifact.

---

## Forbidden Drift Patterns

These patterns indicate the ontology is being violated. Any lane, adapter, or schema exhibiting them must be corrected.

### 1. source vs artifact confusion
**Drift:** Treating raw input as if it were already normalized. Skipping the source → artifact boundary.
**Signal:** A schema that validates claims directly against a PDF or URL without an intermediate artifact.
**Rule:** Sources are never operated on directly. Always normalize to artifact first.

### 2. entity vs claim confusion
**Drift:** Treating entity names as if they carry truth values, or treating claims as if they are entity identifiers.
**Signal:** An entity field that contains assertions ("A1000 — best for heavy duty"). A claim field that contains only a name ("Yaskawa A1000").
**Rule:** Entities identify. Claims assert. They are always separate.

### 3. uncertainty vs validation_state confusion
**Drift:** Using uncertainty markers as validation outcomes, or skipping uncertainty and jumping straight to pass/fail.
**Signal:** A claim marked `uncertain` with no validation_state. A validation_state of `uncertain` (not a valid state).
**Rule:** Uncertainty is the *input* to validation. Validation state is the *output*. Both must exist independently.

### 4. validation_state vs promotion_state confusion
**Drift:** Treating validation as promotion. A claim that `passes` validation being treated as canonical without a promotion step.
**Signal:** No `staged` state. Validated claims appearing directly in Node without promotion review.
**Rule:** Validation gates quality. Promotion gates destination. They are sequential, not synonymous.

### 5. receipt vs report/manifest/audit log confusion
**Drift:** Receipts becoming narrative summaries, aggregated dashboards, or full artifact dumps.
**Signal:** A receipt that contains the full text of an artifact. A receipt that reads like prose. A "receipt" that aggregates multiple operations.
**Rule:** One receipt per operation. Structured, not narrative. References artifacts, does not contain them.

### 6. adapter vs packet/schema confusion
**Drift:** An adapter that defines new fields, reinterprets ontology terms, or acts as a schema extension.
**Signal:** An adapter file that contains term definitions different from this ontology. An adapter that adds required fields not in the core contract.
**Rule:** Adapters translate surface concerns. They wrap and map. They never redefine. If an adapter needs a concept the ontology does not have, the ontology must be updated through review — the adapter does not get to invent it locally.

---

## Governance

- This ontology is the authority for term meaning across the Contract Spine.
- Changes require explicit review (THEO or Malik).
- No lane, adapter, or schema may override these definitions.
- If a term is missing, propose an ontology addition — do not create a local synonym.

---

*— LENY, 2026-04-13*
