#!/usr/bin/env python3
"""Honest count helpers for data/report.json."""

from __future__ import annotations

from typing import Any


def card_events_for_month(fam: dict, month: str) -> list[dict]:
    """Events attributed to this calendar month on this card (by event_date month)."""
    pub = fam.get("publication_id")
    evs = fam.get("family_events") or []
    if not evs:
        if (fam.get("event_date") or "")[:7] == month:
            return [
                {
                    "publication_id": pub,
                    "event_date": fam.get("event_date"),
                    "event_type": fam.get("event_type"),
                }
            ]
        return []
    out = []
    for ev in evs:
        if (ev.get("event_date") or "")[:7] == month:
            out.append(ev)
    return out


def unique_publication_id_set(months: list) -> set[str]:
    """Global dedupe: every month-card publication plus all family_events rows."""
    seen: set[str] = set()
    for m in months:
        for fam in m.get("families") or []:
            pub = fam.get("publication_id")
            if pub:
                seen.add(pub)
            for ev in fam.get("family_events") or []:
                pid = ev.get("publication_id")
                if pid:
                    seen.add(pid)
    return seen


def all_publication_events(months: list) -> list[dict]:
    """Placeholder list length = unique publication id count."""
    return [{"publication_id": p} for p in sorted(unique_publication_id_set(months))]


def recompute_counts(data: dict) -> dict[str, Any]:
    months = data.get("months") or []
    month_entries = 0
    family_ids: set[str] = set()
    core_family_ids: set[str] = set()
    figures_refs = 0
    actually_read = 0

    for m in months:
        ym = m.get("month") or ""
        fams = m.get("families") or []
        month_entries += len(fams)
        ev_in_month = 0
        for fam in fams:
            fid = fam.get("family_id") or fam.get("publication_id")
            if fid:
                family_ids.add(fid)
                if fam.get("scope_status") == "core":
                    core_family_ids.add(fid)
            card_evs = card_events_for_month(fam, ym)
            ev_in_month += len(card_evs)
            if fam.get("team_independent_read"):
                actually_read += 1
            for fig in fam.get("figures") or []:
                figures_refs += 1
        m["family_count"] = len(fams)
        m["event_count"] = ev_in_month

    unique_events = all_publication_events(months)
    pub_event_count = len(unique_events)
    pending_n = len(data.get("pending_or_related") or [])

    counts = {
        "candidates_total": month_entries,
        "events_reviewed": actually_read,
        "events_core": pub_event_count,
        "families_core": len(core_family_ids),
        "related": (data.get("counts") or {}).get("related", 0),
        "pending": pending_n,
        "excluded": (data.get("counts") or {}).get("excluded", 0),
        "figures": figures_refs,
        "month_family_entries": month_entries,
        "publication_events": pub_event_count,
        "unique_families": len(family_ids),
        "actually_read": actually_read,
        "unique_publication_ids": pub_event_count,
    }
    data["counts"] = counts
    return counts
