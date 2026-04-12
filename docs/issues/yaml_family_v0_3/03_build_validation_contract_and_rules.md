# [P0][area:validation][milestone:M1] Build the Validation Contract and Rule Set

## Problem
Validation exists as local behavior, not yet as a fully standardized contract. That makes dry runs, approvals, and write safety inconsistent across lanes.

## Why it matters
Validation is the boundary between structured candidate data and system truth. If it is not standardized:
- uncertain data leaks upward
- lanes interpret pass/fail differently
- receipts lose meaning
- canonical promotion becomes unsafe

## Research-backed recommendation
Build a family-wide validation contract that explicitly handles:
- schema pass/fail
- required checks
- conflicts
- uncertainty
- escalation thresholds
- pass/block/provisional outcomes

Validation should be deterministic where possible and explicit where human review is required.

## Decisions to lock
- raw input never writes directly to canonical state
- provisional and blocked are first-class outcomes
- conflicts are logged, not silently resolved
- validation states are shared across all lanes

## Implementation scope
- create `schemas/validation/validation_contract_v0_3.yaml`
- define validation outcomes and statuses
- create a rules doc for deterministic checks
- define escalation hooks for human review

## Out of scope
- receipt payload details
- surface adapter prompts
- Notion write logic

## Dependencies
- Issue 01
- Issue 02

## Acceptance criteria
- validation contract can represent pass, fail, provisional, blocked, conflict
- deterministic checks are documented
- escalation conditions are explicit
- at least two sample validation results exist

## Failure modes / anti-goals
- validation depends on hidden chat context
- conflict handling is vague
- “unknown” and “blocked” are treated as the same thing
- provisional path is omitted

## Suggested Claude Code execution prompt
```md
Objective:
Define the YAML family validation contract and validation rule set.

Requirements:
- model validation outcomes: pass, fail, provisional, blocked, conflict
- define required checks and escalation triggers
- document deterministic vs human-reviewed checks
- create two sample validation result payloads

Constraints:
- validation must be lane-neutral
- do not rely on chat-only judgments
- do not collapse uncertainty into pass/fail only
- keep rule names stable and readable

Deliverables:
- `schemas/validation/validation_contract_v0_3.yaml`
- `docs/validation/validation_rules.md`
- `schemas/examples/validation_result_pass.yaml`
- `schemas/examples/validation_result_provisional.yaml`

Proof of completion:
- list all validation states
- show escalation triggers
- validate both sample payloads
```

## Suggested proof-of-completion artifacts
- `schemas/validation/validation_contract_v0_3.yaml`
- `docs/validation/validation_rules.md`
- `schemas/examples/validation_result_pass.yaml`
- `schemas/examples/validation_result_provisional.yaml`
