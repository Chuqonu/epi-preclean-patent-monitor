# Automation (Grok Bot platform routines — **not** GitHub Actions)

September **2025-09** remains paused.

## Platform schedules (configuration target)

| Folder | CRON (Asia/Shanghai) | Intent |
|--------|----------------------|--------|
| `epi` | `CRON_TZ=Asia/Shanghai` `0 9 * * 1` | Weekly incremental |
| `epi-2` | `CRON_TZ=Asia/Shanghai` `0 9 1 * *` | Monthly full review |

Next monthly window (planned): **~2026-11-01 09:08** Asia/Shanghai.

**Status:** weekly and monthly jobs have **not** auto-fired on this repo yet. Do not claim scheduler verified until a real timed run is logged.

## Three non-substitutable states

| Label | Meaning |
|-------|---------|
| **配置核实** | Cron expression and folder mapping documented above; not proven in production. |
| **手动跑同流程** | Human/agent runs the same search → evidence → merge → PR → Pages manually (`manual_pages`). |
| **实际定时触发** | A platform cron run completed; must append `docs/runs/YYYY-MM-DD-<job>.md` with timestamp and outcome. |

## Other honest labels

- **`figures_external_pr`** — Real WebP/mapping from reference `image-chunk-*` PR (chunk key ≈ original sha256; do not mix display WebP hash). No mass PDF rasterize in this repo.
- **`import_baseline.py`** — Placeholder; baseline loaded via documented import path, not empty CLI.

## Run log template

See `docs/runs/TEMPLATE.md`.
