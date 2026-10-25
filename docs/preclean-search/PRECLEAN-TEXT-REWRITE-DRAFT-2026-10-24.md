# Preclean 读者字段改写草案（2026-10-24）

依据：live `8694d1ca` / json `5f826eb13fec`；审计 `/workspace/audit-2026-10-24/`；PM brief `/workspace/docs-quality-runs/2026-10-24-quality/PM-FIELD-WHITELIST-AND-STYLE-BRIEF.md`（sha12 `c90384844bc2`）。

**硬约束：** 未改 `report.json`、未 stamp、未 commit/push、未开 PR。本文件仅为字段级提案，供证据/PM 过门后再谈合入。

**范围纠偏：** GM 已将 US12770834B2 / US12768074B2 划给 EPI（`discovery_lane=EPI`）。空 lane 的 US12757648B2 / US20250311241A1 属 EPI sprint_gap_tel，**不起草**。Preclean 只改下列五张。

## 0. 范围表

| 公开号 | 月 | lane | scope | 申请人 | 读者字段主要问题 | 本草案 |
|---|---|---|---|---|---|---|
| US12757665B2 | 2026-10 | Preclean | core | ASM | `scope_reason` 含「晚间」；`technical_summary` 含 GP404/OG 核读过程；claims 堆 claim 1 原文碎片 | 全字段改写 |
| US12660544B2 | 2026-06 | Preclean | core | ASM | 同上（AHF 同族） | 全字段改写（与上共享文案，事件日不同） |
| KR102916044B1 | 2026-01 | Preclean | core | ASM | 同上（AHF 同族） | 全字段改写 |
| US12595560B2 | 2026-04 | Preclean | core | AMAT | `scope_reason` 含「Gap 补录」；两张 caption 含 PDF 页/sha | 简介+相关性+caption |
| JP2026004352A | 2026-01 | Preclean | core | AMAT | `scope_reason` 含「Gap 补录」；两张 caption 含公报页/sha | 简介+相关性+caption |

**同 lane 但不在五案、且读者字段无 Sprint/Gap/ruling/晚间 命中：** KR102920833B1（related，附图 0，「暂无公开附图」）。本次不改；若 PM 扩围再单开。

**Preclean-lane 在五案之外的 Sprint/Gap/ruling 读者字段命中数：0。**

**不起草（他方）：**
- EPI lane：US12770834B2、US12768074B2、US20260062803A1 → EPI
- 空 lane 且含 Sprint/USPTO PDF 等：US12757648B2、US20250311241A1 等 → EPI / 证据 caption 条，非 Preclean

UI 渲染槽位（只改这些）：`short_preview`、`technical_summary`、`purpose`/`novelty`/`use`（可缺）、`claims_or_embodiment_basis`、`scope_reason`、`figures[].caption`、label hover。`event_note` 等不渲染，不写。

禁词（读者字段命中须为 0）：晚间、今早、sighting、prior 候选、Sprint、Gap、ruling、PDF 已下载、已核对、caption 内 PDF 页/sha。

---

## 1. AHF 同族三卡（共用技术文案）

技术事实（三卡一致）：ASM；无水 HF（AHF）+ 水汽去氧化物的半导体预清洁方法与气路（纯化、加热夹套等）；经典 dry oxide preclean，服务预外延去氧化。同族事件：KR102916044B1（2026-01-21 授权）、US12660544B2（2026-06-16 授权）、US12757665B2（2026-10-06 授权）。

`purpose` / `novelty` / `use` 现均为空 → **按 brief 允许缺项，提案里给出可选三行；合入时可整段省略。**

AHF 六张英文 caption 无 PDF 页/sha，**图注保持不动**（证据若另做中文化不在本草案）。label hover：三案当前无 annotations → 维持「整案无」，不混用。

### 1.1 US12757665B2（2026-10-06 授权）

**现况摘录（问题处）：**
- `technical_summary`：…「GP 直链 404，以 USPTO OG 官方授权公告核读 claim 1。」
- `claims_or_embodiment_basis`：「USPTO OG claim 1：method for precleaning…」
- `scope_reason`：「晚间 Preclean 增量：同族授权事件纳入 core。」

**提案：**

