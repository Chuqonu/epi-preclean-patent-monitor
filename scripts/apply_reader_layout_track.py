#!/usr/bin/env python3
"""Reader-layout track: CN display captions, inventors (OG), dot annotations merge."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "report.json"
DOT_EXTRACT = ROOT / "docs/dot-figure-annotations-extract.json"
PRECLEAN_REWRITE = ROOT / "docs/preclean-search/PRECLEAN-READER-REWRITE-2026-10-24.json"
OG_SECTION_BY_WEEK: dict[int, str] = {
    24: "1547-3",
    40: "1551-1",
    41: "1551-2",
    42: "1551-3",
    47: "1540-4",
}
OG_SECTION_FALLBACKS = ("1551-3", "1551-2", "1551-1", "1547-3", "1540-4")


def figure_sha(fig: dict) -> str | None:
    for k in (
        "asset_sha256",
        "source_display_sha256",
        "sha256",
        "source_original_sha256",
    ):
        v = fig.get(k)
        if v:
            return v
    return None


def annotations_verified(fig: dict) -> bool:
    ann = fig.get("annotations")
    if not ann or ann.get("version") != 1:
        return False
    if not (ann.get("labels") or []):
        return False
    sha = figure_sha(fig)
    return bool(sha and ann.get("image_sha256") == sha)


def load_dot_by_sha() -> tuple[dict[str, dict], dict[str, str]]:
    extract = json.loads(DOT_EXTRACT.read_text(encoding="utf-8"))
    by_sha: dict[str, dict] = {}
    caption_by_sha: dict[str, str] = {}
    for row in extract.get("figures") or []:
        cap = (row.get("caption") or "").strip()
        for k in ("display_sha256", "sha256"):
            s = row.get(k)
            if s:
                by_sha[s] = row
                if cap:
                    caption_by_sha[s] = cap
        ann = row.get("annotations") or {}
        s2 = ann.get("image_sha256")
        if s2:
            by_sha[s2] = row
            if cap:
                caption_by_sha[s2] = cap
    return by_sha, caption_by_sha


def merge_dot_annotations(report: dict, by_sha: dict[str, dict]) -> int:
    matched = 0
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            for fig in fam.get("figures") or []:
                sha = figure_sha(fig)
                if not sha or sha not in by_sha:
                    continue
                src = by_sha[sha]
                ann = src.get("annotations")
                if not ann:
                    continue
                fig["annotations"] = ann
                fig["annotation_coverage_status"] = (
                    src.get("annotation_coverage_status") or "verified"
                )
                matched += 1
    return matched


def norm_figure_key(s: str) -> str:
    return re.sub(r"\s+", "", s or "").upper().replace("FIG.", "").replace("FIG", "")


def load_preclean_captions() -> dict[str, dict[str, str]]:
    if not PRECLEAN_REWRITE.is_file():
        return {}
    data = json.loads(PRECLEAN_REWRITE.read_text(encoding="utf-8"))
    out: dict[str, dict[str, str]] = {}
    for patch in data.get("patches") or []:
        pub = patch.get("publication_id")
        caps = patch.get("figure_captions")
        if pub and caps:
            out[pub] = {norm_figure_key(k): v for k, v in caps.items()}
    return out


def clean_english_caption_tail(caption: str) -> str:
    text = (caption or "").strip()
    for sep in ("：", ":"):
        if sep in text:
            tail = text.split(sep, 1)[1].strip()
            if re.match(r"(FIG\.?|Fig\.?|图|図)", tail, re.I):
                text = tail
                break
    text = re.sub(
        r"^(?:US|WO|CN|JP|KR|TW)[A-Z0-9]+\s*(?:当前授权原始附图[,，]?\s*)?",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"PDF第\d+页[^：:]*[：:]?\s*", "", text)
    text = re.sub(r"（附图Sheet[^）]+）\s*", "", text)
    text = re.sub(r"\(附图Sheet[^)]+\)\s*", "", text)
    return text.strip()


def fig_label_to_zh_prefix(figure_number: str) -> str:
    fn = (figure_number or "").strip()
    if not fn:
        return "附图"
    if re.search(r"[\u4e00-\u9fff]", fn) or fn.startswith("図"):
        return fn.split("·")[0].split("—")[0].split("-")[0].strip()
    m = re.match(r"^Figs?\.?\s*([\dA-Za-z][\dA-Za-z.\-/–—]*)", fn, re.I)
    if m:
        return "图" + m.group(1).replace(" ", "")
    m2 = re.match(r"^图\s*([\dA-Za-z][\dA-Za-z.\-/–—]*)", fn)
    if m2:
        return "图" + m2.group(1)
    return "图 " + fn


def caption_needs_translation(cap: str) -> bool:
    if not cap:
        return True
    if re.search(r"[\u4e00-\u9fff]", cap):
        return False
    return bool(re.search(r"[A-Za-z]{4,}", cap))


def translate_batch(texts: list[str]) -> list[str]:
    from deep_translator import GoogleTranslator

    translator = GoogleTranslator(source="en", target="zh-CN")
    out: list[str] = []
    for t in texts:
        try:
            out.append(translator.translate(t[:4500]))
        except Exception:
            out.append(t)
        time.sleep(0.05)
    return out


def build_display_caption(
    fig: dict,
    pub: str,
    caption_by_sha: dict[str, str],
    preclean_caps: dict[str, dict[str, str]],
    translate_cache: dict[str, str],
) -> str | None:
    sha = figure_sha(fig)
    if sha and sha in caption_by_sha:
        return caption_by_sha[sha]
    fn = fig.get("figure_number") or ""
    pc = (preclean_caps.get(pub) or {}).get(norm_figure_key(fn))
    if pc:
        return pc
    raw = (fig.get("caption") or "").strip()
    if not raw:
        return None
    if re.search(r"[\u4e00-\u9fff]", raw) and "FIG." not in raw.upper()[:8]:
        return raw
    cleaned = clean_english_caption_tail(raw)
    prefix = fig_label_to_zh_prefix(fn)
    body = cleaned
    m = re.match(
        r"^Figs?\.?\s*[\dA-Za-z][\dA-Za-z.\-/–—]*\s*[—\-–:：]\s*(.+)$",
        cleaned,
        re.I,
    )
    if m:
        body = m.group(1).strip()
    if caption_needs_translation(body):
        if body not in translate_cache:
            translate_cache[body] = translate_batch([body])[0]
        body = translate_cache[body]
    if "·" in prefix and re.search(r"[\u4e00-\u9fff]", prefix):
        return prefix if "·" in body else f"{prefix} · {body}"
    return f"{prefix} — {body}" if body else prefix


def fetch_og_html(url: str) -> str | None:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (epi-preclean-monitor reader-layout)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError):
        return None


def parse_og_inventors(html: str) -> str | None:
    m = re.search(
        r'<tr align="center">\s*<td colspan="3" class="table_data"><b>\s*([^<]+?)\s*</b></td>\s*</tr>\s*'
        r'<tr align="center">\s*<td colspan="3" class="table_data"><b>Assigned to',
        html,
        re.S | re.I,
    )
    if not m:
        return None
    line = re.sub(r"\s+", " ", m.group(1)).strip()
    if not line or line.startswith("US "):
        return None
    return line


def og_sections_for_week(week: int) -> list[str]:
    if week in OG_SECTION_BY_WEEK:
        return [OG_SECTION_BY_WEEK[week]] + [
            s for s in OG_SECTION_FALLBACKS if s != OG_SECTION_BY_WEEK[week]
        ]
    return list(OG_SECTION_FALLBACKS)


def inventors_from_us_grant(pub: str, event_date: str) -> str | None:
    m = re.match(r"US(\d+)(B2)$", pub)
    if not m or not event_date:
        return None
    num = m.group(1)
    try:
        dt = datetime.strptime(event_date[:10], "%Y-%m-%d")
    except ValueError:
        return None
    ymd = dt.strftime("%Y%m%d")
    week = dt.isocalendar().week
    candidates: list[tuple[int, str]] = []
    for w in (week, week - 1, week + 1):
        if w < 1 or w > 53:
            continue
        sections = og_sections_for_week(w)
        candidates.append((w, sections[0]))
        for section in sections[1:3]:
            candidates.append((w, section))
    seen: set[tuple[int, str]] = set()
    for w, section in candidates:
        key = (w, section)
        if key in seen:
            continue
        seen.add(key)
        url = (
            f"https://patentsgazette.uspto.gov/week{w}/OG/html/"
            f"{section}/US{num}-{ymd}.html"
        )
        html = fetch_og_html(url)
        if not html or num not in html:
            continue
        inv = parse_og_inventors(html)
        if inv:
            return inv
        time.sleep(0.08)
    return None


def collect_og_urls_from_repo() -> dict[str, set[str]]:
    urls: dict[str, set[str]] = {}
    og_re = re.compile(
        r"https://patentsgazette\.uspto\.gov/week\d+/OG/html/[^\"\s]+US\d+-\d{8}\.html"
    )

    def add(pub: str, url: str) -> None:
        urls.setdefault(pub, set()).add(url)

    text = REPORT.read_text(encoding="utf-8")
    for u in og_re.findall(text):
        m = re.search(r"/(US\d+)-(\d{8})\.html", u)
        if m:
            add(m.group(1) + "B2", u)

    for path in ROOT.joinpath("docs").rglob("*"):
        if path.suffix not in (".json", ".md"):
            continue
        try:
            blob = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for u in og_re.findall(blob):
            m = re.search(r"/(US\d+)-(\d{8})\.html", u)
            if m:
                add(m.group(1) + "B2", u)
    return urls


def simplify_inventors(raw: str) -> str:
    parts = re.split(r"\s*;\s*and\s*|\s*;\s*", raw)
    names: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        name = part.split(",")[0].strip()
        if name and name not in names:
            names.append(name)
    return "；".join(names)


def apply_inventors(report: dict, og_urls: dict[str, set[str]]) -> tuple[int, int]:
    filled = 0
    attempted = 0
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id") or ""
            if fam.get("inventors"):
                filled += 1
                continue
            attempted += 1
            inv: str | None = None
            for url in sorted(og_urls.get(pub, [])):
                html = fetch_og_html(url)
                if html:
                    inv = parse_og_inventors(html)
                    if inv:
                        break
            if not inv and pub.startswith("US") and pub.endswith("B2"):
                inv = inventors_from_us_grant(pub, fam.get("event_date") or "")
            if inv:
                fam["inventors"] = simplify_inventors(inv)
                filled += 1
            time.sleep(0.05)
    return filled, attempted


def audit_annotations(report: dict) -> dict:
    total = verified = 0
    residual: list[dict] = []
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            for fig in fam.get("figures") or []:
                total += 1
                if annotations_verified(fig):
                    verified += 1
                else:
                    residual.append(
                        {
                            "publication_id": pub,
                            "figure_number": fig.get("figure_number"),
                            "asset_sha256": (figure_sha(fig) or "")[:12],
                        }
                    )
    return {
        "figures_total": total,
        "figures_verified": verified,
        "figures_residual_empty": len(residual),
        "residual": residual,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-inventor-fetch",
        action="store_true",
        help="Do not network-fetch inventors (OG); keep existing inventors fields only.",
    )
    parser.add_argument(
        "--skip-caption-translate",
        action="store_true",
        help="Skip machine translation for English-only captions.",
    )
    args = parser.parse_args()

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    by_sha, caption_by_sha = load_dot_by_sha()
    ann_matched = merge_dot_annotations(report, by_sha)

    preclean_caps = load_preclean_captions()
    translate_cache: dict[str, str] = {}
    cap_updated = 0
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id") or ""
            for fig in fam.get("figures") or []:
                if args.skip_caption_translate and not (
                    figure_sha(fig) in caption_by_sha
                    or (preclean_caps.get(pub) or {}).get(
                        norm_figure_key(fig.get("figure_number") or "")
                    )
                ):
                    continue
                dc = build_display_caption(
                    fig, pub, caption_by_sha, preclean_caps, translate_cache
                )
                if dc and fig.get("display_caption") != dc:
                    fig["display_caption"] = dc
                    cap_updated += 1

    inv_filled = sum(
        1
        for m in report.get("months") or []
        for f in m.get("families") or []
        if f.get("inventors")
    )
    if not args.skip_inventor_fetch:
        og_urls = collect_og_urls_from_repo()
        inv_filled, _ = apply_inventors(report, og_urls)

    audit = audit_annotations(report)
    inv_total = sum(len(m.get("families") or []) for m in report.get("months") or [])

    report.setdefault("change_history", []).append(
        {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "by": "reader-layout-track",
            "action": "reader_layout_data",
            "detail": (
                f"dot_annotations_matched={ann_matched}; "
                f"display_captions_updated={cap_updated}; "
                f"inventors_filled={inv_filled}/{inv_total}; "
                f"figures_verified={audit['figures_verified']}/{audit['figures_total']}"
            ),
        }
    )

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    summary = {
        "dot_annotations_matched": ann_matched,
        "display_captions_updated": cap_updated,
        "inventors_filled": inv_filled,
        "inventors_total_families": inv_total,
        **audit,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
