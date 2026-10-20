# Recovering the reference report's real patent figures

The baseline import kept 130 figure references but only three image files. Its source report uses progressive loading: blank SVGs in `report-data` reserve image space, and the actual raster bytes appear later in `image-chunk-N` JSON elements. Empty SVGs are not patent drawings.

This recovery contains 130 references to 129 distinct real raster files. The files were copied without rotation, cropping or re-encoding. The image bytes, dimensions, source publication and exact caption were checked against the public reference report. This restores the imported figures; it does not certify the research decisions or supply drawings for the nine separately added entries that have no figure metadata.

## Contents

- `assets/figures/recovered/`: images named by their actual SHA-256 hash.
- `data/figure-recovery-map.json`: a mapping whose key is the JSON encoding of `[representative_publication_id, caption, source_publication_id]`.
- `scripts/restore_reference_figures.py`: a Python standard-library validator and narrowly scoped updater.

The mapping retains the original hash, displayed-image hash, exact source URL, PDF page, dimensions and figure caption. Some optimized WebP bytes match `source_display_sha256`; their source chunk key still uses the original `source_original_sha256`. They must not be rejected or mismatched merely because those two hashes differ.

## Apply to the latest report

Run from the repository root:

```sh
python3 scripts/restore_reference_figures.py --check
python3 scripts/restore_reference_figures.py --apply
python3 scripts/restore_reference_figures.py --check
```

`--check` writes nothing. It returns **0** when already applied, **1** when the validated restoration is needed, and **2** on a validation error. `--apply` validates all 129 asset checksums, sizes and raster dimensions, plus all 130 exact record matches, before atomically replacing the report JSON. Re-running it is a no-op. An optional `--report /path/to/copy.json` allows checking or applying against a temporary copy while reading assets from this repository.

Only image paths, dimensions, asset provenance and unambiguous `Fig.?#1` placeholders are updated. Placeholder labels are recovered from the existing source caption or source figure label; the source captions are preserved. No publication dates, family relationships, research/evidence decisions, pending entries, source URLs or scope classifications are changed. If captions or publication attribution have changed since the mapping was prepared, the updater stops for reconciliation instead of guessing. Additional figures outside the mapping remain intact and must reference existing assets.

`counts.figures`, `counts.figures_available` and `counts.figures_pending` count image references. Multiple patent cards may legitimately use one same-family source image. Publication/event/family totals are deliberately not changed by this image-only operation.

After applying, rebuild the Excel ledger through the repository's normal process, review the report visually, and publish through the normal GitHub workflow. Verify readable figure labels, correct orientation, loading without a page jump, newest-first order in both panes, and that scrolling does not expand collapsed months. Preserve explicit notices when a figure comes from a different same-family publication.

## Repeating the extraction

For a new public reference snapshot, parse `report-data` and all `script[id^="image-chunk-"]` JSON elements without executing JavaScript. Match every target image using its representative publication, exact caption and source publication. Resolve its raster from the chunk bank using its original or displayed-image hash; validate decoded bytes against either recorded hash. Export only matched public patent raster bytes and necessary source metadata. Do not use positional matching, generate substitute drawings, or import unrelated months merely to restore images.

The frozen reference report used here has SHA-256:

`f336e5358a930a5d7430ca266e8bc8f20d03c8f2d348a0c5b6929c775fb5b636`

## Required display rotations

Nine existing image references have `display_rotation: 90` in the reference report. Their bytes are intentionally unrotated; the reference page turns them clockwise in the display layer. The restoration preserves this field. The renderer must honor `display_rotation` and reserve the **swapped** width/height ratio for 90°/270° before loading. Merely inserting the recovered `<img>` will leave these figures sideways. Do not apply `source_geometry.extraction_rotation_degrees` again: that describes a transformation already baked into the saved bytes. Crop geometry is provenance, not a request to crop again.
