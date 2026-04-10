# LOOP YAML → Notion Pipeline Spec
**Version:** v0.1  
**Date:** 2026-04-09  
**Status:** Draft

---

## 1. Purpose

Define the current and near-future pipeline that converts unstructured project input into structured operational state inside LOOP.

This spec is for the bridge between:
- raw capture
- normalized intake
- validation
- write-through into the Node

The current design assumes:
- the **Node** is coordination truth
- the **Container** is behavioral truth
- the **Floor** is execution truth

That means this pipeline must:
- keep business objects lean
- preserve ambiguity without polluting canonical records
- avoid premature promotion
- support future runtime adapters without baking model-specific logic into the core schema

---

## 2. Pipeline objective

Turn messy real-world project input into:
- usable structured entities
- low-ambiguity write candidates
- auditable promotion decisions
- future-compounding operational context

Examples of messy input:
- handwritten notes
- project dumps
- email threads
- screenshots
- PDFs
- photos of whiteboards or notebooks
- informal intake messages

---

## 3. Core pipeline flow

```text
Raw Input
  ↓
Extraction
  ↓
Canonical Intake YAML
  ↓
Normalization + Enrichment
  ↓
Validation Gate
  ↓
Write Candidate Set
  ↓
Node Write-Through
  ↓
Post-Write Receipt / Audit
```

---

## 4. Canonical top-level YAML structure

Use a 4-layer intake hierarchy:

```yaml
intake_envelope:
source_descriptor:
entity_payload:
extraction_control:
```

This is the base pattern.

### Why this shape
It separates:
- routing metadata
- source metadata
- business objects
- ambiguity / parser control

That keeps the project object from becoming a junk drawer.

---

## 5. Intake layer definitions

### 5.1 `intake_envelope`
System-level routing and audit metadata.

Typical fields:
```yaml
intake_envelope:
  schema_version: "0.2"
  intake_type: "media_project_capture"
  media_type: "photo"
  created_at: "2026-04-09T00:00:00Z"
  extraction_method: "vision_llm"
  confidence_profile: "mixed"
  source_id: "src_..."
  batch_id: "batch_..."
```

Use for:
- schema versioning
- run identification
- media type
- extraction method
- batch grouping
- confidence profile
- traceability

Do not store business meaning here.

---

### 5.2 `source_descriptor`
Describe the source itself, not the interpreted business record.

Typical fields:
```yaml
source_descriptor:
  source_title: "Projects notebook page"
  source_type: "handwritten_note"
  author_hint: "Malik"
  capture_context: "manual project dump"
  page_count: 1
  language: "en"
  quality_notes:
    - "handwriting mixed clarity"
    - "implicit grouping"
```

Use for:
- source title
- capture context
- source quality issues
- origin hints
- manual/vision/OCR notes

This prevents source weirdness from contaminating the project entity.

---

### 5.3 `entity_payload`
This is the business payload.

Recommended entity families:

```yaml
entity_payload:
  clients: []
  contacts: []
  projects: []
  tasks: []
  follow_ups: []
  assets: []
  events: []
```

Not every run will populate all families.

Current priority families for LOOP project intake:
- `projects`
- `clients`
- `follow_ups`
- `tasks`

---

### 5.4 `extraction_control`
This is where ambiguity lives.

Typical fields:
```yaml
extraction_control:
  uncertain_fields: []
  normalization_notes: []
  split_recommendations: []
  dedupe_candidates: []
  verification_required: []
  parser_warnings: []
  unmapped_observations: []
```

Use this to hold:
- low-confidence interpretations
- unresolved relationships
- notes that should not yet become first-class fields
- future schema candidates

This is the anti-clutter safety layer.

---

## 6. Entity design rules

### 6.1 Projects stay lean
A project record should only contain fields likely to matter repeatedly.

Suggested minimal structure:

```yaml
projects:
  - project_id: "proj_crosslink_horner_quote"
    project_name: "Horner Quote"
    client_name: "Crosslink"
    status_hint: "open"
    project_type_hint: "quote"
    system_type_hint: "controls"
    scope_summary: "Horner quote / motor service / HVAC-related follow-up"
    source_refs:
      - "src_notebook_001"
```

Do not flatten every observation into the project object.

---

### 6.2 Follow-ups become entities when they have lifecycle
If a follow-up has:
- an owner
- a status
- a due hint
- a linked project
- a completion state

then it should be treated as a trackable work object, not hidden inside project notes.

Example:

```yaml
follow_ups:
  - follow_up_id: "fu_mytox_pittman_001"
    linked_project_id: "proj_mytox_pittman_motor_replacement"
    follow_up_type: "customer_follow_up"
    subject: "Confirm quoted motor replacement"
    due_hint: "next week"
    owner_hint: "Malik"
    status: "open"
```

System-level implication:
- this may later map to Tasks
- or an Actions table
- not necessarily a separate database

---

### 6.3 New fields should not be promoted instantly
If a data point appears rarely, do not immediately elevate it into the core schema.

Rule:
- park it in `extraction_control.unmapped_observations`
- promote only after repeated use across multiple ingestions

This prevents schema sprawl.

