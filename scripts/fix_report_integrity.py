#!/usr/bin/env python3
"""One-shot integrity repairs on data/report.json (WO/TW events, read metadata)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"

sys.path.insert(0, str(ROOT / "scripts"))
from report_metrics import recompute_counts  # noqa: E402


def trim_card_family_events(fam: dict) -> None:
    pub = fam.get("publication_id")
    month = fam.get("month") or (fam.get("event_date") or "")[:7]
    evs = fam.get("family_events") or []
    if not evs:
        return
    kept = [ev for ev in evs if ev.get("publication_id") == pub]
    if not kept:
        kept = [
            ev
            for ev in evs
            if (ev.get("event_date") or "")[:7] == month
        ]
    if kept:
        fam["family_events"] = kept


def scrub_read_metadata(data: dict) -> None:
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            if fam.get("discovery_source") != "independent_search":
                continue
            if fam.get("team_independent_read"):
                if not fam.get("source_sha256"):
                    fam["reviewer"] = None
                    fam["reviewed_at"] = None
                continue
            fam["team_independent_read"] = False
            fam["actual_read_spans"] = []
            fam["reviewer"] = None
            fam["reviewed_at"] = None
            fam.pop("source_sha256", None)


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    before = dict(data.get("counts") or {})

    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            trim_card_family_events(fam)

    scrub_read_metadata(data)

    sys.path.insert(0, str(ROOT / "scripts"))
    import apply_read_ruling as arr

    arr.main()

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    after = recompute_counts(data)
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("before", before)
    print("after", after)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
