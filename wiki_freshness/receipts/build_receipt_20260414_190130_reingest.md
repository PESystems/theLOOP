# Wiki Build — Baseline Emission Receipt

| Field | Value |
|-------|-------|
| **run_id** | `wb-20260414-190130-7f057a` |
| **kind** | build/reingest |
| **timestamp** | 2026-04-14T19:01:30 |
| **script** | `wiki_build_baseline_emit.py` v0.1 |
| **wiki** | LOOP |
| **phase** | Phase K — LOOP_Topology_v1.1 re-ingest |

## Source

- Old source path (row key): `LENY_WrkSps/architecture/LOOP_Topology_v1.0.md`
- New source path (if rewritten): `LENY_WrkSps/architecture/LOOP_Topology_v1.1.md`
- Resolved file: `C:\Users\Malik\Documents\Claude\Projects\LENY_WrkSps\architecture\LOOP_Topology_v1.1.md`
- SHA256 at this emission: `e6c4f5661fab421005cd9b565201712dfcd4c8b2832f01f7e845fe0021d7a8c7`
- Filesystem mtime at this emission: `2026-04-11T17:31:43`

## Wiki pages touched

- The Relay.md
- Connectors & Links.md
- Skills.md
- The Floor.md
- The Node.md
- Lenny's Brain.md
- Theo.md

## Faithfulness note

Re-ingest Topology v1.0 -> v1.1. Source path rewritten to v1.1. Changes applied per page: The Relay (rewritten — content now fully faithful to v1.1; v1.0 source only); Connectors & Links (rewritten — GDrive MCP added; v1.0 source only); Skills (rewritten — brain/floor/global partition added; index-discoverable layer framing from Architecture v3.0 added); The Floor (rewritten — machine names table, Relay complementarity note, sub-layer Cowork detail added; v1.1 added as second source alongside Architecture v3.0); The Node (Sketchpad->Inbox rename only; v1.1 added as second source); Lenny's Brain (Sketchpad->Inbox fix in Relationships; v1.0->v1.1 source citation); Theo (v1.0->v1.1 source citation only — content faithful). No architecture decisions re-opened. No Topology content merged into Phase J Architecture pages. No YASK content touched. No Janitor or detector changes.

## Source_map diff

**before:**

```
| `LENY_WrkSps/architecture/LOOP_Topology_v1.0.md` | Theo.md, Lenny's Brain.md, Skills.md, The Relay.md, Connectors & Links.md | 2026-04-07 | — | — | legacy_no_baseline | Phase A+D. |
```

**after:**

```
| `LENY_WrkSps/architecture/LOOP_Topology_v1.1.md` | Theo.md, Lenny's Brain.md, Skills.md, The Relay.md, Connectors & Links.md | 2026-04-14 | `e6c4f5661fab421005cd9b565201712dfcd4c8b2832f01f7e845fe0021d7a8c7` | 2026-04-11T17:31:43 | current | Phase A+D. Baseline emitted via Phase K — LOOP_Topology_v1.1 re-ingest. |
```

## What was NOT done

- Helper did not write wiki page content (that is the ingest action performed by the operator / wiki-build skill before this helper runs).
- Helper did not create any new source_map rows.
- Helper did not touch any file outside the named source_map and this receipt.