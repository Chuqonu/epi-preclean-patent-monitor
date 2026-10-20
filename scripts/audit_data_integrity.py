#!/usr/bin/env python3
"""Lightweight integrity checks for data/report.json (exit 0 = OK)."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
RULING = ROOT / "docs" / "EVIDENCE-READ-RULING-COMBINED-2026-10-20.json"


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    errors: list[str] = []

    pubs: list[str] = []
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pubs.append(fam.get("publication_id") or "")
    dupes = [p for p, c in Counter(pubs).items() if c > 1]
    if dupes:
        errors.append(f"duplicate publication_id on month cards: {dupes}")

    if RULING.is_file():
        ruling = json.loads(RULING.read_text(encoding="utf-8"))
        locked = int(ruling["locked_team_read_total"])
        team_ids = set(ruling["team_read_publication_ids"])
        flagged = {
            fam.get("publication_id")
            for m in data.get("months") or []
            for fam in m.get("families") or []
            if fam.get("team_independent_read")
        }
        if flagged != team_ids:
            errors.append(f"team_independent_read set mismatch: {flagged} vs {team_ids}")
        ar = (data.get("counts") or {}).get("actually_read")
        if ar != locked:
            errors.append(f"counts.actually_read={ar} != locked {locked}")

    if errors:
        for e in errors:
            print("FAIL:", e, file=sys.stderr)
        return 1
    print("OK: dedupe + team_read ruling")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
