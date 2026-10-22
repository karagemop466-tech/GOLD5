#!/usr/bin/env python3
"""Hallucination / consistency security check for GOLD5.

Run after EVERY review pass:   python3 tools/check_hallucinations.py [--log "label"]

What it enforces (see docs/verification.html):
  C1  every ring row has an official-domain source URL matching its seller
  C2  every evidence file names its source URL + capture date
  C3  every price / karat / weight / "solid" claim appears VERBATIM in the saved evidence
  C4  blank values are flagged unverified (never filled in)
  C5  spot price + purity table agree with the saved Kitco excerpt and with k/24 arithmetic
  C6  seller contact details appear in evidence
  C7  every $ amount published in docs/*.html is traceable to evidence or to a registered calculation
  C8  internal links/anchors in docs resolve; external links are all known source URLs
  C9  sanity: below-melt prices, implausible weights, duplicate URLs, suspicious duplicate specs
Exit code 1 if any FAIL.  WARN/INFO items are published on the Flagged for Review page.
"""
import sys, os, re, json, glob, datetime
from urllib.parse import urlparse, urldefrag
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import goldlib as G

TODAY = "2026-10-22"   # session date given by the environment; pass --today to override
STALE_DAYS = 7

def host_ok(url, domain):
    h = (urlparse(url).hostname or "").lower()
    return urlparse(url).scheme == "https" and (h == domain or h.endswith("." + domain))

class Report:
    def __init__(self): self.items = []
    def add(self, level, code, msg): self.items.append({"level": level, "check": code, "message": msg})
    def count(self, lvl): return sum(1 for i in self.items if i["level"] == lvl)

