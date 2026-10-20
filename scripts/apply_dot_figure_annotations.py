#!/usr/bin/env python3
"""Merge Dot figure annotations into data/report.json by display/asset sha256 (no invent)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
EXTRACT = ROOT / "docs/dot-figure-annotations-extract.json"


def figure_sha(fig: dict) -> str | None:
    for k in (
        "asset_sha256",
        "source_display_sha256",
        "sha256",
        "source_original_sha256",
    ):
        v = fig.get(k)
        if v:
            return v
    return None


def main() -> int:
    if not EXTRACT.is_file():
        print("Missing", EXTRACT, file=sys.stderr)
        return 1
    extract = json.loads(EXTRACT.read_text(encoding="utf-8"))
    by_sha: dict[str, dict] = {}
    for row in extract.get("figures") or []:
        ann = row.get("annotations")
        if not ann:
            continue
        for k in ("display_sha256", "sha256"):
            s = row.get(k)
            if s:
                by_sha[s] = row
        s2 = ann.get("image_sha256")
        if s2:
            by_sha[s2] = row

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    matched = 0
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            for fig in fam.get("figures") or []:
                sha = figure_sha(fig)
                if not sha or sha not in by_sha:
                    continue
                src = by_sha[sha]
                ann = src.get("annotations")
                if not ann:
                    continue
                fig["annotations"] = ann
                fig["annotation_coverage_status"] = src.get("annotation_coverage_status") or "verified"
                matched += 1

    data.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "dot-figure-annotations",
            "action": "merge_dot_label_extract",
            "detail": f"Matched {matched} figures from dot-figure-annotations-extract.json by sha256.",
        }
    )
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("matched", matched)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
