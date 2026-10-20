# Quality improvement plan — EPI / Preclean patent monitor

**Owner:** 总经理（accountable for outcomes; agents/teammates execute in parallel, not as a substitute for ownership）  
**Window:** 2026-10-20 → **2026-10-23 evening** (final delivery checkpoint)  
**Dot benchmark:** https://45-32-39-201.sslip.io:8443/patent-alert/report.html  
**Live Pages:** https://chuqonu.github.io/epi-preclean-patent-monitor/

## Correction (persistent policy)

**Content expansion does NOT pause** while layout/mobile/perf work proceeds. Two tracks run **in parallel** until the evening of 2026-10-23:

| Track | Scope | Does NOT wait on |
|-------|--------|------------------|
| **A — Content** | EPI/Preclean search, evidence review, new figures, `data/report.json` + `ledger/patents.xlsx` | UI sign-off |
| **B — Layout / mobile / perf** | Reader UX vs Dot reference, drawer, colgroup, cache-bust, viewport QA | Research backlog size |

**Serial publish lock:** Only one canonical `data/report.json` version on `main` at a time. Merge order: **content + layout fixes → `python3 scripts/build_xlsx.py` → `python3 scripts/audit_data_integrity.py` (stamps assets) → push `main` → Pages deploy.** No force-push; no old branch overwriting newer patents. Weekly Grok `epi` / monthly `epi-2` routines stay configured but must respect the same lock (do not publish stale SHAs over fresher `main`).

**September 2025-09:** month remains **paused** (no search/review/publish for that month only). This is not a freeze on other months or on Track A expansion.

**Evidence:** No fabricated reads, hashes, or figures. `team_read` stays locked per `docs/EVIDENCE-READ-RULING-COMBINED-2026-10-20.json`.

**Quiet comms:** Ping the user only for **login / permission blockers** or **final delivery** (2026-10-23 evening). Progress lives in repo docs and `docs/quality-runs/`.

## Hard acceptance (A–G)

| ID | Gate | Pass criteria |
|----|------|----------------|
| **A** | Data version | Single `main` SHA; `publication_events` = deduped unique publication IDs; month cards scoped correctly |
| **B** | Team read | `actually_read` = 4 with per-entry evidence (`EPI-EVIDENCE-SUPPLEMENT`); 5 independents `included_not_team_read` |
| **C** | Figures | `restore_reference_figures.py --check` exit 0; 130 refs loadable; `display_rotation` honored (no second `extraction_rotation`) |
| **D** | Ledger | `ledger/patents.xlsx` rebuilt from canonical JSON; disposition / pending columns present |
| **E** | Desktop layout | No top count strip on first screen; patent title above table; `colgroup` ~132px labels; stats only in collapsed「报告信息」 |
| **F** | Mobile | ≤760px: TOC drawer path; readable label column; patent content visible without horizontal trap |
| **G** | Deploy / cache | `index.html` versioned CSS/JS/data URLs; normal refresh loads matching bundle |

## Quality runs convention

```
docs/quality-runs/YYYY-MM-DD-rN/
  README.md          # round goals, defects, PR links, SHAs
  dot-reference/     # benchmark captures (if reachable)
  pages-live/        # GitHub Pages captures
  viewports/         # 1440 / 768 / 390 screenshots + notes
```

## Rounds (through 2026-10-23)

| Round | Focus |
|-------|--------|
| **R1** (2026-10-20) | Dot vs Pages gap record; mobile drawer; colgroup; figure restore on `main`; cache stamps |
| **R2** | Dot parity: typography, month chrome, figure grid density, perf (lazy load audit) |
| **R3** | Content delta from Track A + regression on A–G |
| **Final** | Evening 2026-10-23 — A–G sign-off, delivery note, frozen SHAs in README |

## Tooling checklist (every publish)

```bash
python3 scripts/restore_reference_figures.py --check   # after figure/map changes
python3 scripts/build_xlsx.py
python3 scripts/audit_data_integrity.py              # stamps index.html asset URLs
```

## Teammate notes

- Figure restore: `docs/FIGURE_RECOVERY.md`, `data/figure-recovery-map.json`
- Automation labels: `docs/AUTOMATION.md`（配置核实 / 手动跑同流程 / 实际定时触发）
- 总经理: review each round README + merge SHAs; unblock credentials only
