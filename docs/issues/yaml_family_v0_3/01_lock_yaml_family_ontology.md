# [P0][area:ontology][milestone:M1] Lock the YAML Family Ontology

## Problem
The YAML family currently behaves like related pipelines without a formally locked shared ontology. Terms such as source, artifact, claim, validation state, promotion state, and receipt appear across ingestion, extraction, distillation, and write-through work, but their meanings are not yet fixed at the family level.

## Why it matters
Without a locked ontology:
- schemas drift by lane
- adapters silently redefine concepts
- migration work becomes interpretive instead of mechanical
- Claude.ai and Floor surfaces will develop incompatible assumptions

## Research-backed recommendation
Define the smallest ontology that all lanes must share:
- source
- artifact
- entity
- claim
- uncertainty
- validation_state
- promotion_state
- receipt
- adapter

Make this family-wide and runtime-neutral. Lane-specific language must map back to these canonical terms instead of inventing parallel concepts.

## Decisions to lock
- The YAML family is a contract-layer family, not a set of unrelated schemas.
- Shared ontology is mandatory across all lanes.
- YAML terms must describe state, not execution behavior.
- Node / Notion receives compiled state, not raw ontology-breaking payloads.

## Implementation scope
- create `docs/ontology/yaml_family_ontology.md`
- define each term in one paragraph max
- add allowed relationships between terms
- add anti-terms / forbidden synonyms where useful
- add examples for ingestion and distillation lanes

## Out of scope
- full schema field list
- adapter-specific rules
- Notion property mapping
- execution prompts

## Dependencies
- none

## Acceptance criteria
- every family term has one canonical definition
- ingestion and distillation examples use the same term meanings
- no lane-specific term is required to understand the ontology
- downstream issues can reference ontology terms without redefining them

## Failure modes / anti-goals
- ontology becomes a giant glossary
- terms are defined by current implementation details
- concepts overlap or duplicate each other
- ontology includes tool-specific language

## Suggested Claude Code execution prompt
```md
Objective:
Create the canonical YAML family ontology document for LOOP.

Authority:
Use the current YAML family issue pack as the task contract.
Prefer minimal, stable definitions over implementation-heavy prose.

Requirements:
- define: source, artifact, entity, claim, uncertainty, validation_state, promotion_state, receipt, adapter
- each term gets:
  - definition
  - role in pipeline
  - what it is not
- include one ingestion example and one distillation example
- add a short section: forbidden drift patterns

Constraints:
- runtime-neutral only
- no Notion-specific or Claude-specific assumptions
- no schema field explosion
- no execution logic

Deliverable:
`docs/ontology/yaml_family_ontology.md`

Proof of completion:
- list the final ontology terms
- show the ingestion example
- show the distillation example
- state any unresolved ambiguity explicitly
```

## Suggested proof-of-completion artifacts
- `docs/ontology/yaml_family_ontology.md`
- `docs/ontology/ontology_decision_log.md`
