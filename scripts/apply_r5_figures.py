#!/usr/bin/env python3
"""Attach round-5 figures (JP2026004352A 図1/図4, US12595560B2 FIG. 1A/FIG. 14).

Usage (from repo root):
  python3 scripts/apply_r5_figures.py --src-dir <dir with the original crops> [--src-dir ...]

The crops listed below are the original source bytes (`source_original_sha256`);
only the optimized WebP display derivative is committed, keyed by its own
sha256 under assets/figures/recovered/, as with the other JP/CN/KR and
resized USPTO entries.

A pass needs the crops only for figures whose derivative is not already
committed, so the script still verifies the report against the repo once the
crops are gone.

All four crops are already upright, so `display_rotation` stays 0 and no
rotation is baked into the derivative bytes.

Does NOT touch discovery_lane, actually_read, research_through, or team_read.
Refuses to replace figures that differ from the ones recorded here.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DERIVATIVE_DIR = Path("assets/figures/recovered")
WEBP_QUALITY = 85
WEBP_METHOD = 6
# Derivatives are served at native size up to this long side (the repo already
# serves unresized USPTO derivatives up to 2646px); anything larger is
# downscaled to the long side the bulk of the USPTO derivatives use.
DISPLAY_NATIVE_LONG_SIDE_MAX = 2800
DISPLAY_DOWNSCALE_LONG_SIDE = 2000

PUBLICATIONS = {
    "JP2026004352A": {
        "source_url": "https://www.j-platpat.inpit.go.jp/c1801/PU/JP-2026-004352/15/ja",
        "source_pdf_sha256_prefix": "35e61ab15b65",
        "change_action": "attach_jplatpat_publication_figures",
        "change_detail": (
            "2 upright J-PlatPat crops (p16 図1 / p17 図4) from 公報PDF sha256 35e61ab15b65…; "
            "display_rotation=0; discovery_lane/team_read/research_through unchanged"
        ),
        "figures": [
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
        ],
    },
    "US12595560B2": {
        "source_url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12595560",
        "source_pdf_sha256_prefix": "4041a61c65c8",
        "change_action": "attach_uspto_drawing_sheet_figures",
        "change_detail": (
            "2 upright USPTO crops (p4 FIG. 1A / p19 FIG. 14) cropped 1:1 from the native CCITT "
            "scan of grant PDF sha256 4041a61c65c8…; display_rotation=0; "
            "discovery_lane/team_read/research_through unchanged"
        ),
        "figures": [
            {
                "figure_number": "FIG. 1A",
                "pdf_page": 4,
                "src_name": "US12595560B2_p04_FIG1A_native.png",
                "source_original_sha256": "a09e0e5fb06955a2dd53a09879b78d4a75c4630beec861c7f60f20439357a04a",
                "display_sha256": "f663073323ca31ab77a2cc842be435e9460cd45dfcaff6e91e4d3c87afa3f485",
                "caption": (
                    "US12595560B2（授权日2026-04-07）FIG. 1A，USPTO 当前授权原件PDF第4页（原件PDF sha256 前12位 "
                    "4041a61c65c8）。处理系统100原始附图：左侧为带灯管组（136/138）的工艺腔102与基板支撑，"
                    "经介于两者之间的气体注入组件（125/126/140/146/163）与右侧远程等离子体源104/110 耦合；"
                    "另示气源118、射频/交流电源120、真空接口与控制器180（182/184/186/188）。"
                ),
            },
            {
                "figure_number": "FIG. 14",
                "pdf_page": 19,
                "src_name": "US12595560B2_p19_FIG14_native.png",
                "source_original_sha256": "f07d74355d49d423ddab9d64f2d8c807a95d36fdaf0b318053324eee1c50abbb",
                "display_sha256": "e3720f5e86fb31ff427a885d5094a04b173eb71f4e85aa9f9a8a767720003818",
                "caption": (
                    "US12595560B2（授权日2026-04-07）FIG. 14，USPTO 当前授权原件PDF第19页（原件PDF sha256 前12位 "
                    "4041a61c65c8）。方法流程1400原始附图：将基板置于经气体注入组件与远程等离子体源流体耦合的"
                    "处理体积内（1405）→以远程等离子体源形成第一气体的等离子体（1410）→等离子体流入气体注入组件的"
                    "混合体积（1415）→经一或多个注入口向混合体积通入含氢第二气体（1420）→将第二气体解离为含原子氢的"
                    "活化气体（1425）→活化气体流入工艺腔处理体积（1430）→使基板表面暴露于活化气体（1435）。"
                ),
            },
        ],
    },
}


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def build_display_webp(src: Path) -> tuple[bytes, int, int]:
    from PIL import Image

    with Image.open(src) as im:
        im = im.convert("RGB")
        if max(im.size) > DISPLAY_NATIVE_LONG_SIDE_MAX:
            scale = DISPLAY_DOWNSCALE_LONG_SIDE / max(im.size)
            im = im.resize(
                (round(im.width * scale), round(im.height * scale)), Image.LANCZOS
            )
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=WEBP_QUALITY, method=WEBP_METHOD)
        return buf.getvalue(), im.width, im.height


def find_source(src_dirs: list[Path], name: str) -> Path:
    for directory in src_dirs:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    raise SystemExit(f"missing source crop {name}; pass its directory with --src-dir")


def resolve_figure(root: Path, pub: str, meta: dict, spec: dict,
                   src_dirs: list[Path], write_assets: bool) -> dict:
    """Return the report entry for one figure, generating the derivative if needed."""
    from PIL import Image

    dest = root / DERIVATIVE_DIR / f"{spec['display_sha256']}.webp"
    committed = dest.is_file() and sha256_bytes(dest.read_bytes()) == spec["display_sha256"]

    if committed and not write_assets:
        with Image.open(dest) as im:
            width, height = im.size
        display_sha = spec["display_sha256"]
    else:
        src = find_source(src_dirs, spec["src_name"])
        digest = sha256_bytes(src.read_bytes())
        if digest != spec["source_original_sha256"]:
            raise SystemExit(
                f"source checksum mismatch {src.name}: {digest} != {spec['source_original_sha256']}"
            )
        blob, width, height = build_display_webp(src)
        display_sha = sha256_bytes(blob)
        if write_assets:
            (root / DERIVATIVE_DIR / f"{display_sha}.webp").write_bytes(blob)
            print(f"wrote {DERIVATIVE_DIR}/{display_sha}.webp ({len(blob)} bytes, {width}x{height})")
        if display_sha != spec["display_sha256"]:
            raise SystemExit(
                f"derivative sha changed for {src.name}: {display_sha} != "
                f"{spec['display_sha256']} (libwebp build differs; rerun with --write-assets "
                "and commit the regenerated asset)"
            )

    return {
        "source_publication_id": pub,
        "figure_number": spec["figure_number"],
        "source_url": meta["source_url"],
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", type=Path, action="append", default=[],
                    help="Directory holding the original crops (repeatable)")
    ap.add_argument("--report", type=Path, default=Path("data/report.json"))
    ap.add_argument("--write-assets", action="store_true",
                    help="Regenerate the WebP derivatives instead of reusing committed ones")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    report_path = args.report if args.report.is_absolute() else root / args.report
    report = json.loads(report_path.read_text(encoding="utf-8"))

    wanted = {
        pub: [
            resolve_figure(root, pub, meta, spec, args.src_dir, args.write_assets)
            for spec in meta["figures"]
        ]
        for pub, meta in PUBLICATIONS.items()
    }

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    applied: list[str] = []
    unchanged: list[str] = []

    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            if pub not in wanted:
                continue
            figures = wanted[pub]
            current = fam.get("figures") or []
            if current == figures:
                unchanged.append(pub)
                continue
            if current:
                raise SystemExit(f"Refusing to replace unrecognized figures on {pub}")
            fam["figures"] = figures
            meta = PUBLICATIONS[pub]
            fam.setdefault("change_history", []).append(
                {
                    "at": stamp,
                    "by": "r5-figure-extract",
                    "action": meta["change_action"],
                    "detail": meta["change_detail"],
                }
            )
            applied.append(pub)

    missing = sorted(set(wanted) - set(applied) - set(unchanged))
    if missing:
        raise SystemExit("Report missing month cards for: " + ", ".join(missing))

    if applied:
        report.setdefault("change_history", []).append(
            {
                "at": stamp,
                "by": "r5-figure-extract",
                "action": "apply_r5_figures",
                "detail": (
                    "R5 original drawings attached for " + ", ".join(sorted(applied)) +
                    "; actually_read/research_through/discovery_lane untouched by design"
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
                "applied": sorted(applied),
                "already_present": sorted(unchanged),
                "figures_total": report["counts"].get("figures"),
                "actually_read": report["counts"].get("actually_read"),
                "research_through": report.get("research_through"),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
