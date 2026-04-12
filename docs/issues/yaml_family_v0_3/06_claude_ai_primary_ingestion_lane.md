# [P0][area:claude-cloud][milestone:M2] Refactor the Claude.ai Primary Ingestion Lane

## Problem
Current ingestion work is conceptually aware of Claude.ai constraints but still materially biased toward Floor-first assumptions.

## Why it matters
Claude.ai chat/cloud is expected to be the heavier-use human-facing ingestion surface. If the system remains floor-weighted:
- mobile/cloud usage stays second-class
- packet assumptions drift toward local files
- the primary human workflow remains awkward

## Research-backed recommendation
Make Claude.ai chat/cloud the default ingestion lane for small-to-medium document work. The lane should support:
- source fetch or pasted content
- normalization in-chat or cloud-side
- inline or cloud packetization
- dry-run staging
- receipt emission to shared state

## Decisions to lock
- Claude.ai is the default ingestion surface
- this lane must not require Floor presence for normal use
- cloud-side preflight is mandatory
- output is staged, not directly canonical

## Implementation scope
- define Claude.ai ingestion flow
- define cloud-side preflight
- define cloud packet mode
- define cloud receipt behavior

## Out of scope
- large-batch heavy processing
- local script execution
- final Node write-through implementation details

## Dependencies
- Issue 02
- Issue 03
- Issue 04
- Issue 05

## Acceptance criteria
- cloud lane can process a Google Doc without local path assumptions
- cloud preflight exists
- cloud receipt exists
- one pilot contract runs end-to-end in dry-run mode

## Failure modes / anti-goals
- lane still assumes working_directory or local folders
- cloud contract is just a weakened floor contract
- no receipt to shared state
- direct canonical writes from chat

## Suggested Claude Code execution prompt
```md
Objective:
Design the Claude.ai chat/cloud primary ingestion lane for the YAML family.

Requirements:
- define source fetch/paste modes
- define normalization mode
- define cloud packet mode
- define cloud preflight block
- define cloud receipt output
- produce one Google Doc ingestion dry-run example

Constraints:
- no local path assumptions
- no floor dependency for normal operation
- no direct canonical write
- keep this lane lightweight and human-usable

Deliverables:
- `docs/lanes/claude_ai_ingestion_lane.md`
- `schemas/examples/claude_ai_ingestion_dry_run.yaml`
- `docs/lanes/claude_ai_preflight.md`

Proof of completion:
- show the lane flow
- show the preflight checks
- validate the example dry-run contract
```

## Suggested proof-of-completion artifacts
- lane design doc
- cloud preflight doc
- dry-run example contract
