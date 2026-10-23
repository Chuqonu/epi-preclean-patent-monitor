#!/usr/bin/env python3
"""Attach JP2026004352A figures (図1、図4) to data/report.json.

Usage (from repo root):
  python3 scripts/apply_r5_jp_figures.py --src-dir <dir with the 300dpi crops>

The 300dpi PNG crops are the original source bytes (`source_original_sha256`);
only the optimized WebP display derivative is committed, keyed by its own
sha256 under assets/figures/recovered/, as with the other JP/CN/KR entries.

Crops are already upright, so `display_rotation` stays 0 and no rotation is
baked into the derivative bytes.

Does NOT touch discovery_lane, actually_read, research_through, or team_read.
Refuses to overwrite a non-empty figures array.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PUB = "JP2026004352A"
SOURCE_URL = "https://www.j-platpat.inpit.go.jp/c1801/PU/JP-2026-004352/15/ja"
SOURCE_PDF_SHA256_PREFIX = "35e61ab15b65"
DERIVATIVE_DIR = Path("assets/figures/recovered")
WEBP_QUALITY = 85
WEBP_METHOD = 6
DISPLAY_LONG_SIDE_MAX = 2000

FIGURES = [
    {
        "figure_number": "図1",
        "pdf_page": 16,
        "src_name": "JP2026004352A_p16_zu1_300dpi.png",
        "source_original_sha256": "4af7a32305eedafec2d606804f48b9d2adb52728c1f3a95c57d8f5f37ccc3cbf",
        "display_sha256": "31ab7d533d9e70bab77c84310789035629e4ae0ff96dc5a179ce1450292c937a",
        "caption": (
            "JP2026004352A（公开日2026-01-14）図1，J-PlatPat 公開特許公報原件第16页（公报PDF sha256 前12位 "
            "35e61ab15b65）。集群工具100俯视原始附图：上下两段主框架各设中央搬运机器人与周围多边形腔体，"
            "下部为装载腔与工厂接口102（含晶圆载具），右侧为控制器190（CPU 192、メモリ 194、サポート回路 196）。"
        ),
    },
    {
        "figure_number": "図4",
        "pdf_page": 17,
        "src_name": "JP2026004352A_p17_zu4_300dpi.png",
        "source_original_sha256": "2574e47c0b8df65c668b9f4bbd073511762b3f2e26c8b396635c8ffc2370e9de",
        "display_sha256": "6c17a40d1a5bd9ea41e06b84bb703a5be43611dbcb94eadaf066180d8778345c",
        "caption": (
            "JP2026004352A（公开日2026-01-14）図4，J-PlatPat 公開特許公報原件第17页（公报PDF sha256 前12位 "
            "35e61ab15b65）。方法流程400原始附图：工厂接口放置基板（403）→送入第一腔室第一处理空间（405）→"
            "维持第一压力下处理（407）→压力安定化腔维持第一压力（409）→经第一门送入压力安定化腔（411）→"
            "关闭第一门（413）→升压至700–800 Torr大气压（415）→开启第二门（417）→送入外延堆积腔第二处理空间（419）→"
            "在大气压及摄氏400–1200度下进行外延堆积（421）。"
        ),
    },
]


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def build_display_webp(src: Path) -> tuple[bytes, int, int]:
    from PIL import Image

    with Image.open(src) as im:
        im = im.convert("RGB")
        if max(im.size) > DISPLAY_LONG_SIDE_MAX:
            scale = DISPLAY_LONG_SIDE_MAX / max(im.size)
            im = im.resize(
                (round(im.width * scale), round(im.height * scale)), Image.LANCZOS
            )
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=WEBP_QUALITY, method=WEBP_METHOD)
        return buf.getvalue(), im.width, im.height


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", type=Path, required=True)
    ap.add_argument("--report", type=Path, default=Path("data/report.json"))
    ap.add_argument(
        "--write-assets",
        action="store_true",
        help="Regenerate the WebP derivatives instead of reusing committed ones",
    )
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    report_path = args.report if args.report.is_absolute() else root / args.report
    report = json.loads(report_path.read_text(encoding="utf-8"))

    figures = []
    for spec in FIGURES:
        src = args.src_dir / spec["src_name"]
        if not src.is_file():
            raise SystemExit(f"missing source crop: {src}")
        digest = sha256_bytes(src.read_bytes())
        if digest != spec["source_original_sha256"]:
            raise SystemExit(
                f"source checksum mismatch {src.name}: {digest} != {spec['source_original_sha256']}"
            )

        blob, width, height = build_display_webp(src)
        display_sha = sha256_bytes(blob)
        dest = root / DERIVATIVE_DIR / f"{display_sha}.webp"
        if args.write_assets:
            dest.write_bytes(blob)
            print(f"wrote {dest.relative_to(root)} ({len(blob)} bytes, {width}x{height})")
        elif display_sha != spec["display_sha256"]:
            raise SystemExit(
                f"derivative sha changed for {src.name}: {display_sha} != "
                f"{spec['display_sha256']} (libwebp build differs; rerun with --write-assets "
                "and commit the regenerated asset)"
            )
        if not dest.is_file():
            raise SystemExit(f"missing committed derivative: {dest.relative_to(root)}")

        figures.append(
            {
                "source_publication_id": PUB,
                "figure_number": spec["figure_number"],
                "source_url": SOURCE_URL,
                "local_asset_path": str(DERIVATIVE_DIR / f"{display_sha}.webp"),
                "width": width,
                "height": height,
                "caption": spec["caption"],
                "asset_sha256": display_sha,
                "source_original_sha256": spec["source_original_sha256"],
                "source_display_sha256": display_sha,
                "pdf_page": spec["pdf_page"],
                "display_rotation": 0,
                "source_geometry": {},
            }
        )

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    applied = False
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            if fam.get("publication_id") != PUB:
                continue
            if fam.get("figures"):
                raise SystemExit(f"Refusing to overwrite non-empty figures on {PUB}")
            fam["figures"] = figures
            fam.setdefault("change_history", []).append(
                {
                    "at": stamp,
                    "by": "r5-jp-figure-extract",
                    "action": "attach_jplatpat_publication_figures",
                    "detail": (
                        f"{len(figures)} upright J-PlatPat crops (p16 図1 / p17 図4) from 公報PDF "
                        f"sha256 {SOURCE_PDF_SHA256_PREFIX}…; display_rotation=0; "
                        "discovery_lane/team_read/research_through unchanged"
                    ),
                }
            )
            applied = True

    if not applied:
        raise SystemExit(f"Report has no month card for {PUB}")

    report.setdefault("change_history", []).append(
        {
            "at": stamp,
            "by": "r5-jp-figure-extract",
            "action": "apply_r5_jp_figures",
            "detail": (
                f"{PUB} 図1/図4 from J-PlatPat publication gazette; "
                "actually_read/research_through/discovery_lane untouched by design"
            ),
        }
    )

    sys.path.insert(0, str(root / "scripts"))
    from report_metrics import recompute_counts  # type: ignore

    recompute_counts(report)
    if report.get("research_through") != "2026-10-20":
        raise SystemExit("research_through drifted from 2026-10-20")
    if report["counts"].get("actually_read") != 6:
        raise SystemExit("actually_read drifted from 6")

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "publication": PUB,
                "figures_added": len(figures),
                "figures_total": report["counts"].get("figures"),
                "actually_read": report["counts"].get("actually_read"),
                "research_through": report.get("research_through"),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
