# PATCH_NOTES — Track A figure extraction evening R4 (2026-10-22)

Prepared: 2026-10-22 20:44 Asia/Shanghai
Workdir: `/workspace/epi-figure-r4e/`
Live stamp baseline: `json?v=09d94cf54a4e` (css f60b87bf5c39 / js 0188acb4620b)

## Status
- Extraction: **PASS** for both pubs (real USPTO drawing sheets; no placeholders).
- Assets: **PR-ready** under `assets/figures/recovered/<sha256>.png` (21 PNGs, ~29.9 MB).
- CloudAgent **new launch region-blocked** — parent should apply via owned CloudAgent **reply** OR open a later PR from these box paths.
- Tooling used: `pdftoppm`/`pdfimages` (poppler-utils already present). No pymupdf/tesseract install required for the packaged assets.

## PDF provenance (distinct from OG/html `source_sha256`)

| Pub | PDF sha256 | bytes | pages | drawing sheets | PDF pages |
|---|---|---:|---:|---:|---|
| US12770834B2 | `c8ed1f7d1f7e8748193ac17e0525a1755c7110f6234f1da4955ddc13a69c9ff8` | 1343387 | 20 | 8 | 3,4,5,6,7,8,9,10 |
| ↳ report OG/html `source_sha256` (unchanged) | `b450484e367e7ffb87193cd5f9afc1c518bc3772a673237b98b5ec5a3a69e905` | — | — | — | — |
| US12768074B2 | `4cbc348afd28f58ed9ad2d188100fea936e124c69babd1d2cb5dcf4e9c11c3e8` | 2473309 | 32 | 13 | 4,5,6,7,8,9,10,11,12,13,14,15,16 |
| ↳ report OG/html `source_sha256` (unchanged) | `1b3a430b875c535db049a337a84824e52d3b56ba4e91ef4985551a80d3975739` | — | — | — | — |

Source URLs:
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12770834
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12768074

## Locks / non-goals (do not touch)
- `counts.actually_read` **stays 6**
- `research_through` **stays `2026-10-20`**
- Sept 2025 still paused
- `team_read` / `team_independent_read` lock **untouched**
- Do **not** rewrite OG/html `source_sha256` / `source_retrieved_at` / `actual_read_spans` unless a separate evidence lane asks
- `display_rotation` only in JSON; **never** re-encode pixels to bake rotation (`extraction_rotation` already in sheet bytes if any — we did not apply a second bake)

## counts.figures delta
- before (live): **170**
- add: **21** (US12770834B2 **8** + US12768074B2 **13**)
- after (if applied + `recompute_counts`): **191**
- Both cards currently have `figures: []` on live main.

## Exact JSON patch per family

Locate each card under `months[].families[]` by `publication_id` (month `2026-10`).
**Refuse overwrite** if `figures` is already non-empty.

Set:
```json
{ "figures": [ /* see MANIFEST.json → publications.<PUB>.proposed_report_figures */ ] }
```

Append one `change_history` entry per card:
```json
{
  "at": "<UTC ISO Z now>",
  "by": "evening-r4-figure-extract",
  "action": "attach_uspto_drawing_sheet_figures",
  "detail": "Track A evening R4: N real USPTO drawing-sheet PNGs from image-ppubs PDF; team_read lock unchanged"
}
```

Also append a top-level `change_history` entry summarizing both pubs.
Then run `scripts/report_metrics.recompute_counts` (or equivalent) and `scripts/stamp_asset_versions.py` so `index.html` gets a new `report.json?v=` hash.

### US12770834B2
- `family_id`: `FAM-ASM-PE-EPI-CVD-RPU-QUARTZ`
- card `id`: `2026-10-US12770834B2`
- replace `figures: []` with **8** objects:

