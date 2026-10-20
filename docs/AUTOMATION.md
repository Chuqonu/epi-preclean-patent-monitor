# Automation labels (honest status)

Use these three labels in ops notes and `status_note` until a scheduler is verified end-to-end:

| Label | Meaning |
|-------|---------|
| **`manual_pages`** | Site updates by merged PR to `main`; GitHub Pages rebuild only. No claim of cron. |
| **`schedule_unverified`** | HANDOFF targets (Mon 09:00 Asia/Shanghai incremental; monthly 1st full review) are **not** proven on this repo yet. |
| **`figures_external_pr`** | Real figure WebP/mapping comes from a separate PR (`image-chunk-*` keys ≈ original sha256; do not confuse with display WebP hash). This repo does not mass-rasterize ~130 PDF refs in CI. |

September **2025-09** remains paused (no search, review, or publish).
