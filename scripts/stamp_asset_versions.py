#!/usr/bin/env python3
"""Write content-hash query strings into index.html for cache-safe GitHub Pages deploys."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
MANIFEST = ROOT / "data" / "asset-versions.json"

ASSETS = {
    "report.css": ROOT / "assets" / "css" / "report.css",
    "report.js": ROOT / "assets" / "js" / "report.js",
    "report.json": ROOT / "data" / "report.json",
}


def file_hash(path: Path, nbytes: int = 12) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:nbytes]


def stamp_index(versions: dict[str, str]) -> None:
    html = INDEX.read_text(encoding="utf-8")
    css_q = versions["report.css"]
    js_q = versions["report.js"]
    data_q = versions["report.json"]

    html = re.sub(
        r'href="assets/css/report\.css(?:\?v=[^"]*)?"',
        f'href="assets/css/report.css?v={css_q}"',
        html,
        count=1,
    )
    html = re.sub(
        r'src="assets/js/report\.js(?:\?v=[^"]*)?"',
        f'src="assets/js/report.js?v={js_q}"',
        html,
        count=1,
    )
    meta_pat = r'<meta name="epi-report-data" content="data/report\.json(?:\?v=[^"]*)?">'
    meta_new = f'<meta name="epi-report-data" content="data/report.json?v={data_q}">'
    if re.search(meta_pat, html):
        html = re.sub(meta_pat, meta_new, html, count=1)
    else:
        html = html.replace(
            '<meta name="viewport"',
            meta_new + "\n  " + '<meta name="viewport"',
            1,
        )
    INDEX.write_text(html, encoding="utf-8")


def main() -> int:
    versions = {k: file_hash(p) for k, p in ASSETS.items()}
    manifest = {
        "stamped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": versions,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stamp_index(versions)
    print("stamped", versions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
