#!/usr/bin/env python3
"""Apply docs/EVIDENCE-READ-RULING-COMBINED-2026-10-20-r2.json (+ promote US20260066234A1 read card)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
RULING = ROOT / "docs" / "EVIDENCE-READ-RULING-COMBINED-2026-10-20-r2.json"
EPI = ROOT / "docs" / "EPI-EVIDENCE-SUPPLEMENT-2026-10-20.json"


def promote_us66234(data: dict) -> None:
    pending = data.get("pending_or_related") or []
    row = next((p for p in pending if p.get("publication_id") == "US20260066234A1"), None)
    if not row:
        return
    month_key = "2026-03"
    months = data.get("months") or []
    block = next((m for m in months if m.get("month") == month_key), None)
    if not block:
        return
    if any(f.get("publication_id") == "US20260066234A1" for f in block.get("families") or []):
        return
    card = {
        "publication_id": "US20260066234A1",
        "jurisdiction": "US",
        "event_type": "publication",
        "event_date": "2026-03-05",
        "application_id": None,
        "priority_date": None,
        "family_id": "US20260066234A1",
        "family_id_source": "baseline_claims_review",
        "title_original": "Plasma enhanced epitaxial deposition chamber",
        "title_zh": row.get("title_zh") or "等离子体增强外延沉积腔室",
        "applicant_normalized": row.get("applicant_normalized") or "Applied Materials, Inc.",
        "scope_status": "core",
        "technology_tags": ["epi"],
        "short_preview": "等离子体增强外延沉积腔室与工艺集成（同族 WO2026055216A1 附图来源）。",
        "technical_summary": "等离子体增强外延沉积腔室与工艺集成。",
        "claims_or_embodiment_basis": "基线复核：US20260066234A1 官方公开文本 22 项权利要求已复核（2026-10-15，见 WO2026055216A1 卡 reference_source_status）。",
        "scope_reason": "等离子体增强外延沉积，升格 core 并计 team_read（ruling r2）。",
        "source_urls": ["https://patents.google.com/patent/US20260066234A1/en"],
        "source_retrieved_at": None,
        "source_sha256": None,
        "actual_read_spans": [
            "基线复核：US20260066234A1 权利要求 1–22（官方公开页，2026-10-15 记录）"
        ],
        "reviewer": "baseline-claims-review",
        "reviewed_at": "2026-10-15",
        "family_completion_status": "open",
        "figures": [],
        "change_history": [
            {
                "at": "2026-10-20T12:00:00Z",
                "by": "read-ruling-r2",
                "action": "promote_core_team_read",
                "detail": "由 pending 升格 core 月卡；不计为 Gate③ 独立新发现。",
            }
        ],
        "family_events": [
            {
                "publication_id": "US20260066234A1",
                "event_date": "2026-03-05",
                "event_type": "publication",
                "source_url": "https://patents.google.com/patent/US20260066234A1/en",
            }
        ],
        "id": "2026-03-US20260066234A1",
        "month": month_key,
        "import_tag": None,
        "discovery_source": "baseline_claims_review",
        "team_independent_read": True,
        "read_disposition": "team_read_claims_level",
        "category": "EPI 设备",
    }
    block.setdefault("families", []).append(card)
    row["scope_status"] = "core"
    row["disposition"] = "promoted_core_team_read"
    row["on_main_month_cards"] = True
    row["pending_reason"] = "已升格 2026-03 主表 core 并计 team_read（r2）；保留队列记录。"


def main() -> int:
    ruling = json.loads(RULING.read_text(encoding="utf-8"))
    team_ids = set(ruling["team_read_publication_ids"])
    expected = int(ruling["locked_team_read_total"])
    span = ruling.get("read_span_label") or "权利要求级阅读"

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    promote_us66234(data)

    epi_by_pub = {}
    if EPI.is_file():
        epi = json.loads(EPI.read_text(encoding="utf-8"))
        epi_by_pub = {r["publication_id"]: r for r in epi.get("team_read", [])}

    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id")
            if pub in team_ids:
                fam["team_independent_read"] = True
                fam["read_disposition"] = "team_read_claims_level"
                if pub in epi_by_pub:
                    row = epi_by_pub[pub]
                    fam["actual_read_spans"] = row.get("actual_read_spans") or [span]
                    fam["reviewer"] = row.get("reviewer")
                    fam["reviewed_at"] = row.get("reviewed_at")
                elif pub == "US12660522B2":
                    fam["actual_read_spans"] = [
                        "证据复核 r2：授权全文权利要求已读（revalidated，计 team_read r2）"
                    ]
                    fam["reviewer"] = "evidence-review-r2"
                    fam["reviewed_at"] = "2026-10-20"
                elif pub != "US20260066234A1":
                    fam.setdefault("actual_read_spans", [span])
            elif fam.get("discovery_source") == "independent_search" and pub not in team_ids:
                fam["team_independent_read"] = False

    sys.path.insert(0, str(ROOT / "scripts"))
    from report_metrics import recompute_counts

    recompute_counts(data)
    got = data["counts"]["actually_read"]
    if got != expected:
        print(f"ERROR team_read {got} != locked {expected}", file=sys.stderr)
        return 1

    notes = data.get("notes") or []
    data["notes"] = [n for n in notes if "本团队已读锁定 4" not in n]
    data["notes"].insert(
        0,
        "本团队已读锁定 6（见 EVIDENCE-READ-RULING-COMBINED-2026-10-20-r2.json）。",
    )
    data["status_note"] = (
        data.get("status_note", "")
        .replace("锁定 4", "锁定 6")
        .replace("本团队已读锁定 4", "本团队已读锁定 6")
    )
    if "锁定 6" not in data.get("status_note", ""):
        data["status_note"] = (
            "初版：基线 + Gate③ 增量。本团队已读锁定 6（r2 ruling）。"
        )

    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied team_read={got}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
