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
TRANSLATION_CACHE_PATH = ROOT / "data/figure-caption-translation-cache.json"
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


def load_translation_cache() -> dict[str, str]:
    if not TRANSLATION_CACHE_PATH.is_file():
        return {}
    return json.loads(TRANSLATION_CACHE_PATH.read_text(encoding="utf-8"))


def save_translation_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRANSLATION_CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


_PUB_ID_TOKEN = re.compile(
    r"^(?:US|WO|CN|JP|KR|TW|DE)\d{6,}[A-Z]\d?$",
    re.I,
)


_ALLOWED_LATIN_TOKEN = re.compile(
    r"^(Si|SiGe|SiGe:B|GaN|SiC|FinFET|RPS|CVD|ALD|EPI|HF|NF3|AHF|DRAM|GAA|ICP|PM|TM|B2|A1|DEPATISnet)$",
    re.I,
)


def substantial_latin(text: str) -> bool:
    """True when caption body still reads as English (design gate)."""
    if not text:
        return False
    if re.search(r"Same-family", text, re.I):
        return True
    if re.match(r"^FIG\.?\s*\d", text.strip(), re.I):
        return True
    if re.search(
        r"\b(schematic|showing|including|according to|embodiments?|depicts?|"
        r"view of|semiconductor processing|delivery system)\b",
        text,
        re.I,
    ):
        return True
    if re.search(
        r"USPTO\s+PDF|PDF\s*Sheet\s*\d|/page\s*\d|Fig\.\s*\d+\s*priority",
        text,
        re.I,
    ):
        return True
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    words = re.findall(r"[A-Za-z][A-Za-z0-9:+-]{1,}", text)
    long_english = [
        w
        for w in words
        if len(w) >= 5
        and not _ALLOWED_LATIN_TOKEN.match(w)
        and not _PUB_ID_TOKEN.match(w)
    ]
    if not long_english:
        return False
    if cjk >= 8 and len(long_english) <= 1 and len(long_english[0]) < 8:
        return False
    if cjk >= 12:
        bad_long = [
            w
            for w in long_english
            if w.upper() not in ("PDF", "SHEET", "USPTO", "FIG")
        ]
        if not bad_long:
            return False
        if cjk >= 18 and len(bad_long) <= 2 and max(len(w) for w in bad_long) < 10:
            return False
    return True


def caption_needs_translation(cap: str) -> bool:
    if not cap:
        return True
    prefix, body = split_caption_prefix_body(cap)
    target = body if body else cap
    if re.search(r"[\u4e00-\u9fff]", target) and not substantial_latin(target):
        return False
    return substantial_latin(target)


def split_caption_prefix_body(caption: str) -> tuple[str, str]:
    text = (caption or "").strip()
    for sep in (" — ", " – ", " - ", "·", "：", ":"):
        if sep in text:
            left, right = text.split(sep, 1)
            if re.match(r"^(图|図|FIG\.?|Fig\.?)", left.strip(), re.I) or re.search(
                r"[\u4e00-\u9fff]", left
            ):
                return left.strip(), right.strip()
    return "", text


def translation_acceptable(src: str, dst: str) -> bool:
    if not dst or dst.strip() == src.strip():
        return False
    if substantial_latin(dst) and len(re.findall(r"[\u4e00-\u9fff]", dst)) < 4:
        return False
    return True


def translate_english(text: str, cache: dict[str, str]) -> str:
    src = (text or "").strip()
    if not src or not substantial_latin(src):
        return src
    cjk = len(re.findall(r"[\u4e00-\u9fff]", src))
    if cjk >= 12 and not re.search(
        r"\b(schematic|showing|including|Same-family|depicts?|embodiments?)\b",
        src,
        re.I,
    ):
        return src
    if src in cache and translation_acceptable(src, cache[src]):
        return cache[src]
    from deep_translator import GoogleTranslator, MyMemoryTranslator

    clipped = src[:4500]
    dst: str | None = None
    for attempt in range(3):
        try:
            dst = MyMemoryTranslator(source="en-GB", target="zh-CN").translate(clipped)
            if translation_acceptable(clipped, dst or ""):
                break
        except Exception:
            dst = None
        time.sleep(1.0 + attempt * 2)
    if not translation_acceptable(clipped, dst or ""):
        for attempt in range(2):
            try:
                time.sleep(2.0 + attempt * 3)
                dst = GoogleTranslator(source="en", target="zh-CN").translate(clipped)
                if translation_acceptable(clipped, dst or ""):
                    break
            except Exception:
                dst = None
    if not translation_acceptable(clipped, dst or ""):
        dst = src
    cache[src] = dst
    time.sleep(0.35)
    return dst


