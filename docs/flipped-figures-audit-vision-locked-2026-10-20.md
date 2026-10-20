# Flipped figures audit — GitHub Pages live stamp

- **Live report:** `https://chuqonu.github.io/epi-preclean-patent-monitor/data/report.json?v=7c388ebf1040`
- **Index meta:** `data/report.json?v=7c388ebf1040` from `index.html` meta `epi-report-data`
- **Audit time:** 2026-10-20 ~23:38 Asia/Shanghai
- **Scope:** Chuqonu/epi-preclean-patent-monitor Pages only (no Dot/VPS changes)
- **Method:** Vision review of figure-body crops (header stripped). Tesseract OSD used only as a hunt signal — **not** for final classification (many false positives).
- **Live fact:** all figures currently have `display_rotation=0` (including ones Dot still marks 90).
- **Rule:** `display_rotation` is CSS-only; do **not** also bake a second rotation into bytes. Prefer upright bytes + `rot=0` when re-exporting.

## Summary

- **Vision-confirmed sideways assets:** 9 unique PNGs / **9** live figure rows
- **Recommended:** set `display_rotation=90` (or re-export 90° CW + `display_rotation=0`)
- **Not flipped (controls / parent overrides):** WO/TW Fig.2, other same-dim upright sheets, OSD false positives

## Vision-confirmed FIX list (sideways → need 90° CW)

| pub | fig | sha256 (asset) | path | w×h | current `display_rotation` | recommended | reason |
|---|---|---|---|---|---|---|---|
| US12757647B2 | 图4：用于晶面选择性生长的底部与侧壁表面 | `e5d5f61dac3d4b7a2f379004b3c3e15445c20416f436919f3615fb16546cb288` | `assets/figures/recovered/e5d5f61dac3d4b7a2f379004b3c3e15445c20416f436919f3615fb16546cb288.png` | 1397×1800 | 0 | **90** (or re-export CW + 0) | Vision: USPTO portrait sheet; header upright; FIG.4 label+callouts landscape. Need 90° CW for upright reading. |
| US12740346B2 | 图7：选择性沉积系统、气源和控制器 | `39e66689f3d4ed987e3f3562b40eb24e6b030314892baf2029b0f8a1cab74603` | `assets/figures/recovered/39e66689f3d4ed987e3f3562b40eb24e6b030314892baf2029b0f8a1cab74603.png` | 1397×1800 | 0 | **90** (or re-export CW + 0) | Vision: same pattern; FIG.7 + callouts sideways on portrait sheet. |
| US12701931B2 | 图4：底部与侧壁掺磷层上的本征盖层 | `22dbc8e9baf1a3e5c7e6efed68b2bc752517f8a1fe47b87a0cd020d0ece5acae` | `assets/figures/recovered/22dbc8e9baf1a3e5c7e6efed68b2bc752517f8a1fe47b87a0cd020d0ece5acae.png` | 1397×1800 | 0 | **90** (or re-export CW + 0) | Vision: same pattern; FIG.4 + callouts sideways on portrait sheet. |
| US20260164725A1 | FIGS. 20C–20D | `d0af11401052ea68bfa12e42f563bfbb40a029ee5e09dee02c2ba60aab2ad4b0` | `assets/figures/recovered/d0af11401052ea68bfa12e42f563bfbb40a029ee5e09dee02c2ba60aab2ad4b0.png` | 1800×2320 | 0 | **90** (or re-export CW + 0) | Vision: FIGS.20C/20D labels+callouts landscape on portrait sheet. |
| US20260150594A1 | 图4：带硅源、掺杂源供气和控制器的外延腔室 | `8533597a17f700dfd505913f5ae521fb21245098c68b10c38a4b2d7bfe6ec363` | `assets/figures/recovered/8533597a17f700dfd505913f5ae521fb21245098c68b10c38a4b2d7bfe6ec363.png` | 1707×2200 | 0 | **90** (or re-export CW + 0) | Vision: chamber drawing + FIG.4 label sideways on portrait sheet. |
| US12595587B2 | 图1：多片衬底交替沉积脉冲流程 | `11ec9fb5bbc7be2be3301d79afb8cb1faaba6ac3c6d44dffd94c2e9efe551b9a` | `assets/figures/recovered/11ec9fb5bbc7be2be3301d79afb8cb1faaba6ac3c6d44dffd94c2e9efe551b9a.png` | 1707×2200 | 0 | **90** (or re-export CW + 0) | Vision: flowchart text sideways on portrait sheet. |
| US20260035835A1 | 图2–5：从衬底至SiGe:B源漏接触层结构 | `1516cae0ee73967b9d353b67b29a75de9ddcb5f972180baf1fd1c1146609bfd8` | `assets/figures/recovered/1516cae0ee73967b9d353b67b29a75de9ddcb5f972180baf1fd1c1146609bfd8.png` | 1707×2200 | 0 | **90** (or re-export CW + 0) | Vision: layer-stack labels (SUBSTRATE etc.) sideways on portrait sheet. |
| US20260026275A1 | FIG. 8A | `f77056a140d3fcb39e80b46e7015030ebcaf5b9756af42984a4dc9ee59b52443` | `assets/figures/recovered/f77056a140d3fcb39e80b46e7015030ebcaf5b9756af42984a4dc9ee59b52443.png` | 1800×2320 | 0 | **90** (or re-export CW + 0) | Vision: FIG.8A + callouts sideways on portrait sheet. |
| US20260026275A1 | FIG. 9 | `3f06f16dabb38600dc59c52de04efccc3277ece9207f0b8a004e0ff9abce7175` | `assets/figures/recovered/3f06f16dabb38600dc59c52de04efccc3277ece9207f0b8a004e0ff9abce7175.png` | 1800×2320 | 0 | **90** (or re-export CW + 0) | Vision: FIG.9 + callouts sideways on portrait sheet. |

