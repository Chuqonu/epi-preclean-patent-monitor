#!/usr/bin/env python3
"""HEAD/GET figure assets on live GitHub Pages from published report.json."""
import json
import sys
import urllib.error
import urllib.request

BASE = "https://chuqonu.github.io/epi-preclean-patent-monitor/"
REPORT = BASE + "data/report.json"


def fetch(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "epi-verify/1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        req = urllib.request.Request(url, headers={"User-Agent": "epi-verify/1"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status


def main():
    with urllib.request.urlopen(REPORT, timeout=60) as r:
        data = json.load(r)
    paths = []
    rot90 = []
    for m in data.get("months", []):
        for fam in m.get("families", []):
            for fig in fam.get("figures") or []:
                p = fig.get("local_asset_path")
                if p:
                    paths.append(p)
                if fig.get("display_rotation") == 90:
                    rot90.append(p)
    ok = fail = 0
    failed = []
    for p in paths:
        url = BASE + p.lstrip("/")
        code = fetch(url)
        if code == 200:
            ok += 1
        else:
            fail += 1
            failed.append((p, code))
    out = {
        "report_url": REPORT,
        "figure_refs": len(paths),
        "ok": ok,
        "fail": fail,
        "display_rotation_90_count": len(rot90),
        "figures_available_count": (data.get("counts") or {}).get("figures_available"),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if failed:
        print("failures:", json.dumps(failed[:20], ensure_ascii=False))
    return 0 if fail == 0 and len(paths) == 130 else 1


if __name__ == "__main__":
    sys.exit(main())
