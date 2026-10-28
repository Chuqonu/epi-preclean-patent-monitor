# 每日检索维护运行记录 · 2026-10-28

- **routine folder**: `epi-3`（EPI专利监测-每日检索）
- **label**: 实际定时触发
- **Asia/Shanghai**: start `2026-10-28 09:39`（routine fire UTC 01:39）· search freeze window work earlier same morning · close `2026-10-28 ~09:45`
- **serial publish lock**: FREE（open PRs = 0；周一 epi / 月初 epi-2 未并行）
- **content changed**: **否**（无 Pages stamp / 无 report.json 变更）
- **live baseline**: main `f312944a`；css `15660946b92b` / js `358e8bb63bb5` / json `45e392f3e264`；figures 205；`research_through=2026-10-20`；team_read_lock 6
- **TOC new month**: 不需要（日历仍为 2026-10；左侧已有 `2026-10`；未到 2026-11）
- **September 2025**: 仍暂停

## 双轨独立检索（未互换清单）

| 车道 | 产物 | 候选/事件/族/本冻已读 | 结论 |
|------|------|------------------------|------|
| EPI | `EPI-INCREMENTAL-MAINT-2026-10-28-*` | 3 / 3 / ≤3 / 0 | pending 书目 3；无 include_core 新 |
| Preclean | `PRECLEAN-INCREMENTAL-SPRINT-morning-2026-10-28-*` | 0 / 0 / 0 / 0 | 近窗空 |
| 证据 | `EVIDENCE-MORNING-DIFF-2026-10-28.*` sha12 `4cd3e2e87447` | — | **PASS_INCREMENTAL_EMPTY_NEAR_WINDOW** |

### EPI pending（不入库）
- EP4824859A1、EP4824315A1：ASM IP Holding；详情 CF/403；keep pending
- EP4829093A1：Schunk Xycarb；腔体寄生 SiC 清洁；**待核**（非终裁出界）；下次优先补原文
- EP4831366A1：Shin-Etsu；确认筛除（3C-SiC）

### Preclean
- 近窗主题/对照全 0；抽检湿法/选择性刻蚀不晋升

## 查漏补缺（观察，本轮未改 report）
- 缺发明人 ~118/131；空标注 83 图 / 27 公开号；KR102920833B1 缺图有官方源（未本轮补）
- 无廉价可核增量可合入；禁止编造

## 发布
- docs-only 提交本目录产物；**不**改 HTML/Excel/stamps
