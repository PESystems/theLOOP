---
kind: revalidation_request
run_id: wf-20260416-224745-2f7dc9
raised_at: 2026-04-16T22:47:45
status: hash_changed
source_path: "YASK_WrkSps/reports/rg_speed_hvac_decarbonization_ai_ceo_report_v0.1.md"
wiki_pages: "Ontario HVAC Market.md (UPDATED), HVAC Drive Applications.md (UPDATED), RG Speed Strategy.md (UPDATED)"
action_required: review_and_reingest
canonical_write_authorized: false
---

# Wiki Revalidation Request

**Source:** `YASK_WrkSps/reports/rg_speed_hvac_decarbonization_ai_ceo_report_v0.1.md`  
**Status:** `hash_changed`  
**Affected wiki pages:** Ontario HVAC Market.md (UPDATED), HVAC Drive Applications.md (UPDATED), RG Speed Strategy.md (UPDATED)  
**Detected in run:** `wf-20260416-224745-2f7dc9`

## What the detector saw

- Stored baseline SHA256: `b6458e958d0f71d4`
- Stored baseline mtime: `2026-04-10T05:52:02`
- Current SHA256: `b6458e958d0f71d4d267296e0a42765fa7ae8aeafaf1287df352a67667e8123e`
- Current mtime: `2026-04-10T05:52:02`
- Resolved path: `C:\Users\Malik\Documents\Claude\YASK_WrkSps\reports\rg_speed_hvac_decarbonization_ai_ceo_report_v0.1.md`

## Next action (human or authorized downstream agent)

1. Read the affected wiki page(s) and the current source file.
2. Decide: re-ingest (overwrite page section + update source_map baseline), fold changes into notes, or reject.
3. Invoke the `wiki-build` skill — NOT this detector — to perform the re-ingest.
4. On completion, the new baseline hash/mtime replace the stored values in `source_map.md` and this request file is moved to the `processed/` subfolder of the queue.

## Boundary

This detector MAY NOT rewrite wiki pages. Any canonical mutation must be performed by the existing wiki-build / wiki-write-through path, authorized in an interactive session.