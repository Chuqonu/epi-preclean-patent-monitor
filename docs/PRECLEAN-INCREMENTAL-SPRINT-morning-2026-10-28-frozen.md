# Preclean 增量检索冻结 · morning 2026-10-28

- **lane**: Preclean（独立；未抄 EPI 清单）
- **窗口**: 2026-10-21 .. 2026-10-28（Asia/Shanghai）
- **live research_through**: **保持 2026-10-20**（近窗无已核验 >2026-10-20 事件）
- **generated_at**: 2026-10-28T09:08:22+08:00

## 四计数

| 指标 | 本轮 |
|------|------|
| candidates | **0** |
| events | **0** |
| families | **0** |
| actually_read（本轮） | **0** |
| team_actually_read_lock | **6**（未改） |

## 公开号列表

（空 — 本轮无晋升候选）

近窗命中公开号：无。

## 检索摘要

- 查询数: 118（含近窗多国别 × 主题、fresh gap、申请人/CPC、index-lag 对照）；query_errors 终态: 0
- 近窗 `after:publication:20261021` `before:publication:20261029`: 主题查询与对照 `semiconductor` **全部 0**
- fresh 主题窗 `20260901..20261029`: 主题返回合计 0
- gap-baseline `20251001..20261029`: G1/G4 有大量历史语料；new_vs_known=164（线索，非本轮候选）
- 抽检排除/不晋升: US12500077B2（外延后湿法）、US12532687B2（清洗液）、KR102944561B1（选择性氧化膜刻蚀，待深读但不作本轮增量）

## research_through

**建议保持 2026-10-20**。理由：无已核验、有日期证据的公开/授权事件晚于 2026-10-20。

## 索引滞后 / 覆盖缺口

Google Patents xhr 对 2026-10-21..28 连 `semiconductor` 对照亦为 0；官方 US/CN/JP/KR/EP/WO 公报本轮未独立拉取 → 覆盖缺口保留。禁止宣称零遗漏。

## 查漏补缺（仅观察 live，未改 report）

- 缺发明人: **118**/131 条 family 无 inventors 字段；样例: US20260313994A1, US20260304810A1, US12727402B2, US20260275525A1, US20260282506A1, US20260282794A1, US12745604B2, US20260293620A1
- 空标注: **27** 件公开号含空 annotations（figures 层 83 空 / 122 verified）；样例: CN120797198A, CN120989593A, CN121519154A, CN121693111A, CN122069948A, CN122294515A, DE112021001213B4, JP2026004352A
- 缺图且有官方源: 本轮未单独枚举（live figures=205；未改资产）

## 产物

- `/workspace/preclean-search/morning-2026-10-28/PRECLEAN-INCREMENTAL-SPRINT-morning-2026-10-28-frozen.json`
- 本 md + search-log
