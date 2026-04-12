# [P0][area:contract][milestone:M1] Establish the Core YAML Contract Schema

## Problem
Current YAML artifacts are still too lane-shaped and surface-shaped. The system needs one runtime-neutral core contract that all family members can implement without embedding execution assumptions.

## Why it matters
Without a core contract:
- every lane invents its own top-level structure
- Claude.ai and Floor lanes diverge
- migration becomes brittle
- validation and receipts cannot be standardized

## Research-backed recommendation
Create one core contract schema that covers:
- source
- artifact
- entities
- claims
- uncertainty
- intent
- validation
- promotion
- receipts

Keep the core schema portable and neutral. Surface-specific concerns must move to adapters.

## Decisions to lock
- core contract is the stable family spine
- adapters extend usage, not meaning
- intermediate representation is required before canonical promotion
- contract fields describe state and intent, not tool instructions

## Implementation scope
- create `schemas/core/loop_contract_v0_3.schema.yaml`
- create `schemas/examples/ingestion_example.yaml`
- create `schemas/examples/distillation_example.yaml`
- add schema notes explaining each top-level section
- add versioning rules

## Out of scope
- adapter files
- Notion mapping schema
- execution packet wrappers
- pipeline scripts

## Dependencies
- Issue 01

## Acceptance criteria
- schema validates one ingestion example and one distillation example
- no runtime-specific field is required in the core
- uncertainty, validation, and promotion are first-class sections
- schema versioning is explicit

## Failure modes / anti-goals
- core schema includes local paths or prompt wrappers
- top-level structure depends on a single lane
- claims and entities are mixed together without discipline
- schema becomes a dump of optional fields

## Suggested Claude Code execution prompt
```md
Objective:
Implement the LOOP core YAML contract schema v0.3.

Requirements:
- build a runtime-neutral schema file
- include sections for source, artifact, entities, claims, uncertainty, intent, validation, promotion, receipts
- produce one valid ingestion example
- produce one valid distillation example
- include a short schema notes file for maintainers

Constraints:
- no Claude-specific or Notion-specific fields in the core
- no local path assumptions
- no execution logic embedded in schema
- prefer strictness over convenience where field meaning would drift otherwise

Deliverables:
- `schemas/core/loop_contract_v0_3.schema.yaml`
- `schemas/examples/ingestion_example.yaml`
- `schemas/examples/distillation_example.yaml`
- `docs/schema/core_contract_notes.md`

Proof of completion:
- show the top-level keys
- validate both examples
- list any deferred field decisions
```

## Suggested proof-of-completion artifacts
- `schemas/core/loop_contract_v0_3.schema.yaml`
- `schemas/examples/ingestion_example.yaml`
- `schemas/examples/distillation_example.yaml`
- `docs/schema/core_contract_notes.md`