### Preferred remediation

1. **Preferred:** re-export each of the 9 PNG assets rotated **90° clockwise**, update `width`/`height` (swap), keep `display_rotation=0`, refresh `asset_sha256` / display sha fields.
2. **Dot-parity alternative:** leave bytes unchanged; set `display_rotation=90` (and `source_geometry.display_rotation=90` if present) on every live figure row pointing at these shas. Renderer already supports CSS rot + layout swap.
3. **Never both.** Do not rotate bytes and also set `display_rotation=90`.

### Dot corroboration

Dot extract (`dot-figure-annotations-extract.json`) marks exactly these **9 unique shas** with `display_rotation=90` (11 figure refs counting family duplicates). Live Pages zeroed them (likely `fix_display_rotation_flags.py` clearing portrait `rot=90` under the mistaken assumption that portrait bytes are always upright).

## Same-dimension cohort controls (vision: upright — keep `display_rotation=0`)

| pub | fig | note |
|---|---|---|
| US20260313994A1 | Fig.14–16 | 1397x1800 same cohort; FIG labels+axes upright |
| US20260250878A1 | Fig.3、Fig.4A | 1397x1800 same cohort; MEASUREMENT UNIT text upright |
| US12680191B2 | 图1、2 | 1707x2200; FIG.1/2 upright |
| US12543516B2 | 图1 | 1707x2200; Fig.1 upright |
| WO2026096517A1 | Fig. 1 | parent+vision: upright chamber cross-section |
| WO2026096517A1 | Fig. 2 | parent/design ruled upright; do NOT set rot=90 |
| TW202628839A | Fig. 2 | same asset as WO Fig.2; upright per parent |
| US20250351329A1 | Fig. 2 | vision: landscape chamber upright; OSD FP |
| US20250037997A1 | FIG. 1a | vision: upright stack; OSD FP |
| WO2025222891A1 | Fig.7/8 | parent: upright |

## Explicit non-fixes / false leads

| item | why excluded |
|---|---|
| WO2026096517A1 / TW202628839A Fig. 2 | Parent + design ruling: upright portrait true PNGs; earlier `rot=90` caused live FAIL. Vision of body crop was ambiguous; **do not flip**. |
| WO Fig. 1 / Fig. 3 | Vision upright. |
| OSD hits on US20250351329A1 Fig.2, US20250037997A1 FIG.1a, US20260282506A1, flowcharts, WO2025222891 Fig.7/8 | Vision upright; OSD false positives. |
| Historical acceptance note that US12757647B2 Fig.4 was “正立” at `rot=0` | That meant “no CSS double-rotate”; figure *content* is still landscape-on-portrait and reads sideways without `rot=90`. |
| EXIF Orientation | None of the audited assets had non-normal EXIF orientation. |
| `extraction_rotation` | Not present on live figure records; do not invent. |

## Spot-check of `display_rotation=0` figures (not sideways)

Sampled upright portraits/landscapes with vision: US12765027B2 Fig.3C/3D, US12680191B2 Fig.1–2, US12543516B2 Fig.1, US20260313994A1 Fig.14–16, US20260250878A1 Fig.3/4A, US20250351329A1 Fig.2, WO2026096517A1 Fig.1. No additional flips found in that sample beyond the 9-sha set above.

## Counts

- Live figures total: 143
- Live `display_rotation != 0`: **0**
- Vision-confirmed flipped (unique assets): **9**
- Live rows to update: **9**

## PR checklist

- [ ] Update the 9 assets (bytes **or** `display_rotation`, not both)
- [ ] Mirror on all family-shared rows using the same `asset_sha256`
- [ ] Do not touch Dot/VPS
- [ ] After Pages deploy: visual check that FIG labels read horizontally for the 9 pubs above
- [ ] Confirm WO/TW Fig.2 still upright with `rot=0`