| figure_number | pdf_page | sheet | WxH | display_rotation | asset_sha256 (12) | local_asset_path |
|---|---:|---|---|---:|---|---|
| Fig. 1 | 3 | Sheet 1 of 8 | 5334×6875 | 0 | `0b17e7adebe1…` | `assets/figures/recovered/0b17e7adebe16eafdf837da0be2ae119d1dc99d7846a23b07eaed04604c56805.png` |
| Fig. 2 | 4 | Sheet 2 of 8 | 5334×6875 | 0 | `d9b4cc35724a…` | `assets/figures/recovered/d9b4cc35724a2a6b4276890f3180df4915412f6ffb4790483d82c02693ec7f49.png` |
| Fig. 3 | 5 | Sheet 3 of 8 | 5334×6875 | 0 | `396157ff8ed9…` | `assets/figures/recovered/396157ff8ed9a4e951779287ff1c60073778de125da45b025f31a931d75a5ee5.png` |
| Fig. 4A | 6 | Sheet 4 of 8 | 5334×6875 | 90 | `71edce7844a5…` | `assets/figures/recovered/71edce7844a5ff9b08186ee6f3f1cf88f48a2a6214c36f2238654a92f0170546.png` |
| Fig. 4B | 7 | Sheet 5 of 8 | 5334×6875 | 90 | `307e7872aeab…` | `assets/figures/recovered/307e7872aeaba1ac056c0248544d0f627931d3d5790c553953d09d958eebaf0b.png` |
| Fig. 5 | 8 | Sheet 6 of 8 | 5334×6875 | 0 | `310d513c0040…` | `assets/figures/recovered/310d513c00400e1961ef43c83636010100a9ac5725432dcd64a8714ca8817e5c.png` |
| Fig. 6 | 9 | Sheet 7 of 8 | 5334×6875 | 0 | `ab4d3e43e85f…` | `assets/figures/recovered/ab4d3e43e85f9cd9502d534b7074ccdd840a2abf3e2fb079a22fe82ea644d679.png` |
| Fig. 7 | 10 | Sheet 8 of 8 | 5334×6875 | 0 | `23c85f50b2cc…` | `assets/figures/recovered/23c85f50b2cce358189dbcf63622c846dbe3914e82ac6ab2656a974252353a84.png` |

Schema fields per object (match Gate③ / recovered sample):
`source_publication_id`, `figure_number`, `source_url`, `local_asset_path`, `width`, `height`, `caption`,
`asset_sha256`, `source_original_sha256`, `source_display_sha256`, `pdf_page`, `display_rotation`, `source_geometry` ({}).
No `annotations` block (leave absent; Dot labels are a separate lane).

### US12768074B2
- `family_id`: `FAM-AMAT-EPI-CHAMBER-ARCH-CONT-US12060651`
- card `id`: `2026-10-US12768074B2`
- replace `figures: []` with **13** objects:

