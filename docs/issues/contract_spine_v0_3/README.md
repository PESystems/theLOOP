# LOOP Contract Spine Issue Stack v0.3

This folder is the active issue stack for the LOOP Contract Spine.

## Naming lock
Use these terms consistently:
- LOOP Contract Spine = umbrella system
- Ingress Lane = source intake and normalization lane
- Distillation Lane = reduction into structured meaning
- Validation Layer = checks, conflicts, provisional/block rules
- Adapter Layer = surface-specific wrappers for Claude.ai, Floor, and Node
- Compile Boundary = promotion boundary into Node / canonical state
- Receipt Layer = audit trail and mutation record layer

## Recommended order
1. 01_lock_contract_spine_ontology.md
2. 02_establish_core_contract_spine_schema.md
3. 03_build_validation_layer_contract.md
4. 04_build_receipt_layer_contract.md
5. 05_define_adapter_layer_pattern.md
6. 06_define_claude_ai_ingress_lane.md
7. 07_define_floor_execution_lane.md
8. 08_enforce_node_compile_boundary.md
9. 09_migrate_existing_spine_lanes.md
10. 10_build_contract_spine_acceptance_pack.md

## Milestones
- M1: Core contract spine
- M2: Surface adapters and lane boundaries
- M3: Lane migration
- M4: Acceptance and rollout

## Status note
This folder supersedes the earlier YAML-family naming for active work. Use Contract Spine naming in all new implementation artifacts.

## Companion execution prompts
Token-efficient execution prompts for this stack live in:
- `leny/prompt_packs/contract_spine_prompt_index_v0.1.md`
- `leny/prompt_packs/contract_spine_prompt_pack_v0.1.md`

Use the issue files as the authority/spec layer.
Use the prompt pack as the execution companion.
