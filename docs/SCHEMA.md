# Data schema — EPI / Preclean Patent Monitoring Report

Aligned with Codex handoff **2026-10-20.4.2-r2** (see `HANDOFF-2026-10-20-v4.2-r2.md`).

Canonical file: `data/report.json`.  
HTML (`index.html`) and Excel (`ledger/patents.xlsx`) are both derived from it.

**Honest counts:** candidate ≠ event ≠ family ≠ actually read.  
Empty `families: []` means content pending, **not** proven zero hits.  
**2025-09 is paused** — do not search, review, or publish that month.

---

## Top-level object

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title` | string | yes | Report title |
| `browser_title` | string | yes | Document / tab title |
| `period` | string | yes | Human range, e.g. `2025/10 至 2026/10` |
| `period_start` | string | yes | `YYYY-MM` |
| `period_end` | string | yes | `YYYY-MM` |
| `prepared_date` | string \| null | yes | Edition date `YYYY-MM-DD`; null in scaffold |
| `research_through` | string \| null | yes | Inclusive cutoff for incomplete current month; **null until set** |
| `scope` | string | yes | In-scope technology |
| `excluded_scope` | string | yes | Exclusions + non-exclusion caveats |
| `count_basis` | string | yes | How months / families / events are attributed |
| `coverage_note` | string | yes | Coverage / gap disclaimer |
| `status_note` | string | yes | Edition status |
| `notes` | string[] | no | Ops notes (include 2025-09 paused) |
| `method_trace` | string \| null | no | e.g. `2026-10-20.4.2-r2` |
| `counts` | Counts | yes | Honest metric bag (see below) |
| `search_coverage` | SearchCoverageRow[] | no | Per jurisdiction / branch execution log |
| `pending_or_related` | EventRecord[] | no | Related / pending / excluded-metadata rows not on main month cards |
| `change_history` | ChangeRow[] | no | Edition-level change log |
| `months` | Month[] | yes | **Newest month first** |

### Counts

| Field | Meaning |
|-------|---------|
| `candidates_total` | Search hits / leads (not yet dispositioned) |
| `events_reviewed` | Events actually read / reviewed |
| `events_core` | Core in-scope publication/grant events |
| `families_core` | Core families (deduped by `family_id`) |
| `related` | Related (not core) |
| `pending` | Pending review |
| `excluded` | Explicitly excluded (with reason) |
| `figures` | Real patent figures stored / linked |
| `month_family_entries` | Sum of month card rows (may repeat families across months) |
| `publication_events` | Pub/grant events attributed into months |
| `unique_families` | Cross-month deduped `family_id` count |
| `actually_read` | This team's independent full-text reads (≠ reference import) |

Do **not** use visible card count as family count.

---

## Month

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `month` | string | yes | `YYYY-MM` |
| `status` | string | yes | Screening / incomplete / placeholder |
| `through_date` | string \| null | yes | Last covered day when month incomplete |
| `families` | EventRecord[] | yes | Month cards; may be `[]` |
| `family_count` | number | yes | `len(families)` |
| `event_count` | number | yes | Pub/grant events for this month |

Ordering inside a month: newest `event_date` first; same day → stable `publication_id` sort.

---

## EventRecord (month card / ledger row)

Primary handoff field names. UI may display aliases listed in *Display aliases*.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `publication_id` | string | yes | **Includes kind code**, e.g. `US20250324699A1`, `CN114xxxA` |
| `jurisdiction` | string | yes | `US` / `CN` / `JP` / `KR` / `TW` / `WO` / `EP` / … |
| `event_type` | string | yes | `publication` \| `grant` (WO pub ≠ grant) |
| `event_date` | string | yes | `YYYY-MM-DD` — drives month bucket |
| `application_id` | string \| null | no | |
| `priority_date` | string \| null | no | |
| `family_id` | string \| null | yes | Family key for dedupe |
| `family_id_source` | string \| null | no | e.g. `docdb`, `manual` |
| `title_original` | string \| null | no | |
| `title_zh` | string | yes | Chinese / preferred display title |
| `applicant_original` | string \| null | no | |
| `applicant_normalized` | string | yes | Display / group name |
| `scope_status` | string | yes | `core` \| `related` \| `pending` \| `excluded` \| `metadata_only` |
| `technology_tags` | string[] | no | e.g. `epi`, `preclean`, `chamber_clean` |
| `short_preview` | string | yes | TOC 1–2 line preview |
| `technical_summary` | string | yes | Chinese technical summary |
| `claims_or_embodiment_basis` | string | yes | Key claims / embodiment basis |
| `scope_reason` | string | yes | Why this `scope_status` |
| `source_urls` | string[] | yes | Official / reliable mirrors |
| `source_retrieved_at` | string \| null | no | ISO timestamp |
| `source_sha256` | string \| null | no | Of retrieved primary PDF/HTML if stored |
| `actual_read_spans` | string[] | no | What was actually read (claims, ¶ range, …) |
| `reviewer` | string \| null | no | |
| `reviewed_at` | string \| null | no | |
| `family_completion_status` | string | yes | `open` \| `closed` \| `pending` — closed only after full own publications / DOCDB family table checked for in-window events |
| `figures` | Figure[] | no | Real patent figures only |
| `change_history` | ChangeRow[] | no | Per-record changes |
| `family_events` | FamilyEvent[] | no | Same-family pub/grant events for the card table |
| `id` | string | yes | Stable DOM id: `{YYYY-MM}-{publication_id}` |
| `month` | string | yes | Must match parent month |
| `import_tag` | string \| null | no | e.g. `imported baseline` for transplanted rows |
| `discovery_source` | string \| null | no | e.g. `reference_report` — never claim imported rows as independent discovery |

Unverifiable fields stay `null` or status `pending` — never invent.

### FamilyEvent (sub-row)

| Field | Type | Required |
|-------|------|----------|
| `publication_id` | string | yes |
| `event_date` | string | yes |
| `event_type` | string | yes |
| `source_url` | string \| null | no |
| `application_id` | string \| null | no |

### Figure

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `source_publication_id` | string | yes | Pub id of the figure’s document |
| `figure_number` | string | yes | e.g. `Fig. 1` |
| `source_url` | string | yes | Upstream patent URL |
| `local_asset_path` | string \| null | preferred | Relative path under `assets/figures/` |
| `width` | number | yes | Intrinsic px (layout reservation) |
| `height` | number | yes | Intrinsic px |
| `caption` | string | yes | Must cite publication id + figure number |

**Never generate substitute figures.** Missing art → omit and note the gap. Prefer files over base64.

### ChangeRow

| Field | Type | Required |
|-------|------|----------|
| `at` | string | yes | ISO date/time |
| `by` | string \| null | no |
| `action` | string | yes |
| `detail` | string | no |

### SearchCoverageRow

| Field | Type | Required |
|-------|------|----------|
| `jurisdiction` | string | yes |
| `branch` | string | yes | process / equipment / integration / applicant / IPC-CPC / … |
| `window` | string | yes |
| `status` | string | yes | `done` \| `partial` \| `failed` \| `not_run` |
| `notes` | string | no | Truncation, pager limits, failures |

---

## Display aliases (UI / legacy)

Renderer accepts handoff names first; these aliases map if present:

| Handoff | Alias |
|---------|-------|
| `publication_id` | `publication_number` |
| `event_date` | `publication_date` |
| `title_zh` | `title` |
| `applicant_normalized` | `applicant` |
| `short_preview` | `brief` |
| `technical_summary` | `summary` |
| `claims_or_embodiment_basis` | `claims` |
| `scope_reason` | `relevance` |
| `family_id` | `family_key` |
| `family_events` | `events` |
| `figures[].local_asset_path` | `images[].path` |
| `figures[].figure_number` | `images[].figure_label` |
| `figures[].source_publication_id` | `images[].source_publication` |

---

## scope_status values

| Value | Use |
|-------|-----|
| `core` | Core in-scope epi / preclean / related chamber dry clean |
| `related` | Related but not core |
| `pending` | Needs review; keep reason |
| `excluded` | Out of scope with recorded reason |
| `metadata_only` | Bibliographic / search-report only |

---

## Ledger (`scripts/build_xlsx.py`)

Sheets:

1. **主表** — core (and optionally all) EventRecords flattened  
2. **同族事件** — `family_events` expansion  
3. **关联待核** — `pending_or_related` + non-core statuses  
4. **检索覆盖** — `search_coverage`  
5. **变更记录** — top-level + per-record `change_history`

Public download must not contain internal chat, credentials, or VPS endpoints.
