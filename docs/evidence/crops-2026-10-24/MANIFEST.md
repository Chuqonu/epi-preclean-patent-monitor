# 像素 crop 交付清单（2026-10-24）

> 证据复核产出。**未改** report.json / stamp / 仓库 / 未开 PR。
> 冻结口径：像素内正立（不靠 CSS）、长边≤3000、去 letter 页边；一页多图优先拆分。

## 汇总

- 总产出 PNG：**37**
- `US12770834B2`: **8** 张（源报告 8 条；本轮按页出图，含 rot 校正）
- `US12768074B2`: **23** 张（源报告 13 条；子图拆分后多于 13；拆分张数 17）
- §3 `TW202628839A`: **3** 张
- §3 `WO2026096517A1`: **3** 张

## 口径核对

- 长边 >3000：**0**（应为 0）
- content_fill（墨迹外接框/画面）<0.70：**0**（目标 ≥~0.70；偏低见 notes）
- `ink_density` = 非近白像素占比（线稿天然偏低，**不是**验收主指标）；`content_fill` 才反映去留白松紧。

## 逐张

| 公开号 | figure_number | 源PDF页 | 原 display_rotation | 实烤方向 | 新 W×H | 长边 | content_fill | ink_density | 子图拆分 | sha256 | 文件 | notes |
|---|---|---:|---:|---|---|---:|---:|---:|---|---|---|---|
| US12770834B2 | Fig. 1 | 3 | 0 | 90CW | 3000×1793 | 3000 | 0.923 | 0.021 | 否 | `6b285dec7534627c01ae21ad529ac7ca8f6e649f922c1f8d265c3bc5bd32d053` | `US12770834B2/US12770834B2_Fig1_upright.png` | report_display_rotation=0; baked_orient=90CW; downscaled long≤3000 |
| US12770834B2 | Fig. 2 | 4 | 0 | 90CW | 3000×1972 | 3000 | 0.929 | 0.022 | 否 | `72cef99fd1db6028fe58e46543ef82d045d73c6ed659c6c846c43c53aa11a826` | `US12770834B2/US12770834B2_Fig2_upright.png` | report_display_rotation=0; baked_orient=90CW; downscaled long≤3000 |
| US12770834B2 | Fig. 3 | 5 | 0 | none | 2594×3000 | 3000 | 0.938 | 0.064 | 否 | `6679b08380f59ce0862c67cada8a4cbcd6c4d03c1a1584c554282f881fdb3e0e` | `US12770834B2/US12770834B2_Fig3_upright.png` | report_display_rotation=0; baked_orient=none; downscaled long≤3000 |
| US12770834B2 | Fig. 4A | 6 | 90 | 90CW | 3000×2423 | 3000 | 0.935 | 0.028 | 否 | `dbcd7b83e3603e5f6276b2dd4ca3b4b5c1cbe2f7466d1dafc57ef00540444a4f` | `US12770834B2/US12770834B2_Fig4A_upright.png` | report_display_rotation=90; baked_orient=90CW; downscaled long≤3000 |
| US12770834B2 | Fig. 4B | 7 | 90 | 90CW | 1728×2609 | 2609 | 0.928 | 0.115 | 否 | `4b956f769d7e82eecca723cf5dc38e4e4210cc4ec57da0203f88acd6364126d7` | `US12770834B2/US12770834B2_Fig4B_upright.png` | report_display_rotation=90; baked_orient=90CW |
| US12770834B2 | Fig. 5 | 8 | 0 | none | 1627×3000 | 3000 | 0.920 | 0.048 | 否 | `4a64bd199c1b585975790690fbc8bf77cefed4c9d07b6f5fdc23bd1c92a8a2a4` | `US12770834B2/US12770834B2_Fig5_upright.png` | report_display_rotation=0; baked_orient=none; downscaled long≤3000 |
| US12770834B2 | Fig. 6 | 9 | 0 | none | 2177×3000 | 3000 | 0.933 | 0.045 | 否 | `0bc58ffbb32fc37bd12380e8c3766894f3bbf832336c299562a325a79c18cf4b` | `US12770834B2/US12770834B2_Fig6_upright.png` | report_display_rotation=0; baked_orient=none; downscaled long≤3000 |
| US12770834B2 | Fig. 7 | 10 | 0 | none | 1794×3000 | 3000 | 0.923 | 0.029 | 否 | `4e19e1d5edbb421ae37b5b8626972d38e5de5cf2591d86653f4978245cd61d9d` | `US12770834B2/US12770834B2_Fig7_upright.png` | report_display_rotation=0; baked_orient=none; downscaled long≤3000 |
| US12768074B2 | Fig. 10A | 15 | 0 | 90CW | 3000×2220 | 3000 | 0.933 | 0.086 | 否 | `ba08e318df5dc95718b30e28174f492ecb080bdd6fcfa47434a3a3d2a06ea375` | `US12768074B2/US12768074B2_Fig10A_upright.png` | report_display_rotation=0; baked_orient=90CW; downscaled long≤3000 |
| US12768074B2 | Fig. 10B | 16 | 0 | 90CW | 2888×3000 | 3000 | 0.957 | 0.032 | 是 | `b086c0fd0cdc7dbde01c6eaebebbda862b0e365014d9911bebacb6227f5673f3` | `US12768074B2/US12768074B2_Fig10B_upright.png` | report_display_rotation=0; baked_orient=90CW; OCR-split; labels=['FIG. 10B', 'FIG. 10C']; downscaled long≤3000 |
| US12768074B2 | Fig. 10C | 16 | 0 | 90CW | 1937×1871 | 1937 | 0.955 | 0.083 | 是 | `b5cba75acd01a422e75b2842ea829fd4a586068bdfec82f7dd3ce63c41091d47` | `US12768074B2/US12768074B2_Fig10C_upright.png` | report_display_rotation=0; baked_orient=90CW; OCR-split; labels=['FIG. 10B', 'FIG. 10C'] |
| US12768074B2 | Fig. 1 | 4 | 0 | 90CW | 3000×2671 | 3000 | 0.939 | 0.094 | 否 | `9958ef16fc59f61098aca422d86af5458a1664383835d89aa5b38b9acb55fc36` | `US12768074B2/US12768074B2_Fig1_upright.png` | report_display_rotation=0; baked_orient=90CW; downscaled long≤3000 |
| US12768074B2 | Fig. 2A | 5 | 0 | none | 3000×1753 | 3000 | 0.948 | 0.053 | 是 | `4cba0412be0c133020aabe2b5b294c3a3601e5892478fcbc95a744c8c8d6d629` | `US12768074B2/US12768074B2_Fig2A_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 2A', 'FIG. 2B', 'FIG. 2C']; downscaled long≤3000 |
| US12768074B2 | Fig. 2B | 5 | 0 | none | 2843×1931 | 2843 | 0.951 | 0.099 | 是 | `3373c9b7c58071538c3e188188c4d3ebcd7e984c77e692b5d9eaf8a33d35c6ad` | `US12768074B2/US12768074B2_Fig2B_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 2A', 'FIG. 2B', 'FIG. 2C'] |
| US12768074B2 | Fig. 2C | 5 | 0 | none | 2838×1641 | 2838 | 0.937 | 0.061 | 是 | `c154f86d9eefb467cfe731f396b531958b8c086520111290bafc7984bf85bf6d` | `US12768074B2/US12768074B2_Fig2C_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 2A', 'FIG. 2B', 'FIG. 2C'] |
| US12768074B2 | Fig. 3A | 6 | 0 | none | 2969×2801 | 2969 | 0.956 | 0.071 | 是 | `ee1dd07a323d8ba905009a14371697fadb221c9b42c64292ca73ff596fa08f15` | `US12768074B2/US12768074B2_Fig3A_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 3A', 'FIG. 3B', 'FIG. 3C'] |
| US12768074B2 | Fig. 3B | 6 | 0 | none | 2907×1795 | 2907 | 0.971 | 0.097 | 是 | `16e9343702f0015a331a142e080d5cd3aa53031f13ce1e27a62a943431a1af1e` | `US12768074B2/US12768074B2_Fig3B_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 3A', 'FIG. 3B', 'FIG. 3C'] |
| US12768074B2 | Fig. 3C | 6 | 0 | none | 2599×1186 | 2599 | 0.940 | 0.081 | 是 | `5175d4272f6c106b07ead14751fb8dc8c1aa43d3a4056f70eb16c446c2bc0668` | `US12768074B2/US12768074B2_Fig3C_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 3A', 'FIG. 3B', 'FIG. 3C'] |
| US12768074B2 | Fig. 4A | 7 | 0 | 90CW | 3000×1381 | 3000 | 0.909 | 0.087 | 否 | `abb485d8abe83526a9e400a3d16009bccaf02fa596b1432d3f85774f29a0ea6f` | `US12768074B2/US12768074B2_Fig4A_upright.png` | report_display_rotation=0; baked_orient=90CW; downscaled long≤3000 |
| US12768074B2 | Fig. 4B | 8 | 90 | 90CW | 3000×1248 | 3000 | 0.904 | 0.055 | 否 | `c1875bba22d8a5a8758d0c299f68b988501c663d223079f5c22290e2c43479f9` | `US12768074B2/US12768074B2_Fig4B_upright.png` | report_display_rotation=90; baked_orient=90CW; downscaled long≤3000 |
| US12768074B2 | Fig. 4C | 9 | 0 | none | 3000×1698 | 3000 | 0.946 | 0.061 | 是 | `5cb76252114894080429552e54cbf1a8bbacaae40562ce3716b6e80cac30aa86` | `US12768074B2/US12768074B2_Fig4C_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 4C', 'FIG. 4D', 'FIG. 4E']; downscaled long≤3000 |
| US12768074B2 | Fig. 4D | 9 | 0 | none | 3000×1848 | 3000 | 0.971 | 0.069 | 是 | `65bc9df1ecc57ec0095cf7225476a6c9d8efdd77ac7d0ff5808ae511aab742b3` | `US12768074B2/US12768074B2_Fig4D_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 4C', 'FIG. 4D', 'FIG. 4E']; downscaled long≤3000 |
| US12768074B2 | Fig. 4E | 9 | 0 | none | 3000×1244 | 3000 | 0.938 | 0.075 | 是 | `76594cf98286e0e456bd4fa90f738de1c8c8fac58626b1513069347023411240` | `US12768074B2/US12768074B2_Fig4E_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 4C', 'FIG. 4D', 'FIG. 4E']; downscaled long≤3000 |
| US12768074B2 | Fig. 5A | 10 | 0 | 90CW | 3000×717 | 3000 | 0.854 | 0.071 | 是 | `33f49325b51b8d8fa7dd01840ea84761a764210ac60af181e4500c2a6a50c025` | `US12768074B2/US12768074B2_Fig5A_upright.png` | report_display_rotation=0; baked_orient=90CW; ink-gap-split (OCR incomplete); downscaled long≤3000 |
| US12768074B2 | Fig. 5B | 10 | 0 | 90CW | 3000×2041 | 3000 | 0.930 | 0.085 | 是 | `af353fa4a08b13c50e27e7c2a132e38e4e1d86af510f6d5ce5049e35579cc3b2` | `US12768074B2/US12768074B2_Fig5B_upright.png` | report_display_rotation=0; baked_orient=90CW; ink-gap-split (OCR incomplete); downscaled long≤3000 |
| US12768074B2 | Fig. 6A | 11 | 0 | none | 3000×2477 | 3000 | 0.953 | 0.051 | 是 | `082cea5a8a1849e22b641616e6ca108b3031c16ff181009f578a341607c939b9` | `US12768074B2/US12768074B2_Fig6A_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 6A', 'FIG. 6B']; downscaled long≤3000 |
| US12768074B2 | Fig. 6B | 11 | 0 | none | 3000×1698 | 3000 | 0.946 | 0.039 | 是 | `d280f4d3b1380aeb42bc646573de301f8cd932046d2403fee71642f8662cf528` | `US12768074B2/US12768074B2_Fig6B_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 6A', 'FIG. 6B']; downscaled long≤3000 |
| US12768074B2 | Fig. 7 | 12 | 0 | none | 2963×3000 | 3000 | 0.942 | 0.027 | 否 | `3eb3f52c10a210697054fb4759a22d357ecac051596ae1ba4ae876d22dbc0203` | `US12768074B2/US12768074B2_Fig7_upright.png` | report_display_rotation=0; baked_orient=none; downscaled long≤3000 |
| US12768074B2 | Fig. 8A | 13 | 0 | none | 3000×2766 | 3000 | 0.956 | 0.044 | 是 | `b09ab6a36305f977240a46a4e242ffe4f5375efed64e96849eb5a2728d801865` | `US12768074B2/US12768074B2_Fig8A_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 8A', 'FIG. 8B']; downscaled long≤3000 |
| US12768074B2 | Fig. 8B | 13 | 0 | none | 3000×1612 | 3000 | 0.944 | 0.030 | 是 | `4af87fa1022670383413c4fe72a493b62d0b64352381685a1cad01101043bbbf` | `US12768074B2/US12768074B2_Fig8B_upright.png` | report_display_rotation=0; baked_orient=none; OCR-split; labels=['FIG. 8A', 'FIG. 8B']; downscaled long≤3000 |
| US12768074B2 | Fig. 9 | 14 | 0 | none | 3000×2718 | 3000 | 0.940 | 0.029 | 否 | `9a1665923d096ad89020b7604f29d3668c19f4b8f2dd00ccab2df7b62d527f19` | `US12768074B2/US12768074B2_Fig9_upright.png` | report_display_rotation=0; baked_orient=none; downscaled long≤3000 |
| TW202628839A | Fig. 1 | — | 0 | none | 2011×2222 | 2222 | 0.882 | 0.038 | 否 | `cf97aec6deef9240a25b0859bec3800f6210315d8726cb12d88362da13b9b16c` | `TW202628839A/TW202628839A_Fig1_upright.png` | source_png from repo assets/figures/; TW↔WO byte-identical upstream assets |
| TW202628839A | Fig. 2 | — | 0 | none | 1935×2367 | 2367 | 0.876 | 0.052 | 否 | `d5e30e8d179f8544d19274320a6dae583cf8928d951b37c5604e158424f19512` | `TW202628839A/TW202628839A_Fig2_upright.png` | source_png from repo assets/figures/; TW↔WO byte-identical upstream assets |
| TW202628839A | Fig. 3 | — | 0 | none | 1895×2361 | 2361 | 0.875 | 0.061 | 否 | `33a0004ed812ebc5dfd384ddfe8c2c59827790c07109c03305f126368ed0ccd3` | `TW202628839A/TW202628839A_Fig3_upright.png` | source_png from repo assets/figures/; TW↔WO byte-identical upstream assets |
| WO2026096517A1 | Fig. 1 | — | 0 | none | 2011×2222 | 2222 | 0.882 | 0.038 | 否 | `cf97aec6deef9240a25b0859bec3800f6210315d8726cb12d88362da13b9b16c` | `WO2026096517A1/WO2026096517A1_Fig1_upright.png` | source_png from repo assets/figures/; TW↔WO byte-identical upstream assets |
| WO2026096517A1 | Fig. 2 | — | 0 | none | 1935×2367 | 2367 | 0.876 | 0.052 | 否 | `d5e30e8d179f8544d19274320a6dae583cf8928d951b37c5604e158424f19512` | `WO2026096517A1/WO2026096517A1_Fig2_upright.png` | source_png from repo assets/figures/; TW↔WO byte-identical upstream assets |
| WO2026096517A1 | Fig. 3 | — | 0 | none | 1895×2361 | 2361 | 0.875 | 0.061 | 否 | `33a0004ed812ebc5dfd384ddfe8c2c59827790c07109c03305f126368ed0ccd3` | `WO2026096517A1/WO2026096517A1_Fig3_upright.png` | source_png from repo assets/figures/; TW↔WO byte-identical upstream assets |

## 源与限制

- **US12770834B2 / US12768074B2**：官方 USPTO PDF → `pdftoppm -r 150` → 去页眉 → **OCR/墨迹自动正立**（不盲信 report 的 display_rotation）→ 紧裁 → 长边>3000 则等比缩小。
- **一页多图**：优先 OCR `FIG. N` 标签分带；失败则墨迹投影缺口拆分；仍失败则整页紧裁并在 notes 标明 UNSPLIT。
- **TW202628839A / WO2026096517A1**：工作区无可用官方 PDF（`figures-fetch/*.pdf` 实为 HTML）。从仓库现网 PNG 去留白。**上游资产 TW↔WO 三对 PNG 字节级相同**（仓库既有问题），本轮如实裁切并标注；补官方公报 PDF 前无法区分二者图面。
- 未写入 report.json，未重算 stamp，未 push，未开 PR。
