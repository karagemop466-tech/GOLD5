"""Derived analysis for GOLD5.

Every figure here is computed from data/*.json with an explicit formula. Nothing is
hand-typed, which is why the money pass in verify.py can import this module and treat
its outputs as traceable.
"""
from __future__ import annotations

from .base import load

TROY_OZ_G = 31.1034768


def _entries() -> dict[str, dict]:
    return {e["id"]: e for e in load("entries.json")["entries"]}


def _per_gram() -> float:
    data = load("gold-prices.json")
    ref = next(o for o in data["observations"] if o["id"] == data["reference_id"])
    return ref["usd_per_troy_oz"] / data["troy_ounce_grams"]


def melt(entry: dict) -> float | None:
    if entry.get("weight_g") is None or not entry.get("karat"):
        return None
    return entry["weight_g"] * entry["karat"] / 24 * _per_gram()


def fleur_delta() -> dict:
    """Same setting, 18K vs 14K — the cleanest read on the price of extra gold."""
    e = _entries()
    a, b = e["BE-BE1574-14KY"], e["BE-BE1574-18KY"]
    delta = b["price_usd"] - a["price_usd"]
    return {
        "low": a["price_usd"],
        "high": b["price_usd"],
        "delta": delta,
        "pct": delta / a["price_usd"] * 100,
        "low_id": a["id"],
        "high_id": b["id"],
    }


def band_rows() -> list[dict]:
    """Rows where a seller-published weight makes price-per-gram possible."""
    out = []
    for e in load("entries.json")["entries"]:
        if e.get("weight_g") is None:
            continue
        m = melt(e)
        out.append(
            {
                "id": e["id"],
                "title": e["title"],
                "seller": e["seller"],
                "karat": e["karat"],
                "weight_g": e["weight_g"],
                "fine_g": e["weight_g"] * e["karat"] / 24,
                "melt": m,
                "price": e["price_usd"],
                "ratio": e["price_usd"] / m if m else None,
                "labour": e["price_usd"] - m if m else None,
            }
        )
    return sorted(out, key=lambda r: r["ratio"] or 0)


def spreads() -> dict:
    entries = [e for e in load("entries.json")["entries"] if e.get("price_usd")]
    settings = [e["price_usd"] for e in entries if e["category"].endswith("setting") or e["category"] == "18k-gold"]
    complete = [e["price_usd"] for e in entries if e["category"] == "complete-ring"]
    bands = [e["price_usd"] for e in entries if e["category"] == "gold-band"]
    return {
        "settings": (min(settings), max(settings)) if settings else None,
        "complete": (min(complete), max(complete)) if complete else None,
        "bands": (min(bands), max(bands)) if bands else None,
    }


def all_money_tokens() -> set[str]:
    """Every dollar figure this module can cause a page to render."""
    tokens: set[str] = set()

    def add(value):
        if value is None:
            return
        tokens.add(f"${value:,.0f}")
        tokens.add(f"${value:,.2f}")

    add(fleur_delta()["delta"])
    for row in band_rows():
        add(row["melt"])
        add(row["labour"])
        add(row["price"])
        add(row["price"] / row["weight_g"])
    for key in ("settings", "complete", "bands"):
        pair = spreads()[key]
        if pair:
            add(pair[0])
            add(pair[1])
    return tokens


def checklist_coverage() -> dict:
    """Coverage per checklist metric, computed from the data so the page cannot go stale."""
    entries = load("entries.json")["entries"]
    sellers = load("sellers.json")["sellers"]
    n = len(entries)
    return {
        "karat": (sum(1 for e in entries if e.get("karat")), n),
        "solid": (sum(1 for e in entries if e["solid_gold"] == "explicit"), n),
        "hallmark": (sum(1 for e in entries if e.get("hallmark") not in (None, "", "not-stated")), n),
        "weight": (sum(1 for e in entries if e.get("weight_g") is not None), n),
        "price_vs_melt": (sum(1 for e in entries if e.get("price_usd") and e.get("weight_g")), n),
        "contact": (sum(1 for s in sellers if s["contact"]["status"] == "verified"), len(sellers)),
        "returns": (sum(1 for s in sellers if s["returns"]["status"].startswith("verified")), len(sellers)),
        "payment": (sum(1 for s in sellers if s["payment"]["status"] == "verified"), len(sellers)),
        "documentation": (sum(1 for e in entries if e.get("url") and e.get("checked_on")), n),
        "offline": (0, 0),
    }