| figure_number | pdf_page | sheet | WxH | display_rotation | asset_sha256 (12) | local_asset_path |
|---|---:|---|---|---:|---|---|
| Fig. 1 | 4 | Sheet 1 of 13 | 5334×6875 | 0 | `77cfda679381…` | `assets/figures/recovered/77cfda6793810f68833040dd064ed18fedea53e6f01a9dbffe871ededada1d02.png` |
| Fig. 2A/2B/2C | 5 | Sheet 2 of 13 | 5334×6875 | 0 | `6bdabb7cc2d5…` | `assets/figures/recovered/6bdabb7cc2d50e1baeaedad10ea61a72073ba433edfdbb3854a10c0a1e60fe1a.png` |
| Fig. 3A/3B/3C | 6 | Sheet 3 of 13 | 5334×6875 | 0 | `2b77f4b4c63d…` | `assets/figures/recovered/2b77f4b4c63d01df16bc3a37946ebafc4e551533d7f0f1af74e0ceb183ff23ec.png` |
| Fig. 4A | 7 | Sheet 4 of 13 | 5334×6875 | 0 | `03fc2da10b8a…` | `assets/figures/recovered/03fc2da10b8ad6a8ab9fe879faf907224625be1b6e3f26ed3383556b8c7951db.png` |
| Fig. 4B | 8 | Sheet 5 of 13 | 5334×6875 | 90 | `44210a17cd91…` | `assets/figures/recovered/44210a17cd9175cd6321bef359d6b856fb03a5ae1041bcb4b3e6ef2f3dea6924.png` |
| Fig. 4C/4D/4E | 9 | Sheet 6 of 13 | 5334×6875 | 0 | `ba99e0e110c6…` | `assets/figures/recovered/ba99e0e110c637fa099a9604aa3a2d93b3b434680fa7fec96066542c21eff2ae.png` |
| Fig. 5A/5B | 10 | Sheet 7 of 13 | 5334×6875 | 0 | `253a6f49a2cf…` | `assets/figures/recovered/253a6f49a2cf1851e975fb747f5c71c4273c1248a2e111aca0a5d1231b1bd1a6.png` |
| Fig. 6A/6B | 11 | Sheet 8 of 13 | 5334×6875 | 0 | `c0fdb78c0bc4…` | `assets/figures/recovered/c0fdb78c0bc4384baecf737c6f52d04aa055d47ec8b55f5be7b07e021c91d120.png` |
| Fig. 7 | 12 | Sheet 9 of 13 | 5334×6875 | 0 | `a247a234ba74…` | `assets/figures/recovered/a247a234ba744df1e8634cba7dd42ecd1bd8d4b886a3be7f21131ee88bac76c0.png` |
| Fig. 8A/8B | 13 | Sheet 10 of 13 | 5334×6875 | 0 | `e7d7a6d8929f…` | `assets/figures/recovered/e7d7a6d8929f51937b29f9fa0d545df390e6e911453b452cad778eb7f6168a5f.png` |
| Fig. 9 | 14 | Sheet 11 of 13 | 5334×6875 | 0 | `6708fd0ced14…` | `assets/figures/recovered/6708fd0ced1466dad7486d6d29567faf92c14f39f35d5cc7d32357ea862eeef3.png` |
| Fig. 10A | 15 | Sheet 12 of 13 | 5334×6875 | 0 | `2adc9c8b3c35…` | `assets/figures/recovered/2adc9c8b3c35e8fa59070f8ced979bec684d3651f814618def5502fb3ff2d35b.png` |
| Fig. 10B/10C | 16 | Sheet 13 of 13 | 5334×6875 | 0 | `9d99da5d3e4c…` | `assets/figures/recovered/9d99da5d3e4c2071df116a29e0a2500b65c6240a33c5dfadf0bdce94f3e1d936.png` |

Schema fields per object (match Gate③ / recovered sample):
`source_publication_id`, `figure_number`, `source_url`, `local_asset_path`, `width`, `height`, `caption`,
`asset_sha256`, `source_original_sha256`, `source_display_sha256`, `pdf_page`, `display_rotation`, `source_geometry` ({}).
No `annotations` block (leave absent; Dot labels are a separate lane).

## Copy into repo (for PR / CloudAgent reply)

```text
box: /workspace/epi-figure-r4e/assets/figures/recovered/*.png
  → repo: assets/figures/recovered/<same sha256>.png
box: /workspace/epi-figure-r4e/MANIFEST.json
  → optional docs/: docs/EPI-FIGURE-R4E-EVENING-2026-10-22-MANIFEST.json
box: /workspace/epi-figure-r4e/apply_evening_r4e_figures.py
  → optional scripts/: scripts/apply_evening_r4e_figures.py
```

Suggested CloudAgent reply prompt:
> Copy `/workspace/epi-figure-r4e/assets/figures/recovered/*.png` into `assets/figures/recovered/`.
> Run `/workspace/epi-figure-r4e/apply_evening_r4e_figures.py` against `data/report.json` (or port the script into the repo).
> Recompute counts + stamp asset versions. Do not bump `actually_read` or `research_through`. Open PR; do not squash-merge until evidence/PM PASS.

## Rotation notes
- US12770834B2: `display_rotation=90` on Fig.4A, Fig.4B (landscape bodies on portrait USPTO sheets); Fig.1 is **0** (evidence PASS: raster already upright).
- US12768074B2: `display_rotation=90` on Fig.4B only; others 0.
- Renderer must honor `display_rotation` and reserve swapped WxH for 90/270.

## Blockers
- CloudAgent **new** launches region-blocked (parent already aware); use reply-to-owned-agent or later PR.
- Google Patents HTML 404 for these 2026-10-20 grants (expected freshness); captions taken from USPTO PDF BRIEF DESCRIPTION pages via vision, not fabricated.
- tesseract not in apt cache on this box; not needed once vision-labeled.

