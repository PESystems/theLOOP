# [LENY] Plan — Issue 01: Lock the YAML Family Ontology

> Status: `draft` — awaiting THEO review
> Date: 2026-04-13

## What THEO asked for
A canonical ontology document that locks 9 terms across all YAML family lanes, with ingestion + distillation examples, anti-drift rules, and no runtime-specific language.

## My read of the issue
This is the foundation stone. Every downstream issue (02–10) references these terms. Getting this wrong means the whole contract stack drifts. Getting it *too big* means nobody reads it and the same drift happens by neglect.

The key tension: **minimal enough to be stable, complete enough that no lane needs to invent parallel terms.**

## Proposed approach

### 1. Term definitions (9 terms, ~1 paragraph each)
Each term gets three things:
- **Definition** — what it is, in one sentence
- **Role in pipeline** — where it appears and what it enables
- **What it is NOT** — the single most likely confusion to prevent

Terms: `source`, `artifact`, `entity`, `claim`, `uncertainty`, `validation_state`, `promotion_state`, `receipt`, `adapter`

### 2. Relationship map
A simple directed list showing which terms relate to which:
```
source → artifact → entity + claim
claim → uncertainty + validation_state
validation_state → promotion_state
promotion_state → receipt
adapter wraps [source, artifact, receipt] per surface
```
Not a full graph — just enough to show the pipeline spine.

### 3. Two worked examples

**Ingestion example** — a Google Doc flows in:
- source (the doc) → artifact (normalized YAML) → entities + claims extracted → uncertainty tagged → validation_state set → promotion_state = `staged` → receipt emitted

**Distillation example** — a wiki article gets refined:
- source (raw wiki draft) → artifact (structured claim set) → claims validated → uncertainty resolved or escalated → promotion_state = `promoted` → receipt emitted → Node receives compiled pointer

### 4. Forbidden drift patterns
A short list of patterns that indicate the ontology is being violated:
- A lane inventing a synonym for a canonical term
- An adapter redefining what a term means on its surface
- A schema embedding execution logic in an ontology field
- A receipt that uses different state names than `validation_state` / `promotion_state`

### 5. Decision log
Capture any term boundary calls that could go either way — so THEO can review the judgment calls rather than discovering them later.

## Deliverables
| File | Purpose |
|------|---------|
| `docs/ontology/yaml_family_ontology.md` | The locked ontology |
| `docs/ontology/ontology_decision_log.md` | Boundary calls and open questions |

## What I need from THEO before building
1. **Confirm the 9-term list is complete** — should `intent` be in the ontology or stay schema-only (Issue 02)?
2. **Confirm the relationship map approach** — directed list vs. table vs. diagram?
3. **Any terms THEO has already seen drift** — so I can address those head-on in the anti-drift section?

## Estimated scope
Small. This is a writing + structuring task, not code. One focused session to draft, then THEO reviews before it becomes canonical.

---
*— LENY, 2026-04-13*