def check_data(today=TODAY):
    R = Report()
    rings, sellers = G.load("rings.json"), {s["id"]: s for s in G.load("sellers.json")}
    flags = {f["id"]: f for f in G.load("flags.json")}
    spot = G.load("spot.json")
    npass = 0
    def ok(): 
        nonlocal npass; npass += 1

    # ---- spot ----
    ev = G.evidence(spot["evidence"])
    src, cap = G.evidence_meta(spot["evidence"])
    if src != spot["source_url"] or not host_ok(src, "kitco.com"): R.add("FAIL", "C5", "spot source URL mismatch / not kitco.com")
    else: ok()
    if spot["usd_per_troy_oz_bid_text"] not in ev: R.add("FAIL", "C5", "spot bid not found verbatim in evidence")
    else: ok()
    if abs(float(spot["usd_per_troy_oz_bid_text"].replace(",", "")) - spot["usd_per_troy_oz_bid"]) > 1e-9:
        R.add("FAIL", "C5", "spot numeric != text")
    else: ok()
    if spot["grams_per_troy_oz_text"] not in ev: R.add("FAIL", "C5", "grams per troy oz not in evidence")
    else: ok()
    oz, gpo = spot["usd_per_troy_oz_bid"], spot["grams_per_troy_oz"]
    pg = G.per_gram(oz, gpo)
    if abs(pg - float(spot["usd_per_gram_kitco_text"])) > 0.01 or spot["usd_per_gram_kitco_text"] not in ev:
        R.add("FAIL", "C5", "per-gram spot disagrees with Kitco's own per-gram figure")
    else: ok()
    for k, txt in spot["kitco_value_by_purity_per_oz"].items():
        if txt not in ev: R.add("FAIL", "C5", f"Kitco {k} value {txt} not in evidence"); continue
        calc = oz * int(k[:-1]) / 24
        diff = abs(calc - float(txt.replace("$", "").replace(",", "")))
        if diff > 0.50: R.add("WARN", "C5", f"{k}: Kitco {txt} vs k/24 arithmetic differs by ${diff:.2f}")
        else: ok()
    if cap and (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(cap)).days > 0:
        R.add("WARN", "C5", f"spot snapshot captured {cap}; today is {today} — refresh from kitco.com")
    else: ok()

    # ---- rings ----
    seen_urls, specs = {}, {}
    for r in rings:
        rid, s = r["id"], sellers.get(r["seller_id"])
        if not s: R.add("FAIL", "C1", f"{rid}: unknown seller"); continue
        for u in filter(None, [r["url"], r.get("price_source_url")]):
            if not host_ok(u, s["domain"]): R.add("FAIL", "C1", f"{rid}: URL {u} is not on official domain {s['domain']}")
            else: ok()
        if r["url"] in seen_urls: R.add("FAIL", "C9", f"{rid}: duplicate URL with {seen_urls[r['url']]}")
        seen_urls[r["url"]] = rid
        try: ev = G.evidence(r["evidence"])
        except FileNotFoundError: R.add("FAIL", "C2", f"{rid}: evidence file missing"); continue
        esrc, ecap = G.evidence_meta(r["evidence"])
        expected = r.get("price_source_url") or r["url"]
        if esrc != expected: R.add("FAIL", "C2", f"{rid}: evidence SOURCE {esrc} != price source {expected}")
        else: ok()
        if not ecap: R.add("FAIL", "C2", f"{rid}: evidence has no CAPTURED date")
        else:
            age = (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(ecap)).days
            if age > STALE_DAYS: R.add("WARN", "C2", f"{rid}: evidence is {age} days old — re-verify")
            else: ok()
        # price
        if r["price_text"] is None:
            if r["price_usd"] is not None: R.add("FAIL", "C4", f"{rid}: price_usd set but no price_text")
            if not any(f in flags and "PRICE" in f for f in r["flags"]): R.add("FAIL", "C4", f"{rid}: blank price without a price flag")
            else: ok()
        else:
            if r["price_text"] not in ev: R.add("FAIL", "C3", f"{rid}: price {r['price_text']} NOT found verbatim in evidence (possible hallucination)")
            else: ok()
            if abs(float(r["price_text"].replace("$", "").replace(",", "")) - r["price_usd"]) > 1e-9: R.add("FAIL", "C3", f"{rid}: price numeric != text")
            else: ok()
        # karat
        if r["karat"] is None:
            if "F-KARAT-SLUG" not in r["flags"]: R.add("FAIL", "C4", f"{rid}: blank karat without flag")
            else: ok()
        else:
            if not r["karat_text"] or r["karat_text"] not in ev: R.add("FAIL", "C3", f"{rid}: karat text not found verbatim in evidence")
            elif int(re.match(r"\d+", r["karat_text"]).group()) != r["karat"]: R.add("FAIL", "C3", f"{rid}: karat number != karat text")
            else: ok()
        # weight
        if r["weight_g"] is None:
            if "F-WEIGHT" not in r["flags"] or r["weight_text"]: R.add("FAIL", "C4", f"{rid}: blank weight without F-WEIGHT flag")
            else: ok()
        else:
            if not r["weight_text"] or r["weight_text"] not in ev: R.add("FAIL", "C3", f"{rid}: weight text not found verbatim in evidence")
            elif abs(float(re.match(r"[\d.]+", r["weight_text"]).group()) - r["weight_g"]) > 1e-9: R.add("FAIL", "C3", f"{rid}: weight numeric != text")
            else: ok()
            if not (0.5 <= r["weight_g"] <= 30): R.add("WARN", "C9", f"{rid}: implausible ring weight {r['weight_g']} g")
        # solid
        if r["solid_stated"]:
            if r.get("solid_quote", "") not in ev or not r.get("solid_quote"): R.add("FAIL", "C3", f"{rid}: 'solid' claim has no verbatim quote in evidence")
            else: ok()
        elif "F-SOLID" not in r["flags"]: R.add("FAIL", "C4", f"{rid}: solid not stated and no F-SOLID flag")
        else: ok()
        # hallmark: none are stated anywhere; ensure no hallmark claim sneaks in
        if "hallmark" in json.dumps(r).lower().replace("f-hallmark", ""): R.add("FAIL", "C3", f"{rid}: hallmark mentioned in row without evidence handling")
        if "F-HALLMARK" not in r["flags"] and not re.search(r"hallmark|stamped", ev, re.I): R.add("FAIL", "C4", f"{rid}: no hallmark evidence and no flag")
        else: ok()
        for fid in r["flags"]:
            if fid not in flags: R.add("FAIL", "C4", f"{rid}: unknown flag {fid}")
        # melt sanity
        gv = G.gold_value(r["weight_g"], r["karat"], oz, gpo)
        if gv is not None and r["price_usd"] is not None:
            if r["price_usd"] < gv: R.add("WARN", "C9", f"{rid}: price {G.money(r['price_usd'])} is BELOW calculated melt value {G.money(gv)} — red flag")
            else: ok()
            specs.setdefault((r["weight_g"], r["karat"]), []).append(rid)
    for k, ids in specs.items():
        if len(ids) > 1: R.add("INFO", "C9", f"{', '.join(ids)} share identical weight/karat {k[0]} g / {k[1]}K from different listings — confirm each seller's figure independently")

    # ---- sellers ----
    for s in sellers.values():
        for c in s["contact"]:
            if c["text"] not in G.evidence(c["evidence"]): R.add("FAIL", "C6", f"{s['name']}: contact '{c['text']}' not found in evidence")
            elif not host_ok(c["source"], s["domain"]): R.add("FAIL", "C6", f"{s['name']}: contact source not on official domain")
            else: ok()
        if not host_ok(s["returns_url"], s["domain"]): R.add("FAIL", "C1", f"{s['name']}: returns URL not official")
        else: ok()
        if s["returns_verified"]:
            # every quoted exclusion keyword must be in the policy evidence
            ev = G.evidence(s["returns_evidence"])
            for w in ("30 days",):
                if w not in ev: R.add("FAIL", "C3", f"{s['name']}: '{w}' missing from policy evidence")
                else: ok()
    # flags: any $ amount in flag text must be in evidence
    all_ev = " ".join(G.evidence(os.path.basename(p)[:-4]) for p in glob.glob(os.path.join(G.EVID, "*.txt")))
    ev_amts = G.amounts(all_ev)
    for f in flags.values():
        bad = G.amounts(f["title"] + " " + f["detail"]) - ev_amts
        if bad: R.add("FAIL", "C7", f"flag {f['id']}: amounts not in evidence: {sorted(bad)}")
        else: ok()
    R.npass = npass
    return R

