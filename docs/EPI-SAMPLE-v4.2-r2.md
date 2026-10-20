# EPI检索 · 字段模板 SAMPLE（v4.2-r2 · 对齐复核提醒）

**全部为假数据。** `document_type=SAMPLE`。不得纳入报告。

## stats（与 Preclean 计数袋对齐）

| 键 | 值 |
|----|----|
| candidates | 2 |
| publication_events | 3 |
| unique_families | 2 |
| actually_read / fulltext_read | 0 |
| pending | 2 |

候选≠事件：条目1嵌套2个 `events`（US+TW），条目2嵌套1个 → 事件合计3。

## 字段对齐

- 待核主字段：`pending_reason`（兼容保留 `failure_or_pending_reason`）
- 事件模型：候选下 `events[]`
- HANDOFF 键保留：`priority_date` / `source_sha256` / `reviewer` / `reviewed_at` / `change_history`（可 null）
