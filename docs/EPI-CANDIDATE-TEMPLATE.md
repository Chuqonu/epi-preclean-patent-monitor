# EPI 独立检索 — 冻结输出模板（HANDOFF v4.2-r2）

日期：2026-10-20（Asia/Shanghai）  
方法：HANDOFF-2026-10-20-v4.2-r2  
状态：**仅固化字段模板**；推送通道就绪前不开正式月度检索；禁止宣称「月度完成」。

配套 SAMPLE：`docs/EPI-SAMPLE-v4.2-r2.json`（假数据，`document_type=SAMPLE`）。  
工作副本：`/workspace/epi-independent-search/`。

---

## 1. EPI 纳入边界

**IN**：Si/SiGe 外延设备结构、工艺窗口、选择性外延、掺杂与盖层、源气体与腔体设计；与该 EPI 流程明确关联的腔体干式清洁；具有具体生长关系的集成路线中的 EPI 硬件/测量/温控/流场/承载/转移/真空集成。

**OUT**：仅以 SiC/GaN 为生长对象；独立湿法清洗。

**勿整案排除**：SiC 涂层/腔体部件、Si:C/SiCP、冷却水、EPI 路线中顺带湿步骤。

**边界**：外延仅作可选背景 → `related`；器件类若对 Si/SiGe 生长位置/顺序/种子/几何/选择性有实质集成方案可相关。无明确 EPI 关系的通用设备留关联层。

状态：`core` | `related` | `pending` | `excluded` | `metadata_only`。

时间：不开始 2025/09；基线至少 2025/11–2026/10（可含参考已有 2025/10）；按**公开/授权日**归月；当前月写 `research_through`。

---

## 2. 顶层与 stats（与 Preclean / 证据复核对齐）

| 字段 | 说明 |
|------|------|
| `lane` | `"EPI"` |
| `document_type` | 正式：`frozen_candidates`；样例：`SAMPLE` |
| `method_ref` | `"2026-10-20.4.2-r2"` |
| `search_window` / `research_through` | 事件日窗与当月截止 |
| `queries_run` / `sources_tried` / `limitations` | 分支与法域覆盖、截断、失败 |
| `stats` | **正式计数袋（为准）** |

`stats` 键：

- `candidates` / `publication_events` / `unique_families`
- `actually_read`（可并列 `fulltext_read`）
- `pending` / `core_events` / `related` / `excluded`

顶层 `*_count` 仅作兼容别名，以 `stats` 为准。候选数 ≠ 事件数 ≠ 族数 ≠ 已读数。

---

## 3. 候选条目字段

| 字段 | 要求 |
|------|------|
| `publication_id` | 含 kind code |
| `jurisdiction` / `event_type` / `event_date` / `month` | 归月用事件日 |
| `application_id` / `priority_date` | 可 null，**键保留** |
| `family_id` / `family_id_source` / `family_completion_status` | 未闭合 → pending |
| `title_original` / `title_zh` | |
| `applicant_original` / `applicant_normalized` | 别名/受让人 |
| `scope_status` / `scope_reason` / `disposition` | |
| `technology_tags` | |
| `short_preview` / `technical_summary` / `claims_or_embodiment_basis` | |
| `source_urls` / `source_retrieved_at` / `source_sha256` | sha256 可 null，**键保留** |
| `actual_read_spans` / `verification_level` | |
| `pending_reason` | 待核/失败主字段；可兼容旧名 `failure_or_pending_reason` |
| `reviewer` / `reviewed_at` / `change_history` | 可 null / `[]`，**键保留** |
| `figures` | 仅真图元数据；禁止 AI 图 |
| `events[]` | 嵌套公开/授权事件（候选 ≠ 事件） |
| `search_entry` | 发现分支 |

---

## 4. 交件约定

- 先独立冻结，再交证据复核；不与 Preclean 互换清单。
- 文件：`epi-independent-search/<window>-candidates.json|.md` + `search-log-<window>.md`
- 不承诺零遗漏；失败与待核必须保留原因。
