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
| Multi-figure grid | `.patent-fig-grid` 2-col desktop; 3-up last row centered; 1-col ≤760px |
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

**Merge SHA:** _(fill on merge)_  
**Live stamp:** _(verify index.html after Pages deploy)_
