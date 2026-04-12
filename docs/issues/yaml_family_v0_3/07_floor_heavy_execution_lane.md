# [P1][area:floor][milestone:M2] Define the Floor Heavy-Execution Lane

## Problem
The Floor lane exists, but it is still mixed with assumptions that should move to the adapter layer and lacks a clean role boundary relative to Claude.ai.

## Why it matters
Floor execution is still necessary for:
- large documents
- heavy normalization
- batch processing
- scripts and repo work
- local file manipulation

If its role is not clearly bounded, the system will keep defaulting to Floor unnecessarily.

## Research-backed recommendation
Define the Floor lane as the secondary heavy-execution lane. Keep it optimized for scale, fidelity, and tools, not as the default path for all ingestion.

## Decisions to lock
- Floor is secondary, not primary
- Floor is the heavy-execution escalation path
- local preflight remains stronger here than in cloud lane
- Floor outputs still route through shared validation and receipts

## Implementation scope
- define floor lane responsibilities
- define when work escalates from cloud to floor
- define floor preflight rules
- define floor receipt output contract

## Out of scope
- cloud lane behavior
- Node compilation rules
- external automation

## Dependencies
- Issue 05
- Issue 06

## Acceptance criteria
- escalation rules from cloud to floor are explicit
- floor preflight is documented
- floor lane has a valid sample contract
- floor lane does not claim default ownership of all ingestion

## Failure modes / anti-goals
- floor remains the implicit default
- local file paths leak into core contract
- no clear escalation logic
- duplicate receipt semantics

## Suggested Claude Code execution prompt
```md
Objective:
Define the LOOP floor heavy-execution lane for the YAML family.

Requirements:
- define the role of Cowork / Claude Code in the family
- define escalation conditions from cloud lane to floor lane
- define floor preflight
- define floor receipt behavior
- provide one heavy-execution sample contract

Constraints:
- do not let floor assumptions leak into the core contract
- keep floor as secondary path
- preserve shared validation and receipt semantics

Deliverables:
- `docs/lanes/floor_heavy_execution_lane.md`
- `docs/lanes/floor_preflight.md`
- `schemas/examples/floor_heavy_execution_sample.yaml`

Proof of completion:
- list escalation triggers
- show floor preflight
- validate the sample contract
```

## Suggested proof-of-completion artifacts
- floor lane doc
- floor preflight doc
- heavy-execution sample contract
