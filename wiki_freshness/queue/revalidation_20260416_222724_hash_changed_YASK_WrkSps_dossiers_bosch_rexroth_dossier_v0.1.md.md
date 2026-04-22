---
kind: revalidation_request
run_id: wf-20260416-222724-2f97fe
raised_at: 2026-04-16T22:27:24
status: hash_changed
source_path: "YASK_WrkSps/dossiers/bosch_rexroth_dossier_v0.1.md"
wiki_pages: "Bosch Rexroth Drives.md (NEW)"
action_required: review_and_reingest
canonical_write_authorized: false
---

# Wiki Revalidation Request

**Source:** `YASK_WrkSps/dossiers/bosch_rexroth_dossier_v0.1.md`  
**Status:** `hash_changed`  
**Affected wiki pages:** Bosch Rexroth Drives.md (NEW)  
**Detected in run:** `wf-20260416-222724-2f97fe`

## What the detector saw

- Stored baseline SHA256: `ceb2b312700d33e4`
- Stored baseline mtime: `2026-04-10T05:52:02`
- Current SHA256: `ceb2b312700d33e457e28488824ac37bb9577cc184d734b826d08681449b0a99`
- Current mtime: `2026-04-10T05:52:02`
- Resolved path: `C:\Users\Malik\Documents\Claude\YASK_WrkSps\dossiers\bosch_rexroth_dossier_v0.1.md`

## Next action (human or authorized downstream agent)

1. Read the affected wiki page(s) and the current source file.
2. Decide: re-ingest (overwrite page section + update source_map baseline), fold changes into notes, or reject.
3. Invoke the `wiki-build` skill — NOT this detector — to perform the re-ingest.
4. On completion, the new baseline hash/mtime replace the stored values in `source_map.md` and this request file is moved to the `processed/` subfolder of the queue.

## Boundary

This detector MAY NOT rewrite wiki pages. Any canonical mutation must be performed by the existing wiki-build / wiki-write-through path, authorized in an interactive session.