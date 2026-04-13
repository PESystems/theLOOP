# [P1][area:adapter][milestone:M2] Skill Sync Hook as Contract Spine Ingress Adapter

## Objective
Frame the skill sync hook correctly inside the LOOP Contract Spine and define the execution shape clearly enough for packetization and Claude Code implementation.

## Placement lock
This work belongs under the **LOOP Contract Spine** umbrella.

Primary placement:
- **Ingress Lane** — detect and validate incoming `*-SKILL.md` bundles
- **Adapter Layer** — translate validated bundles into safe local install actions
- **Floor execution lane** — Claude Code builds and maintains the local hook/runtime on the Floor
- **Receipt Layer** — YAML machine receipts plus Markdown run summaries

Intentionally thin / bypassed in v1:
- **Distillation Lane** — not primary here because `SKILL.md` is already a structured behavioral artifact
- **Node compile boundary** — no default Node write in v1

## Why this matters
Without this framing, the hook can be misread as:
- a generic file move
- a full dual-lane pipeline
- a Node-facing promotion flow

That would overbuild v1 and blur the actual role of the hook.

## Locked decisions
- Sidecar manifest is the routing signal
- Partitioned skills tree remains canonical target
- No silent overwrite
- Quarantine on conflict
- Leave Drive source untouched
- Claude Code is the execution surface for the build
- Scheduled local sweep is the v1 runtime shape

## Dependencies
- Google Drive for Desktop installed and configured on the Floor machine
- `C:\Users\Malik\Documents\Claude\Projects\LENY_WrkSps\skills\` canonical tree already exists
- Windows Task Scheduler available on the execution machine

## Required config values before execution
1. local synced Drive intake folder path
2. local quarantine folder path
3. local receipts folder path
4. scheduled sweep interval
5. conflict normalization/hash rule

## Next action
LENY converts the skill sync spec into a **Contract Spine execution packet** for Claude Code.

The packet must preserve this shape:
**Ingress Lane + Adapter Layer + Floor execution + Receipt Layer**.