def strip_reader_process_junk(caption: str) -> str:
    text = (caption or "").strip()
    text = re.sub(
        r"\s*[（(]\s*USPTO\s+PDF[^）)]*[）)]\s*",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"\s*;\s*Fig\.\s*\d+\s*priority[^;）)]*", "", text, flags=re.I)
    text = re.sub(
        r"[；;]\s*USPTO[^。；;]*PDF[^。；;]*[。.]?\s*",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"[；;]\s*USPTO[^。；;]*[。.]?\s*",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text


def strip_provenance_metadata(caption: str) -> str:
    text = (caption or "").strip()
    if "来源：" in text:
        text = text.split("来源：", 1)[0].strip().rstrip("。.")
    if "来源:" in text:
        text = text.split("来源:", 1)[0].strip().rstrip("。.")
    for marker in ("该图来自不同的同族文献", "本图来自不同文献", "不据此替代本条"):
        if marker in text:
            text = text.split(marker, 1)[0].strip().rstrip("。；;，,")
    return text.strip()


def dedupe_figure_prefix(caption: str) -> str:
    text = (caption or "").strip()
    m = re.match(
        r"^(图[\dA-Za-z][\dA-Za-z./、，\-\(\)（）]*)\s*[—\-–·]\s*"
        r"(图[\dA-Za-z][\dA-Za-z./、，\-\(\)（）]*)\s*[—\-–·]\s*(.+)$",
        text,
    )
    if m and re.sub(r"\s", "", m.group(1)) == re.sub(r"\s", "", m.group(2)):
        return f"{m.group(1)} — {m.group(3).strip()}"
    return text


def collapse_duplicate_caption_segments(caption: str) -> str:
    parts = [p.strip() for p in re.split(r"\s*·\s*", (caption or "").strip()) if p.strip()]
    if len(parts) <= 1:
        return (caption or "").strip()
    seen: list[str] = []
    for part in parts:
        if part not in seen:
            seen.append(part)
    return " · ".join(seen)


def extract_chinese_reader_core(caption: str, figure_number: str) -> str | None:
    """Turn US/WO-style Chinese metadata captions into 图N — body."""
    raw = (caption or "").strip()
    if not raw or not re.search(r"[\u4e00-\u9fff]", raw):
        return None
    head, tail = split_caption_prefix_body(raw)
    if (
        head
        and tail
        and re.match(r"^图", head)
        and not substantial_latin(tail)
    ):
        return dedupe_figure_prefix(raw)
    text = clean_english_caption_tail(raw)
    text = re.sub(r"^Figs?\.?\s*[\dA-Za-z./–—]+[,，]\s*", "", text, flags=re.I)
    m_pub_fig = re.match(
        r"^(?:US|WO|CN|JP|KR|TW)[A-Z0-9]+\s*原始公开图\s*([\d/]+)\s*[；;](.+)$",
        text,
        re.I,
    )
    if m_pub_fig:
        tail = m_pub_fig.group(2).strip()
        prefix = fig_label_to_zh_prefix(figure_number)
        return f"{prefix} — {tail}"
    if "；" in text:
        for part in reversed([p.strip() for p in text.split("；")]):
            if len(re.findall(r"[\u4e00-\u9fff]", part)) >= 6 and not substantial_latin(
                part
            ):
                prefix = fig_label_to_zh_prefix(figure_number)
                sep = " · " if "·" in raw else " — "
                core = strip_provenance_metadata(strip_reader_process_junk(part))
                return f"{prefix}{sep}{core}".strip()
    core = ""
    for sep in ("：", ":"):
        if sep in text:
            core = text.rsplit(sep, 1)[-1].strip()
            break
    if not core and re.search(r"[\u4e00-\u9fff]", text):
        core = text
    if not core or len(re.findall(r"[\u4e00-\u9fff]", core)) < 4:
        return None
    if substantial_latin(core) and len(re.findall(r"[\u4e00-\u9fff]", core)) < 8:
        return None
    core = strip_provenance_metadata(core)
    core = strip_reader_process_junk(core)
    prefix = fig_label_to_zh_prefix(figure_number)
    sep = " · " if "·" in raw else " — "
    return f"{prefix}{sep}{core}".strip()


def normalize_reader_display_caption(
    caption: str | None,
    figure_number: str,
    translate_cache: dict[str, str],
    *,
    do_translate: bool = True,
) -> str | None:
    if not caption:
        return None
    text = (caption or "").strip()
    _, body_probe = split_caption_prefix_body(text)
    if substantial_latin(body_probe or text):
        core = extract_chinese_reader_core(text, figure_number)
        if core:
            text = core
    text = polish_reader_caption(text, figure_number)
    if do_translate:
        text = finalize_chinese_caption(text, translate_cache)
    return strip_provenance_metadata(text).strip() or None


def compress_family_substitute_caption(caption: str, figure_number: str) -> str:
    text = (caption or "").strip()
    if "同族替代图" not in text and "原始专利" not in text:
        return text
    m = re.search(r"PDF第\s*\d+\s*页[。.]\s*([^；。]+)", text)
    if not m:
        m = re.search(r"原始专利[^，。]+[，,]\s*([^；。]+)", text)
    if not m:
        return text
    core = re.sub(r"\s+", "", m.group(1).strip())
    core = core.replace("FinFET", "鳍式场效应晶体管")
    prefix = fig_label_to_zh_prefix(figure_number)
    return f"{prefix} — {core}"


def polish_reader_caption(caption: str, figure_number: str) -> str:
    text = strip_reader_process_junk(caption)
    text = compress_family_substitute_caption(text, figure_number)
    text = re.sub(r"\bFigs?\.\s*", "图", text, flags=re.I)
    text = collapse_duplicate_caption_segments(text)
    text = dedupe_figure_prefix(text)
    return text.strip()


def finalize_chinese_caption(caption: str, cache: dict[str, str]) -> str:
    text = (caption or "").strip()
    if not text:
        return text
    if not caption_needs_translation(text):
        return text
    prefix, body = split_caption_prefix_body(text)
    chunk = body if body else text
    zh = translate_english(chunk, cache)
    if prefix:
        sep = " — " if "—" in text or "–" in text else " · "
        return f"{prefix}{sep}{zh}"
    return zh


def build_display_caption(
    fig: dict,
    pub: str,
    caption_by_sha: dict[str, str],
    preclean_caps: dict[str, dict[str, str]],
    translate_cache: dict[str, str],
    *,
    do_translate: bool = True,
) -> str | None:
    sha = figure_sha(fig)
    fn = fig.get("figure_number") or ""
    if sha and sha in caption_by_sha:
        cap = polish_reader_caption(caption_by_sha[sha], fn)
        if do_translate:
            cap = finalize_chinese_caption(cap, translate_cache)
        return strip_provenance_metadata(cap)
    pc = (preclean_caps.get(pub) or {}).get(norm_figure_key(fn))
    if pc:
        return normalize_reader_display_caption(
            pc, fn, translate_cache, do_translate=do_translate
        )
    raw = (fig.get("caption") or "").strip()
    if not raw:
        return None
    zh_core = extract_chinese_reader_core(raw, fn)
    if zh_core:
        if do_translate:
            return finalize_chinese_caption(zh_core, translate_cache)
        return zh_core
    if re.search(r"[\u4e00-\u9fff]", raw) and not substantial_latin(raw):
        polished = strip_provenance_metadata(strip_reader_process_junk(raw))
        if do_translate:
            return finalize_chinese_caption(polished, translate_cache)
        return polished
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
    if do_translate and caption_needs_translation(body):
        body = translate_english(body, translate_cache)
    assembled = f"{prefix} — {body}" if body and prefix else (body or prefix)
    if "·" in prefix and re.search(r"[\u4e00-\u9fff]", prefix):
        assembled = prefix if "·" in body else f"{prefix} · {body}"
    if do_translate:
        return finalize_chinese_caption(assembled, translate_cache)
    return assembled


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


def audit_caption_zh(report: dict) -> dict:
    english_leaning: list[dict] = []
    total = 0
    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id")
            for fig in fam.get("figures") or []:
                total += 1
                cap = (fig.get("display_caption") or "").strip()
                _, body = split_caption_prefix_body(cap)
                probe = body or cap
                if substantial_latin(probe):
                    english_leaning.append(
                        {
                            "publication_id": pub,
                            "figure_number": fig.get("figure_number"),
                        }
                    )
    return {
        "figures_total": total,
        "english_leaning_count": len(english_leaning),
        "english_leaning": english_leaning,
    }


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
    translate_cache = load_translation_cache()
    cap_updated = 0
    pending_bodies: set[str] = set()
    figure_rows: list[tuple[dict, str, dict]] = []

    for month in report.get("months") or []:
        for fam in month.get("families") or []:
            pub = fam.get("publication_id") or ""
            for fig in fam.get("figures") or []:
                figure_rows.append((fig, pub, fam))

    if not args.skip_caption_translate:
        for fig, pub, _fam in figure_rows:
            dc = build_display_caption(
                fig,
                pub,
                caption_by_sha,
                preclean_caps,
                translate_cache,
                do_translate=False,
            )
            if not dc:
                continue
            _, body = split_caption_prefix_body(dc)
            if caption_needs_translation(body or dc):
                pending_bodies.add((body or dc).strip())
        for body in sorted(pending_bodies, key=len):
            if not caption_needs_translation(body):
                continue
            if body not in translate_cache or not translation_acceptable(
                body, translate_cache.get(body, "")
            ):
                translate_english(body, translate_cache)
        save_translation_cache(translate_cache)

        for fig, pub, _fam in figure_rows:
            dc = build_display_caption(
                fig, pub, caption_by_sha, preclean_caps, translate_cache
            )
            if dc:
                dc = normalize_reader_display_caption(
                    dc,
                    fig.get("figure_number") or "",
                    translate_cache,
                    do_translate=not args.skip_caption_translate,
                )
            if dc and fig.get("display_caption") != dc:
                fig["display_caption"] = dc
                cap_updated += 1
        save_translation_cache(translate_cache)

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
    cap_audit = audit_caption_zh(report)
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
                f"figures_verified={audit['figures_verified']}/{audit['figures_total']}; "
                f"caption_english_leaning={cap_audit['english_leaning_count']}"
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
        **cap_audit,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
