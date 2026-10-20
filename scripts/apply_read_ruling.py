#!/usr/bin/env python3
"""Apply docs/EVIDENCE-READ-RULING-COMBINED-2026-10-20.json to data/report.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
RULING = ROOT / "docs" / "EVIDENCE-READ-RULING-COMBINED-2026-10-20.json"


def main() -> int:
    if not RULING.is_file():
        print("Missing ruling file", RULING, file=sys.stderr)
        return 1
    ruling = json.loads(RULING.read_text(encoding="utf-8"))
    team_ids = set(ruling["team_read_publication_ids"])
    expected = int(ruling["locked_team_read_total"])
    span = ruling.get("read_span_label") or "Gate③ 证据复核：权利要求级阅读"

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id")
            if pub in team_ids:
                fam["team_independent_read"] = True
                fam["actual_read_spans"] = [span]
            elif fam.get("discovery_source") == "independent_search":
                fam["team_independent_read"] = False
                fam["actual_read_spans"] = []

    sys.path.insert(0, str(ROOT / "scripts"))
    import merge_evidence_r2 as mer

    mer.recompute_counts(data)
    got = sum(
        1
        for mo in data.get("months") or []
        for fa in mo.get("families") or []
        if fa.get("team_independent_read")
    )
    data["counts"]["actually_read"] = got
    data["counts"]["events_reviewed"] = got

    if got != expected:
        print(f"ERROR team_read {got} != locked {expected}", file=sys.stderr)
        return 1

    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied team_read={got}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
