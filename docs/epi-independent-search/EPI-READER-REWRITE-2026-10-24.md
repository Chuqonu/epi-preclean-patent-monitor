# EPI 读者字段改写提案（2026-10-24）

依据：Chuqono 反馈 + 总经理拆任务；PM brief `PM-FIELD-WHITELIST-AND-STYLE-BRIEF.md`（预期 sha12 `c90384844bc2`）；live 审计 `/workspace/audit-2026-10-24/report.json`（`8694d1ca` / json `5f826eb13fec`）。

- **不 stamp、不 push、不开 PR**；不写回 live `report.json`。
- 仅提案读者可见字段：`short_preview` / `technical_summary` / `purpose`·`novelty`·`use` / `claims_or_embodiment_basis` / `scope_reason`。
- `caption` 去 PDF页/sha 归证据复核；本文件不改图注。
- 锁未动：`actually_read=6`，`research_through=2026-10-20`。
- 运行记录：会话内手动执行，没有平台 run id。不宣称零遗漏。

## 摘要
- 拟改写：**6** 条（2 优先 US + 4 EPI 执笔 Sprint/ruling/gap 读者句）
- 跳过 Preclean：5 条（见文末）
- 机器可读补丁：`EPI-READER-REWRITE-2026-10-24.json`
- 可选家族对象摘录：`EPI-READER-REWRITE-2026-10-24.family-objects.json`

## 2026-10-US12770834B2
- discovery_source: `independent_search`；discovery_lane: `EPI`
- 理由：去掉晚间 sighting / prior 候选 / PDF 已下载等过程痕迹；按谁/做什么/关键点/为何监测改写。
- 残留风险：当地 USPTO 影像 PDF OCR 为空，改写依据条目内 technical_summary 与授权题名/OG claim 摘要，未重读全文权项拓扑。

| 字段 | 改前 | 改后 |
|---|---|---|
| `short_preview` | ASM：石英外延腔+远程等离子体分解含硅前驱体，沉积含硅外延层（授权 2026-10-20；晚间 sighting 今早提升）。 | ASM：石英外延腔外挂远程等离子体，分解含硅前驱体后沉积含硅外延层。 |
| `purpose` | （无） | 在外延腔中用远程等离子体分解含硅前驱体，形成含硅外延材料层。 |
| `novelty` | （无） | 将远程等离子体单元与石英腔、旋转石墨/SiC 基座及腔外光学加热阵列组合为系统。 |
| `use` | （无） | 含硅外延 CVD / 等离子体增强外延成膜。 |
| `claims_or_embodiment_basis` | USPTO OG week42 代表 claim 1（quartz chamber + rotating graphite/SiC support + external heater + RPU for epitaxial Si）；OG 摘要同旨。USPTO PDF 已下载（影像页）。 | 独立项主张石英腔、可旋转石墨/SiC 基座、腔外光学加热与远程等离子体单元，用于沉积含硅外延层。 |
| `scope_reason` | 独立权利要求明确主张 Si 外延 CVD 设备；生长对象为含硅外延层；非 SiC/GaN 生长对象。晚间仅 sighting，prior 候选未收。 | 独立项明确为含硅外延 CVD 设备，生长对象非 SiC/GaN。 |

## 2026-10-US12768074B2
- discovery_source: `independent_search`；discovery_lane: `EPI`
- 理由：去掉晚间 sighting / prior 候选 / PDF 已下载；保留续案一句，不把 terminal disclaimer 当主体。
- **PM条件PASS补丁（2026-10-24）**：补写 `technical_summary`，去掉 CPC 与 terminal disclaimer。
- 残留风险：当地 OCR 文本为空；未展开从属项边界，claims 概括止于独立项结构要素。

| 字段 | 改前 | 改后 |
|---|---|---|
| `short_preview` | AMAT：外延沉积腔架构（上下灯模组、基座/注入环/基环）；续案自 US12,060,651（授权 2026-10-20；晚间 sighting 今早提升）。 | AMAT：外延沉积腔（上下灯、基座、基环与注入环）；续案自 US12,060,651。 |
| `technical_summary` | 过程腔：上/下灯模组、基座组件、上下窗口、基环与注入环。CPC 主分 C30B25/14。续自 17/317,363（现 US12,060,651），terminal disclaimer。 | 外延沉积过程腔：上/下灯模组、基座组件、上下窗口，以及基环与注入环；续案自 US12,060,651。 |
| `purpose` | （无） | 为先进外延膜提供可配置的灯加热外延过程腔架构。 |
| `novelty` | （无） | 上下灯模组与基座/基环/注入环的组合腔结构（续自 US12,060,651）。 |
| `use` | （无） | 硅基外延沉积腔与先进外延膜工艺。 |
| `claims_or_embodiment_basis` | USPTO OG week42 代表 claim 1（upper/lower lamp modules, susceptor, windows, base+inject rings）；题名与 C30B25/14。USPTO PDF 已下载。 | 独立项主张外延沉积过程腔：上/下灯模组、基座、上下窗口，以及基环与注入环。 |
| `scope_reason` | 独立权利要求主张外延沉积过程腔；AMAT；非 SiC/GaN 生长对象限定。晚间仅 sighting，prior 候选未收。 | 独立项主张外延沉积过程腔结构，申请人 AMAT，未限定 SiC/GaN 生长对象。 |

