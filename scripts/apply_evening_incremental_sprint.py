#!/usr/bin/env python3
"""Apply evening 2026-10-20 frozen EPI/Preclean incrementals to data/report.json (idempotent)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
EPI = ROOT / "docs" / "EPI-INCREMENTAL-SPRINT-evening-2026-10-20-frozen.json"
PRECLEAN = ROOT / "docs" / "PRECLEAN-INCREMENTAL-SPRINT-evening-2026-10-20-frozen.json"

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
    return {
        "publication_id": pub,
        "jurisdiction": c.get("jurisdiction", "US"),
        "event_type": c.get("event_type", "publication"),
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
        "reviewer": None,
        "reviewed_at": None,
        "family_completion_status": c.get("family_completion_status", "open"),
        "figures": [],
        "change_history": [
            {
                "at": STAMP,
                "by": "evening-incremental-sprint",
                "action": "include_core_epi",
                "detail": "EPI-INCREMENTAL-SPRINT-evening-2026-10-20-frozen.json",
            }
        ],
        "family_events": [
            {
                "publication_id": ev.get("publication_id", pub),
                "event_date": ev.get("event_date", c["event_date"]),
                "event_type": ev.get("event_type", c.get("event_type", "publication")),
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
        "family_merge_note": None,
        "event_note": "晚间增量独立检索（informal）",
        "category": "EPI 工艺与设备",
        "team_independent_read": False,
        "read_disposition": "included_not_team_read",
        "read_status": "晚间 EPI 纳入；未计 team_read。",
    }


def build_asm_family_cards(rep: dict) -> list[dict]:
    family_id = rep["family_id"]
    events = rep.get("events") or []
    merge = (
        f"{family_id}：同族 KR/US 授权分月成卡；代表 US12660544B2。"
        " AHF+水汽 dry oxide preclean（USPTO OG 核读）。"
    )
    cards = []
    for ev in events:
        pub = ev["publication_id"]
        month = ev["event_date"][:7]
        jur = "KR" if pub.startswith("KR") else "US"
        sha = ev.get("source_sha256") or rep.get("source_sha256")
        cards.append(
            {
                "publication_id": pub,
                "jurisdiction": jur,
                "event_type": ev.get("event_type", "grant"),
                "event_date": ev["event_date"],
                "application_id": None,
                "priority_date": None,
                "family_id": family_id,
                "family_id_source": rep.get("family_id_source", "independent_search"),
                "title_original": rep.get("title_original"),
                "title_zh": "半导体预清洁方法及装置（无水 HF + 水汽去氧化物）",
                "applicant_original": rep.get("applicant_original"),
                "applicant_normalized": rep.get("applicant_normalized", "ASM"),
                "scope_status": "core",
                "technology_tags": ["preclean", "AHF", "dry_oxide_removal"],
                "short_preview": "ASM 无水 HF 与水汽半导体预清洁方法/气路系统（dry oxide preclean，预外延去氧化）。",
                "technical_summary": rep.get("why_relevant", ""),
                "claims_or_embodiment_basis": rep.get("claims_or_embodiment_basis", ""),
                "scope_reason": "晚间 Preclean 增量：同族授权事件纳入 core。",
                "source_urls": [
                    u
                    for u in dict.fromkeys(
                        ([ev.get("source_url")] if ev.get("source_url") else [])
                        + (rep.get("source_urls") or [])
                    )
                    if u
                ],
                "source_retrieved_at": rep.get("source_retrieved_at"),
                "source_sha256": sha,
                "actual_read_spans": rep.get("actual_read_spans") or [],
                "reviewer": None,
                "reviewed_at": None,
                "family_completion_status": "open",
                "figures": [],
                "change_history": [
                    {
                        "at": STAMP,
                        "by": "evening-incremental-sprint",
                        "action": "include_core_preclean_family",
                        "detail": "PRECLEAN-INCREMENTAL-SPRINT-evening-2026-10-20-frozen.json",
                    }
                ],
                "family_events": [
                    {
                        "publication_id": e["publication_id"],
                        "event_date": e["event_date"],
                        "event_type": e.get("event_type", "grant"),
                        "source_url": e.get("source_url"),
                        "application_id": None,
                    }
                    for e in events
                ],
                "id": f"{month}-{pub}",
                "month": month,
                "import_tag": None,
                "discovery_source": "independent_search",
                "independent_of_ref": True,
                "discovery_lane": "Preclean",
                "family_merge_note": merge,
                "event_note": "晚间增量独立检索（informal）",
                "category": "Preclean",
                "team_independent_read": False,
                "read_disposition": "included_not_team_read",
                "read_status": "晚间 Preclean 纳入；未计 team_read。",
            }
        )
    return cards


def tag_lam_baseline(data: dict) -> bool:
    loc = None
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            if fam.get("publication_id") == "US20260090293A1":
                loc = fam
                break
    if not loc:
        return False
    tags = list(loc.get("technology_tags") or [])
    changed = False
    if "preclean" not in tags:
        tags.append("preclean")
        changed = True
    loc["technology_tags"] = tags
    loc.setdefault("change_history", []).append(
        {
            "at": STAMP,
            "by": "evening-incremental-sprint",
            "action": "label_baseline_preclean_tag",
            "detail": "US20260090293A1 已 live baseline；补 Preclean 技术标签（claim12），不计晚间新发现。",
        }
    )
    return changed


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
    pc_doc = json.loads(PRECLEAN.read_text(encoding="utf-8"))
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    added: list[str] = []

    for c in epi_doc.get("candidates") or []:
        if c.get("disposition") != "include_core":
            continue
        pub = c["publication_id"]
        if pub_exists(data, pub):
            continue
        block = month_block(data, c["month"])
        block.setdefault("families", []).append(build_epi_card(c))
        block["families"].sort(key=family_sort_time, reverse=True)
        added.append(pub)

    asm_rep = next(
        (
            c
            for c in pc_doc.get("candidates") or []
            if c.get("family_id") == "FAM-ASM-AHF-PRECLEAN" and c.get("disposition") == "include_core"
        ),
        None,
    )
    if asm_rep:
        for card in build_asm_family_cards(asm_rep):
            pub = card["publication_id"]
            if pub_exists(data, pub):
                continue
            block = month_block(data, card["month"])
            block.setdefault("families", []).append(card)
            block["families"].sort(key=family_sort_time, reverse=True)
            added.append(pub)

    tag_lam_baseline(data)

    note = (
        "晚间增量（informal 2026-10-20）：EPI US20260062803A1 + "
        "Preclean FAM-ASM-AHF-PRECLEAN（KR102916044B1 / US12660544B2 / US12757665B2）；"
        "Lam US20260090293A1 仅补标签，不计新发现。"
    )
    notes = data.get("notes") or []
    if note not in notes:
        notes.append(note)
    data["notes"] = notes

    hist = data.get("change_history") or []
    hist.append(
        {
            "at": STAMP,
            "by": "evening-incremental-sprint",
            "action": "evening_include_core",
            "detail": f"Added publication cards: {', '.join(added) or '(none new)'}. team_read locked 6.",
        }
    )
    data["change_history"] = hist

    recompute_counts(data)
    locked_read = 6
    data["counts"]["actually_read"] = locked_read
    data["counts"]["events_reviewed"] = locked_read
    data["counts"]["figures_available"] = figures_available(data)

    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("added:", added)
    print("publication_events:", data["counts"]["publication_events"])
    print("actually_read:", data["counts"]["actually_read"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