class _Links(HTMLParser):
    def __init__(self): super().__init__(); self.links = []; self.ids = set(); self.text = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "a" and "href" in a: self.links.append(a["href"])
        if tag in ("script", "style"): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.text.append(d)

def check_site(R, today=TODAY):
    """C7 + C8 over docs/*.html."""
    docs = G.DOCS
    pages = sorted(glob.glob(os.path.join(docs, "*.html")))
    if not pages: R.add("FAIL", "C8", "docs/ has no HTML pages — build first"); return R
    all_ev = " ".join(G.evidence(os.path.basename(p)[:-4]) for p in glob.glob(os.path.join(G.EVID, "*.txt")))
    allowed = G.amounts(all_ev)
    reg = os.path.join(G.DATA, "computed_amounts.json")
    if os.path.exists(reg): allowed |= set(json.load(open(reg)))
    known_ext = set()
    for r in G.load("rings.json"): known_ext |= {r["url"], r.get("price_source_url") or r["url"]}
    for s in G.load("sellers.json"):
        known_ext |= {s["home"], s["returns_url"]} | {c["source"] for c in s["contact"]}
    known_ext.add(G.load("spot.json")["source_url"])
    for f in G.load("flags.json"): known_ext |= set(f["links"])
    known_ext |= {"https://github.com/karagemop466-tech/GOLD5", "https://corp.kitco.com/", "https://www.kitco.com/"}
    parsed = {}
    for p in pages:
        h = _Links(); h.feed(open(p, encoding="utf-8").read()); parsed[os.path.basename(p)] = h
    bad_amt = 0
    for name, h in parsed.items():
        text = " ".join(h.text)
        miss = G.amounts(text) - allowed
        if miss: bad_amt += 1; R.add("FAIL", "C7", f"{name}: $ amounts not traceable to evidence or a registered calculation: {sorted(miss)}")
        for href in h.links:
            if href.startswith(("mailto:", "tel:", "javascript:")): continue
            if href.startswith("http"):
                base = urldefrag(href)[0]
                if not any(base == k or base.rstrip("/") == k.rstrip("/") or base.startswith("https://github.com/karagemop466-tech/GOLD5") for k in known_ext):
                    R.add("FAIL", "C8", f"{name}: external link not in verified source list: {href}")
                continue
            tgt, _, frag = href.partition("#")
            tname = tgt or name
            full = os.path.join(docs, tname)
            if not os.path.exists(full): R.add("FAIL", "C8", f"{name}: broken internal link {href}"); continue
            if frag and tname.endswith(".html") and frag not in parsed.get(tname, _Links()).ids:
                R.add("FAIL", "C8", f"{name}: broken anchor {href}")
    if not bad_amt: R.npass += len(pages)
    return R

def run(today=TODAY, with_site=True):
    R = check_data(today)
    if with_site: check_site(R, today)
    return R

if __name__ == "__main__":
    today = TODAY
    if "--today" in sys.argv: today = sys.argv[sys.argv.index("--today") + 1]
    R = run(today)
    for i in R.items: print(f"[{i['level']:4}] {i['check']}: {i['message']}")
    print(f"\nPASSED checks: {R.npass}   FAIL: {R.count('FAIL')}   WARN: {R.count('WARN')}   INFO: {R.count('INFO')}")
    rep = {"date": today, "passed": R.npass, "fail": R.count("FAIL"), "warn": R.count("WARN"), "info": R.count("INFO"), "items": R.items}
    json.dump(rep, open(os.path.join(G.DATA, "check_report.json"), "w"), indent=2)
    if "--log" in sys.argv:
        hp = os.path.join(G.DATA, "pass_history.json")
        hist = json.load(open(hp)) if os.path.exists(hp) else []
        hist.append({"date": today, "label": sys.argv[sys.argv.index("--log") + 1], "passed": R.npass, "fail": R.count("FAIL"), "warn": R.count("WARN"), "info": R.count("INFO")})
        json.dump(hist, open(hp, "w"), indent=2)
    sys.exit(1 if R.count("FAIL") else 0)
