#!/usr/bin/env python3
"""Apply vision-confirmed display_rotation for a single figure (US12757647B2 Fig.4).

Do not bulk-restore historical rot90 list or Tesseract OSD output — see docs/FIGURE-ORIENTATION-RESTORE-2026-10-20.json.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
MAP = ROOT / "data" / "figure-recovery-map.json"

TARGET_PUB = "US12757647B2"
TARGET_SHA_PREFIX = "e5d5f61dac3d4b7a"
TARGET_ROT = 90


def set_rot(fig: dict, rot: int) -> None:
    fig["display_rotation"] = rot
    geom = fig.get("source_geometry")
    if isinstance(geom, dict):
        geom["display_rotation"] = rot


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    changed = False
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id") or ""
            if pub != TARGET_PUB:
                continue
            for fig in fam.get("figures") or []:
                sha = str(fig.get("asset_sha256") or fig.get("sha256") or "")
                if TARGET_SHA_PREFIX not in sha:
                    continue
                set_rot(fig, TARGET_ROT)
                changed = True

    if not changed:
        print("target figure not found", file=sys.stderr)
        return 1

    data.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "vision-figure-orientation",
            "action": "set_display_rotation_90",
            "detail": f"{TARGET_PUB} Fig.4 vision-confirmed sideways drawing body.",
        }
    )
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if MAP.is_file():
        mapping = json.loads(MAP.read_text(encoding="utf-8"))
        for item in (mapping.get("entries") or {}).values():
            sha = str(item.get("asset_sha256") or "")
            if TARGET_SHA_PREFIX in sha:
                set_rot(item, TARGET_ROT)
        MAP.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"publication_id": TARGET_PUB, "display_rotation": TARGET_ROT}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
