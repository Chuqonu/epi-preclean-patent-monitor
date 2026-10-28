# 早间交/差集 — 2026-10-28（非正式）

## 输入（独立冻结，未互换清单）

| 车道 | 路径 | 候选｜事件｜族｜本冻已读 | sha12 |
|---|---|---|---|
| Preclean | `/workspace/preclean-search/morning-2026-10-28/PRECLEAN-INCREMENTAL-SPRINT-morning-2026-10-28-frozen.json` | **0｜0｜0｜0** | `e555b45466c3`（md `54af4f6efb90` / log `0c8563bb27c0`） |
| EPI | `/workspace/epi-maintenance-2026-10-28/EPI-INCREMENTAL-MAINT-2026-10-28-frozen.json` | **2｜2｜≤2｜0** | frozen.json `523b848f7837`（md `38ac4e00b054` / log `026c8f3816d7`） |

Live 基线抽检：Pages `report.json` 实算 sha12 **`45e392f3e264`**；`research_through=2026-10-20`；`actually_read=6`；`figures=205`。上述四公开号均 **不在 live**。

## 集合

- **交集**：空（公开号无重叠；族链未读，亦无共 family_id）
- **EPI-only**：`EP4824859A1`、`EP4824315A1`（均为 pending 书目 carry；`already_in_prior_freeze=true`，非本窗新发现）
- **Preclean-only**：空（候选 0；gap 抽检排除/不晋升 3 条不进本轮差集候选）

## 纳入 / 待核 / 筛除

### 纳入报告（core / related）
- **无**。两 EP 均未读 claims/实施方式，不能定 core/related。

### 待核队列（保留原因）

| 公开号 | 车道 | 事件日 | 申请人 | 原文已读 | 图号 | 官方链接 | 裁定 | 原因 |
|---|---|---|---|---|---|---|---|---|
| EP4824859A1 | EPI | 2026-10-21 | ASM IP Holding | **否**（`actual_read_spans=[]`；详情 Cloudflare；GP 503） | 无（figures=[]） | Register 列表 sha12 `1dc6cd45122c` 可核书目；详情页未过 | **keep pending，不入库** | 标题含硅层+硅前驱体，IPC H01L21/02 / C23C16/455 / H01J37/32；无法区分外延 vs ALD/CVD |
| EP4824315A1 | EPI | 2026-10-21 | ASM IP Holding | **否**（同上） | 无 | 同上列表源 | **keep pending，不入库** | 标题含硅层；IPC C23C16/22·16/24 / H01L21/02；同未读原文 |

### 同族
- 申请号不同：`EP24904965` vs `EP24904972`；无 priority / family_id。
- **裁定：`family_unverified`（≤2 族，不并族）**。未读同族链前禁止 family_share。

### EPO 出界核对

| 公开号 | EPI 声称 | 证据侧 | 书目证据 |
|---|---|---|---|
| EP4831366A1 | exclude（3C-SiC 异质外延） | **确认出界 / 筛除** | 标题 heteroepitaxial wafer；IPC **C30B29/36**（SiC）；申请人 Shin-Etsu Handotai；列表 sha12 `7a8675e3b820` |
| EP4829093A1 | exclude（SiC 寄生沉积腔清洁） | **改挂待核，不终裁出界** | 标题「parasitic grown silicon carbides」+ epitaxy chamber；IPC C23C16/32·16/44；申请人 Schunk Xycarb。书目倾向 SiC 语境，但腔体清洁也可能落在 Si/SiGe 外延腔清寄生 SiC——**未读原文不得整案终裁排除**；本轮不入库 |

### Preclean 非候选（观察，不进报告）
- US12500077B2 / US12532687B2：湿法 — 同意不晋升
- KR102944561B1：not_promoted_pending_deep_read — 同意本轮不进差集

## 已读锁 / research_through

- **team / actually_read = 6**（不变；两车道本冻已读均为 0，不升锁）
- **不建议**将 live `research_through` 推过 **2026-10-20**（无已核 scoped core；两 pending 仅书目；近窗索引滞后声明保留）
- **不发明 stamp**、不改 live

## 缺项与冲突

- 没有找到 ≠ 不存在；两侧均声明 GP/索引滞后与未穷尽官方公报 → **禁止宣称零遗漏**
- 两 EP 详情 Cloudflare / GP 503：**检索失败原因必须保留**（pending_reason 已在 EPI 冻结）
- 查漏补缺（发明人缺 118/131、空标注 83 图）：本轮**不拦**；未见会埋雷的证据错误
- 不开始 2025/09

## 结论

**PASS_INCREMENTAL_EMPTY_NEAR_WINDOW**（近窗无新 core；交集空 OK；两 EP **继续 pending 不入库**；EP4831366A1 确认筛除；EP4829093A1 **待核非终裁排除**；`research_through` 保持 2026-10-20；已读锁 6）。未 stamp。正式交付仍关总经理闸。
