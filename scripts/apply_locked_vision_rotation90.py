#!/usr/bin/env python3
"""Set display_rotation=90 on vision-locked figure rows by asset sha256 (bytes unchanged)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
MAP = ROOT / "data" / "figure-recovery-map.json"

LOCKED_SHA90 = frozenset(
    {
        "e5d5f61dac3d4b7a2f379004b3c3e15445c20416f436919f3615fb16546cb288",
        "39e66689f3d4ed987e3f3562b40eb24e6b030314892baf2029b0f8a1cab74603",
        "22dbc8e9baf1a3e5c7e6efed68b2bc752517f8a1fe47b87a0cd020d0ece5acae",
        "d0af11401052ea68bfa12e42f563bfbb40a029ee5e09dee02c2ba60aab2ad4b0",
        "8533597a17f700dfd505913f5ae521fb21245098c68b10c38a4b2d7bfe6ec363",
        "11ec9fb5bbc7be2be3301d79afb8cb1faaba6ac3c6d44dffd94c2e9efe551b9a",
        "1516cae0ee73967b9d353b67b29a75de9ddcb5f972180baf1fd1c1146609bfd8",
        "f77056a140d3fcb39e80b46e7015030ebcaf5b9756af42984a4dc9ee59b52443",
        "3f06f16dabb38600dc59c52de04efccc3277ece9207f0b8a004e0ff9abce7175",
    }
)

WO_TW_FIG2_SHA = "77e2a1525aeebf656f5b7d348a4c1c6f363d0a0cb3b5b2e4d57ec3aa7546571c"


def figure_shas(fig: dict) -> set[str]:
    out = set()
    for k in ("asset_sha256", "source_display_sha256", "sha256", "source_original_sha256"):
        v = fig.get(k)
        if v:
            out.add(str(v))
    return out


def set_rot(fig: dict, rot: int) -> None:
    fig["display_rotation"] = rot
    geom = fig.get("source_geometry")
    if isinstance(geom, dict):
        geom["display_rotation"] = rot


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    changed: list[dict] = []
    matched_shas: set[str] = set()

    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id") or fam.get("publication_number") or ""
            for fig in fam.get("figures") or []:
                shas = figure_shas(fig)
                if WO_TW_FIG2_SHA in shas:
                    continue
                hit = shas & LOCKED_SHA90
                if not hit:
                    continue
                prev = fig.get("display_rotation") or 0
                set_rot(fig, 90)
                sha = next(iter(hit))
                matched_shas.add(sha)
                if prev != 90:
                    changed.append(
                        {
                            "publication_id": pub,
                            "figure_number": fig.get("figure_number"),
                            "sha256": sha,
                            "display_rotation_before": prev,
                            "display_rotation_after": 90,
                        }
                    )

    missing = LOCKED_SHA90 - matched_shas
    if missing:
        raise SystemExit(f"locked sha not found in report: {sorted(missing)}")

    data.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "vision-locked-rotation90",
            "action": "set_display_rotation_90_by_sha",
            "detail": f"Vision-locked 9 unique assets → {len(changed)} row updates (incl. family mirrors).",
        }
    )
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    map_updates = 0
    if MAP.is_file():
        mapping = json.loads(MAP.read_text(encoding="utf-8"))
        for item in (mapping.get("entries") or {}).values():
            shas = figure_shas(item)
            if WO_TW_FIG2_SHA in shas:
                continue
            if shas & LOCKED_SHA90:
                set_rot(item, 90)
                map_updates += 1
        MAP.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = ROOT / "docs" / "FIGURE-ORIENTATION-RESTORE-2026-10-20.json"
    manifest.write_text(
        json.dumps(
            {
                "date": "2026-10-20",
                "policy": "Vision-locked 9 unique asset shas; metadata display_rotation=90 only; never rotate bytes.",
                "wo_tw_fig2_unchanged_sha": WO_TW_FIG2_SHA,
                "locked_sha_count": len(LOCKED_SHA90),
                "row_updates": changed,
                "figure_recovery_map_entries": map_updates,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"rows": len(changed), "unique_shas": len(matched_shas), "map": map_updates}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
