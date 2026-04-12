# [P1][area:migration][milestone:M3] Migrate Existing YAML Family Lanes

## Problem
The current family has multiple partially-complete lanes with overlapping concepts and uneven surface assumptions.

## Why it matters
Without a migration plan:
- old artifacts continue shaping behavior
- new contracts cannot be trusted
- duplicate concepts survive
- rollout stalls

## Research-backed recommendation
Migrate lane by lane using the new core contract and adapters. Start with the highest-leverage existing members:
- inbound ingestion
- YAML write-through
- extraction / claim lane
- naming / cohesion support layer

## Decisions to lock
- migration is staged, not big-bang
- old artifacts remain reference-only once replaced
- migration receipts are required
- lane owners must prove semantic equivalence or explicitly log change

## Implementation scope
- create migration map
- map old fields to new core contract
- identify deprecated fields
- define rollout order and rollback path

## Out of scope
- brand-new lane creation
- external automation rollout
- issue dashboarding

## Dependencies
- Issues 01–08

## Acceptance criteria
- migration map exists for each current lane
- deprecated fields are listed
- rollout order is documented
- rollback path is defined

## Failure modes / anti-goals
- silent field renames
- partial migrations with no receipts
- core contract changed to fit old lane slop
- no deprecation list

## Suggested Claude Code execution prompt
```md
Objective:
Produce the YAML family migration plan from current lanes to the v0.3 core contract + adapter model.

Requirements:
- inventory current lane artifacts
- map current concepts to ontology terms
- map current fields to new contract sections
- list deprecated fields
- define rollout order and rollback strategy

Constraints:
- do not rewrite the core contract to preserve bad legacy patterns
- preserve semantic intent where possible
- log explicit behavior changes where not possible

Deliverables:
- `docs/migration/yaml_family_migration_map.md`
- `docs/migration/deprecated_fields.md`
- `docs/migration/rollout_order.md`
- `docs/migration/rollback_strategy.md`

Proof of completion:
- show one completed field mapping table
- list deprecated fields
- show rollout order
```

## Suggested proof-of-completion artifacts
- migration map
- deprecated fields list
- rollout order
- rollback strategy
