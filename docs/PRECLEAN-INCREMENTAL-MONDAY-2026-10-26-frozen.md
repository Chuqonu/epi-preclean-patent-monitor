# Preclean 增量 Monday 冻结 2026-10-26（窗口 2026-10-21..10-26）

方法：HANDOFF 2026-10-20.4.2-r2｜Asia/Shanghai｜**禁止零遗漏宣称**｜2025/09 暂停｜未改 report/stamp/push/VPS｜**未读未抄 EPI lane**。

## 四个计数

| 候选 candidates | 公开/授权事件 publication_events | 族 unique_families | 已实际阅读 actually_read |
|---|---|---|---|
| **1** | **1** | **1**（族未跨局闭合，暂 1） | **1**（USPTO 全文 claims+description 今日重读） |

## include_core

| 公开号 | vs live | vs 既有 Preclean freeze | 处置 |
|---|---|---|---|
| **US20260327849A1** | **新（live 无）** | 已在 OFFICIAL-SWEEP-2026-10-23 | **core** 结转待 evidence+PM |

无「相对既有 Preclean freeze 的全新 core」。

## 候选

1. **US20260327849A1**，Kokusai Electric，公开 **2026-10-22**，**core**（结转）。  
   Claim 1：含氟气体 + 还原气体循环改性氧化膜 → 升温去除改性层 → 再生外延膜（说明书 FIG.4 / epitaxial film 600）。  
   source_sha256=`a43695e7e4829f8d103809f6153d954902f113c58d9b2a7353305bf71d7faeb0`；附图未提；同族待核。

## out_of_window_sighting

- **US12772772B2**（AMAT，授权 2026-10-20）：related 倾向；日期 = research_through，**不在**本窗 AFTER 10-20；live 仍无。

## 筛除样例（窗内）

TES US20260334118A1；Kokusai US20260334176A1；TEL US20260333813A1 / US20260334130A1（湿法）；TSMC 湿法/外延结构多件；Shin-Etsu SiC US20260334174A1；EP4827304（SiC 刻蚀）等——详见 json `excluded_samples`。

## 检索与覆盖

- **GP**：P0–P6 预取 + 今日 P7–P20（sort:new：NF3/ClF3 RPC、HF vapor、SiCoNi、Applied/TEL/Lam、CPC H01L21/02041|/0206、CN 预清洗/原位清洗、JP/KR）+ after:publication 探针 → **窗内 0 命中**；`semiconductor` after:20261021 亦 0（索引滞后）。
- **USPTO PPUBS 今日 API**：session 可用，但 `searchWithBeFamily`/`query` 400/404；highlight 对已知号 NOT_FOUND → **回退** 2026-10-23 官方全文与 q1–q4。
- **日历**：窗内仅 **10-22 US PGPub** 与 **10-21 EP**（EP 已在官方扫 6192 件、0 纳入）；10-23..26 无 US 授权/公开日、无 EP 公开日。
- **J-PlatPat / CNIPA / KIPRIS / Espacenet / PATENTSCOPE**：仍 FAIL。

## research_through

建议维持 **2026-10-20**，直至结转 core 过 evidence+PM 再议上调。

## 文件

- `/workspace/epi-monday-2026-10-26/PRECLEAN-INCREMENTAL-MONDAY-2026-10-26-frozen.json`
- `/workspace/epi-monday-2026-10-26/PRECLEAN-INCREMENTAL-MONDAY-2026-10-26-search-log.md`
- raw：`/workspace/epi-monday-2026-10-26/raw/preclean/`（含 `SHA256SUMS.txt`、`uspto/r5carry_*`、`P7`–`P20`）
