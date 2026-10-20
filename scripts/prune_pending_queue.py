#!/usr/bin/env python3
"""Keep pending_or_related to active unresolved rows only (hygiene)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"

ACTIVE_PENDING = {"CN122564748A"}
DROP = {"US20260066234A1", "US12757451B2", "WO2026084898A1"}


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    before = data.get("pending_or_related") or []
    after = [p for p in before if p.get("publication_id") in ACTIVE_PENDING]
    dropped = [p.get("publication_id") for p in before if p.get("publication_id") in DROP]
    data["pending_or_related"] = after

    for note in list(data.get("notes") or []):
        if "待核队列见 pending_or_related；不入主表为新接受的 4 条" in note:
            data["notes"].remove(note)
    data.setdefault("notes", []).append(
        "关联待核（active）：仅 CN122564748A；已升格/已排除项不再列于 pending_or_related。"
    )
    data["coverage_note"] = (
        "在 Dot 基线上合并 Gate③ 与 Sprint 增量。"
        "关联待核队列现仅 CN122564748A（见 pending_or_related）。"
        "不得伪称零遗漏或正式交付。"
    )

    data.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "pending-queue-hygiene",
            "action": "prune_pending_or_related",
            "detail": "Removed promoted/excluded from queue: " + ", ".join(dropped),
        }
    )

    sys.path.insert(0, str(ROOT / "scripts"))
    from report_metrics import recompute_counts

    recompute_counts(data)
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"dropped": dropped, "remaining": [p["publication_id"] for p in after], "pending": data["counts"]["pending"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
