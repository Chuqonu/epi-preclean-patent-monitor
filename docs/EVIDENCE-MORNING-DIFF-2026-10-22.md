# 早间交/差集 — 2026-10-22（非正式 · R4）

## 输入
- EPI：`docs/EPI-INCREMENTAL-SPRINT-morning-2026-10-22-frozen.json` → **候选 2｜事件 2｜族 2｜已读 2**（pending 0｜窗内新 0｜overlap_backfill 2｜排除核读 3）；search_window `2026-10-21..2026-10-22`
- Preclean：`docs/PRECLEAN-INCREMENTAL-SPRINT-morning-2026-10-22-frozen.json` → **候选 1｜事件 1｜族 1**；lane 已读 10（读后排除 9，related 2；**不升团队锁**）；近窗诚实空

四类计数与冻结 JSON `stats` 一致；房间口头声明无冲突。

## 集合
- 交集：空（公开号与 family_id 均无重叠；未互换清单）
- EPI-only：`US12770834B2`、`US12768074B2`（include_core；均为 overlap_backfill）
- Preclean-only：`KR102918757B1`（冻结标 include_core，但 **live 已有 baseline**）、`CN122406228A` / `KR20260113276A`（include_related）

## 纳入 / 待核 / 筛除
### 纳入建议（core）
| 公开号 | 车道 | 分类 | 事件日 | 说明 |
|--------|------|------|--------|------|
| US12770834B2 | EPI | **overlap_backfill** → 建议 include_core | 2026-10-20 | ASM PE epi CVD；live 未见；晚间窗外 sighting 今早提升；**非** 10-21..22 窗内新 |
| US12768074B2 | EPI | **overlap_backfill** → 建议 include_core | 2026-10-20 | AMAT epi chamber；live 未见；同上 |
| KR102918757B1 | Preclean | **baseline_already_live**（不计新发现） | 2026-01-28 | live `data/report.json` 已 core（baseline-import）；本早独立复核可记，**不**升新 core 计数；勿与 AHF 族混同 |

### 纳入建议（related）
| 公开号 | 车道 | 事件日 | 说明 |
|--------|------|--------|------|
| CN122406228A | Preclean | 2026-07-17 | ASM preclean/etch 装置高温涂层（含 RPS）→ related；live 未见 |
| KR20260113276A | Preclean | 2026-07-21 | AMAT 低温 EPI 腔，清洁附带 → related；live 未见 |

### 待核
- 无新增 pending
- Preclean 注明同族闭合仍 open（KR102918757B1 族成员未全量核读；related 两族待闭合）— 不升格

### 筛除（本早不进报告）
- EPI 排除核读 3：`US12772522B2`（Intel 接触/盖层）、`US12772611B2`（氮化物 HEMT）、`US12768073B2`（SiC 生长对象）
- Preclean 读后排除 9：见源包 `excluded_after_read`（接触/金属氧化物蚀刻/加热器/气体制备噪声/III-V/Ga2O3/gap-fill/掺杂沉积等）

## 已读锁
- **actually_read = 6**（不变）
- Preclean lane `actually_read=10`、EPI lane `=2` 均为车道内部读数，**不升**团队锁

## 缺项与冲突
- 窗内 2026-10-21..22 / 近窗 >2026-10-20：**诚实空 ≠ 零遗漏**（索引滞后可能；两侧均声明）
- EPI 本批 2 条均为 **10-20 授权补录**（相对 search_window 为 overlap_backfill）；空窗本身不构成推进 `research_through` 的证据
- **live 指针冲突（未 stamp）**：`data/report.json` 仍写 `research_through=2026-10-19`；团队操作口径与两侧冻结建议为保持 **2026-10-20**。本包**不发明 stamp**、不改 live
- Preclean 将 `KR102918757B1` 标为本早 include_core / `also_in_ref=false`，但 live 已有同号 baseline core → 裁定为 **已在基线，不计新发现**（与晚间 Lam 先例同类）
- 不开始 2025/09

## 结论
**PASS_INCREMENTAL**（有 EPI overlap_backfill 纳入建议 + Preclean related；窗内新发现 0；Preclean core 撞基线不计新）。未 stamp。正式交付仍关。不开始 2025/09。**不建议**将 live `research_through` 推过 **2026-10-20**。
