# PM：读者字段白名单 + 文风 brief（2026-10-24）
依据 live `8694d1ca` / json `5f826eb13fec` 与 `/workspace/audit-2026-10-24/AUDIT-META.json`。stamp/PR 仍不动；本文件只定规则。运行记录：会话内手动执行，没有平台 run id。

## 1. 读者可见字段白名单（UI 会渲染）

| 槽位 | JSON 字段 | 读者用途 | 允许缺省 |
|---|---|---|---|
| TOC 一句 | `short_preview`，否则 `technical_summary` | 谁 + 做什么 | 否（至少一项） |
| 中文技术简介 | `technical_summary`，否则 `short_preview`；若有则附 `purpose` / `novelty` / `use` | 技术要点 | purpose/novelty/use **允许缺** |
| 关键权利要求/实施例 | `claims_or_embodiment_basis` | 读权项依据 | 可短，不可空话 |
| 相关性 | `scope_reason`（主文）；`scope_status`、`discovery_source`、`import_tag`、`family_merge_note` 仅作标签/注 | 为何进监测 | scope_reason 必有实质句 |
| 图注 | `figures[].caption` | 图是什么 | 有图必有可读图注 |
| 图号 hover | `figures[].annotations`（version=1 + labels[].display_name/description + occurrences） | 零件释义 | **整案全有或整案全无**，禁止同案混用 |

### 仅内部（UI 不渲染，勿把过程写进上面槽位）
`event_note`、`overlap_note`、`change_history`、`notes[]`、`status_note`、`verification`、`verification_level`、`reviewer`、`reviewed_at`、`source_retrieved_at`、`source_sha256`、`actual_read_spans`、`team_independent_read`、`read_disposition`、`read_status`、`overlap_backfill`、`independent_of_ref`、`discovery_lane`（lane 供内部溯源，不进读者句）、`pdf_page` / 文件 sha 不得进 caption。

### 相关性槽位禁写（②）
下列一律不进 `short_preview` / `technical_summary` / `claims_or_embodiment_basis` / `scope_reason` / `caption`：
- 流程词：晚间、sighting、今早提升、prior 候选、Sprint、Gap、ruling、overlap_backfill、补录窗
- 作业痕迹：USPTO PDF 已下载、OG week、影像页、已核对、官方原件已核对、技术全文与当前权利要求已核对
- 内部口径：空≠无、不宣称零遗漏、待核队列编号（可留内部笔记）

`scope_reason` 只写：**技术边界 + 为何 core/related**（生长对象、腔/工艺关联、非 SiC/GaN 生长对象等）。标签类字段承载来源，不把「独立检索/参考导入」写成散文套话。

### caption 白名单
- 要：公开号、图号（Fig./図）、一句话内容
- 不要：PDF 第 N 页、Sheet N/M、sha、下载状态、「当前授权原始附图」套话堆砌

## 2. 文风 brief（④）

### 目标句式（简介 / short_preview）
按序覆盖，能写则写，**允许 purpose / novelty / use 缺项**：
1. **谁**：申请人短名（ASM、AMAT…）
2. **解决什么**：一句话问题或目标
3. **关键点**：结构/工艺/控制上的抓手（2–4 个名词短语即可）
4. **为何进监测**：落到 Si/SiGe 外延或外延前干法 preclean 的边界（一句）

禁止：以「已核对」「官方原件」「技术全文」开场；堆权项编号串（「2→1、6→4→1」）；中英重复同一句；把 CPC、terminal disclaimer、续案号当简介主体（续案可一句带过，勿占主句）。

### claims_or_embodiment_basis
- 用读者语言概括独立项主张 + 必要从属边界
- 可点 1–2 个代表 claim，不要 OG week / PDF 已下载
- 少写权项拓扑箭头

### purpose / novelty / use（可选）
- 有则各一行、口语、无「已验证/未独立验证」元评论（效果存疑写进内部 verification）
- 无则整段省略，勿填「暂无」「N/A」

### 反例 → 正例（优先两案）
**US12770834B2**  
- 现 short_preview：含「晚间 sighting 今早提升」→ 删过程。例：「ASM：石英外延腔外挂远程等离子体，分解含硅前驱体后沉积含硅外延层。」  
- 现 claims…：「USPTO PDF 已下载」→ 删。例：「独立项主张石英腔、可旋转石墨/SiC 基座、腔外光学加热与远程等离子体单元，用于沉积含硅外延层。」  
- 现 scope_reason：删 sighting/prior。例：「独立项明确为含硅外延 CVD 设备，生长对象非 SiC/GaN。」

**US12768074B2**  
- 例 short_preview：「AMAT：外延沉积腔（上下灯、基座、基环与注入环）；续案自 US12,060,651。」  
- 例 scope_reason：「独立项主张外延沉积过程腔结构，申请人 AMAT，未限定 SiC/GaN 生长对象。」

### 验收（PM 过门用）
各人清单齐后抽检：上述禁词在五类读者字段命中 = 0；两优先案四要素齐或明确缺 optional 三字段；同案 hover 不混用（证据/设计条）。通过后再谈开 PR；开 PR 后仍走 证据+PM（图 PR 再加设计）PASS，PM 不自 squash。

## 3. 分工衔接
- 检索：按本 brief 改读者字段，先两案再其余约 8 条 Sprint/Gap/ruling。  
- 证据：caption 去 PDF页/sha；hotspot 规则跟设计「有图必有释义或整案无」。  
- 设计：①③ 视觉与 hover 一致性。  
- PM：收齐后按本文件过门，再建议开 PR。
