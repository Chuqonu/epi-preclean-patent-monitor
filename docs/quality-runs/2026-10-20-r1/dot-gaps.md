# Dot A/B gap log — R1 (2026-10-20)

**Reference:** https://45-32-39-201.sslip.io:8443/patent-alert/report.html  
**Ours:** https://chuqonu.github.io/epi-preclean-patent-monitor/

TLS: reachable from cloud build (HTTP 200). No user action required for benchmark capture.

| Area | Dot | Ours (after R1) | Round |
|------|-----|-----------------|-------|
| First screen | Patent title + fields immediately | Title above table; stats only in collapsed「报告信息」footer | R1 ✓ |
| Label column | Fixed narrow labels | `clamp(110px,18%,140px)` desktop; `clamp(84px,22%,100px)` mobile; nested `.events` `table-layout:auto` | R1 B ✓ |
| Sidebar mobile | Collapsible / full-width read | Off-canvas drawer via「目录」; backdrop + Esc | R1 ✓ |
| Asset cache | N/A (their host) | Content-hash `?v=` on CSS/JS + meta JSON URL | R1 ✓ |
| Baseline figures | Embedded | 130/130 recovered paths live; 9× `display_rotation=90` | Done (separate PR) |
| Month chrome | Rich month headers / badges | Plain `<details>` month rows | R2 |
| Figure grid | Tighter multi-fig rows | Single-column fig stack | R2 |
| Side meta | Edition + date prominence | Compact `side-meta` | R2 |
| Search UX | (reference TOC filter) | `toc-search` on publication/title | Parity ≈ |

Gate③ new figureless independents remain separate from the baseline 130 restore.
