# Preclean 独立检索 — 冻结输出模板（HANDOFF v4.2-r2）

日期：2026-10-20（Asia/Shanghai）  
方法：HANDOFF-2026-10-20-v4.2-r2  
状态：**仅固化字段模板**；仓就绪前不开正式月度检索；禁止宣称「月度完成」。

配套空壳：`/workspace/preclean-search/baseline-2025-11_2026-10-candidates.json`（`status=schema_shell_only`）。

---

## 1. Preclean 纳入边界（执行时）

**IN**：外延前干法/等离子体 preclean；集成 preclean；相关 IPC/CPC 与设备集成分支；与上述场景**明确相关**的腔体干法清洗。

**OUT**：仅以 SiC/GaN 为生长对象；独立湿法清洗。

**勿整案排除**：SiC 涂层/腔体部件、Si:C/SiCP、冷却水、EPI 路线中顺带湿步骤。

**边界提醒（HANDOFF §二）**：先长完外延再做后续处理（如 channel release），不因出现 HF/NH3 或 native oxide 就自动认作外延前 preclean。外延仅作可选背景 → 关联层，非核心。

状态取值：`core` | `related` | `pending` | `excluded` | `metadata_only`（对应 HANDOFF：核心纳入/关联/待核/排除/仅元数据）。

时间：不开始 2025/09；基线至少 2025/11–2026/10（可含参考页已有 2025/10）；按**公开/授权日**归月；当前月写 `research_through`。

---

## 2. 独立冻结清单顶层

| 字段 | 说明 |
|------|------|
| `role` | `"Preclean独立检索"` |
| `method_ref` | `"2026-10-20.4.2-r2"` |
| `period` / `period_start` / `period_end` | 监测窗 |
| `research_through` | 未完结月截止日；正式前 `null` |
| `frozen_at` | 清单冻结时间 ISO |
| `count_basis` | 四类定义说明 |
| `queries_run` | 各法域/分支实际查询、截断、失败 |
| `stats` | 见下 |
| `candidates` | 事件级或族行条目数组（先事件后归族） |
| `excluded_samples` | 读后排除样例+理由 |
| `coverage_gaps` | 失败入口/未完整覆盖/未读完 |
| `notes` | 含「禁止零遗漏」 |

### stats（必须分开，禁止用卡片数冒充族数）

| 键 | 含义 |
|----|------|
| `candidates` | 线索/待审候选总数 |
| `events_reviewed` | 实际已审事件数 |
| `core_events` | 核心纳入事件数 |
| `core_families` | 核心族数 |
| `related` | 关联数 |
| `pending` | 待核数 |
| `fulltext_read` | 已实际阅读 claims/实施方式（非仅摘要）数 |
| `figures` | 真图数（禁止 AI 替代） |
| `excluded_after_read` | 读后排除数 |

---

## 3. 单条候选 / 事件字段（对齐 HANDOFF §四 + 交复核最小集）

交 @证据复核 时每条至少含：

| 字段 | 说明 |
|------|------|
| `publication_id` | 含 kind code |
| `jurisdiction` | US/CN/JP/KR/TW/WO/EP… |
| `event_type` | 公开 / 授权（WO 公开≠授权） |
| `event_date` | `YYYY-MM-DD`（归月依据） |
| `month` | `YYYY-MM` |
| `application_id` / `priority_date` | 可 null |
| `family_id` / `family_id_source` | 同族键及来源；未闭合标待核 |
| `title_original` / `title_zh` | |
| `applicant_original` / `applicant_normalized` | |
| `scope_status` | core/related/pending/excluded/metadata_only |
| `technology_tags` | 如 `preclean`,`remote_plasma`,`chamber_dry_clean`,`integrated_preclean` |
| `short_preview` | 1–2 行 |
| `technical_summary` | |
| `claims_or_embodiment_basis` | 依据原文位置 |
| `scope_reason` | 为何纳入/待核/筛除 |
| `source_urls` | 官方优先；可辅 Google Patents |
| `source_retrieved_at` / `source_sha256` | 能核则填 |
| `actual_read_spans` | 实际阅读范围；摘要≠语义读完 |
| `family_completion_status` | open/pending/closed |
| `figures` | `{source_publication_id, figure_number, source_url, …}`；无真图则省略并记缺口 |
| `search_branch` | 命中分支（工艺/设备/集成/申请人/IPC/多语） |
| `search_failure` | 入口失败原因；无则 null |
| `independent_of_ref` | true（独立发现）；imported baseline 另标 |
| `also_in_ref_preclean_set` | 对照参考合刊，不作抄录依据 |

映射到报告 `FamilyEntry` 时另见 `docs/SCHEMA.md`（`preclean: true` 等展示字段）。

---

## 4. 检索分支计划（仓就绪后执行，v4.2-r2 §三）

多语 + 申请人别名 + IPC/CPC 交叉；多法域并记录覆盖；先公开号+kind+事件日，再归族；两路独立冻结后再交差集。

Preclean 侧重分支：native oxide / remote plasma / HF·NH3·NF3 / SiCoNi / hydrogen bake / 外延前表面准备 / 明确关联腔体干清洁；设备与集成分支不强制标题含 epitaxy。

---

## 5. 闸门

1. 方法材料：✅ HANDOFF v4.2-r2  
2. 仓就绪（Codex 代建 `Chuqonu/epi-preclean-patent-monitor`）：⏳  
3. 正式独立检索 → 冻结清单 → @证据复核  
4. 禁止空跑宣称月度完成；禁止与 EPI 互换清单。


---

## 6. 与证据复核 SAMPLE 格式提醒的对齐（正式冻结前）

- 计数：以 `stats.*` 为准，同时输出顶层别名 `candidates_count` / `events_count` / `families_count` / `actually_read_count`，便于与 EPI `*_count` 对表。
- 待核字段：同时写 `pending_reason` 与 `failure_or_pending_reason`（同义）。
- 事件模型：保持候选下嵌套 `events[]`（显式候选≠事件）；归月仍按各事件 `event_date`。
- 每条补齐可空键：`reviewer`、`reviewed_at`、`change_history`、`priority_date`、`source_sha256`。
