# [P0][area:node][milestone:M2] Enforce the Node Compile Boundary

## Problem
Node / Notion is at risk of becoming a mixed intake, execution, and canonical surface unless the compile boundary is made explicit in this contract family.

## Why it matters
The architecture depends on Node as compiled coordination truth. If raw or unstable payloads enter Node directly:
- canonical state becomes polluted
- review discipline collapses
- cross-surface trust weakens

## Research-backed recommendation
Define Node as a compile boundary. Only compiled, reviewed, or approved representations should land there. Raw intake, unstable IR, and heavy execution artifacts stay off Node.

## Decisions to lock
- Node is compiled state only
- raw source never lands as canonical Node truth
- Node copies are coordination-depth, not execution-depth
- Node receives pointers, summaries, approved records, and receipts where appropriate

## Implementation scope
- document Node compile boundary
- define allowed Node payload classes
- define forbidden Node payload classes
- define how receipts/pointers land in Node

## Out of scope
- exact Notion database mapping
- floor artifact storage
- ingestion adapter behavior

## Dependencies
- Issue 02
- Issue 03
- Issue 04
- Issue 05

## Acceptance criteria
- allowed and forbidden Node payload classes are explicit
- compile boundary is documented with examples
- at least one compile example exists
- no ambiguity remains about raw vs compiled Node state

## Failure modes / anti-goals
- Node used as raw intake dump
- direct YAML family writes with unresolved uncertainty
- execution-depth artifacts mirrored into Node
- receipts too detailed for coordination use

## Suggested Claude Code execution prompt
```md
Objective:
Define and document the Node compile boundary for the YAML family.

Requirements:
- define what may land in Node
- define what may not land in Node
- give examples of raw, staged, compiled representations
- show how receipts or pointers may appear in Node without duplicating floor artifacts

Constraints:
- keep Node at coordination depth
- do not turn Node into a file system
- do not duplicate execution-depth artifacts

Deliverables:
- `docs/node/node_compile_boundary.md`
- `schemas/examples/node_compiled_record_example.yaml`
- `schemas/examples/node_pointer_receipt_example.yaml`

Proof of completion:
- show allowed vs forbidden Node payload classes
- show one compiled record example
- show one pointer/receipt example
```

## Suggested proof-of-completion artifacts
- Node boundary doc
- compiled record example
- pointer/receipt example
