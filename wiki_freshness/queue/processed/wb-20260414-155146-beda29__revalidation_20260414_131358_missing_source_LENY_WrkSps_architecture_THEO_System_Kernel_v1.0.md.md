---
kind: revalidation_request
run_id: wf-20260414-131358-94e6ce
raised_at: 2026-04-14T13:13:58
status: missing_source
source_path: "LENY_WrkSps/architecture/THEO_System_Kernel_v1.0.md"
wiki_pages: "Theo.md"
action_required: review_and_reingest
canonical_write_authorized: false
---

# Wiki Revalidation Request

**Source:** `LENY_WrkSps/architecture/THEO_System_Kernel_v1.0.md`  
**Status:** `missing_source`  
**Affected wiki pages:** Theo.md  
**Detected in run:** `wf-20260414-131358-94e6ce`

## What the detector saw

- Stored baseline SHA256: `—`
- Stored baseline mtime: `—`
- Current SHA256: `None`
- Current mtime: `None`
- Resolved path: `None`

## Next action (human or authorized downstream agent)

1. Read the affected wiki page(s) and the current source file.
2. Decide: re-ingest (overwrite page section + update source_map baseline), fold changes into notes, or reject.
3. Invoke the `wiki-build` skill — NOT this detector — to perform the re-ingest.
4. On completion, the new baseline hash/mtime replace the stored values in `source_map.md` and this request file is moved to the `processed/` subfolder of the queue.

## Boundary

This detector MAY NOT rewrite wiki pages. Any canonical mutation must be performed by the existing wiki-build / wiki-write-through path, authorized in an interactive session.