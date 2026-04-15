# Wiki Freshness — Revalidation Handoff Contract v0.1

**Date:** 2026-04-14
**Status:** draft
**Purpose:** Specify exactly how the detector hands work off to downstream canonical paths without mutating wiki pages itself.

---

## Principle

Detection and mutation are separated. The wiki freshness verifier **detects**. Canonical wiki pages are **mutated only by** the `wiki-build` skill or the `wiki-write-through` skill, both invoked in authorized interactive sessions. The verifier's only write is a request artifact.

---

## Request artifact shape

One file per drifted row, written to `Git/theLOOP/wiki_freshness/queue/`.

Filename: `revalidation_{YYYYMMDD}_{HHMMSS}_{status}_{sanitized_source_path}.md`

Frontmatter:

```yaml
---
kind: revalidation_request
run_id: wf-20260414-084300-245c8f
raised_at: 2026-04-14T08:43:00
status: hash_changed | mtime_newer_than_ingest | missing_source
source_path: "..."
wiki_pages: "page_a.md, page_b.md"
action_required: review_and_reingest
canonical_write_authorized: false
---
```

Body: human-readable summary of what changed, stored vs current hash/mtime, and the required next actions (review source, re-ingest via `wiki-build`, or reject).

`canonical_write_authorized: false` is a **hard interlock**: any downstream tool reading the queue must refuse to rewrite wiki pages unless authorization is explicitly escalated in a separate step.

---

## Downstream paths

| Request status | Canonical downstream | Notes |
|---|---|---|
| `hash_changed` | `wiki-build` skill (interactive) | Re-ingest the affected source, update page(s), write new baseline into source_map |
| `mtime_newer_than_ingest` | `wiki-build` skill (interactive) | Same as above; stronger drift signal |
| `missing_source` | Manual triage first, then `wiki-build` if path recoverable | If truly gone, the source_map row is converted to `Baseline Status: source_missing` and the wiki page is re-evaluated for relevance |
| YASK claim-level drift | `wiki-write-through` skill | For rows whose wiki pages carry vendor claims that need re-evidenced against current PDFs / web sources |

The detector does not choose between these paths. The human operator reads the request and invokes the right skill.

---

## Request lifecycle

```
queue/revalidation_*.md           (detector writes)
        │
        ├── operator reviews
        │
        ├── invokes wiki-build → re-ingest happens
        │        │
        │        └── wiki-build writes new baseline to source_map AND
        │            moves the request file to queue/processed/
        │
        └── OR operator rejects → moves to queue/rejected/ with note
```

`queue/processed/` and `queue/rejected/` are convention-only subfolders; no script currently moves files between them. Movement is operator-driven. Future automation may add a close-out check, but not in v0.1.

---

## Non-goals

- The detector does not invoke `wiki-build`.
- The detector does not invoke `wiki-write-through`.
- The detector does not trigger scheduled tasks on other systems (Notion, Janitor, Relay).
- The detector does not create Node tracker entries.
- The detector does not modify queue request files after writing them.

---

## Why this separation matters

1. **Auditability.** Every canonical change still flows through `wiki-build` with its existing log + source-link + index contract. The detector leaves a breadcrumb; it does not bypass the build process.
2. **Authority boundary.** Silent rewriting of canonical pages from a scheduled sweep would violate the `anti-hallucination` and `execution-guardrails` principles. Even if the diff looks obvious, the detector has no claim-validation capability.
3. **Reversibility.** Staged requests are cheap to delete. A bad automated rewrite is expensive to back out. This design accepts a latency penalty (a request sits until a session picks it up) in exchange for safety.

---

## Baseline emission contract (for `wiki-build` follow-up patch)

When `wiki-build` performs an ingest, it must — after the page write succeeds — update the source_map row with:

```
Source SHA256 At Ingest = sha256(source_file_at_read_time)
Source MTime At Ingest  = iso8601(fs_mtime_at_read_time)
Baseline Status         = current
Last Ingested           = today
```

The hash and mtime are captured **at the moment the build reads the source**, not at the moment the row is written. If the source is re-read mid-build (for example, during a lint refactor), the emission uses the final read. This keeps the baseline aligned with what the wiki page actually reflects.

---

*Wiki Freshness — Revalidation Handoff Contract v0.1 — 2026-04-14*
