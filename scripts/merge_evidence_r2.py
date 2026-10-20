#!/usr/bin/env python3
"""Idempotent merge of docs/EVIDENCE-REVIEW-2026-10-20-r2.json into data/report.json."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "data" / "report.json"
EVIDENCE_PATH = ROOT / "docs" / "EVIDENCE-REVIEW-2026-10-20-r2.json"

sys.path.insert(0, str(ROOT / "scripts"))
from report_metrics import recompute_counts, card_events_for_month  # noqa: E402


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


def normalize_card_events(raw: dict) -> list[dict]:
    pub = raw["publication_id"]
    evs = raw.get("family_events")
    if evs:
        own = [ev for ev in evs if ev.get("publication_id") == pub]
        if own:
            return own
    return [
        {
            "publication_id": pub,
            "event_date": raw["event_date"],
            "event_type": raw.get("event_type", "publication"),
            "source_url": (raw.get("source_urls") or [f"https://patents.google.com/patent/{pub}/en"])[0],
            "application_id": raw.get("application_id"),
        }
    ]


def build_independent_record(raw: dict, stamp: str) -> dict:
    pub = raw["publication_id"]
    ym = month_key(raw["event_date"])
    return {
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
        "claims_or_embodiment_basis": raw.get(
            "claims_or_embodiment_basis",
            "独立检索纳入；详见来源链接与证据复核记录。",
        ),
        "scope_reason": raw.get("scope_reason", "独立检索纳入。"),
        "source_urls": raw.get("source_urls") or [f"https://patents.google.com/patent/{pub}/en"],
        "source_retrieved_at": raw.get("source_retrieved_at"),
        "source_sha256": raw.get("source_sha256"),
        "actual_read_spans": raw.get("actual_read_spans") or [],
        "team_independent_read": bool(raw.get("team_independent_read")),
        "reviewer": raw.get("reviewer"),
        "reviewed_at": raw.get("reviewed_at"),
        "family_completion_status": raw.get("family_completion_status", "open"),
        "figures": raw.get("figures") or [],
        "change_history": raw.get("change_history")
        or [
            {
                "at": stamp,
                "by": "evidence-review-r2",
                "action": "independent_add",
                "detail": raw.get("merge_note") or "独立检索新纳入（非基线导入）。",
            }
        ],
        "family_events": normalize_card_events(raw),
        "id": f"{ym}-{pub}",
        "month": ym,
        "import_tag": None,
        "discovery_source": "independent_search",
        "independent_of_ref": True,
        "family_merge_note": raw.get("family_merge_note"),
        "event_note": raw.get("event_note", "独立检索发现"),
        "category": raw.get("category"),
    }


def upsert_independent(months: list, raw: dict, stamp: str) -> str:
    pub = raw["publication_id"]
    rec = build_independent_record(raw, stamp)
    hit = find_family(months, pub)
    if hit:
        _, fi, fam = hit
        for k, v in rec.items():
            if k == "change_history":
                continue
            fam[k] = v
        return "updated"
    m = ensure_month(months, rec["month"])
    m["families"].append(rec)
    return "inserted"


def merge_pending(existing: list, incoming: list, months: list) -> list:
    by_id = {row.get("publication_id"): deepcopy(row) for row in existing if row.get("publication_id")}
    for p in incoming:
        pub = p["publication_id"]
        hit = find_family(months, pub)
        row = {
            "publication_id": pub,
            "jurisdiction": p.get("jurisdiction"),
            "event_type": p.get("event_type"),
            "event_date": p.get("event_date"),
            "title_zh": p.get("title_zh", pub),
            "applicant_normalized": p.get("applicant_normalized", ""),
            "scope_status": "pending",
            "pending_reason": p["pending_reason"],
            "failure_or_pending_reason": p.get("failure_or_pending_reason") or p["pending_reason"],
            "discovery_source": p.get("discovery_source", "independent_search"),
            "import_tag": p.get("import_tag"),
            "on_main_month_cards": bool(hit),
            "disposition": p.get("disposition", "pending_not_promoted"),
            "kind_verified": p.get("kind_verified", True),
        }
        if pub in by_id:
            by_id[pub].update({k: v for k, v in row.items() if v is not None})
        else:
            by_id[pub] = row
    return list(by_id.values())


def apply_baseline_confirm(fam: dict, note: str, stamp: str) -> None:
    if fam.get("independent_search_confirmation") == note:
        return
    fam.setdefault("change_history", []).append(
        {
            "at": stamp,
            "by": "evidence-review-r2",
            "action": "independent_search_confirm",
            "detail": note,
        }
    )
    fam["independent_search_confirmation"] = note


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
        if hit:
            apply_baseline_confirm(hit[2], item["note"], stamp)

    for raw in evidence.get("independent_discoveries", []):
        upsert_independent(months, raw, stamp)

    incoming_pending = []
    for p in evidence.get("pending", []):
        incoming_pending.append(p)

    data["pending_or_related"] = merge_pending(
        data.get("pending_or_related") or [], incoming_pending, months
    )

    meta = evidence.get("report_meta_patch") or {}
    for k, v in meta.items():
        data[k] = v

    recompute_counts(data)
    REPORT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    import apply_independent_evidence as aie

    aie.main()
    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    print("counts:", json.dumps(data["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
