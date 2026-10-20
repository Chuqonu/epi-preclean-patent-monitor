#!/usr/bin/env python3
"""Restore display_rotation=90 for USPTO portrait-page figures with sideways drawing bodies.

These were display_rotation=90 in figure-restore (0a10af4) and were incorrectly zeroed.
WO/TW Gate③ Fig.2 (77e2a152…) stays at 0 — upright portrait bytes.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
MAP = ROOT / "data" / "figure-recovery-map.json"

# publication_id -> unique substring of figure_number (first match wins per pub)
RESTORE: dict[str, str] = {
    "US12595587B2": "图1：",
    "US12701931B2": "图4：",
    "US12740346B2": "图7：",
    "US12757647B2": "图4：",
    "US20260026275A1": "FIG. 8A",
    "US20260150594A1": "图4：",
    "US20260035835A1": "图2",
    "US20260164725A1": "FIGS. 20C",
}

# Second fig on same publication
RESTORE_EXTRA: list[tuple[str, str]] = [
    ("US20260026275A1", "FIG. 9"),
]

WO_TW_FIG2_SHA_PREFIX = "77e2a1525aeebf656"


def set_rot(fig: dict, rot: int = 90) -> None:
    fig["display_rotation"] = rot
    geom = fig.get("source_geometry")
    if isinstance(geom, dict):
        geom["display_rotation"] = rot


def match_figure(pub: str, fig_num: str, needle: str) -> bool:
    return pub == pub and needle in (fig_num or "")


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    changed: list[dict] = []
    seen_pub: set[str] = set()

    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id") or fam.get("publication_number") or ""
            for fig in fam.get("figures") or []:
                sha = str(fig.get("sha256") or fig.get("asset_sha256") or "")
                if WO_TW_FIG2_SHA_PREFIX in sha:
                    continue
                fn = fig.get("figure_number") or ""
                needle = RESTORE.get(pub)
                should = False
                if needle and pub not in seen_pub and needle in fn:
                    should = True
                    seen_pub.add(pub)
                for p, n in RESTORE_EXTRA:
                    if pub == p and n in fn:
                        should = True
                if not should:
                    continue
                prev = fig.get("display_rotation") or 0
                if prev == 90:
                    continue
                set_rot(fig, 90)
                changed.append(
                    {
                        "publication_id": pub,
                        "figure_number": fn,
                        "sha256_prefix": sha[:16],
                        "local_asset_path": fig.get("local_asset_path"),
                        "from": prev,
                        "to": 90,
                    }
                )

    data.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "uspto-portrait-sheet-rotation-restore",
            "action": "restore_display_rotation_90",
            "detail": f"Restored display_rotation=90 on {len(changed)} USPTO portrait-sheet figures (sideways drawing body).",
        }
    )
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    map_changed = 0
    if MAP.is_file():
        mapping = json.loads(MAP.read_text(encoding="utf-8"))
        prefixes = {c["sha256_prefix"] for c in changed}
        for item in (mapping.get("entries") or {}).values():
            sha = str(item.get("asset_sha256") or item.get("sha256") or "")
            if not any(sha.startswith(p) for p in prefixes):
                continue
            if (item.get("display_rotation") or 0) == 90:
                continue
            set_rot(item, 90)
            map_changed += 1
        MAP.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    out = ROOT / "docs" / "FIGURE-ORIENTATION-RESTORE-2026-10-20.json"
    out.write_text(
        json.dumps(
            {
                "date": "2026-10-20",
                "rule": "display_rotation is display-only CSS; extraction_rotation never applied in renderer",
                "wo_tw_fig2_unchanged_sha_prefix": WO_TW_FIG2_SHA_PREFIX,
                "changed": changed,
                "figure_recovery_map_entries_updated": map_changed,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"changed": len(changed), "map": map_changed}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
