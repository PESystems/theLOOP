# Wiki Build — Baseline Emission Receipt

| Field | Value |
|-------|-------|
| **run_id** | `wb-20260414-183447-63ece2` |
| **kind** | build/reingest |
| **timestamp** | 2026-04-14T18:34:47 |
| **script** | `wiki_build_baseline_emit.py` v0.1 |
| **wiki** | LOOP |
| **phase** | Phase J — LOOP_Architecture_v3.0 doctrine re-ingest |

## Source

- Old source path (row key): `LENY_WrkSps/architecture/LOOP_Architecture_v2_4.md`
- New source path (if rewritten): `LENY_WrkSps/architecture/LOOP_Architecture_v3.0.md`
- Resolved file: `C:\Users\Malik\Documents\Claude\Projects\LENY_WrkSps\architecture\LOOP_Architecture_v3.0.md`
- SHA256 at this emission: `0e1f3c4f9c72d94ac2b0f3e5117f1509d35cf97b68576e49735befd0615e4628`
- Filesystem mtime at this emission: `2026-04-11T17:33:18`

## Wiki pages touched

- LOOP Architecture.md
- Tier Model.md
- The Container.md
- Anti-Hallucination Rule.md
- Theo.md
- Lenny's Brain.md
- The Node.md
- The Floor.md
- Distill Don't Duplicate.md
- Task Classification.md

## Faithfulness note

Re-ingest of LOOP_Architecture v2_4 -> v3.0. 6 pages fully rewritten for material doctrinal changes (LOOP Architecture, Tier Model, The Container, Anti-Hallucination Rule, Theo, Lenny's Brain). 4 pages received lineage refresh only (The Node, The Floor, Distill Don't Duplicate, Task Classification) -- v3.0 preserves these concepts without material change; body faithful to v3.0. 4 pages deferred with justification (Skills, Wiki System, The Relay, Connectors & Links) -- not architecture-derived under v3.0 scope; belong to Skills_Layer / Topology v1.1 / operational wiki docs. No topology content merged. No silent v2.4 wording preservation where v3.0 changed it. No manual source_map edits.

## Source_map diff

**before:**

```
| `LENY_WrkSps/architecture/LOOP_Architecture_v2_4.md` | LOOP Architecture.md, Tier Model.md, The Node.md, The Floor.md, The Container.md, Distill Don't Duplicate.md, Task Classification.md, Anti-Hallucination Rule.md, Wiki System.md, Theo.md, Lenny's Brain.md, Skills.md, The Relay.md, Connectors & Links.md | 2026-04-07 | — | — | legacy_no_baseline | Phase D: Connectors & Links added. |
```

**after:**

```
| `LENY_WrkSps/architecture/LOOP_Architecture_v3.0.md` | LOOP Architecture.md, Tier Model.md, The Node.md, The Floor.md, The Container.md, Distill Don't Duplicate.md, Task Classification.md, Anti-Hallucination Rule.md, Wiki System.md, Theo.md, Lenny's Brain.md, Skills.md, The Relay.md, Connectors & Links.md | 2026-04-14 | `0e1f3c4f9c72d94ac2b0f3e5117f1509d35cf97b68576e49735befd0615e4628` | 2026-04-11T17:33:18 | current | Phase D: Connectors & Links added. Baseline emitted via Phase J — LOOP_Architecture_v3.0 doctrine re-ingest. |
```

## What was NOT done

- Helper did not write wiki page content (that is the ingest action performed by the operator / wiki-build skill before this helper runs).
- Helper did not create any new source_map rows.
- Helper did not touch any file outside the named source_map and this receipt.