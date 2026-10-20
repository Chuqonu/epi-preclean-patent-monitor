# EPI / Preclean Patent Monitoring Report

Independent public HTML report for **Si/SiGe epitaxy equipment & process**, **pre-epi dry / plasma preclean**, and **chamber dry clean** clearly tied to that flow.

This repository is a **GitHub Pages** edition. It is **not** the VPS Dot report and does not share credentials, workspaces, or internal PDFs with that stack.

## Scope

**In scope**

- Si / SiGe epitaxial process and equipment
- Pre-epitaxy dry / plasma preclean
- Chamber dry cleaning clearly associated with that epi flow

**Out of scope (default)**

- Technologies whose growth target is SiC or GaN
- Standalone wet clean

**Non-exclusion caveats:** SiC as hardware material, Si:C, cooling water, or incidental wet steps are **not** by themselves grounds to exclude an entire case.

## Period

Baseline months: **2025-10 through 2026-10** (newest first in the UI).  
Current month, when filled, is cut off at the actual research date (`research_through`) and labeled incomplete until month-end review.

**Do not** start 2025-09 work unless the owner reopens it.

## Honest counting

Distinguish:

| Metric | Meaning |
|--------|---------|
| Candidates | Hits / leads from search, not yet confirmed |
| Events | Publication or grant events dated into a month |
| Families | Patent families (rows may repeat a family across months) |
| Read | Documents actually reviewed |

Empty months in the scaffold mean **content pending**, not “zero patents found”. Search failure and pending items must keep a reason. No zero-omission claims.

## Data model

Field names follow Codex handoff **2026-10-20.4.2-r2** (`publication_id` with kind code, `scope_status`, `family_completion_status`, `figures` metadata). See `docs/SCHEMA.md` and `docs/HANDOFF-2026-10-20-v4.2-r2.md`.

**2025-09 paused.** `research_through` stays null until a real research cutoff is set.

## Data → HTML → Excel

| Path | Role |
|------|------|
| `data/report.json` | Canonical structured data |
| `index.html` + `assets/` | Client report UI (loads JSON) |
| `ledger/patents.xlsx` | Multi-sheet ledger (元数据/主表/同族事件/关联待核/检索覆盖/变更记录) |
| `docs/SCHEMA.md` | Field definitions |

```bash
# Rebuild Excel ledger after editing report.json
python3 scripts/build_xlsx.py
```

## GitHub Pages

Serve from the **repository root** on branch **`main`**:

1. Create empty public repo `Chuqonu/epi-preclean-patent-monitor` (owner action).
2. Push this tree to `main`.
3. Settings → Pages → Source: **Deploy from a branch** → `main` → `/` (root).
4. Site URL will be `https://chuqonu.github.io/epi-preclean-patent-monitor/`.

Only public patent sources, report HTML/CSS/JS, figures copied from public patents, and build scripts belong here. **No** internal PDFs, chat logs, VPS keys, or publish credentials.

## Local preview

Because the page fetches `data/report.json`, open via a local static server (file:// may block fetch):

```bash
cd epi-preclean-patent-monitor
python3 -m http.server 8080
# then open http://127.0.0.1:8080/
```

## UI rules (implemented)

- Narrow sticky left TOC (`#tree`), **resizable** width
- Months as collapsible `<details>`, newest first; patent **previews** inside
- Right column continuous scroll (`#content`); one patent page per family, variable height
- Click TOC → jump to patent; **scroll does not auto-open** closed months
- No large top chrome title bar
- Text and TOC first; images **lazy-load** with reserved width/height
- **Real** patent figures only (caption must cite publication number + figure label)

## Automation status

Weekly Monday 09:00 (Asia/Shanghai) incremental checks and monthly day-1 reviews are **not** claimed live in this scaffold. Schedule only after a real scheduler is verified.

## License / sources

Patent text and figures remain under their respective patent office / publisher terms. Cite source URLs on every entry.
