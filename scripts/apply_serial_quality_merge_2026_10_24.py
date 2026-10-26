#!/usr/bin/env python3
"""Serial merge Oct 24–25 quality package into data/report.json (Pages only).

- Ingest upright crops (display_rotation=0) for US12768074B2 (align 13→23),
  US12770834B2, TW202628839A, WO2026096517A1 from MANIFEST.json.
- Apply EPI + Preclean reader-field rewrites (PM brief whitelist).
- Does NOT touch actually_read, research_through, or team_read locks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERED = Path("assets/figures/recovered")
FIGURE_PUBS = frozenset(
    {
        "US12768074B2",
        "US12770834B2",
        "TW202628839A",
        "WO2026096517A1",
    }
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"not PNG: {path}")
    return struct.unpack(">II", data[16:24])


def clean_caption_from_report(old: str) -> str:
    for sep in ("：", ":"):
        if sep in old:
            tail = old.split(sep, 1)[1].strip()
            if tail.upper().startswith("FIG.") or tail.startswith("FIG."):
                return tail
    return old.strip()


def publication_id_from_patch(patch: dict) -> str:
    if patch.get("publication_id"):
        return patch["publication_id"]
    pid = patch.get("id", "")
    m = re.search(r"(US|WO|TW|JP|KR|CN|DE)[A-Z0-9]+", pid)
    if not m:
        raise ValueError(f"cannot derive publication_id from patch id {pid}")
    return m.group(0)


def apply_reader_patches(report: dict, epi_path: Path, preclean_path: Path) -> dict[str, list[str]]:
    epi = json.loads(epi_path.read_text(encoding="utf-8"))
    preclean = json.loads(preclean_path.read_text(encoding="utf-8"))
    by_pub: dict[str, dict] = {}
    caption_overrides: dict[str, dict[str, str]] = {}

    for patch in epi.get("patches") or []:
        pub = publication_id_from_patch(patch)
        by_pub[pub] = {**(by_pub.get(pub) or {}), **(patch.get("set") or {})}

    for patch in preclean.get("patches") or []:
        pub = patch["publication_id"]
        by_pub[pub] = {**(by_pub.get(pub) or {}), **(patch.get("set") or {})}
        if patch.get("figure_captions"):
            caption_overrides[pub] = patch["figure_captions"]

    applied: dict[str, list[str]] = {}
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            if pub not in by_pub and pub not in caption_overrides:
                continue
            fields = by_pub.get(pub) or {}
            touched: list[str] = []
            for key, val in fields.items():
                if fam.get(key) != val:
                    fam[key] = val
                    touched.append(key)
            caps = caption_overrides.get(pub) or {}
            for fig in fam.get("figures") or []:
                cap = caps.get(fig.get("figure_number"))
                if cap and fig.get("caption") != cap:
                    fig["caption"] = cap
                    touched.append(f"caption:{fig.get('figure_number')}")
            if touched:
                applied[pub] = touched
    return applied


def copy_crop_to_recovered(crops_root: Path, rel: str, expected_sha: str) -> Path:
    src = crops_root / rel
    if not src.is_file():
        raise FileNotFoundError(src)
    digest = sha256_file(src)
    if digest != expected_sha:
        raise ValueError(f"checksum mismatch {rel}: {digest} != {expected_sha}")
    dest = ROOT / RECOVERED / f"{digest}.png"
    if not dest.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    elif sha256_file(dest) != digest:
        raise ValueError(f"existing asset corrupt: {dest}")
    return dest


def build_uspto_style_figure(
    pub: str,
    row: dict,
    *,
    caption: str,
    source_url: str | None,
    family_share_from: str | None = None,
    annotations: list | None = None,
) -> dict:
    rel = row["output_file"]
    sha = row["sha256"]
    dest = copy_crop_to_recovered(
        Path(row["_crops_root"]), rel, sha
    )
    w, h = png_dimensions(dest)
    out: dict = {
        "source_publication_id": pub,
        "figure_number": row["figure_number"],
        "local_asset_path": str(RECOVERED / f"{sha}.png"),
        "width": w,
        "height": h,
        "caption": caption,
        "asset_sha256": sha,
        "source_original_sha256": sha,
        "source_display_sha256": sha,
        "display_rotation": 0,
        "source_geometry": {},
    }
    if source_url:
        out["source_url"] = source_url
    page = row.get("source_pdf_page")
    if page is not None:
        out["pdf_page"] = page
    if family_share_from:
        out["family_share_from"] = family_share_from
    if annotations is not None:
        out["annotations"] = annotations
    return out


def build_gate3_style_figure(pub: str, row: dict, *, caption: str, source_url: str | None) -> dict:
    rel = row["output_file"]
    sha = row["sha256"]
    dest = copy_crop_to_recovered(Path(row["_crops_root"]), rel, sha)
    w, h = png_dimensions(dest)
    out: dict = {
        "source_publication_id": pub,
        "figure_number": row["figure_number"],
        "local_asset_path": str(RECOVERED / f"{sha}.png"),
        "width": w,
        "height": h,
        "caption": caption,
        "sha256": sha,
        "display_rotation": 0,
    }
    if source_url:
        out["source_url"] = source_url
    if pub == "TW202628839A":
        out["family_share_from"] = "WO2026096517A1"
    return out


def fig_sort_key(fn: str) -> tuple[int, str]:
    m = re.match(r"Fig\.?\s*(\d+)([A-Za-z/]*)", fn, re.I)
    if not m:
        return (99999, fn)
    suffix = (m.group(2) or "").replace("/", "")
    return (int(m.group(1)), suffix)


def ingest_figures(
    report: dict,
    crops_root: Path,
    manifest_path: Path,
    align_path: Path,
) -> dict[str, int]:
    manifest_raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_pub_manifest: dict[str, list[dict]] = {}
    for row in manifest_raw:
        pub = row["publication_id"]
        row = dict(row)
        row["_crops_root"] = str(crops_root)
        by_pub_manifest.setdefault(pub, []).append(row)

    align = json.loads(align_path.read_text(encoding="utf-8"))
    align_figs = align.get("figures") or []

    counts: dict[str, int] = {}
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            if pub not in FIGURE_PUBS:
                continue
            old_figs = fam.get("figures") or []
            source_url = None
            for of in old_figs:
                if of.get("source_url"):
                    source_url = of["source_url"]
                    break
            old_by_fn = {f.get("figure_number"): f for f in old_figs}

            if pub == "US12768074B2":
                new_figs = []
                for row in align_figs:
                    mrow = next(
                        (
                            r
                            for r in by_pub_manifest[pub]
                            if r["figure_number"] == row["figure_number"]
                        ),
                        None,
                    )
                    if not mrow:
                        raise ValueError(f"manifest missing {pub} {row['figure_number']}")
                    mrow = dict(mrow)
                    mrow["_crops_root"] = str(crops_root)
                    if mrow["sha256"] != row["png_sha256"]:
                        raise ValueError(
                            f"align/manifest sha mismatch {row['figure_number']}"
                        )
                    new_figs.append(
                        build_uspto_style_figure(
                            pub,
                            mrow,
                            caption=row["caption_proposed"],
                            source_url=source_url,
                            annotations=list(row.get("annotations") or []),
                        )
                    )
                fam["figures"] = new_figs
                counts[pub] = len(new_figs)
                continue

            rows = sorted(by_pub_manifest.get(pub) or [], key=lambda r: fig_sort_key(r["figure_number"]))
            if not rows:
                raise ValueError(f"no manifest rows for {pub}")
            new_figs = []
            for row in rows:
                old = old_by_fn.get(row["figure_number"]) or {}
                if pub in ("TW202628839A", "WO2026096517A1"):
                    caption = old.get("caption") or f"{pub} {row['figure_number']}"
                    new_figs.append(
                        build_gate3_style_figure(
                            pub, row, caption=caption, source_url=source_url
                        )
                    )
                else:
                    caption = clean_caption_from_report(old.get("caption") or "")
                    if not caption:
                        raise ValueError(f"missing caption for {pub} {row['figure_number']}")
                    new_figs.append(
                        build_uspto_style_figure(
                            pub,
                            row,
                            caption=caption,
                            source_url=source_url,
                        )
                    )
            fam["figures"] = new_figs
            counts[pub] = len(new_figs)
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--crops-dir",
        type=Path,
        default=ROOT / "docs" / "evidence" / "crops-2026-10-24",
        help="Directory containing MANIFEST.json and per-pub PNG subfolders",
    )
    ap.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="MANIFEST.json (default: <crops-dir>/MANIFEST.json)",
    )
    ap.add_argument(
        "--align-json",
        type=Path,
        default=ROOT / "docs" / "evidence" / "EVIDENCE-US12768074B2-13to23-ALIGN-2026-10-25.json",
    )
    ap.add_argument(
        "--epi-rewrite",
        type=Path,
        default=ROOT / "docs" / "epi-independent-search" / "EPI-READER-REWRITE-2026-10-24.json",
    )
    ap.add_argument(
        "--preclean-rewrite",
        type=Path,
        default=ROOT / "docs" / "preclean-search" / "PRECLEAN-READER-REWRITE-2026-10-24.json",
    )
    ap.add_argument("--report", type=Path, default=ROOT / "data" / "report.json")
    args = ap.parse_args()

    crops_root = args.crops_dir.resolve()
    manifest_path = (args.manifest or crops_root / "MANIFEST.json").resolve()
    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    report = json.loads(report_path.read_text(encoding="utf-8"))

    if report.get("research_through") != "2026-10-20":
        raise SystemExit("research_through must stay 2026-10-20")
    if (report.get("counts") or {}).get("actually_read") != 6:
        raise SystemExit("counts.actually_read must stay 6")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fig_counts = ingest_figures(report, crops_root, manifest_path, args.align_json)
    reader_applied = apply_reader_patches(report, args.epi_rewrite, args.preclean_rewrite)

    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            if pub not in FIGURE_PUBS:
                continue
            for fig in fam.get("figures") or []:
                rot = fig.get("display_rotation") or 0
                if rot != 0:
                    raise SystemExit(f"{pub} {fig.get('figure_number')} display_rotation={rot} != 0")

    report.setdefault("change_history", []).append(
        {
            "at": stamp,
            "by": "serial-quality-merge-2026-10-24",
            "action": "apply_serial_quality_merge",
            "detail": (
                f"Oct24-25 package: figure ingest {fig_counts}; "
                f"reader fields {sorted(reader_applied)}; "
                "locks unchanged; display_rotation=0 upright crops"
            ),
        }
    )

    sys.path.insert(0, str(ROOT / "scripts"))
    from report_metrics import recompute_counts  # type: ignore

    recompute_counts(report)
    if report.get("research_through") != "2026-10-20":
        raise SystemExit("research_through drifted after recompute")
    if report["counts"].get("actually_read") != 6:
        raise SystemExit("actually_read drifted after recompute")

    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "figure_counts": fig_counts,
                "reader_patches": reader_applied,
                "figures_total": report["counts"].get("figures"),
                "actually_read": report["counts"].get("actually_read"),
                "research_through": report.get("research_through"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
