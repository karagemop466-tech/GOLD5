"""Shared helpers for GOLD5. Pure standard library.

NO-HALLUCINATION RULE: this module never supplies prices, weights or karats.
It only (a) loads the verified data files and (b) does arithmetic on them.
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
EVID = os.path.join(DATA, "evidence")
DOCS = os.path.join(ROOT, "docs")

def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)

def evidence(name):
    with open(os.path.join(EVID, name + ".txt"), encoding="utf-8") as f:
        return f.read()

def evidence_meta(name):
    txt = evidence(name)
    src = re.search(r"^SOURCE: (\S+)", txt, re.M)
    cap = re.search(r"^CAPTURED: (\d{4}-\d{2}-\d{2})", txt, re.M)
    return (src.group(1) if src else None, cap.group(1) if cap else None)

def per_gram(usd_per_oz, grams_per_oz):
    return usd_per_oz / grams_per_oz

def fineness(karat):
    """k/24 (US karat definition). CALCULATED, not source data."""
    return karat / 24.0

def gold_value(weight_g, karat, usd_per_oz, grams_per_oz):
    """Melt value of the gold in a piece = weight x spot/gram x karat/24."""
    if weight_g is None or karat is None:
        return None
    return weight_g * per_gram(usd_per_oz, grams_per_oz) * fineness(karat)

def money(x):
    return "${:,.2f}".format(x)

AMOUNT_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")
def amounts(text):
    """All $ amounts in text, normalised to 2-dp strings without commas."""
    out = set()
    for m in AMOUNT_RE.findall(text):
        v = float(m.replace("$", "").replace(",", "").strip())
        out.add("{:.2f}".format(v))
    return out