---

## 7. Normalization stage

After extraction, a normalization pass should standardize:
- names
- casing
- obvious duplicates
- entity IDs
- common abbreviations
- date formats
- client/project separation

Examples:
- `Cross Link` → `Crosslink`
- `VFD install` → normalized project type hint
- contact name extraction separated from client entity

Normalization should be:
- conservative
- reversible
- logged when meaningful

Do not silently “clean” into false certainty.

---

## 8. Validation gate

Before write-through, each candidate entity must pass validation.

Validation categories:

### 8.1 Schema validation
- required fields present
- allowed shape
- ID rules valid
- no malformed arrays / nesting

### 8.2 Dedupe validation
- probable duplicate projects
- client name collision
- same scope with slightly varied titles

### 8.3 Ambiguity validation
- uncertain client linkage
- project vs follow-up confusion
- unclear ownership
- unclear actionability

### 8.4 Promotion validation
- is the field safe for canonical write?
- should it remain provisional?
- is human approval needed?

---

## 9. Write-through model

The pipeline should use a write-through pattern, not direct uncontrolled insertion.

Core sequence:

```text
Extract
→ Normalize
→ Validate
→ Prepare write candidate
→ Write to Node
→ Emit receipt
```

### Write-through rules
- do not write uncertain fields as canonical truth
- prefer create-or-merge over blind create
- log nontrivial merge decisions
- keep write behavior deterministic where possible

---

## 10. Notion / Node targets

Initial target surfaces in the Node:
- Projects database
- Clients database
- Tasks or Actions database
- Import notes / pointers if needed

### Node write principle
Only coordination-depth truth belongs in the Node.

That means:
- concise state
- linked relations
- summaries
- next actions
- pointers to deeper material

Do not dump raw extraction text into live operational records.

---

## 11. Suggested field mapping

### Project fields
| YAML source | Node target |
|---|---|
| `project_name` | Project Name |
| `client_name` / relation result | Client relation |
| `project_type_hint` | Project Type |
| `system_type_hint` | System Type |
| `status_hint` | Service Lane or Status |
| `scope_summary` | AI Scope Summary / Description |
| `source_refs` | Import Notes / source pointer |

### Client fields
| YAML source | Node target |
|---|---|
| `client_name` | Client Name |
| `contacts[]` | related contacts or notes |
| `source_refs` | Import Notes |

### Follow-up / task fields
| YAML source | Node target |
|---|---|
| `subject` | Task / Action title |
| `owner_hint` | Assignee |
| `due_hint` | Due Date hint / follow-up date |
| `linked_project_id` | Project relation |
| `status` | Task status |

---

## 12. Dedupe strategy

Minimum dedupe keys should consider:
- normalized client name
- normalized project title
- scope similarity
- recency
- linked contacts / assets when available

Possible decisions:
- create
- merge
- hold for review
- write as provisional

Do not silently merge low-confidence duplicates.

---

## 13. Receipts and audit

Every nontrivial pipeline run should produce a receipt.

Receipt should capture:
- run ID
- source ID
- counts of entities extracted
- counts written
- counts held
- counts provisional
- duplicate candidates
- unresolved fields
- destination surfaces
- timestamp

Example:

```yaml
write_receipt:
  run_id: "run_20260409_001"
  source_id: "src_notebook_001"
  extracted:
    projects: 8
    clients: 6
    follow_ups: 5
  written:
    projects: 7
    clients: 6
    follow_ups: 3
  provisional:
    follow_ups: 2
  held_for_review:
    projects: 1
  node_targets:
    - "Projects DB"
    - "Clients DB"
    - "Tasks DB"
```

---

## 14. Portable packet bridge

Canonical YAML is knowledge.

To make it executable across runtimes, wrap it in a portable packet.

Recommended high-level shape:

```yaml
portable_package:
  package_meta:
  doctrine_refs:
  schema_refs:
  payload:
  execution_intent:
  adapter_hints:
  validation:
```

### Meaning
- `payload` = neutral system data
- `execution_intent` = what should be done
- `adapter_hints` = runtime-specific guidance
- `doctrine_refs` = what rules apply
- `validation` = what success looks like

This is what makes the pipeline portable beyond a single model/runtime.

---

## 15. Failure modes to guard against

- project objects absorbing too much raw detail
- notes being written as truth instead of ambiguity
- client/project/follow-up confusion
- duplicate project creation
- schema drift from one-off fields
- model-specific assumptions leaking into the canonical schema
- writing uncertain fields directly to the Node
- treating intake as storage instead of controlled promotion

---

## 16. Recommended rollout order

### Phase A
Lock the YAML hierarchy and entity families.

### Phase B
Implement conservative normalization + dedupe.

### Phase C
Implement validation gate and receipts.

### Phase D
Implement write-through to Node with create-or-merge.

### Phase E
Wrap outputs in portable packets for multi-runtime execution.

---

## 17. Current design stance

This pipeline should remain:
- schema-first
- conservative
- auditable
- portable
- not model-shaped

The long-term win is not “extract more fields.”

The long-term win is:
> reliably converting messy human input into structured operational context without polluting the canonical layer.
