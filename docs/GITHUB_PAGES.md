# GitHub Pages deployment note

**Source:** Deploy from branch  
**Branch:** `main`  
**Folder:** `/` (repository root)

Expected URL after the public repo exists:

`https://chuqonu.github.io/epi-preclean-patent-monitor/`

Root must contain `index.html`. Relative paths (`assets/…`, `data/report.json`) resolve from that root.

Do not enable custom Actions secrets for VPS publish. This site is static Pages only.
