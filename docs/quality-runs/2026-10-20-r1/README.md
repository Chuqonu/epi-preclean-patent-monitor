# Quality run R1 — 2026-10-20

**Plan:** `docs/QUALITY_IMPROVEMENT_PLAN.md`  
**Dot reference:** https://45-32-39-201.sslip.io:8443/patent-alert/report.html  
**Pages:** https://chuqonu.github.io/epi-preclean-patent-monitor/  
**Dot vs ours:** `dot-gaps.md`

## R1 delivered (this PR)

| Item | Status |
|------|--------|
| Baseline 130 figures on live | Done (`6913c58` lineage; verify script 130/130) |
| Mobile TOC drawer | `toc-drawer-toggle` + off-canvas `#side-panel` |
| Desktop colgroup / no top strip | Prior + cache-bust on `main` |
| Viewport artifacts | `viewports/`, `pages-live/`, `dot-reference/` |
| Sprint docs | `QUALITY_IMPROVEMENT_PLAN.md`, `SPRINT-KICKOFF-NOTES.md` |

## Artifacts

| Path | Description |
|------|-------------|
| `viewports/local-*.png` | Repo static server @ merge SHA |
| `pages-live/github-*.png` | Live GitHub Pages (1440 / 768 / 390) |
| `dot-reference/dot-1440.png` | Dot benchmark |

Regenerate: `python3 -m http.server 8765` then `./scripts/capture_quality_screenshots.sh`.

## Sign-off (A–G spot-check)

- [x] A–D data/figures/ledger (prior merges)
- [x] E–F layout R1 scope (drawer + colgroup + footer stats)
- [x] G cache-bust URLs (stamp on publish)

**Merge SHA:** _(set on merge)_
