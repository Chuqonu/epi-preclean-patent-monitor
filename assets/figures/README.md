# Patent figures

Store **real** patent drawings extracted from official PDFs or patent office pages only.

Naming suggestion: `{publication_number}_fig{N}.png`  
Example: `US20250324699A1_fig1.png`

Each image referenced from `data/report.json` must include:

- `path` relative to repo root (e.g. `assets/figures/US….png`)
- `width` / `height` (intrinsic pixels, for layout reservation)
- `source_publication` + `figure_label` (shown in caption)
- `source_url` back to the patent source

**Never** commit AI-generated or placeholder “fake patent” artwork as figures.
