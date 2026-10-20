#!/usr/bin/env python3
"""Restore reviewed public figure assets into an evolving report, using stdlib only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile


def key_for(publication, caption, source_publication):
    return json.dumps([publication, caption, source_publication], ensure_ascii=False, separators=(",", ":"))


def image_dimensions(data):
    """Read PNG, JPEG and WebP dimensions without re-encoding the image."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        offset = 12
        while offset + 8 <= len(data):
            kind = data[offset:offset + 4]
            length = int.from_bytes(data[offset + 4:offset + 8], "little")
            payload = data[offset + 8:offset + 8 + length]
            if kind == b"VP8X":
                return 1 + int.from_bytes(payload[4:7], "little"), 1 + int.from_bytes(payload[7:10], "little")
            if kind == b"VP8 " and payload[3:6] == b"\x9d\x01\x2a":
                width, height = struct.unpack("<HH", payload[6:10])
                return width & 0x3FFF, height & 0x3FFF
            if kind == b"VP8L" and payload[:1] == b"\x2f":
                value = int.from_bytes(payload[1:5], "little")
                return (value & 0x3FFF) + 1, ((value >> 14) & 0x3FFF) + 1
            offset += 8 + length + (length % 2)
    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset < len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            while offset < len(data) and data[offset] == 0xFF:
                offset += 1
            marker = data[offset]
            offset += 1
            if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
                continue
            length = int.from_bytes(data[offset:offset + 2], "big")
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height, width = struct.unpack(">HH", data[offset + 3:offset + 7])
                return width, height
            if length < 2:
                break
            offset += length
    raise ValueError("Unsupported or malformed raster image")


def safe_asset(root, relative_path):
    path = (root / relative_path).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Asset path escapes repository root")
    return path


def validate_map(root, mapping):
    entries = mapping["entries"]
    if len(entries) != mapping["reference_count"]:
        raise ValueError("Map reference count mismatch")
    verified = set()
    for key, item in entries.items():
        expected = key_for(item["representative_publication_id"], item["caption"], item["source_publication_id"])
        if key != expected:
            raise ValueError("Malformed composite match key")
        path = safe_asset(root, item["local_asset_path"])
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != item["asset_sha256"] or len(data) != item["bytes"]:
            raise ValueError("Asset checksum/size mismatch: " + item["local_asset_path"])
        if digest not in (item["source_original_sha256"], item["source_display_sha256"]):
            raise ValueError("Asset has no matching source digest")
        if image_dimensions(data) != (item["width"], item["height"]):
            raise ValueError("Asset dimensions mismatch: " + item["local_asset_path"])
        verified.add(digest)
    if len(verified) != mapping["unique_asset_count"]:
        raise ValueError("Map unique asset count mismatch")
    return len(verified)


def restore(root, document, mapping):
    result = copy.deepcopy(document)
    matched = set()
    changed_figures = 0
    repaired_labels = 0
    figures = []
    for month in result.get("months", []):
        for row in month.get("families", []):
            publication = row.get("publication_id", row.get("publication_number", ""))
            for figure in row.get("figures", []):
                figures.append(figure)
                key = key_for(publication, figure.get("caption", ""), figure.get("source_publication_id", ""))
                item = mapping["entries"].get(key)
                if item is None:
                    continue
                if key in matched:
                    raise ValueError("Ambiguous duplicate figure match: " + publication)
                matched.add(key)
                before = copy.deepcopy(figure)
                # Preserve the exact existing caption, publication/source attribution and
                # every research/evidence field. Only restore asset provenance and dimensions.
                for field in (
                    "local_asset_path",
                    "width",
                    "height",
                    "asset_sha256",
                    "source_original_sha256",
                    "source_display_sha256",
                    "pdf_page",
                    "display_rotation",
                    "source_geometry",
                ):
                    if item.get(field) is not None:
                        figure[field] = item[field]
                rot = figure.get("display_rotation") or 0
                w = int(figure.get("width") or 0)
                h = int(figure.get("height") or 0)
                if rot in (90, 270) and w > 0 and h > w:
                    figure["display_rotation"] = 0
                    geom = figure.get("source_geometry")
                    if isinstance(geom, dict):
                        geom["display_rotation"] = 0
                if "?" in figure.get("figure_number", "") and item.get("figure_number"):
                    figure["figure_number"] = item["figure_number"]
                    repaired_labels += 1
                changed_figures += figure != before
    missing = sorted(set(mapping["entries"]) - matched)
    if missing:
        names = [mapping["entries"][key]["representative_publication_id"] for key in missing]
        raise ValueError("Map entries no longer match current report; reconcile captions/source IDs before applying: " + ", ".join(names))
    available = 0
    for figure in figures:
        relative_path = figure.get("local_asset_path")
        if not relative_path:
            continue
        path = safe_asset(root, relative_path)
        if not path.is_file():
            raise ValueError("Existing report references missing asset: " + relative_path)
        image_dimensions(path.read_bytes())
        available += 1
    counts = result.setdefault("counts", {})
    # These count figure references, not deduplicated files or patent events.
    counts["figures"] = len(figures)
    counts["figures_available"] = available
    counts["figures_pending"] = len(figures) - available
    return result, {"matched_references": len(matched), "changed_figures": changed_figures, "repaired_labels": repaired_labels, "figure_references": len(figures), "available_figure_references": available, "missing_figure_references": len(figures) - available}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--report", type=Path, help="Report path; default ROOT/data/report.json. Use a temporary copy for a dry-run integration.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Validate assets and mapping; return 1 if report needs restoration, 0 if already current.")
    mode.add_argument("--apply", action="store_true", help="Atomically apply the narrow figure-only update after all validations pass.")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        report_path = (args.report or root / "data/report.json").resolve()
        mapping = json.loads((root / "data/figure-recovery-map.json").read_text(encoding="utf-8"))
        original = json.loads(report_path.read_text(encoding="utf-8"))
        unique_assets = validate_map(root, mapping)
        result, stats = restore(root, original, mapping)
        changed = original != result
        if args.apply and changed:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=report_path.parent, prefix=report_path.name + ".", suffix=".tmp", delete=False) as handle:
                json.dump(result, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
                temp_path = Path(handle.name)
            temp_path.replace(report_path)
        print(json.dumps({"mode": "apply" if args.apply else "check", "unique_assets_verified": unique_assets, "needs_changes": changed, "written": bool(args.apply and changed), **stats}, ensure_ascii=False))
        return 1 if args.check and changed else 0
    except (ValueError, KeyError, OSError, struct.error, IndexError) as error:
        print("Figure recovery failed: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
