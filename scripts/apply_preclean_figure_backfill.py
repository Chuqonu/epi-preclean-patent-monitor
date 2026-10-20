#!/usr/bin/env python3
"""Apply docs/PRECLEAN-REPORT-FIGURES-BACKFILL-2026-10-20.json to data/report.json."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
BACKFILL = ROOT / "docs" / "PRECLEAN-REPORT-FIGURES-BACKFILL-2026-10-20.json"


def verify_asset(root: Path, relative: str, expected_sha: str | None) -> None:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Asset path escapes repo: " + relative)
    if not path.is_file():
        raise FileNotFoundError(relative)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected_sha and digest != expected_sha:
        raise ValueError(f"Checksum mismatch for {relative}")


def main() -> int:
    backfill = json.loads(BACKFILL.read_text(encoding="utf-8"))
    pubs: dict[str, list] = backfill.get("publications") or {}
    if not pubs:
        raise SystemExit("Backfill has no publications")

    data = json.loads(REPORT.read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    applied: list[str] = []

    for month in data.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            figures = pubs.get(pub)
            if not figures:
                continue
            for fig in figures:
                verify_asset(ROOT, fig["local_asset_path"], fig.get("asset_sha256"))
            fam["figures"] = figures
            fam.setdefault("change_history", []).append(
                {
                    "at": stamp,
                    "by": "preclean-figure-backfill",
                    "action": "attach_gate3_family_figures",
                    "detail": f"Applied {len(figures)} figures from {BACKFILL.name}",
                }
            )
            applied.append(pub)

    missing = sorted(set(pubs) - set(applied))
    if missing:
        raise SystemExit("Report missing month cards for: " + ", ".join(missing))

    data.setdefault("change_history", []).append(
        {
            "at": stamp,
            "by": "preclean-figure-backfill",
            "action": "apply_preclean_report_figures",
            "detail": "WO/TW hybrid-preclean Gate③ figure paths from Preclean backfill manifest.",
        }
    )

    sys.path.insert(0, str(ROOT / "scripts"))
    from report_metrics import recompute_counts

    recompute_counts(data)
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"applied": applied, "figures_total": data["counts"].get("figures")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
