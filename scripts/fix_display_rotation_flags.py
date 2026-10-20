#!/usr/bin/env python3
"""Clear display_rotation when raster is portrait (h>w): bytes already upright post-recovery."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    cleared = 0
    kept = 0
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            for fig in fam.get("figures") or []:
                rot = fig.get("display_rotation") or 0
                if rot not in (90, 270):
                    continue
                w = int(fig.get("width") or 0)
                h = int(fig.get("height") or 0)
                if w > 0 and h > w:
                    fig["display_rotation"] = 0
                    geom = fig.get("source_geometry")
                    if isinstance(geom, dict):
                        geom["display_rotation"] = 0
                    cleared += 1
                else:
                    kept += 1
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cleared_portrait_rot90": cleared, "kept_landscape_rot": kept}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
