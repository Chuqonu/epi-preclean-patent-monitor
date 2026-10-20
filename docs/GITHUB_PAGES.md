# GitHub Pages deployment note

**Source:** Deploy from branch  
**Branch:** `main`  
**Folder:** `/` (repository root)

Expected URL after the public repo exists:

`https://chuqonu.github.io/epi-preclean-patent-monitor/`

Root must contain `index.html`. Relative paths (`assets/…`, `data/report.json`) resolve from that root.

**Cache busting:** After any change to `assets/css/report.css`, `assets/js/report.js`, or `data/report.json`, run `python3 scripts/stamp_asset_versions.py` (also run automatically by `audit_data_integrity.py` / `build_xlsx.py`). `index.html` gets `?v=<sha256-prefix>` on CSS/JS and a `<meta name="epi-report-data">` URL for JSON so normal refresh loads matching assets without hard-refresh.

Do not enable custom Actions secrets for VPS publish. This site is static Pages only.
