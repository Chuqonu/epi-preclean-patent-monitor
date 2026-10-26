# 设计 · PR#43 reader 布局验收（附图中文复检）

**结论：附图中文门待设计目视确认**（数据/脚本门已过；head `26d1261`）

- PR：https://github.com/Chuqonu/epi-preclean-patent-monitor/pull/43
- head：`26d12612144d2e55e1eb7c167acc07cdcac980bd`
- css/js/json：`15660946b92b` / `358e8bb63bb5` / `d99256556f40`
- 预览：`http://127.0.0.1:8766/#2026-10-US12770834B2` / `#2026-10-US12765027B2`（须带 `index.html` 内 json `?v=d99256556f40`）

## 对照截图（FAIL 基线 vs 当前数据）

| 专利 | 设计 FAIL 截图现象 | 当前 `display_caption`（`data/report.json`） |
|------|-------------------|---------------------------------------------|
| US12770834B2 Fig.1/2 | `图N —` + **英文** schematic view… | `图1 — 包括远程等离子体单元…` / `图2 — 图1的半导体处理系统…`（全中文正文） |
| US12765027B2 | 中文正文（元数据 + 冒号后技术句） | `…图3C/3D…：掺杂接触层与未掺杂保护帽层。`（仍为对照 OK 风格） |

## 门禁（工程审计）

| 门 | 结果 | 说明 |
|---|---|---|
| 专利基本信息含发明人 | **PASS** | 未改 UI 结构 |
| 无相关性行 / 无工艺 chip | **PASS** | |
| 附图 `display_caption` 正文中文 | **数据 PASS** | `apply_reader_layout_track.py` 审计 `english_leaning_count=0/205` |
| 标注 hover（65027） | **PASS** | 122 verified；70834 空标为已知 residual |
| Fig.3 US12770834B2 lock | **PASS** | `asset_sha256` `86d43c6237ae`，`display_rotation=0` |

## 改法（已落地）

1. `display_caption` 正文机器翻译 + preclean 归一化（`图N —` + 中文技术句，不单改前缀）。
2. 读者 `readerFigureCaption()` 优先 `display_caption`（`report.js` 未改行为）。
3. 重新 `stamp_asset_versions.py` → json `d99256556f40`。

**设计复检**：请硬刷新或确认加载 json 戳非 `1e0593123ee1`（旧 FAIL 头 `aa6c722`）。
