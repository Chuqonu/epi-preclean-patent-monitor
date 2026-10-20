#!/usr/bin/env python3
"""Clear mistaken display_rotation on portrait bytes only when explicitly listed.

USPTO portrait *pages* with sideways drawing bodies keep display_rotation=90 (see restore_uspto_portrait_sheet_rotation.py).
Do not auto-clear all h>w rotation — that breaks US12757647B2-class figures.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
MAP = ROOT / "data" / "figure-recovery-map.json"


# Gate③ WO/TW Fig.2 true PNG — portrait bytes already upright; rot90 was wrong.
UPRIGHT_PORTRAIT_SHA_PREFIXES = ("77e2a1525aeebf656",)


def normalize_rot(fig: dict) -> bool:
    rot = fig.get("display_rotation") or 0
    if rot not in (90, 270):
        return False
    sha = str(
        fig.get("sha256")
        or fig.get("asset_sha256")
        or fig.get("source_display_sha256")
        or ""
    )
    if not any(sha.startswith(p) for p in UPRIGHT_PORTRAIT_SHA_PREFIXES):
        return False
    fig["display_rotation"] = 0
    geom = fig.get("source_geometry")
    if isinstance(geom, dict):
        geom["display_rotation"] = 0
    return True


def main() -> int:
    cleared_report = 0
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            for fig in fam.get("figures") or []:
                if normalize_rot(fig):
                    cleared_report += 1
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cleared_map = 0
    if MAP.is_file():
        mapping = json.loads(MAP.read_text(encoding="utf-8"))
        for item in mapping.get("entries", {}).values():
            if normalize_rot(item):
                cleared_map += 1
        MAP.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"cleared_report": cleared_report, "cleared_map": cleared_map}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
