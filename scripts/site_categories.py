#!/usr/bin/env python3
"""Category rules shared by the site builder and the verification harness.

A category is a *grouping label only*. It is derived from
  - the seller's own product name (the words "solitaire", "halo", "pave"), or
  - a value the seller states (karat, and whether the price is for the setting
    only or a complete ring), or
  - the row's declared category ("band", "case-study").
It never asserts purity, quality, weight or a price.
"""

STYLE_LABEL = {
    "solitaires": "Solitaires",
    "halo-pave": "Halo & pavé",
    "bands": "Gold bands",
    "case-study": "Case study (sold)",
    "other": "Other styles",
}


def style_of(e):
    n = (e.get("name") or "").lower()
    if e.get("category") == "band":
        return "bands"
    if e.get("category") == "case-study":
        return "case-study"
    if "halo" in n or "pavé" in n or "pave" in n:
        return "halo-pave"
    if "solitaire" in n:
        return "solitaires"
    return "other"


CATEGORY_DEFS = [
    dict(key="solitaires", title="Solitaire engagement rings",
         blurb="Rings the seller names a solitaire: one centre setting, no halo. Setting prices exclude the centre stone; check the basis column before comparing."),
    dict(key="halo-pave", title="Halo & pavé engagement rings",
         blurb="Rings the seller names a halo or a pavé design. The diamonds in the band or halo are part of the price; the centre stone usually is not."),
    dict(key="18k", title="18K gold rings",
         blurb="Only rows where the seller states 18K. 18K is 75% fine gold, versus 58.33% for 14K — which is why an 18K ring of the same design weighs more and costs more."),
    dict(key="complete-rings", title="Complete rings (stone included)",
         blurb="Rows whose price includes the centre stone. These are the only rows where price ÷ metal value is a like-for-like number."),
    dict(key="settings-only", title="Settings only (centre stone extra)",
         blurb="Rows whose price buys the setting alone. The centre diamond is extra, so the price must never be compared directly with a complete ring."),
    dict(key="bands", title="Gold bands",
         blurb="Plain or domed bands included as reference points for gold weight and price per gram."),
    dict(key="case-study", title="Case study: a sold ring priced below its metal",
         blurb="One sold listing kept only because it shows the fraud pattern this project screens for: a complete ring asking less than the gold it contains."),
]

PREDICATES = {
    "solitaires": lambda e: style_of(e) == "solitaires",
    "halo-pave": lambda e: style_of(e) == "halo-pave",
    "18k": lambda e: e.get("karat") == 18,
    "complete-rings": lambda e: e.get("priceBasis") == "complete",
    "settings-only": lambda e: e.get("priceBasis") == "setting",
    "bands": lambda e: e.get("category") == "band",
    "case-study": lambda e: e.get("category") == "case-study",
}


def categories():
    return [dict(c, pred=PREDICATES[c["key"]]) for c in CATEGORY_DEFS]


def category_members(cat, entries):
    return [e for e in entries if cat["pred"](e)]


def median(vals):
    vals = sorted(vals)
    n = len(vals)
    if n == 0:
        return None
    m = n // 2
    return vals[m] if n % 2 else (vals[m - 1] + vals[m]) / 2
