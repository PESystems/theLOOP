# [P0][area:adapters][milestone:M2] Define the Surface Adapter Pattern

## Problem
The system knows it has multiple surfaces, but it does not yet have a formal adapter pattern separating core contract from surface-specific execution assumptions.

## Why it matters
Without adapters:
- core contract gets polluted by runtime-specific needs
- Claude.ai and Floor assumptions leak into one another
- migration becomes messy
- portability fails

## Research-backed recommendation
Build a formal adapter layer that wraps the core contract without redefining it. Start with:
- Claude.ai chat/cloud adapter
- Cowork / Claude Code floor adapter
- Node/Notion compile adapter

Adapters should specify how a surface consumes or emits the core contract, not what the contract means.

## Decisions to lock
- adapters are usage wrappers, not truth layers
- the core contract remains runtime-neutral
- each surface may add constraints, never redefine ontology
- read order and proof-of-completion may differ by adapter

## Implementation scope
- create adapter interface doc
- create per-surface adapter specs
- define allowed adapter fields and forbidden drift patterns

## Out of scope
- full implementation of every lane
- external connector automation
- issue dashboards

## Dependencies
- Issue 01
- Issue 02
- Issue 03
- Issue 04

## Acceptance criteria
- adapter pattern is documented
- at least three adapter specs exist
- forbidden drift patterns are listed
- adapter files do not redefine core schema terms

## Failure modes / anti-goals
- adapters become parallel schemas
- adapters inject ontology changes
- surface-specific fields migrate back into core
- adapter rules are too vague to implement

## Suggested Claude Code execution prompt
```md
Objective:
Define the LOOP surface adapter pattern for the YAML family.

Requirements:
- produce one adapter interface doc
- produce adapter specs for claude_chat_cloud, floor_execution, node_compile
- define allowed adapter concerns vs forbidden concerns
- include a short read-order rule per adapter

Constraints:
- no ontology changes in adapters
- no execution logic hidden in the core contract
- adapter concerns must stay surface-specific
- keep adapter specs compact and implementable

Deliverables:
- `docs/adapters/adapter_interface.md`
- `adapters/claude_chat_cloud_adapter_v0_3.md`
- `adapters/floor_execution_adapter_v0_3.md`
- `adapters/node_compile_adapter_v0_3.md`

Proof of completion:
- list the allowed adapter fields
- list forbidden drift patterns
- show one example of the same contract viewed through two adapters
```

## Suggested proof-of-completion artifacts
- adapter interface doc
- three adapter spec files
- one cross-adapter example
