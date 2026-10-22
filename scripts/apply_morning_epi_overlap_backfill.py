#!/usr/bin/env python3
"""Apply morning 2026-10-22 EPI overlap_backfill (2× include_core) to data/report.json (idempotent)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
EPI = ROOT / "docs" / "EPI-INCREMENTAL-SPRINT-morning-2026-10-22-frozen.json"

STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

sys.path.insert(0, str(ROOT / "scripts"))
from report_metrics import recompute_counts  # noqa: E402


def pub_exists(data: dict, pub: str) -> bool:
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            if fam.get("publication_id") == pub:
                return True
    return False


def month_block(data: dict, ym: str) -> dict:
    for m in data.get("months") or []:
        if m.get("month") == ym:
            return m
    raise SystemExit(f"Missing month block: {ym}")


def family_sort_time(raw: dict) -> str:
    return raw.get("event_date") or ""


def build_epi_card(c: dict) -> dict:
    pub = c["publication_id"]
    month = c["month"]
    ev = (c.get("events") or [{}])[0]
    overlap = bool(c.get("overlap_backfill"))
    return {
        "publication_id": pub,
        "jurisdiction": c.get("jurisdiction", "US"),
        "event_type": c.get("event_type", "grant"),
        "event_date": c["event_date"],
        "application_id": c.get("application_id"),
        "priority_date": c.get("priority_date"),
        "family_id": c.get("family_id") or pub,
        "family_id_source": c.get("family_id_source", "independent_search"),
        "title_original": c.get("title_original"),
        "title_zh": c.get("title_zh"),
        "applicant_original": c.get("applicant_original"),
        "applicant_normalized": c.get("applicant_normalized"),
        "scope_status": "core",
        "technology_tags": c.get("technology_tags") or ["epi"],
        "short_preview": c.get("short_preview", ""),
        "technical_summary": c.get("technical_summary", c.get("short_preview", "")),
        "claims_or_embodiment_basis": c.get("claims_or_embodiment_basis", ""),
        "scope_reason": c.get("scope_reason", ""),
        "source_urls": c.get("source_urls") or [],
        "source_retrieved_at": c.get("source_retrieved_at"),
        "source_sha256": c.get("source_sha256"),
        "actual_read_spans": c.get("actual_read_spans") or [],
        "verification_level": c.get("verification_level"),
        "reviewer": None,
        "reviewed_at": None,
        "family_completion_status": c.get("family_completion_status", "open"),
        "figures": [],
        "change_history": [
            {
                "at": STAMP,
                "by": "morning-epi-overlap-backfill",
                "action": "include_core_overlap_backfill",
                "detail": "EPI-INCREMENTAL-SPRINT-morning-2026-10-22-frozen.json; EVIDENCE-MORNING-DIFF-2026-10-22 PASS_INCREMENTAL",
            }
        ],
        "family_events": [
            {
                "publication_id": ev.get("publication_id", pub),
                "event_date": ev.get("event_date", c["event_date"]),
                "event_type": ev.get("event_type", c.get("event_type", "grant")),
                "source_url": ev.get("source_url") or (c.get("source_urls") or [None])[0],
                "application_id": c.get("application_id"),
            }
        ],
        "id": f"{month}-{pub}",
        "month": month,
        "import_tag": None,
        "discovery_source": "independent_search",
        "independent_of_ref": True,
        "discovery_lane": "EPI",
        "overlap_backfill": overlap,
        "overlap_note": c.get("overlap_note"),
        "family_merge_note": None,
        "event_note": (
            "早间 overlap_backfill：2026-10-20 USPTO OG 授权补录（非 10-21..22 窗内新事件）。"
            if overlap
            else "早间 EPI 增量独立检索（informal）"
        ),
        "category": "EPI 工艺与设备",
        "team_independent_read": False,
        "read_disposition": "included_not_team_read",
        "read_status": "早间 EPI overlap_backfill 纳入；未计 team_read（锁 6）。",
    }


def figures_available(data: dict) -> int:
    n = 0
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            for fig in fam.get("figures") or []:
                if (fig.get("local_asset_path") or fig.get("path") or "").strip():
                    n += 1
    return n


def main() -> int:
    epi_doc = json.loads(EPI.read_text(encoding="utf-8"))
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    added: list[str] = []

    for c in epi_doc.get("candidates") or epi_doc.get("entries") or []:
        if c.get("disposition") != "include_core":
            continue
        pub = c["publication_id"]
        if pub_exists(data, pub):
            continue
        block = month_block(data, c["month"])
        block.setdefault("families", []).append(build_epi_card(c))
        block["families"].sort(key=family_sort_time, reverse=True)
        added.append(pub)

    note = (
        "早间增量（2026-10-22 PASS_INCREMENTAL）：EPI overlap_backfill "
        "US12770834B2（ASM PE epi CVD）、US12768074B2（AMAT epi chamber）；"
        "event_date=2026-10-20；research_through 保持 2026-10-20；team_read 锁 6。"
    )
    notes = data.get("notes") or []
    if note not in notes:
        notes.append(note)
    data["notes"] = notes

    if data.get("research_through") != "2026-10-20":
        print("WARN: research_through is", data.get("research_through"), "(expected 2026-10-20)")

    hist = data.get("change_history") or []
    hist.append(
        {
            "at": STAMP,
            "by": "morning-epi-overlap-backfill",
            "action": "morning_overlap_backfill_include_core",
            "detail": (
                f"Added: {', '.join(added) or '(none new)'}. "
                "research_through unchanged 2026-10-20; team_read locked 6; "
                "docs/EVIDENCE-MORNING-DIFF-2026-10-22.json"
            ),
        }
    )
    data["change_history"] = hist

    recompute_counts(data)
    locked_read = 6
    data["counts"]["actually_read"] = locked_read
    data["counts"]["events_reviewed"] = locked_read
    data["counts"]["figures"] = figures_available(data)

    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("added:", added)
    print("research_through:", data.get("research_through"))
    print("publication_events:", data["counts"]["publication_events"])
    print("unique_families:", data["counts"]["unique_families"])
    print("actually_read:", data["counts"]["actually_read"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
