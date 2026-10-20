#!/usr/bin/env python3
"""Clear portrait display_rotation in report.json and figure-recovery-map (upright bytes)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
MAP = ROOT / "data" / "figure-recovery-map.json"


def normalize_rot(fig: dict) -> bool:
    rot = fig.get("display_rotation") or 0
    if rot not in (90, 270):
        return False
    w = int(fig.get("width") or 0)
    h = int(fig.get("height") or 0)
    if w > 0 and h > w:
        fig["display_rotation"] = 0
        geom = fig.get("source_geometry")
        if isinstance(geom, dict):
            geom["display_rotation"] = 0
        return True
    return False


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
