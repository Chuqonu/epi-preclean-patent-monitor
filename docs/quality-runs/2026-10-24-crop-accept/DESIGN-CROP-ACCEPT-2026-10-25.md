# 设计 · 像素 crop 1440 复拍验收（2026-10-25 22:40 CST）

**结论：PASS**（优先两案 + §3 六张；未改 stamp / 未开 PR）

## 素材
- MANIFEST：`/workspace/evidence/crops-2026-10-24/MANIFEST.md` sha12 **`b15c1af7c348`**（与证据交版一致）
- PNG 根：`/workspace/evidence/crops-2026-10-24/`（37 张）
- 本目录复拍：
  - `v1440-priority-contact.png`（12 张代表图联系表，1440 宽）
  - `v1440-US12770834B2.png`（Fig.4A / 4B / 1）
  - `v1440-US12768074B2.png`（Fig.4B / 2A / 5A）

## 冻结口径核对（全 37）
| 口径 | 结果 |
|---|---|
| 像素内正立（不靠 CSS `display_rotation`） | PASS（优先目视 Fig.4A/4B 等；文字/结构朝向正常） |
| 长边 ≤3000 | PASS（>3000：0） |
| content_fill（墨迹外接框/画面）≥0.70 | PASS（<0.70：0；优先抽检 ≥0.85） |
| sha 与 `SHA256SUMS` | PASS（0  mismatch） |
| 一页多图拆分 | PASS（68074：2A–2C / 4C–4E / 5A–5B 等已拆） |

## 优先目视
- **US12770834B2** Fig.4A / Fig.4B：正立；线圈/微波标注可读；letter 页边已去。
- **US12768074B2** Fig.4B：正立横剖；callout 清楚。
- 拆分代表：Fig.2A–2C、4C–4E、5A–5B 子图各自成张、图号对。

## Info（不阻断）
1. Fig.2A 左下角仍有邻图少许笔墨，可再收 1–2mm，非必须。
2. TW↔WO 三对裁后 sha 相同（上游同源）；补官方 PDF 前图面分不开——挂账。
3. 合入时：若干条原 report `display_rotation=0` 实为侧躺，本轮已烤正 → 字段一律写 **0**；US12768074B2 图条由 13→23，caption/annotations 须跟新 `figure_number`。

## 未覆盖
其余 rot90（全库原 13 张中，优先两案已含 3 张）及非优先 5334×6875 仍待后续物料；**不挡**本轮优先两案+§3 的图面门。

## 下游
@产品经理：图面侧 PASS，可与读者改写（EPI `cab6d499da7e` / Preclean `9f3397d8debe`）串联合入；开 PR 前仍听总经理发令。
