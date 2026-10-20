# Quality run R2 — 2026-10-20

**Plan:** `docs/QUALITY_IMPROVEMENT_PLAN.md`  
**Dot reference:** https://45-32-39-201.sslip.io:8443/patent-alert/report.html (TLS OK from cloud agent, HTTP 200)  
**Pages:** https://chuqonu.github.io/epi-preclean-patent-monitor/  
**Prior round:** `docs/quality-runs/2026-10-20-r1/`

**Policy:** Gate③ WO/TW Fig.2 bytes + `display_rotation=0` on live `report.json?v=5423b7abc03a` — **do not reopen** figures/rotation unless regression.

## R2 scope (this PR)

| Item | Change |
|------|--------|
| Month chrome | Card-style month rows; YYYY-MM split label; status chip; 44px summary targets |
| Multi-figure grid | `.patent-fig-grid` 2-col (2 figs) / **3 equal cols** (3 figs); no max-height crop; caption row-gap |
| Side-meta | Edition line + 2×2 stat grid (截至 / 条目 / 已读 / 附图可载) |
| Mobile drawer | Safe-area padding; sticky「目录」; backdrop dismiss; `pointer-events` fix @390px |
| Data | `change_history` UX note only — no figure or rotation edits |

## Out of scope

- `display_rotation` logic / PNG assets / CN figures
- Dot pixel-perfect clone (reference only)

## Verify

```bash
python3 scripts/audit_data_integrity.py   # stamps index.html ?v=
# Optional: python3 -m http.server 8765 && ./scripts/capture_quality_screenshots.sh
```

## Sign-off

- [x] E–F R2 layout items above
- [x] G cache-bust CSS/JS (+ report.json history bump)
- [x] Gate③ fig2 regression: sha `77e2a152…`, rot `0` unchanged

**Stamps (pre-merge):** `report.json?v=08c93d605895`, `report.css?v=3260c9f82342`, `report.js?v=e0a80aa03cee`

## R2 design major — WO/TW 3-up grid (@1440)

| Before | After |
|--------|--------|
| `.fig-media` `max-height: min(52vh, 420px)` cropped tall patent sheets | Full-height `contain`; `aspect-ratio` box overridden in grid only |
| Fig.3 spanned 2 cols, narrower/wider than Fig.1/2 | Three **equal** columns on desktop |
| Fig.1 caption「来源」wrapped into Fig.3 cell | Per-cell flex column + **22px** row-gap; caption stays under its figure |

CSS-only; Gate③ WO/TW bytes + `display_rotation=0` unchanged. Month TOC / side-meta untouched.

**Merge SHA:** `fe6955e` (R2 layout) + fig-grid follow-up PR  
**Live CSS:** bump `report.css?v=` on merge (see `index.html`)
