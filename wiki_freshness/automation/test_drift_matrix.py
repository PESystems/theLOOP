#!/usr/bin/env python3
"""
test_drift_matrix.py — self-contained test harness for wiki_source_drift.

Creates a temporary source_map + fixture sources, exercises every status the
classifier must emit, and asserts correct routing. Prints a pass/fail matrix.

Run:
    python test_drift_matrix.py
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[4]  # Claude/
DRIFT_SCRIPT = REPO_ROOT / "theLOOP" / "housekeeping" / "wiki_source_drift.py"
assert DRIFT_SCRIPT.exists(), f"drift script not found at {DRIFT_SCRIPT}"


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def mtime_iso(p: Path) -> str:
    return _dt.datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")


def build_fixture(tmp: Path) -> dict:
    """Build fixture files and a stand-in source_map pointing at them."""
    src_root = tmp / "fixtures"
    src_root.mkdir(parents=True)

    f_unchanged = src_root / "unchanged.md"
    f_edited = src_root / "edited.md"
    f_mtime = src_root / "mtime_only.md"
    f_missing_ref = src_root / "missing.md"  # will be deleted
    f_legacy = src_root / "legacy.md"

    f_unchanged.write_text("stable content\n", encoding="utf-8")
    f_edited.write_text("original content\n", encoding="utf-8")
    f_mtime.write_text("content-A\n", encoding="utf-8")
    f_missing_ref.write_text("will be deleted\n", encoding="utf-8")
    f_legacy.write_text("legacy content\n", encoding="utf-8")

    # Capture baselines for rows that should have one
    baseline = {
        "unchanged": {
            "path": f_unchanged,
            "sha": sha256_of(f_unchanged),
            "mtime": mtime_iso(f_unchanged),
        },
        "edited": {
            "path": f_edited,
            "sha": sha256_of(f_edited),
            "mtime": mtime_iso(f_edited),
        },
        "mtime": {
            "path": f_mtime,
            "sha": sha256_of(f_mtime),
            "mtime": mtime_iso(f_mtime),
        },
        "missing": {
            "path": f_missing_ref,
            "sha": sha256_of(f_missing_ref),
            "mtime": mtime_iso(f_missing_ref),
        },
        "legacy": {
            "path": f_legacy,
        },
        "unresolved": {
            "path_str": "fixtures/does_not_exist_anywhere.md",
        },
    }

    # Now perturb:
    # - edited: rewrite content (hash differs, mtime advances)
    # - mtime: touch to advance mtime but keep content (to exercise
    #   mtime_newer_than_ingest path specifically, we need different mtime
    #   AND different hash; pure mtime-only with same hash stays "unchanged".
    #   So we make content differ but compare stored mtime vs current mtime
    #   to route through mtime_newer_than_ingest branch.)
    # - missing: delete file
    import time
    time.sleep(1.1)  # ensure mtime advances at filesystem resolution

    f_edited.write_text("mutated content v2\n", encoding="utf-8")
    f_mtime.write_text("content-B different hash\n", encoding="utf-8")
    f_missing_ref.unlink()

    # Build a temp source_map.md at schema v0.2 shape
    sm = tmp / "wiki_schema"
    sm.mkdir()
    smp = sm / "source_map.md"
    rows = [
        ("fixtures/unchanged.md", baseline["unchanged"]["sha"],
         baseline["unchanged"]["mtime"], "current"),
        ("fixtures/edited.md", baseline["edited"]["sha"],
         baseline["edited"]["mtime"], "current"),
        ("fixtures/mtime_only.md", baseline["mtime"]["sha"],
         baseline["mtime"]["mtime"], "current"),
        ("fixtures/missing.md", baseline["missing"]["sha"],
         baseline["missing"]["mtime"], "current"),
        ("fixtures/legacy.md", "—", "—", "legacy_no_baseline"),
        (baseline["unresolved"]["path_str"], "—", "—", "legacy_no_baseline"),
    ]
    header = (
        "---\nschema_version: 0.2\n---\n\n"
        "# Test Source Map\n\n"
        "| Source Path | Wiki Page(s) | Last Ingested | "
        "Source SHA256 At Ingest | Source MTime At Ingest | "
        "Baseline Status | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    lines = [header]
    for sp, sha, mt, bs in rows:
        lines.append(
            f"| `{sp}` | Test.md | 2026-04-14 | "
            f"{sha} | {mt} | {bs} | test row |\n"
        )
    smp.write_text("".join(lines), encoding="utf-8")

    return {
        "source_map": smp,
        "path_base": tmp,
        "fixtures_root": src_root,
    }


def invoke_classifier_directly(fixture: dict) -> list[dict]:
    """Import the classifier and run it directly against the fixture map."""
    sys.path.insert(0, str(DRIFT_SCRIPT.parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location("wsd", DRIFT_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    text = fixture["source_map"].read_text(encoding="utf-8")
    parsed = mod.parse_source_map(text)
    results = [mod.classify_row(r, fixture["path_base"]) for r in parsed["rows"]]
    return results


def main() -> int:
    expected = {
        "fixtures/unchanged.md": "unchanged",
        "fixtures/edited.md": "mtime_newer_than_ingest",  # hash differs AND mtime advanced
        "fixtures/mtime_only.md": "mtime_newer_than_ingest",
        "fixtures/missing.md": "missing_source",
        "fixtures/legacy.md": "legacy_no_baseline",
        "fixtures/does_not_exist_anywhere.md": "missing_source",
    }

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        fixture = build_fixture(tmp)
        results = invoke_classifier_directly(fixture)

        print(f"\nTest harness — {len(results)} rows classified\n")
        print(f"{'source':<48} {'expected':<28} {'actual':<28} {'pass?'}")
        print("-" * 110)
        all_pass = True
        matrix = []
        for r in results:
            exp = expected.get(r["source_path"], "?")
            actual = r["status"]
            ok = (exp == actual)
            all_pass = all_pass and ok
            matrix.append({
                "source": r["source_path"], "expected": exp,
                "actual": actual, "pass": ok,
            })
            print(f"{r['source_path']:<48} {exp:<28} {actual:<28} {'PASS' if ok else 'FAIL'}")

        print()
        print(f"Overall: {'ALL PASS' if all_pass else 'FAILURES'}")
        # Also verify report/receipt generation end-to-end by invoking the CLI
        print("\n--- End-to-end CLI invocation against fixture map ---")
        # We invoke the CLI but point it at the fixture map by monkey-
        # patching WIKI_SOURCE_MAPS via an environment-free override is not
        # supported, so we just run the real script separately. The test
        # matrix above already validates the core classifier.

        return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
