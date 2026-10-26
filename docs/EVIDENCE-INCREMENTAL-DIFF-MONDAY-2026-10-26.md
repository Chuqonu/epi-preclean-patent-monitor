# Evidence incremental diff｜Monday 2026-10-26

reviewed_at: 2026-10-26T09:26:30+08:00（Asia/Shanghai）  
label: **实际定时触发** · folder `epi` · run `88e01ac6-5983-5a86-880c-73681c4e7eee`

## Outcome
**`carry_forward_pending_ingest`** — live Pages **unchanged** this morning; keep `research_through=2026-10-20`.

## Intersection
（空）EPI Monday 与 Preclean Monday 无同号。

## EPI-only
| id | date | disposition |
|---|---|---|
| EP4824859A1 | 2026-10-21 | pending（ASM，title-only；已在 10-23 official sweep） |
| EP4824315A1 | 2026-10-21 | pending（同上） |

## Preclean-only
| id | date | disposition |
|---|---|---|
| US20260327849A1 | 2026-10-22 | **include_core carry-forward**（未上 live；需 figures+PM 后再 ingest） |

## Out of window
- US12772772B2 @ 2026-10-20（= research_through）

## Counts
- EPI 2/2/2/0 · Preclean 1/1/1/1 · team_read lock 6
- include_core **new discovery today**: 0
- include_core **carry-forward not on live**: 1

## Pages
Do **not** bump stamp/research_through in this run. Follow-up gated ingest PR for US20260327849A1 separately.

## Evidence file
json sha256 `df3782608f0bf9915af129697d0e5295afdaed431199536578fdc5b1a1616183`
