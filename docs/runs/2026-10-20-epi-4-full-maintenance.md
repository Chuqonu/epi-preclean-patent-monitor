# EPI完整维护-一次性验收 — 2026-10-20 18:37 Asia/Shanghai

- **Trigger:** 实际定时触发
- **Routine:** epi-4（EPI完整维护-一次性验收）· platform run `7f5c5a15-85ba-5c96-b4cd-60d1f99f3863`
- **Window:** since live `research_through` 2026-10-19 → 2026-10-20 Asia/Shanghai (overlap scan from 2026-10-16)
- **Serial queue:** clear (no open PRs); prior layout/TEL merge `544b9a0` already on main before publish
- **Patents changed this run:** **no** (dual-track empty set)
- **team_read:** locked **6** (EVIDENCE-READ-RULING r2) — not fabricated
- **Outcome:** success (empty incremental + research_through bump + run log)
- **Counts snapshot (pre-bump live):** month_family_entries 122 / publication_events 150 / actually_read 6 / related 1 / pending 4 / figures 130

## Dual-track search

| Track | Candidates | Events | Families est. | Queries |
|-------|------------|--------|---------------|---------|
| EPI | 0 | 0 | 0 | 26 |
| Preclean | 0 | 0 | 0 | 22 |
| Intersection / EPI-only / Preclean-only | 0 / 0 / 0 | — | — | — |

### EPI queries
- `(selective epitaxy OR selective epitaxial) SiGe after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28selective+epitaxy+OR+selective+epitaxial%29+SiGe+after%3A2026-10-14+before%3A2026-10-21&num=100
- `("epi chamber" OR "epitaxial chamber" OR "epitaxy reactor") silicon after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28%22epi+chamber%22+OR+%22epitaxial+chamber%22+OR+%22epitaxy+reactor%22%29+silicon+after%3A2026-10-14+before%3A2026-10-21&num=100
- `susceptor (epitax OR epi) silicon after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=susceptor+%28epitax+OR+epi%29+silicon+after%3A2026-10-14+before%3A2026-10-21&num=100
- `(boron OR doped) (SiGe OR "silicon germanium") epitax after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28boron+OR+doped%29+%28SiGe+OR+%22silicon+germanium%22%29+epitax+after%3A2026-10-14+before%3A2026-10-21&num=100
- `("source/drain" OR "source drain") epitax (SiGe OR silicon) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28%22source%2Fdrain%22+OR+%22source+drain%22%29+epitax+%28SiGe+OR+silicon%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `("dry clean" OR "chamber clean") (epitax OR epi) (silicon OR SiGe) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28%22dry+clean%22+OR+%22chamber+clean%22%29+%28epitax+OR+epi%29+%28silicon+OR+SiGe%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `CPC/C30B25/02 after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=CPC%2FC30B25%2F02+after%3A2026-10-14+before%3A2026-10-21&num=100
- `CPC/H01L21/0262 after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=CPC%2FH01L21%2F0262+after%3A2026-10-14+before%3A2026-10-21&num=100
- `assignee:"Applied Materials" (epitax OR SiGe OR epi) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=assignee%3A%22Applied+Materials%22+%28epitax+OR+SiGe+OR+epi%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `assignee:"ASM IP Holding" (epitax OR SiGe) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=assignee%3A%22ASM+IP+Holding%22+%28epitax+OR+SiGe%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `assignee:"Tokyo Electron" (epitax OR SiGe) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=assignee%3A%22Tokyo+Electron%22+%28epitax+OR+SiGe%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `assignee:"Taiwan Semiconductor" (epitax OR SiGe) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=assignee%3A%22Taiwan+Semiconductor%22+%28epitax+OR+SiGe%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `assignee:"Lam Research" (epitax OR SiGe) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=assignee%3A%22Lam+Research%22+%28epitax+OR+SiGe%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `(外延 OR 硅锗 OR SiGe) (设备 OR 腔室 OR 选择性) country:CN after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28%E5%A4%96%E5%BB%B6+OR+%E7%A1%85%E9%94%97+OR+SiGe%29+%28%E8%AE%BE%E5%A4%87+OR+%E8%85%94%E5%AE%A4+OR+%E9%80%89%E6%8B%A9%E6%80%A7%29+country%3ACN+after%3A2026-10-14+before%3A2026-10-21&num=100
- `(epitax OR SiGe) country:WO after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28epitax+OR+SiGe%29+country%3AWO+after%3A2026-10-14+before%3A2026-10-21&num=100
- `(epitax OR SiGe OR エピタキシャル) country:JP after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28epitax+OR+SiGe+OR+%E3%82%A8%E3%83%94%E3%82%BF%E3%82%AD%E3%82%B7%E3%83%A3%E3%83%AB%29+country%3AJP+after%3A2026-10-14+before%3A2026-10-21&num=100
- `(epitax OR SiGe) country:KR after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28epitax+OR+SiGe%29+country%3AKR+after%3A2026-10-14+before%3A2026-10-21&num=100
- `(epitaxial OR epitaxy OR SiGe OR "silicon germanium") after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%28epitaxial+OR+epitaxy+OR+SiGe+OR+%22silicon+germanium%22%29+after%3A2026-10-14+before%3A2026-10-21&num=100
- `(epitax OR SiGe) after:2026-10-15 before:2026-10-16` · google_patents · hits≈0 · https://patents.google.com/?q=%28epitax+OR+SiGe%29+after%3A2026-10-15+before%3A2026-10-16&num=100
- `USPTO Official Gazette notices 2026 index — latest listed Week 41 / October 13, 2026; Week 42 (expected ~Oct 20, 2026 grant day) not yet on index (week42 patentee pages still show October 21, 2025)` · uspto · hits≈0 · https://www.uspto.gov/learning-and-resources/official-gazette/official-gazette-notices-2026
- `week41 OG patentee + HTML for US12765027 / US12760442 / US12760441 (2026-10-13 grants; OUT of acceptance window)` · uspto · hits≈3 · https://patentsgazette.uspto.gov/week41/OG/patentee/alphaA.html
- `site:patents.google.com / WebSearch: SiGe selective epitaxy OR epi chamber OR susceptor with dates 2026-10-16..2026-10-20` · other · hits≈0 · https://patents.google.com/?q=SiGe+OR+%22silicon+germanium%22+epitax*&after=publication:20261016&before=publication:20261017&num=100
- `选择性外延 OR 硅锗外延 OR 外延腔室 专利 公开日 2026年10月16日 OR 2026年10月20日` · other · hits≈0 · websearch://cn-epi-oct2026
- `Applied Materials Justia patent grants (newest listed = 2026-10-13; includes US12765027 selective epitaxy and US12760441 EPI isolation plate — both out of window)` · other · hits≈0 · https://companyprofiles.justia.com/company/applied-materials/patents/patent
- `Espacenet worldwide search pd=2026-10-16..2026-10-20 AND (epitax* OR SiGe)` · espacenet · hits≈0 · https://worldwide.espacenet.com/patent/search
- `Google Patents xhr sort=new thematic (selective SiGe / chamber / AMAT / ASM / TEL / CN / dry-clean) — inspected top hits' publication_date; none in 2026-10-16..2026-10-20` · google_patents · hits≈0 · https://patents.google.com/?q=(selective+epitaxy+OR+%22SiGe+epitaxy%22)&num=100&sort=new

