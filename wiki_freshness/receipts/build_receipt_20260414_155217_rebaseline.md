# Wiki Build — Baseline Emission Receipt

| Field | Value |
|-------|-------|
| **run_id** | `wb-20260414-155217-f1de23` |
| **kind** | build/rebaseline |
| **timestamp** | 2026-04-14T15:52:17 |
| **script** | `wiki_build_baseline_emit.py` v0.1 |
| **wiki** | LOOP |
| **phase** | Phase I — doctrine-critical re-ingest batch 2026-04-14 |

## Source

- Old source path (row key): `LENY_WrkSps/architecture/LOOP_Workspace_AI_Rules.md`
- New source path (if rewritten): `— unchanged —`
- Resolved file: `C:\Users\Malik\Documents\Claude\Projects\LENY_WrkSps\architecture\LOOP_Workspace_AI_Rules.md`
- SHA256 at this emission: `cf040f0b3227d67950c06e3f879d70aa78e95c46e65d212e59d303a85dbbd159`
- Filesystem mtime at this emission: `2026-04-10T05:52:01`

## Wiki pages touched

- Workspace AI Rules.md

## Faithfulness note

Source re-read 2026-04-14. Body content (Confirmation Rule, What This Workspace Is, governance clauses) matches the Workspace AI Rules.md wiki page. mtime 2026-04-10 is from tag_vault frontmatter pass — additive YAML tags only, no semantic content change. Wiki page remains faithful; establishing baseline.

## Source_map diff

**before:**

```
| `LENY_WrkSps/architecture/LOOP_Workspace_AI_Rules.md` | Workspace AI Rules.md | 2026-04-07 | — | — | legacy_no_baseline | Phase B. |
```

**after:**

```
| `LENY_WrkSps/architecture/LOOP_Workspace_AI_Rules.md` | Workspace AI Rules.md | 2026-04-14 | `cf040f0b3227d67950c06e3f879d70aa78e95c46e65d212e59d303a85dbbd159` | 2026-04-10T05:52:01 | current | Phase B. Rebaseline (faithfulness verified) via Phase I — doctrine-critical re-ingest batch 2026-04-14. |
```

## What was NOT done

- Helper did not write wiki page content (that is the ingest action performed by the operator / wiki-build skill before this helper runs).
- Helper did not create any new source_map rows.
- Helper did not touch any file outside the named source_map and this receipt.