## 2026-10-US12757648B2
- discovery_source: `sprint_gap_tel`
- 理由：读者句去掉 Sprint gap A / 授权事件过程口径；补上申请人与为何进监测。
- 残留风险：当地 .body 为 404 页，未重拉官方 PDF；claims 概括沿用条目既有独立项要素，未核从属温度/Ge 源细节。

| 字段 | 改前 | 改后 |
|---|---|---|
| `short_preview` | HF/碱性气体去除氧化膜、氢热处理、Ge 稀释气预清洗后 SiGe（及可选 Si）外延生长。 | TEL：先去氧化膜并做氢热处理与 Ge 稀释气预清洗，再生长 SiGe（可选 Si）外延。 |
| `technical_summary` | HF/碱性气体去除氧化膜、氢热处理、Ge 稀释气预清洗后 SiGe（及可选 Si）外延生长。 | 基板处理方法：用 HF/碱性气体去除氧化膜，经氢热处理与含 Ge 稀释氢气预清洗后，外延生长 SiGe，并可叠加 Si 外延层。 |
| `purpose` | （无） | 在外延前清掉表面氧化物并活化表面，以便选择性生长 SiGe。 |
| `novelty` | （无） | 把氧化物去除、氢热处理、Ge 稀释气预清洗与随后的 SiGe 外延写进同一方法链。 |
| `use` | （无） | SiGe 源漏或沟槽外延前的干法预清洗与成膜衔接。 |
| `scope_reason` | Sprint gap A：2026-10 授权事件（仅当期 B2）；TEL SiGe 外延前预清洗，纳入 core。 | 独立方法将外延前干法预清洗与 SiGe（及可选 Si）外延串在同一流程，属 Si/SiGe 外延前集成监测对象。 |

## 2026-03-US20260066234A1
- discovery_source: `baseline_claims_review`
- 理由：去掉 ruling r2 / 升格 / 已复核作业痕迹；用 GP 摘要与独立项结构重写读者句。
- 残留风险：同族 WO2026055216A1 附图来源未改动；未在本提案中重核全部 22 项从属边界。

| 字段 | 改前 | 改后 |
|---|---|---|
| `short_preview` | 等离子体增强外延沉积腔室与工艺集成（同族 WO2026055216A1 附图来源）。 | AMAT：电感耦合等离子体增强外延沉积腔，用顶置线圈、基座偏压与气环在较低温形成外延层。 |
| `technical_summary` | 等离子体增强外延沉积腔室与工艺集成。 | 用于形成外延层的等离子体处理腔：基座内电极与偏压源、腔盖上方电感耦合线圈、盖下气环喷嘴，以及与基座同轴的抽气口，在等离子体处理区沉积外延膜。 |
| `purpose` | （无） | 在低于传统热外延的温度下形成高质量外延层。 |
| `novelty` | （无） | 顶置 ICP、基座偏压与气环同轴抽气的腔体组合，面向外延成膜。 |
| `use` | （无） | 等离子体增强硅外延沉积腔。 |
| `claims_or_embodiment_basis` | 基线复核：US20260066234A1 官方公开文本 22 项权利要求已复核（2026-10-15，见 WO2026055216A1 卡 reference_source_status）。 | 独立项主张形成外延层的等离子体处理腔，含基座电极、腔盖上方 ICP 源、基座偏压源与气环；说明书指向低温高质量外延。 |
| `scope_reason` | 等离子体增强外延沉积，升格 core 并计 team_read（ruling r2）。 | 独立项直接主张外延层沉积用等离子体腔，含硅烷类工艺气体路径，属 Si 外延设备监测对象。 |

## 2026-03-US20260062803A1
- discovery_source: `independent_search`；discovery_lane: `EPI`
- 理由：去掉基线/gap 未收等检索过程话；保留双入口+RPU+超晶格技术要点。
- 残留风险：claims 编号沿用条目既有「系统/方法独立项」区分，未逐条核对从属项编号。

