# Sprint kickoff notes — 2026-10-20

**总经理** owns delivery by **2026-10-23 evening**. Parallel tracks — **do not pause content expansion**.

- **Track A:** Keep searching/reviewing EPI & Preclean; update JSON + Excel; evidence only from real sources.
- **Track B:** Layout/mobile vs Dot (`sslip.io:8443` benchmark); rounds in `docs/quality-runs/`.

**PR #7** (figure restore) merged as `cac3f98` on `main`. Always run restore `--check` before publish.

**Serial lock:** merge to `main` in order — data → xlsx → audit/stamp → push. Weekly `epi` / monthly `epi-2` documented in `docs/AUTOMATION.md`; do not publish an older SHA over a newer one.

Ping user only for auth blockers or final delivery.
