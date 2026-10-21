#!/usr/bin/env python3
"""Apply Gate③ morning figure + optional TEL evidence backfills to data/report.json."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
EPI_WIRE = ROOT / "docs" / "EPI-FIGURELESS-BACKFILL-wire-2026-10-21.json"
PRECLEAN = ROOT / "docs" / "PRECLEAN-AHF-FIGURES-BACKFILL-2026-10-21.json"
TEL_EVIDENCE = ROOT / "docs" / "EPI-TEL-GAP-EVIDENCE-BACKFILL-2026-10-21.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_asset(relative: str, expected: str) -> None:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError("path escapes repo: " + relative)
    if not path.is_file():
        raise FileNotFoundError(relative)
    digest = sha256_file(path)
    if digest != expected:
        raise ValueError(f"checksum mismatch {relative}: {digest} != {expected}")


def wire_to_report_fig(row: dict, pub_id: str) -> dict:
    rel = row["local_path"] if "local_path" in row else row["local_asset_path"]
    sha = row["sha256"] if "sha256" in row else row.get("asset_sha256")
    verify_asset(rel, sha)
    out: dict = {
        "source_publication_id": pub_id,
        "figure_number": row["figure_number"],
        "source_url": row["source_url"],
        "local_asset_path": rel,
        "width": row["width"],
        "height": row["height"],
        "caption": row["caption"],
        "asset_sha256": sha,
        "source_original_sha256": sha,
        "source_display_sha256": sha,
        "display_rotation": int(row.get("display_rotation") or 0),
        "source_geometry": {},
    }
    if row.get("pdf_page"):
        out["pdf_page"] = row["pdf_page"]
    if row.get("family_share_from"):
        out["family_share_from"] = row["family_share_from"]
    return out


def build_epi_map() -> dict[str, list[dict]]:
    data = json.loads(EPI_WIRE.read_text(encoding="utf-8"))
    by_pub: dict[str, list[dict]] = {}
    for section in ("wire", "fetch"):
        for row in data.get(section) or []:
            pub = row["publication_id"]
            by_pub.setdefault(pub, []).append(wire_to_report_fig(row, pub))
    return by_pub


def build_preclean_map() -> dict[str, list[dict]]:
    data = json.loads(PRECLEAN.read_text(encoding="utf-8"))
    by_pub: dict[str, list[dict]] = {}
    for block in data.get("publications") or []:
        pub = block["publication_id"]
        figs = []
        for row in block.get("figures") or []:
            figs.append(wire_to_report_fig(row, pub))
        by_pub[pub] = figs
    return by_pub


def build_evidence_map() -> dict[str, dict]:
    if not TEL_EVIDENCE.is_file():
        return {}
    data = json.loads(TEL_EVIDENCE.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for ent in data.get("entries") or []:
        if ent.get("status") != "ok":
            continue
        out[ent["publication_id"]] = {
            "source_url": ent["source_url"],
            "source_sha256": ent["source_sha256"],
            "source_retrieved_at": ent["retrieved_at"],
            "actual_read_spans": ent.get("actual_read_spans") or [],
        }
    return out


def main() -> int:
    epi = build_epi_map()
    preclean = build_preclean_map()
    evidence = build_evidence_map()
    merged: dict[str, list[dict]] = {**epi}
    for pub, figs in preclean.items():
        merged[pub] = figs

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    applied: list[str] = []

    for month in data.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            if not pub or pub not in merged:
                continue
            if fam.get("figures"):
                raise SystemExit(f"Refusing to overwrite non-empty figures on {pub}")
            fam["figures"] = merged[pub]
            ev = evidence.get(pub)
            if ev:
                fam["source_sha256"] = ev["source_sha256"]
                fam["source_retrieved_at"] = ev["source_retrieved_at"]
                fam["actual_read_spans"] = ev["actual_read_spans"]
            fam.setdefault("change_history", []).append(
                {
                    "at": stamp,
                    "by": "morning-gate3-figures",
                    "action": "attach_gate3_family_figures",
                    "detail": f"Gate③ backfill {len(merged[pub])} figures",
                }
            )
            applied.append(pub)

    expected = sorted(merged.keys())
    missing = sorted(set(expected) - set(applied))
    if missing:
        raise SystemExit("Report missing month cards for: " + ", ".join(missing))

    data.setdefault("change_history", []).append(
        {
            "at": stamp,
            "by": "morning-gate3-figures",
            "action": "apply_morning_gate3_figure_backfill",
            "detail": f"EPI figureless + Preclean AHF; pubs={len(expected)}; team_read lock unchanged",
        }
    )

    sys.path.insert(0, str(ROOT / "scripts"))
    from report_metrics import recompute_counts

    recompute_counts(data)
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"applied": applied, "figures": data["counts"].get("figures")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