### Preclean queries
- `pre-epi plasma clean OR "native oxide" dry clean patent 2026` · other · hits≈5 · https://www.google.com/search?q=pre-epi+plasma+clean+OR+%22native+oxide%22+dry+clean+patent+2026
- `"remote plasma" preclean epi OR epitaxial patent after:2026-10-01` · other · hits≈5 · https://www.google.com/search?q=%22remote+plasma%22+preclean+epi+OR+epitaxial+patent+after%3A2026-10-01
- `SiCoNi OR "NF3" chamber clean epitaxial OR preclean patent 2026` · other · hits≈5 · https://www.google.com/search?q=SiCoNi+OR+NF3+chamber+clean+epitaxial+OR+preclean+patent+2026
- `site:patents.google.com preclean OR "pre-clean" OR "native oxide" epitaxy OR epitaxial after:2026-10-15 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=preclean+OR+%22pre-clean%22+OR+%22native+oxide%22+(epitax*+OR+epi)+after:2026-10-15+before:2026-10-21
- `(H01L21/02041 OR H01L21/02046 OR H01L21/02049) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=(H01L21/02041+OR+H01L21/02046+OR+H01L21/02049)+after:2026-10-14+before:2026-10-21
- `(C23C16/4405 OR C23C16/0245) after:2026-10-14 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=(C23C16/4405+OR+C23C16/0245)+after:2026-10-14+before:2026-10-21
- `pre-epi plasma clean OR "plasma preclean" epitaxy after:2026-10-01 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=pre-epi+plasma+clean+OR+%22plasma+preclean%22+epitaxy+after:2026-10-01+before:2026-10-21
- `"native oxide" (dry OR plasma OR remote) (epitax* OR epi) after:2026-10-10 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%22native+oxide%22+(dry+OR+plasma+OR+remote)+(epitax*+OR+epi)+after:2026-10-10+before:2026-10-21
- `"HF vapor" OR "anhydrous hydrogen fluoride" OR "anhydrous HF" (preclean OR oxide) after:2026-10-01 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%22HF+vapor%22+OR+%22anhydrous+HF%22+(preclean+OR+oxide)+after:2026-10-01+before:2026-10-21
- `"remote plasma" (preclean OR "oxide removal") (epi OR epitax*) after:2026-10-01 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%22remote+plasma%22+(preclean+OR+%22oxide+removal%22)+(epi+OR+epitax*)+after:2026-10-01+before:2026-10-21
- `NF3 ("chamber clean" OR "chamber cleaning") (epitax* OR epi OR preclean) after:2026-09-15 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=NF3+(%22chamber+clean%22+OR+%22chamber+cleaning%22)+(epitax*+OR+epi+OR+preclean)+after:2026-09-15+before:2026-10-21
- `SiCoNi OR Selectra (preclean OR oxide) after:2026-10-01 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=SiCoNi+OR+Selectra+(preclean+OR+oxide)+after:2026-10-01+before:2026-10-21
- `"integrated preclean" OR "integrated epitaxy and preclean" after:2026-10-01 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=%22integrated+preclean%22+OR+%22integrated+epitaxy+and+preclean%22+after:2026-10-01+before:2026-10-21
- `(预清洗 OR 预清洁) (外延) (等离子体 OR 干法 OR 远程) after:2026-09-01 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=(%E9%A2%84%E6%B8%85%E6%B4%97+OR+%E9%A2%84%E6%B8%85%E6%B4%81)+(%E5%A4%96%E5%BB%B6)+(%E7%AD%89%E7%A6%BB%E5%AD%90%E4%BD%93+OR+%E5%B9%B2%E6%B3%95+OR+%E8%BF%9C%E7%A8%8B)+after:2026-09-01+before:2026-10-21
- `(腔室清洗 OR 腔室清洁) (NF3 OR 远程等离子体) (外延 OR CVD) after:2026-09-01 before:2026-10-21` · google_patents · hits≈0 · https://patents.google.com/?q=(%E8%85%94%E5%AE%A4%E6%B8%85%E6%B4%97+OR+%E8%85%94%E5%AE%A4%E6%B8%85%E6%B4%81)+(NF3+OR+%E8%BF%9C%E7%A8%8B%E7%AD%89%E7%A6%BB%E5%AD%90%E4%BD%93)+(%E5%A4%96%E5%BB%B6+OR+CVD)+after:2026-09-01+before:2026-10-21
- `外延 预清洗 OR 等离子体清洗 OR 干法去氧化 专利 2026年10月` · other · hits≈5 · https://www.google.com/search?q=%E5%A4%96%E5%BB%B6+%E9%A2%84%E6%B8%85%E6%B4%97+OR+%E7%AD%89%E7%A6%BB%E5%AD%90%E4%BD%93%E6%B8%85%E6%B4%97+OR+%E5%B9%B2%E6%B3%95%E5%8E%BB%E6%B0%A7%E5%8C%96+%E4%B8%93%E5%88%A9+2026%E5%B9%B410%E6%9C%88
- `CNIPA 公开 2026-10-16 OR 2026-10-17 OR 2026-10-20 预清洗 OR 干法清洗 OR 远程等离子体 外延` · other · hits≈0 · https://www.google.com/search?q=CNIPA+2026-10-16+OR+2026-10-20+%E9%A2%84%E6%B8%85%E6%B4%97+%E5%A4%96%E5%BB%B6
- `Espacenet pd within 20261016:20261020 preclean OR native oxide OR H01L21/02046` · espacenet · hits≈0 · https://worldwide.espacenet.com/patent/search?q=pd%20within%20%2220261016%3A20261020%22%20AND%20(preclean%20OR%20%22native%20oxide%22)
- `USPTO Official Gazette week41 (2026-10-13 issue) remote plasma chamber clean / preclean scan; week42 (2026-10-20) unavailable` · uspto · hits≈1 · https://patentsgazette.uspto.gov/week41/OG/html/1551-2/US12760412-20261013.html
- `publication_number:CN122564748A (pending disposition check)` · google_patents · hits≈1 · https://patents.google.com/patent/CN122564748A/en
- `publication_number:WO2026084898A1 (pending disposition check)` · google_patents · hits≈1 · https://patents.google.com/patent/WO2026084898A1/en
- `"HF vapor" OR "anhydrous HF" OR "remote plasma" preclean OR "oxide removal" patent granted:2026-10` · other · hits≈3 · https://www.google.com/search?q=%22anhydrous+HF%22+OR+%22remote+plasma%22+preclean+patent+granted+2026-10

## Evidence diff

See `docs/EVIDENCE-DIFF-2026-10-20-epi-4.json` and track dumps under `docs/runs/2026-10-20-epi-4/`.

Pending unchanged: WO2026084898A1, CN122564748A, US12757451B2 (no disposition-changing evidence).

## Backlog (NOT included this run)

Out-of-window / near-window sightings for a **separate** content gate — not claimed as this acceptance’s discoveries:
- US12760442B2, US12760441B2 (≈2026-10-13, flagged missing from known set by EPI track)
- US12757665B2 (near-window preclean note)

## Publish

- Conditional: log + `research_through` → **2026-10-20** only; no invented patents; Excel unchanged this empty set
- Live verify after deploy stamps
- Delete one-shot epi-4 after receipt; leave weekly `epi` and monthly `epi-2` enabled

## Notes

- Automation subagent could not message group teammates (no SendToAgent in this run); dual-track executed as independent executors with the same independence rules.
- Does **not** claim zero misses. USPTO week42 gazette unavailable at search time.
