# Flipped figures audit (vision-confirmed)

Live stamp: `report.json?v=7c388ebf1040` — all `display_rotation=0`.

## Confirmed sideways (fix)

| Pub | Fig | Recommended display_rotation | Notes |
|-----|-----|------------------------------|-------|
| US12757647B2 | 图4 / Fig.4 | **90** | USPTO header upright; drawing + callouts (400–412) and FIG.4 text sideways (need CW 90 to read). sha `e5d5f61dac3d4b7a…` |

## Checked OK (same 1397×1800 sheet class — do not rotate)

- US12740346B2 图7
- US12701931B2 图4
- US20260313994A1 Fig.14–16
- US20260250879A1 Fig.3 / Fig.4A

## OSD false positives (do NOT apply)

- TW202628839A Fig.2, WO2026096517A1 Fig.2 (Gate③ upright art)
- US20260076125A1 Fig.1 flowchart
- WO2025222891A1 Fig.7/8
- US20260150594A1 图4 (chamber drawing upright on visual)

## Rule

Vision confirm before any `display_rotation` change. Prefer metadata rotate over re-encoding pixels.
