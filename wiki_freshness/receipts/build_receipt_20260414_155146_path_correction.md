# Wiki Build — Baseline Emission Receipt

| Field | Value |
|-------|-------|
| **run_id** | `wb-20260414-155146-beda29` |
| **kind** | build/path_correction |
| **timestamp** | 2026-04-14T15:51:46 |
| **script** | `wiki_build_baseline_emit.py` v0.1 |
| **wiki** | LOOP |
| **phase** | Phase I — doctrine-critical re-ingest batch 2026-04-14 |

## Source

- Old source path (row key): `LENY_WrkSps/architecture/THEO_System_Kernel_v1.0.md`
- New source path (if rewritten): `LENY_WrkSps/architecture/theo/THEO_System_Kernel_v1.0.md`
- Resolved file: `C:\Users\Malik\Documents\Claude\Projects\LENY_WrkSps\architecture\theo\THEO_System_Kernel_v1.0.md`
- SHA256 at this emission: `c6c7f31037b681afa04a22b6eded3dfd965d0f57eeeadcc801047bc4a9b9302c`
- Filesystem mtime at this emission: `2026-04-10T05:52:01`

## Wiki pages touched

- Theo.md

## Faithfulness note

Reviewed: Theo.md Sources section already points to theo/THEO_System_Kernel_v1.0.md. Source file content at actual path verified to match Theo.md content (role/scope/relationships). Stale Source Path in source_map was the only error; no wiki page mutation needed.

## Source_map diff

**before:**

```
| `LENY_WrkSps/architecture/THEO_System_Kernel_v1.0.md` | Theo.md | 2026-04-07 | — | — | legacy_no_baseline | Phase A. |
```

**after:**

```
| `LENY_WrkSps/architecture/theo/THEO_System_Kernel_v1.0.md` | Theo.md | 2026-04-14 | `c6c7f31037b681afa04a22b6eded3dfd965d0f57eeeadcc801047bc4a9b9302c` | 2026-04-10T05:52:01 | current | Phase A. Source path corrected + baseline emitted via Phase I — doctrine-critical re-ingest batch 2026-04-14. |
```

## What was NOT done

- Helper did not write wiki page content (that is the ingest action performed by the operator / wiki-build skill before this helper runs).
- Helper did not create any new source_map rows.
- Helper did not touch any file outside the named source_map and this receipt.