| 字段 | 改前 | 改后 |
|---|---|---|
| `short_preview` | ASM：双入口+远程等离子体+隔离件的外延腔，等温沉积 Si/SiGe 超晶格（2026-03-05 公开；基线 ASM 缺口补强）。 | ASM：双入口外延腔配合远程等离子体，等温交替沉积 Si 与 SiGe 以形成超晶格。 |
| `technical_summary` | 系统权利要求：纵流冷壁腔、第一气相入口与分离的第二等离子体反应物入口、远程等离子体单元、隔离件直至基座附近才汇合。方法权利要求：超循环交替外延 Si 层与外延 SiGe 层形成超晶格；控制器可向注入法兰供 Ge 前驱体、向 RPU 供 Si 前驱体并等温外延。 | 纵流冷壁外延系统：第一气相入口与分离的第二等离子体反应物入口、远程等离子体单元，以及使两路气体临近基座才汇合的隔离件；方法上以超循环交替外延 Si 层与 SiGe 层形成超晶格，控制器可向注入法兰供 Ge 前驱体、向远程等离子体单元供 Si 前驱体并等温生长。 |
| `purpose` | （无） | 在可控热预算下提高 Si/SiGe 超晶格外延的前驱体分解与成膜均匀性。 |
| `novelty` | （无） | 气相入口与远程等离子体入口分离，并用隔离件推迟汇合；超循环交替 Si 与 SiGe。 |
| `use` | （无） | Si/SiGe 超晶格与等离子体增强外延成膜。 |
| `claims_or_embodiment_basis` | GP claims 1（双入口+RPU+isolating member 系统）与 claim 16（Si/SiGe 超晶格超循环外延方法）；摘要与 [0007][0016][0041] 实施方式一致。 | 系统独立项主张双入口、远程等离子体单元与隔离件；方法独立项主张交替外延 Si/SiGe 超晶格的超循环。 |
| `scope_reason` | 独立权利要求与实施方式明确主张 Si/SiGe 外延设备与工艺；属缺口申请人 ASM 变体窗内公开，基线/gap 未收。 | 独立项明确主张 Si/SiGe 外延设备与超晶格工艺，生长对象非 SiC/GaN。 |

## 2025-10-US20250311241A1
- discovery_source: `sprint_gap_tel`
- 理由：去掉 Sprint gap A / 非核心纳入套话；说清 related 边界（有外延层但非 EPI 设备主线）。
- 残留风险：related 判定依赖摘要与独立项中的 epitaxial layer 用语；未逐段核说明书是否主张 SiGe 组分。

| 字段 | 改前 | 改后 |
|---|---|---|
| `short_preview` | TEL 垂直 DRAM 与外围电路集成路线；与 Si/SiGe 外延主线关联但非核心 EPI/preclean 纳入。 | TEL：垂直 DRAM 与外围电路的三维集成，流程中含缓冲/外延层堆叠与 GAA 沟道。 |
| `technical_summary` | TEL 垂直 DRAM 与外围电路集成路线；与 Si/SiGe 外延主线关联但非核心 EPI/preclean 纳入。 | 垂直 DRAM 与外围电路集成：在衬底上交替沉积缓冲层与外延层，刻蚀形成垂直沟道并做成 GAA 晶体管与垂直电容，再通过翻转、减薄暴露外延层并与外围晶圆混合键合。 |
| `purpose` | （无） | 把垂直 DRAM 阵列与外围电路在三维方向集成。 |
| `novelty` | （无） | 垂直 GAA+电容与双晶圆混合键合路线，并在堆叠中使用外延层。 |
| `use` | （无） | 垂直 DRAM 与逻辑/外围的三维集成；外延仅作结构层。 |
| `claims_or_embodiment_basis` | （无） | 独立方法要求交替缓冲/外延层堆叠、垂直沟道 GAA、垂直电容，以及后续翻转减薄与混合键合接到外围电路。 |
| `scope_reason` | Sprint gap A：关联监测（DRAM 集成），不计 core。 | 主体是垂直 DRAM 集成，但堆叠与暴露步骤明确使用外延层，故作 Si/SiGe 外延相关监测，不作外延设备/工艺核心条。 |

## 跳过（Preclean / 非 EPI 执笔）

- `2026-04-US12595560B2` — discovery_lane=Preclean；团队裁定为 Preclean 发现/Gap 补录，EPI 不改读者字段
- `2026-01-JP2026004352A` — discovery_lane=Preclean；团队裁定为 Preclean 发现/Gap 补录，EPI 不改读者字段
- `2026-10-US12757665B2` — Preclean 侧条目（父消息点名跳过），EPI 不改
- `2026-*-US12660544B2` — Preclean 侧条目（父消息点名跳过），EPI 不改
- `*-KR102916044B1` — Preclean 侧条目（父消息点名跳过），EPI 不改

## 禁词自检
六案 `set` 字段对 PM 禁词正则未命中（sighting / 晚间 / 今早 / prior 候选 / Sprint|Gap|ruling / PDF已下载 / 已核对 / OG week 等）。

## 样例（US12770834B2 改后）

- short_preview：ASM：石英外延腔外挂远程等离子体，分解含硅前驱体后沉积含硅外延层。
- scope_reason：独立项明确为含硅外延 CVD 设备，生长对象非 SiC/GaN。
