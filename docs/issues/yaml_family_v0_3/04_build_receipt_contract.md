# [P0][area:receipts][milestone:M1] Build the Receipt Contract

## Problem
Receipts are already part of system behavior, but there is no single family-wide receipt contract for dry runs, writes, skips, blocks, failures, and approvals.

## Why it matters
Without a receipt contract:
- auditability weakens
- dry-run and live-write logs diverge
- multi-surface runs are hard to compare
- rollback and replay become unreliable

## Research-backed recommendation
Define a receipt schema that can represent:
- run identity
- contract identity
- action attempted
- surface
- mutability mode
- outcome
- blockers/conflicts
- emitted artifacts
- operator/human approval markers

Receipts should be light enough to emit everywhere, but structured enough to compare across surfaces.

## Decisions to lock
- every mutating or potentially mutating operation gets a receipt
- dry run is a first-class receipt mode
- blocked/skipped/failure outcomes are as important as success
- receipt semantics are stable across surfaces

## Implementation scope
- create `schemas/receipts/receipt_contract_v0_3.yaml`
- create docs for receipt semantics
- create sample receipts for dry_run, write_success, blocked_conflict, and failure

## Out of scope
- pipeline-specific storage locations
- adapter wrappers
- issue reporting dashboards

## Dependencies
- Issue 02
- Issue 03

## Acceptance criteria
- receipt schema supports all required outcomes
- sample receipts validate
- receipt includes enough fields for replay/audit
- receipt clearly differentiates dry run and live write

## Failure modes / anti-goals
- receipts become giant execution transcripts
- success-only receipts
- missing contract IDs or artifact references
- surface-specific meaning drift

## Suggested Claude Code execution prompt
```md
Objective:
Implement the YAML family receipt contract and sample receipt payloads.

Requirements:
- model dry_run, write_success, skipped, blocked_conflict, failure
- include contract_id, run_id, surface, mutability, outcome, emitted_artifacts, notes
- document receipt semantics in a maintainer note

Constraints:
- keep receipt lightweight but auditable
- no platform-specific logging assumptions in schema
- no giant prose payloads
- avoid duplicate fields where contract identity already covers them

Deliverables:
- `schemas/receipts/receipt_contract_v0_3.yaml`
- `docs/receipts/receipt_semantics.md`
- `schemas/examples/receipt_dry_run.yaml`
- `schemas/examples/receipt_write_success.yaml`
- `schemas/examples/receipt_blocked_conflict.yaml`
- `schemas/examples/receipt_failure.yaml`

Proof of completion:
- validate all sample receipts
- list supported outcomes
- show how dry run differs from write success
```

## Suggested proof-of-completion artifacts
- `schemas/receipts/receipt_contract_v0_3.yaml`
- `docs/receipts/receipt_semantics.md`
- sample receipt YAMLs
