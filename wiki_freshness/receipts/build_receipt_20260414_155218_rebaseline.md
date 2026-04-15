# Wiki Build — Baseline Emission Receipt

| Field | Value |
|-------|-------|
| **run_id** | `wb-20260414-155218-4bad70` |
| **kind** | build/rebaseline |
| **timestamp** | 2026-04-14T15:52:18 |
| **script** | `wiki_build_baseline_emit.py` v0.1 |
| **wiki** | LOOP |
| **phase** | Phase I — doctrine-critical re-ingest batch 2026-04-14 |

## Source

- Old source path (row key): `LENY_WrkSps/container/current/dispatch_operating_model_v0.2.md`
- New source path (if rewritten): `— unchanged —`
- Resolved file: `C:\Users\Malik\Documents\Claude\Projects\LENY_WrkSps\container\current\dispatch_operating_model_v0.2.md`
- SHA256 at this emission: `fe2bc7118659d423b63e63d981dd6bbce987bb82efd8914e868659ce3152f12c`
- Filesystem mtime at this emission: `2026-04-10T05:52:01`

## Wiki pages touched

- Dispatch.md

## Faithfulness note

Source re-read 2026-04-14. Dispatch operating model content (cross-project routing, gate model) still reflected in Dispatch.md. mtime 2026-04-10 from tag_vault frontmatter pass. No semantic drift. Note: Dispatch.md has a second source (LOOP_Dispatch_Protocol_v1.0.md) which is a separate row still legacy_no_baseline — baselined separately when that row is re-ingested.

## Source_map diff

**before:**

```
| `LENY_WrkSps/container/current/dispatch_operating_model_v0.2.md` | Dispatch.md | 2026-04-07 | — | — | legacy_no_baseline | Phase A. |
```

**after:**

```
| `LENY_WrkSps/container/current/dispatch_operating_model_v0.2.md` | Dispatch.md | 2026-04-14 | `fe2bc7118659d423b63e63d981dd6bbce987bb82efd8914e868659ce3152f12c` | 2026-04-10T05:52:01 | current | Phase A. Rebaseline (faithfulness verified) via Phase I — doctrine-critical re-ingest batch 2026-04-14. |
```

## What was NOT done

- Helper did not write wiki page content (that is the ingest action performed by the operator / wiki-build skill before this helper runs).
- Helper did not create any new source_map rows.
- Helper did not touch any file outside the named source_map and this receipt.