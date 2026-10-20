#!/usr/bin/env python3
"""Apply display_rotation from data/vision-display-rotation.json (vision-confirmed shas only)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "vision-display-rotation.json"
REPORT = ROOT / "data" / "report.json"
MAP = ROOT / "data" / "figure-recovery-map.json"


def figure_shas(fig: dict) -> set[str]:
    out: set[str] = set()
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


def load_targets() -> dict[str, int]:
    raw = json.loads(MANIFEST.read_text(encoding="utf-8"))
    targets: dict[str, int] = {}
    for row in raw.get("display_rotation_90") or []:
        sha = row.get("sha256")
        if sha:
            targets[str(sha)] = 90
    for row in raw.get("display_rotation_270") or []:
        sha = row.get("sha256")
        if sha:
            targets[str(sha)] = 270
    for row in raw.get("display_rotation_180") or []:
        sha = row.get("sha256")
        if sha:
            targets[str(sha)] = 180
    return targets


def main() -> int:
    if not MANIFEST.is_file():
        print("missing", MANIFEST, file=sys.stderr)
        return 1
    targets = load_targets()
    if not targets:
        print("no targets in manifest", file=sys.stderr)
        return 1

    target_shas = set(targets.keys())
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    changed: list[dict] = []

    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id") or ""
            for fig in fam.get("figures") or []:
                shas = figure_shas(fig)
                hit = shas & target_shas
                if hit:
                    sha = next(iter(hit))
                    rot = targets[sha]
                    prev = fig.get("display_rotation") or 0
                    if prev != rot:
                        set_rot(fig, rot)
                        changed.append(
                            {
                                "publication_id": pub,
                                "figure_number": fig.get("figure_number"),
                                "sha256": sha,
                                "before": prev,
                                "after": rot,
                            }
                        )
                elif (fig.get("display_rotation") or 0) != 0:
                    prev = fig.get("display_rotation") or 0
                    set_rot(fig, 0)
                    changed.append(
                        {
                            "publication_id": pub,
                            "figure_number": fig.get("figure_number"),
                            "sha256": next(iter(shas), ""),
                            "before": prev,
                            "after": 0,
                            "reason": "not_in_vision_manifest",
                        }
                    )

    found = set()
    for m in data.get("months") or []:
        for fam in m.get("families") or []:
            for fig in fam.get("figures") or []:
                found |= figure_shas(fig) & target_shas
    missing = target_shas - found
    if missing:
        print("manifest sha not in report:", sorted(missing), file=sys.stderr)
        return 1

    data.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "vision-display-rotation-manifest",
            "action": "apply_vision_display_rotation",
            "detail": f"Manifest {len(target_shas)} sha(s); {len(changed)} row change(s).",
        }
    )
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if MAP.is_file():
        mapping = json.loads(MAP.read_text(encoding="utf-8"))
        for item in (mapping.get("entries") or {}).values():
            shas = figure_shas(item)
            hit = shas & target_shas
            if hit:
                set_rot(item, targets[next(iter(hit))])
            elif (item.get("display_rotation") or 0) != 0:
                set_rot(item, 0)
        MAP.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"changed": changed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
