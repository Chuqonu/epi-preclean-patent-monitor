# Dot figure-label interaction spec (from live reference 2026-10-20)

Reference: https://45.32.39.201:8443/patent-alert/report.html (do NOT modify Dot/VPS).

## Data
Per figure picture object:
- `annotations` (version 1): `labels[]` with `{number, kind, display_name, display_description, original_name?}`
- `occurrences[]` with `{figure, number, box:[x,y,w,h]}` normalized 0–1 in `coordinate_system: normalized-original-image-xywh`
- Validate: `image_sha256 === (picture.display_sha256 || picture.sha256)`

~197 figures have labels on reference.

## UI classes
- `.figure-display-stage` / `.figure-display-plane` / `.figure-label-overlay`
- `button.figure-label-hotspot` absolute % box over label ink
- `#figure-label-popup.figure-label-popup` fixed dialog: strong `number · display_name` + `p display_description` + close ×
- `details.figure-label-list` below figure: summary「标号释义（N项）」+ dl of all labels

## Events
- pointerenter (non-touch) → show popup
- pointerleave → scheduleClose 160ms (unless pinned / popup hovered)
- focus → show; blur → close if focus left
- click → show + pin; click again when pinned → close
- Esc / pointerdown outside → close
- scroll/resize/visualViewport → reposition; off-screen → close
- Lazy mount via IntersectionObserver rootMargin 700px

## Layout simplify toward Dot shell
Dot first screen: sticky side with home link + filter chips (硬件/工艺, EPI/Preclean) + monthly TOC; resizer; main continuous patents. No heavy top stats bar. Mobile ☰ drawer.
