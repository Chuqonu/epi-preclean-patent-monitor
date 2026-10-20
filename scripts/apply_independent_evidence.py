#!/usr/bin/env python3
"""Apply EPI/Preclean evidence supplements + event attribution fixes to report.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
EPI = ROOT / "docs" / "EPI-EVIDENCE-SUPPLEMENT-2026-10-20.json"
PRE = ROOT / "docs" / "PRECLEAN-EVIDENCE-SUPPLEMENT-2026-10-20.json"

sys.path.insert(0, str(ROOT / "scripts"))
from report_metrics import recompute_counts, card_events_for_month  # noqa: E402


def trim_hybrid_preclean_cross_events(fam: dict) -> None:
    """WO/TW month cards must not list the sibling's primary publication (double-count fix)."""
    if fam.get("family_id") != "FAM-merge-hybrid-preclean":
        return
    pub = fam.get("publication_id")
    evs = fam.get("family_events") or []
    fam["family_events"] = [e for e in evs if e.get("publication_id") == pub]


def apply_epi_team_read(data: dict, supplement: dict) -> None:
    by_pub = {r["publication_id"]: r for r in supplement.get("team_read", [])}
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id")
            if pub not in by_pub:
                continue
            row = by_pub[pub]
            fam["team_independent_read"] = True
            fam["read_disposition"] = "team_read_claims_level"
            fam["source_urls"] = row.get("source_urls") or fam.get("source_urls")
            fam["source_retrieved_at"] = row.get("source_retrieved_at")
            fam["source_sha256"] = row.get("source_sha256")
            fam["actual_read_spans"] = row.get("actual_read_spans") or []
            fam["read_query"] = row.get("read_query")
            fam["reviewer"] = row.get("reviewer")
            fam["reviewed_at"] = row.get("reviewed_at")
            if row.get("read_evidence_note"):
                fam["read_evidence_note"] = row["read_evidence_note"]
            if row.get("official_source_url"):
                fam["official_source_url"] = row["official_source_url"]


def apply_preclean_not_read(data: dict, supplement: dict) -> None:
    by_pub = {r["publication_id"]: r for r in supplement.get("included_not_team_read", [])}
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id")
            if pub not in by_pub:
                if fam.get("discovery_source") == "independent_search":
                    fam.setdefault("team_independent_read", False)
                continue
            row = by_pub[pub]
            fam["team_independent_read"] = False
            fam["read_disposition"] = row.get("disposition", "included_not_team_read")
            fam["read_status"] = row.get("read_status")
            fam["actual_read_spans"] = []
            fam["reviewer"] = None
            fam["reviewed_at"] = None
            fam["source_sha256"] = None
            fam["source_retrieved_at"] = None
            if row.get("pending_reason"):
                fam["pending_reason"] = row["pending_reason"]


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    epi = json.loads(EPI.read_text(encoding="utf-8"))
    pre = json.loads(PRE.read_text(encoding="utf-8"))

    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            trim_hybrid_preclean_cross_events(fam)

    apply_epi_team_read(data, epi)
    apply_preclean_not_read(data, pre)

    counts = recompute_counts(data)
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("counts", counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