| 字段 | 提案文案 |
|---|---|
| `short_preview` | ASM：无水 HF 与水汽去氧化物的半导体预清洁方法与气路，用于预外延干法去氧化。 |
| `technical_summary` | ASM 的预清洁方案：向处理腔输送无水氟化氢与水汽，去除衬底表面氧化物，并配套纯化与加热夹套气路。面向外延前干法去氧化，而非独立湿法清洗。同族另有 KR102916044B1（2026-01）、US12660544B2（2026-06）授权事件。 |
| `purpose`（可选） | 在外延前以干法去掉衬底氧化物，避免湿法残留与队列打断。 |
| `novelty`（可选） | 无水 HF 输送链（纯化、加热夹套）与水汽路径组合，形成可重复的氧化物去除流程。 |
| `use`（可选） | Si/SiGe 外延前的 chamber 内 dry oxide preclean。 |
| `claims_or_embodiment_basis` | 独立项主张含无水 HF 输送系统（含纯化与加热夹套）的预清洁方法；摘要对应 AHF+水汽去氧化物。 |
| `scope_reason` | 独立项为半导体预清洁（AHF+水汽去氧化物），落入外延前干法 preclean；生长对象非 SiC/GaN。同族授权事件，core。 |
| `caption` | 六张维持现英文示意图注（无过程词）。 |
| label hover | 整案无 annotations，保持整案无。 |

### 1.2 US12660544B2（2026-06-16 授权）

与 1.1 相同技术文案；仅同族指称微调：

| 字段 | 提案文案 |
|---|---|
| `short_preview` | ASM：无水 HF 与水汽去氧化物的半导体预清洁方法与气路，用于预外延干法去氧化。 |
| `technical_summary` | ASM 的预清洁方案：向处理腔输送无水氟化氢与水汽，去除衬底表面氧化物，并配套纯化与加热夹套气路。面向外延前干法去氧化，而非独立湿法清洗。同族另有 KR102916044B1（2026-01）、US12757665B2（2026-10）授权事件。 |
| `purpose` / `novelty` / `use` | 同 1.1（可选）。 |
| `claims_or_embodiment_basis` | 同 1.1。 |
| `scope_reason` | 独立项为半导体预清洁（AHF+水汽去氧化物），落入外延前干法 preclean；生长对象非 SiC/GaN。同族授权事件，core。 |
| `caption` / hover | 同 1.1，不动。 |

### 1.3 KR102916044B1（2026-01-21 授权）

| 字段 | 提案文案 |
|---|---|
| `short_preview` | ASM：无水 HF 与水汽去氧化物的半导体预清洁方法与气路，用于预外延干法去氧化。 |
| `technical_summary` | ASM 的预清洁方案：向处理腔输送无水氟化氢与水汽，去除衬底表面氧化物，并配套纯化与加热夹套气路。面向外延前干法去氧化，而非独立湿法清洗。同族另有 US12660544B2（2026-06）、US12757665B2（2026-10）授权事件。 |
| `purpose` / `novelty` / `use` | 同 1.1（可选）。 |
| `claims_or_embodiment_basis` | 同 1.1（读者语言概括；不写 USPTO OG / GP 链状态）。 |
| `scope_reason` | 独立项为半导体预清洁（AHF+水汽去氧化物），落入外延前干法 preclean；生长对象非 SiC/GaN。同族授权事件，core。 |
| `caption` / hover | 同 1.1，不动。 |

---

## 2. US12595560B2（AMAT，2026-04-07 授权）

**现况问题：**
- `scope_reason`：「Gap 补录：…Applied 设备缺口…」
- `claims_or_embodiment_basis`：偏摘要堆砌
- caption FIG.1A / FIG.14：含「USPTO…PDF第N页」「sha256 前12位…」

**提案：**

| 字段 | 提案文案 |
|---|---|
| `short_preview` | AMAT：远程等离子体源与工艺腔之间的气体注入组件，向处理体积输送活性自由基/分子种。 |
| `technical_summary` | 气体注入组件串在远程等离子体源与工艺腔之间：本体与介电衬套形成混合体积，双法兰分别接腔体与 RPS，周向注入口补气。用于电子器件制造中把亚稳态自由基种送入处理体积，改善气流与活性种分布。 |
| `purpose`（可选） | 改善 RPS 到工艺腔的活性种输送与混合。 |
| `novelty`（可选） | 介电衬套混合体积 + 周向注入口 + 双法兰 RPS/腔体耦合。 |
| `use`（可选） | 外延/CVD 类工艺腔的远程等离子体辅助处理与腔前活性种注入。 |
| `claims_or_embodiment_basis` | 独立项主张位于远程等离子体源与工艺腔之间的气体注入组件，向处理体积供应亚稳态自由基种。 |
| `scope_reason` | 独立装置项覆盖外延/CVD 类工艺腔的气体输送与 RPS 耦合；申请人 AMAT；非独立湿法清洗整案，core。 |
| `caption` FIG. 1A | US12595560B2 FIG. 1A：工艺腔与远程等离子体源之间的气体注入组件及整体处理系统示意。 |
| `caption` FIG. 14 | US12595560B2 FIG. 14：基板置于耦合处理体积 → RPS 成等离子体 → 注入组件混合并通入含氢气体 → 活化气体进入工艺腔并暴露基板表面。 |
| label hover | 现无 annotations → 整案无；若证据后续加 hotspot，须整案成套，禁止只标一图。 |

