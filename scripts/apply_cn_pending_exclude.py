#!/usr/bin/env python3
"""Clear CN122564748A from pending_or_related per exclude disposition (pending → 0)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
DISPOSITION = ROOT / "docs" / "EVIDENCE-PENDING-DISPOSITION-CN122564748A-2026-10-20.json"


def main() -> int:
    disp = json.loads(DISPOSITION.read_text(encoding="utf-8"))
    if disp.get("disposition") != "exclude":
        raise SystemExit("Unexpected disposition: " + str(disp.get("disposition")))

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    before = data.get("pending_or_related") or []
    removed = [p.get("publication_id") for p in before]
    data["pending_or_related"] = []

    for note in list(data.get("notes") or []):
        if "关联待核（active）" in note or "CN122564748A" in note and "待核" in note:
            data["notes"].remove(note)
    data.setdefault("notes", []).append(
        "关联待核（content-pending）：无 active 行；CN122564748A 已裁定 exclude（见 EVIDENCE-PENDING-DISPOSITION-CN122564748A-2026-10-20.json）。"
    )
    data["coverage_note"] = (
        "在 Dot 基线上合并 Gate③ 与 Sprint 增量。"
        "关联待核 content-pending 队列现为空（CN122564748A exclude）。"
        "不得伪称零遗漏或正式交付。"
    )

    data.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "cn-pending-exclude",
            "action": "clear_pending_or_related",
            "detail": "Removed from queue (exclude): " + ", ".join(removed) if removed else "already empty",
        }
    )

    sys.path.insert(0, str(ROOT / "scripts"))
    from report_metrics import recompute_counts

    recompute_counts(data)
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"removed": removed, "pending": data["counts"]["pending"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
