# EPI 增量 · 维护冻结 2026-10-28

- 窗：`2026-10-21..2026-10-28`（Asia/Shanghai）· 冻结 `2026-10-28T09:25:16+08:00` · **收口修订** `2026-10-28T09:30:32+08:00`
- 方法：HANDOFF `2026-10-20.4.2-r2`
- Live 基线：stamp `45e392f3e264` · `research_through=2026-10-20` · figures 205 · team_read_lock 6
- 四类计数：**候选 3｜事件 3｜族 ≤3（估计，同族未核）｜已读 0**（团队已读锁仍 6）
- include_core **新 vs baseline：无** · include_related：无 · exclude（入清单）：无 · pending：**3**
- research_through 建议：**不推进，保持 2026-10-20**（无已核 scoped core；pending 仅书目）
- **收口**：证据 `PASS_INCREMENTAL_EMPTY_NEAR_WINDOW`；两 ASM EP keep pending **不入库**；无 Pages stamp

## 新/复核候选（pending）

| publication_id | event_date | applicant | disposition | 备注 |
|---|---|---|---|---|
| EP4824859A1 | 2026-10-21 | ASM IP Holding | pending | 含硅层+硅前驱体；Register 列表复核；详情 CF/403；GP 未索引；收口 keep pending 不入库 |
| EP4824315A1 | 2026-10-21 | ASM IP Holding | pending | 含硅层；同上 |
| EP4829093A1 | 2026-10-28 | Schunk Xycarb | pending | **收口改挂待核**（原误标出界）；外延腔寄生 SiC 清洁；**下次优先补原文**再定 |

不重列：US12770834B2、US12768074B2（已 live）。

## USPTO OG week43（主新源）

- `patent.html` IssueDate=**20261027**，folder `html/1551-4`，约 5925 IDs
- 主题扫描：C23C(20)+C30B(5)+H01J(18)+H10P(49)+H10D(66)=**158** 件详情全取并读代表权利要求
- **EPI-scoped core/related 入清单：无（诚实空）**
- 可见但排除/出界 sightings（未入候选）：如 US12777889B2（AMAT susceptor，无明确外延关联）、US12777858B2（TEL Si 膜等离子体刻蚀）、若干器件「epitaxial layer」结构案、US12774537B2（SiC 衬底）等 — 见 JSON `out_of_scope_sightings_og_week43`

## EPO pd=20261028

| publication_id | applicant | 结论 |
|---|---|---|
| EP4831366A1 | Shin-Etsu Handotai | **确认筛除** — 3C-SiC 异质外延（C30B29/36） |
| EP4829093A1 | Schunk Xycarb | **改挂待核**（见上表；勿终裁出界） |

## 查漏补缺（live stamp `45e392f3e264`）

- **缺发明人**：118 公开号（见 `/workspace/epi-gap-tags-live-2026-10-28.json`）
- **空标注**：83 图 / 27 公开号（侧车汇总）；顶：US12768074B2 **23**、US12770834B2 **8**、…
- **缺图且有官方源**：KR102920833B1
- 本任务**不**改写 reader 字段

## 局限

- 不宣称零遗漏。
- GP xhr 近窗仍空或滞后；OG week43 未穷尽全部 5925 件。
- EPO 部分入口超时/403；未读 Preclean；无 2025/09；未 stamp；已读锁仍 6。
- EP4829093A1 下次检索优先补原文后再定 scope。

## 产物

- `EPI-INCREMENTAL-MAINT-2026-10-28-frozen.json`
- `EPI-INCREMENTAL-MAINT-2026-10-28-frozen.md`
- `EPI-INCREMENTAL-MAINT-2026-10-28-search-log.md`
- `raw/` + `sha256sums.txt`