---

## 3. JP2026004352A（AMAT，2026-01-14 公开）

**现况问题：**
- `scope_reason`：「Gap 补录：…Applied 缺口申请人…」
- `claims_or_embodiment_basis`：堆 `[0004]–[0005]` 段落号
- caption 図1 / 図4：含「原件第N页」「公报PDF sha256…」

**提案：**

| 字段 | 提案文案 |
|---|---|
| `short_preview` | AMAT：真空主框架上的预清洁/工艺腔与常压外延腔经压力稳定腔衔接的集群工具。 |
| `technical_summary` | 集群工具分两段主框架：一段在低于约 700 Torr 做工艺（含洗浄/预清洁），另一段在约 700–800 Torr 做常压外延堆积；压力稳定腔承接真空段与常压外延段之间的转移，以提高外延成膜速率与接口稳定性。 |
| `purpose`（可选） | 让预清洁/低压工艺与常压外延在同一集群内衔接，减少压力冲击、提高外延速率。 |
| `novelty`（可选） | 压力稳定腔作为真空工艺段与常压外延段的缓冲接口。 |
| `use`（可选） | 含硅外延路线的集群：预清洁/洗浄 → 压力过渡 → 常压外延堆积。 |
| `claims_or_embodiment_basis` | 系统项主张含圧力安定化腔的集群：洗浄/预清洁腔在第一压力运行，外延堆积腔在大气压附近运行，二者经压力稳定腔衔接。 |
| `scope_reason` | 实施方式明确常压外延堆积与预清洁/洗浄集成；申请人 AMAT；生长对象为含硅外延，非 SiC/GaN 生长对象整案，core。 |
| `caption` 図1 | JP2026004352A 図1：集群工具俯视——两段主框架、中央搬运机器人、周围工艺腔、装载/工厂接口与控制器。 |
| `caption` 図4 | JP2026004352A 図4：基板从工厂接口进入低压第一处理 → 经压力安定化腔升压至约 700–800 Torr → 再入外延堆积腔做常压高温外延。 |
| label hover | 现无 annotations → 整案无；加 hotspot 须整案成套。 |

---

## 4. 其他命中与归属（检索侧备忘）

对 live `report.json` 读者字段扫描（`short_preview` / `technical_summary` / `claims_or_embodiment_basis` / `scope_reason` / `caption` / label desc；模式含 sighting|prior候选|PDF已下载|Sprint|Gap|ruling|已核对|USPTO PDF|晚间）：

| 归属建议 | 公开号（例） | 说明 |
|---|---|---|
| **Preclean（本草案五案）** | US12757665B2、US12660544B2、KR102916044B1、US12595560B2、JP2026004352A | 全部 `discovery_lane=Preclean`；五案外 Preclean-lane 同类命中 **0** |
| **Preclean 同 lane、本次不改** | KR102920833B1 | related；读者字段无上述禁词；附图 0 |
| **EPI** | US12770834B2、US12768074B2、US20260062803A1 | lane=EPI；含晚间/USPTO PDF/gap 等 |
| **EPI / 空 lane（勿由 Preclean 起草）** | US12757648B2、US20250311241A1 等大量「已核对」开场的 scope_reason、部分 caption「USPTO PDF」 | lane 空或非 Preclean；按 GM/PM 归 EPI 或证据 caption 条 |

空 lane 上大量「已核对」开场的 `scope_reason` 不在 Preclean 本包；避免越界改 EPI/基线卡。

---

## 5. 自检（对照 PM brief）

- 五案提案读者字段禁词：晚间 / Gap / Sprint / ruling / sighting / prior候选 / PDF已下载 / 已核对 / caption 内 PDF页·sha → **草案正文为 0**
- 四要素：谁/解决什么/关键点/为何进监测 → 落在 short_preview + technical_summary + scope_reason；purpose/novelty/use 标为可选
- 未改 `event_note` 冒充交付
- 未触碰 `report.json` / stamp / PR

## 6. 交付与锁

- 路径 A：`docs/PRECLEAN-TEXT-REWRITE-DRAFT-2026-10-24.md`（本仓库）
- 路径 B：`/workspace/preclean-search/PRECLEAN-TEXT-REWRITE-DRAFT-2026-10-24.md`
- 锁未动：`actually_read=6`，`research_through=2026-10-20`
- 下一步：等证据 caption/hotspot 条与 PM 过门；**不要**自行 stamp 或开 PR
