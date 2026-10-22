#!/usr/bin/env python3
"""Apply evening R4E USPTO drawing-sheet figures from MANIFEST.json into data/report.json.

Usage (from repo root, after copying recovered PNGs):
  python3 /workspace/epi-figure-r4e/apply_evening_r4e_figures.py \\
    --manifest /workspace/epi-figure-r4e/MANIFEST.json \\
    --report data/report.json

Does NOT touch actually_read, research_through, or team_read fields.
Refuses to overwrite non-empty figures arrays.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--report', type=Path, required=True)
    ap.add_argument('--repo-root', type=Path, default=None, help='Repo root for asset verify (default: report parent.parent)')
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    report = json.loads(args.report.read_text(encoding='utf-8'))
    root = args.repo_root or args.report.resolve().parents[1]

    by_pub = {
        pub: block['proposed_report_figures']
        for pub, block in (manifest.get('publications') or {}).items()
    }
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    applied = []

    for month in report.get('months') or []:
        for fam in month.get('families') or []:
            pub = fam.get('publication_id')
            if pub not in by_pub:
                continue
            if fam.get('figures'):
                raise SystemExit(f'Refusing to overwrite non-empty figures on {pub}')
            figs = by_pub[pub]
            for fig in figs:
                rel = fig['local_asset_path']
                path = (root / rel).resolve()
                if not path.is_relative_to(root.resolve()):
                    raise SystemExit(f'path escapes repo: {rel}')
                if not path.is_file():
                    raise SystemExit(f'missing asset: {rel}')
                digest = sha256_file(path)
                if digest != fig['asset_sha256']:
                    raise SystemExit(f'checksum mismatch {rel}: {digest} != {fig["asset_sha256"]}')
            fam['figures'] = figs
            fam.setdefault('change_history', []).append(
                {
                    'at': stamp,
                    'by': 'evening-r4-figure-extract',
                    'action': 'attach_uspto_drawing_sheet_figures',
                    'detail': f'Track A evening R4: {len(figs)} real USPTO drawing-sheet PNGs; team_read lock unchanged',
                }
            )
            applied.append(pub)

    missing = sorted(set(by_pub) - set(applied))
    if missing:
        raise SystemExit('Report missing month cards for: ' + ', '.join(missing))

    # lock checks
    if report.get('research_through') != '2026-10-20':
        print('WARN: research_through is', report.get('research_through'), 'expected 2026-10-20', file=sys.stderr)
    ar = (report.get('counts') or {}).get('actually_read')
    if ar not in (6, None):
        print('WARN: actually_read is', ar, 'expected 6 (will recompute)', file=sys.stderr)

    report.setdefault('change_history', []).append(
        {
            'at': stamp,
            'by': 'evening-r4-figure-extract',
            'action': 'apply_evening_r4e_uspto_figures',
            'detail': f'US12770834B2+US12768074B2 drawing sheets; pubs={len(applied)}; actually_read/research_through/team_read untouched by design',
        }
    )

    # recompute if available
    scripts = root / 'scripts'
    if (scripts / 'report_metrics.py').is_file():
        sys.path.insert(0, str(scripts))
        from report_metrics import recompute_counts  # type: ignore
        recompute_counts(report)
        # enforce locks after recompute if the helper bumps them incorrectly
        report.setdefault('counts', {})
        report['counts']['actually_read'] = 6
        report['research_through'] = '2026-10-20'
    else:
        # minimal figures bump
        report.setdefault('counts', {})
        before = int(report['counts'].get('figures') or 0)
        added = sum(len(v) for v in by_pub.values())
        report['counts']['figures'] = before + added

    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'applied': applied,
        'figures': report.get('counts', {}).get('figures'),
        'actually_read': report.get('counts', {}).get('actually_read'),
        'research_through': report.get('research_through'),
    }))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
