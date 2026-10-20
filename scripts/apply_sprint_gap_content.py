#!/usr/bin/env python3
"""Apply docs/EPI-INCREMENTAL-SPRINT-gap-2026-10-20.json to data/report.json."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
GAP = ROOT / "docs" / "EPI-INCREMENTAL-SPRINT-gap-2026-10-20.json"


def family_sort_time(raw: dict) -> str:
    return raw.get("event_date") or ""


def build_card(entry: dict) -> dict:
    pub = entry["publication_id"]
    month = entry["month"]
    return {
        "publication_id": pub,
        "jurisdiction": "US",
        "event_type": entry["event_type"],
        "event_date": entry["event_date"],
        "application_id": entry.get("application_id"),
        "priority_date": None,
        "family_id": pub,
        "family_id_source": entry.get("discovery_source", "sprint_gap_tel"),
        "title_original": entry.get("title_original"),
        "title_zh": entry.get("title_zh"),
        "applicant_original": None,
        "applicant_normalized": entry.get("applicant_normalized"),
        "scope_status": entry["scope_status"],
        "technology_tags": entry.get("technology_tags") or [],
        "short_preview": entry.get("short_preview", ""),
        "technical_summary": entry.get("short_preview", ""),
        "claims_or_embodiment_basis": entry.get("claims_or_embodiment_basis", ""),
        "scope_reason": entry.get("scope_reason", ""),
        "source_urls": entry.get("source_urls") or [],
        "source_retrieved_at": None,
        "source_sha256": None,
        "actual_read_spans": [],
        "reviewer": None,
        "reviewed_at": None,
        "family_completion_status": "open",
        "figures": [],
        "change_history": [
            {
                "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "by": "sprint-gap-a",
                "action": "content_add",
                "detail": "EVIDENCE-SPRINT-A / EPI-INCREMENTAL-SPRINT-gap",
            }
        ],
        "family_events": [
            {
                "publication_id": pub,
                "event_date": entry["event_date"],
                "event_type": entry["event_type"],
                "source_url": (entry.get("source_urls") or [None])[0],
                "application_id": entry.get("application_id"),
            }
        ],
        "id": f"{month}-{pub}",
        "month": month,
        "import_tag": None,
        "discovery_source": entry.get("discovery_source", "sprint_gap_tel"),
        "team_independent_read": False,
        "event_note": entry.get("event_note"),
        "category": "EPI 工艺与设备" if entry["scope_status"] == "core" else "关联集成",
    }


def main() -> int:
    gap = json.loads(GAP.read_text(encoding="utf-8"))
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    added = 0
    for entry in gap.get("entries") or []:
        pub = entry["publication_id"]
        month = entry["month"]
        if month == "2025-09":
            print("SKIP forbidden month 2025-09:", pub, file=sys.stderr)
            return 1
        exists = any(
            f.get("publication_id") == pub
            for m in data.get("months") or []
            for f in m.get("families") or []
        )
        if exists:
            continue
        block = next((m for m in data.get("months") or [] if m.get("month") == month), None)
        if not block:
            print("Missing month block:", month, file=sys.stderr)
            return 1
        card = build_card(entry)
        block.setdefault("families", []).append(card)
        block["families"].sort(key=family_sort_time, reverse=True)
        added += 1

    note = "Sprint gap A（2026-10-20）：已纳入 TEL US20250311241A1（related）与 US12757648B2（core，2026-10 授权）。"
    notes = data.get("notes") or []
    if note not in notes:
        notes.append(note)
    data["notes"] = notes

    sys.path.insert(0, str(ROOT / "scripts"))
    from report_metrics import recompute_counts

    recompute_counts(data)
    related_n = sum(
        1
        for m in data.get("months") or []
        for f in m.get("families") or []
        if f.get("scope_status") == "related"
    )
    data["counts"]["related"] = related_n

    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"added": added, "counts": data["counts"]}, ensure_ascii=False))
    return 0 if added >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
