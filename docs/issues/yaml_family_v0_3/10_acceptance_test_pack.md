# [P0][area:testing][milestone:M4] Build the Acceptance Test Pack

## Problem
The YAML family refactor will look coherent on paper unless it is proved end-to-end across both primary and secondary surfaces.

## Why it matters
Without acceptance tests:
- adapter drift goes undetected
- validation/receipt contracts remain theoretical
- cloud-vs-floor behavior will diverge silently

## Research-backed recommendation
Build an acceptance test pack that proves:
- ontology coherence
- core schema validity
- validation contract behavior
- receipt behavior
- cloud lane dry run
- floor lane heavy-execution example
- Node compile boundary behavior
- migration compatibility

## Decisions to lock
- acceptance tests are required before calling v0.3 operational
- both cloud and floor lanes must be tested
- dry run and live-write semantics must be distinguishable
- migration compatibility must be demonstrated

## Implementation scope
- test matrix
- sample contracts
- validation assertions
- receipt assertions
- compile-boundary assertions

## Out of scope
- CI implementation details beyond immediate test artifacts
- full production automation rollout

## Dependencies
- Issues 01–09

## Acceptance criteria
- test matrix exists
- all required sample contracts validate
- cloud and floor lane tests pass
- Node compile boundary test exists
- migration compatibility test exists

## Failure modes / anti-goals
- tests only cover one surface
- tests assert shape but not meaning
- no blocked/provisional cases
- migration not tested

## Suggested Claude Code execution prompt
```md
Objective:
Build the acceptance test pack for the LOOP YAML family v0.3 contract system.

Requirements:
- create a test matrix covering ontology, schema, validation, receipts, cloud lane, floor lane, node compile boundary, and migration compatibility
- create sample contracts and expected outcomes
- include blocked/provisional/conflict cases
- document what must pass before v0.3 is called operational

Constraints:
- test both surfaces
- test meaning, not just syntax
- keep the pack execution-oriented and reviewable

Deliverables:
- `tests/yaml_family_test_matrix.md`
- `tests/contracts/*.yaml`
- `tests/expected_outcomes.md`

Proof of completion:
- show the full test matrix
- list all sample contracts
- state pass/fail expectations clearly
```

## Suggested proof-of-completion artifacts
- test matrix
- sample contracts
- expected outcomes doc
