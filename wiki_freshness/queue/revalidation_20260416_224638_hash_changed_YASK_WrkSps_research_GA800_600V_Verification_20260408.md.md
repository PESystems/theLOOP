---
kind: revalidation_request
run_id: wf-20260416-224638-50c45e
raised_at: 2026-04-16T22:46:38
status: hash_changed
source_path: "YASK_WrkSps/research/GA800_600V_Verification_20260408.md"
wiki_pages: "GA800 600V Field Reference.md (NEW), Yaskawa Drives.md (UPDATED)"
action_required: review_and_reingest
canonical_write_authorized: false
---

# Wiki Revalidation Request

**Source:** `YASK_WrkSps/research/GA800_600V_Verification_20260408.md`  
**Status:** `hash_changed`  
**Affected wiki pages:** GA800 600V Field Reference.md (NEW), Yaskawa Drives.md (UPDATED)  
**Detected in run:** `wf-20260416-224638-50c45e`

## What the detector saw

- Stored baseline SHA256: `f3a66512c160a268`
- Stored baseline mtime: `2026-04-10T05:52:02`
- Current SHA256: `f3a66512c160a2686b2365b6523e77083a81ccc74f806370ddc3e4943db9ccb3`
- Current mtime: `2026-04-10T05:52:02`
- Resolved path: `C:\Users\Malik\Documents\Claude\YASK_WrkSps\research\GA800_600V_Verification_20260408.md`

## Next action (human or authorized downstream agent)

1. Read the affected wiki page(s) and the current source file.
2. Decide: re-ingest (overwrite page section + update source_map baseline), fold changes into notes, or reject.
3. Invoke the `wiki-build` skill — NOT this detector — to perform the re-ingest.
4. On completion, the new baseline hash/mtime replace the stored values in `source_map.md` and this request file is moved to the `processed/` subfolder of the queue.

## Boundary

This detector MAY NOT rewrite wiki pages. Any canonical mutation must be performed by the existing wiki-build / wiki-write-through path, authorized in an interactive session.