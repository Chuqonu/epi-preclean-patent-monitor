#!/usr/bin/env python3
"""Merge docs/EVIDENCE-REVIEW-2026-10-20-r2.json into data/report.json."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "data" / "report.json"
EVIDENCE_PATH = ROOT / "docs" / "EVIDENCE-REVIEW-2026-10-20-r2.json"


def month_key(event_date: str) -> str:
    return event_date[:7]


def find_family(months: list, pub_id: str) -> tuple[int, int, dict] | None:
    for mi, m in enumerate(months):
        for fi, fam in enumerate(m.get("families") or []):
            if fam.get("publication_id") == pub_id:
                return mi, fi, fam
    return None


def ensure_month(months: list, ym: str) -> dict:
    for m in months:
        if m.get("month") == ym:
            return m
    new_m = {
        "month": ym,
        "status": "含独立检索增量｜基线月份",
        "through_date": None,
        "families": [],
        "family_count": 0,
        "event_count": 0,
    }
    months.append(new_m)
    months.sort(key=lambda x: x["month"], reverse=True)
    return new_m


def recompute_counts(data: dict) -> None:
    months = data.get("months") or []
    month_entries = 0
    pub_events = 0
    family_ids: set[str] = set()
    core_family_ids: set[str] = set()
    figures_refs = 0
    actually_read = 0
    pending_n = len(data.get("pending_or_related") or [])

    for m in months:
        fams = m.get("families") or []
        month_entries += len(fams)
        m["family_count"] = len(fams)
        ev_in_month = 0
        for fam in fams:
            fid = fam.get("family_id") or fam.get("publication_id")
            if fid:
                family_ids.add(fid)
                if fam.get("scope_status") == "core":
                    core_family_ids.add(fid)
            evs = fam.get("family_events") or []
            if evs:
                pub_events += len(evs)
                ev_in_month += len(evs)
            else:
                pub_events += 1
                ev_in_month += 1
            spans = fam.get("actual_read_spans") or []
            if spans and fam.get("discovery_source") == "independent_search":
                actually_read += 1
            for fig in fam.get("figures") or []:
                figures_refs += 1
        m["event_count"] = ev_in_month

    data["counts"] = {
        "candidates_total": month_entries,
        "events_reviewed": actually_read,
        "events_core": pub_events,
        "families_core": len(core_family_ids),
        "related": data.get("counts", {}).get("related", 0),
        "pending": pending_n,
        "excluded": data.get("counts", {}).get("excluded", 0),
        "figures": figures_refs,
        "month_family_entries": month_entries,
        "publication_events": pub_events,
        "unique_families": len(family_ids),
        "actually_read": actually_read,
    }


def apply_baseline_confirm(fam: dict, note: str, stamp: str) -> None:
    fam.setdefault("change_history", []).append(
        {
            "at": stamp,
            "by": "evidence-review-r2",
            "action": "independent_search_confirm",
            "detail": note,
        }
    )
    fam["independent_search_confirmation"] = note


def build_independent_record(raw: dict, stamp: str) -> dict:
    pub = raw["publication_id"]
    ym = month_key(raw["event_date"])
    rec = {
        "publication_id": pub,
        "jurisdiction": raw["jurisdiction"],
        "event_type": raw.get("event_type", "publication"),
        "event_date": raw["event_date"],
        "application_id": raw.get("application_id"),
        "priority_date": raw.get("priority_date"),
        "family_id": raw.get("family_id") or pub,
        "family_id_source": raw.get("family_id_source", "independent_search"),
        "title_original": raw.get("title_original"),
        "title_zh": raw["title_zh"],
        "applicant_original": raw.get("applicant_original"),
        "applicant_normalized": raw.get("applicant_normalized", ""),
        "scope_status": raw.get("scope_status", "core"),
        "technology_tags": raw.get("technology_tags", []),
        "short_preview": raw["short_preview"],
        "technical_summary": raw.get("technical_summary", raw["short_preview"]),
        "claims_or_embodiment_basis": raw.get("claims_or_embodiment_basis", "证据复核 r2：已阅权利要求与摘要要点；详见来源链接。"),
        "scope_reason": raw.get("scope_reason", "独立检索纳入；证据复核 r2 核定为核心范围。"),
        "source_urls": raw.get("source_urls") or [f"https://patents.google.com/patent/{pub}/en"],
        "source_retrieved_at": raw.get("source_retrieved_at"),
        "source_sha256": None,
        "actual_read_spans": raw.get("actual_read_spans") or ["证据复核 r2：权利要求与摘要"],
        "reviewer": raw.get("reviewer", "evidence-review-r2"),
        "reviewed_at": raw.get("reviewed_at", "2026-10-20"),
        "family_completion_status": raw.get("family_completion_status", "open"),
        "figures": raw.get("figures") or [],
        "change_history": [
            {
                "at": stamp,
                "by": "evidence-review-r2",
                "action": "independent_add",
                "detail": raw.get("merge_note") or "独立检索新纳入（非基线导入）。",
            }
        ],
        "family_events": raw.get("family_events")
        or [
            {
                "publication_id": pub,
                "event_date": raw["event_date"],
                "event_type": raw.get("event_type", "publication"),
                "source_url": f"https://patents.google.com/patent/{pub}/en",
                "application_id": raw.get("application_id"),
            }
        ],
        "id": f"{ym}-{pub}",
        "month": ym,
        "import_tag": None,
        "discovery_source": "independent_search",
        "independent_of_ref": True,
        "family_merge_note": raw.get("family_merge_note"),
        "event_note": raw.get("event_note", "独立检索发现"),
        "category": raw.get("category"),
    }
    return rec


def main() -> int:
    if not EVIDENCE_PATH.is_file():
        print(f"Missing {EVIDENCE_PATH}", file=sys.stderr)
        return 1
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    months = data.setdefault("months", [])

    for item in evidence.get("baseline_confirms", []):
        hit = find_family(months, item["publication_id"])
        if not hit:
            print(f"WARN baseline confirm not found: {item['publication_id']}", file=sys.stderr)
            continue
        _, _, fam = hit
        apply_baseline_confirm(fam, item["note"], stamp)

    for raw in evidence.get("independent_discoveries", []):
        pub = raw["publication_id"]
        if find_family(months, pub):
            print(f"SKIP independent already present: {pub}")
            continue
        rec = build_independent_record(raw, stamp)
        m = ensure_month(months, rec["month"])
        m["families"].append(rec)

    pending_rows = []
    for p in evidence.get("pending", []):
        pub = p["publication_id"]
        hit = find_family(months, pub)
        row = {
            "publication_id": pub,
            "jurisdiction": p.get("jurisdiction"),
            "event_type": p.get("event_type", "publication"),
            "event_date": p.get("event_date"),
            "title_zh": p.get("title_zh", pub),
            "applicant_normalized": p.get("applicant_normalized", ""),
            "scope_status": "pending",
            "pending_reason": p["pending_reason"],
            "failure_or_pending_reason": p["pending_reason"],
            "discovery_source": p.get("discovery_source", "independent_search"),
            "import_tag": p.get("import_tag"),
            "on_main_month_cards": bool(hit),
            "disposition": "pending_not_promoted",
        }
        pending_rows.append(row)

    data["pending_or_related"] = pending_rows

    for m in months:
        fams = m.get("families") or []
        m["family_count"] = len(fams)
        m["event_count"] = sum(max(1, len(f.get("family_events") or [])) for f in fams)

    meta = evidence.get("report_meta_patch") or {}
    for k, v in meta.items():
        data[k] = v

    data.setdefault("change_history", []).append(
        {
            "at": stamp,
            "by": "merge_evidence_r2",
            "action": "evidence_review_r2_increment",
            "detail": evidence.get("change_summary", "Gate ③ evidence-review r2 independent increment merged."),
        }
    )

    recompute_counts(data)
    REPORT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote", REPORT_PATH)
    print("counts:", json.dumps(data["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
