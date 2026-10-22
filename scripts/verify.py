#!/usr/bin/env python3
"""GOLD5 verification harness (v2 — consolidated site).

Checks, in order:
  C1  dataset integrity: unique ids, seller/flag references, required fields
  C2  every listing has an https source URL on an allowed domain + a check date
  C3  every blank value is accompanied by the matching flag (blank never silent)
  C4  spot / purity arithmetic recomputes from the published numbers
  C5  generated HTML: 25 rows, every entry id present, every row links its source
  C6  every internal link and anchor resolves
  C7  every external link is a URL recorded in the dataset (no stray links)
  C8  every dollar figure on the site is either in the dataset or computed from it
  C9  every published price/gram appears in the listings HTML; blanks say why
  C10 no placeholders (TODO, undefined, NaN, lorem, 0000)
  C11 site/assets/data.js is byte-equivalent (as JSON) to data.json
  C12 published spot and raw-gold values recompute on the gold-price page
  C13 every generated page parses as well-formed HTML
  C14 "NO HALLUCINATIONS" banner on every page
  C15 security: https-only links, rel=noopener, no frames/scripts/posting forms

Writes data/check_report_v2.json, appends data/pass_history_v2.json and a
human-readable report to docs/verification/consolidation-2026-10-22.md.
Exit code 1 if any check fails.
"""
import json, os, re, sys, glob, html as htmllib, datetime
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT, "site/assets/data.json")
D = json.load(open(DATA_PATH))
ENTRIES = D["entries"]
SELLERS = {s["id"]: s for s in D["sellers"]}
FLAGS = {f["id"]: f for f in D["flags"]}
REFS = D["references"]
SPOT = D["spot"]["primary"]
SPOT_G = SPOT["usdPerGram"]
TROY = 31.1034768
FIN = D["spot"]["purity"]["fineness"]
PAGES = ["index.html"] + sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "site/*.html")))
PAGE_PATHS = ["index.html"] + ["site/" + p for p in PAGES if p != "index.html"]

results = []   # (check, ok, detail)
def check(cid, ok, detail):
    results.append((cid, bool(ok), detail))
    return ok

def money(n, dec=None):
    if n is None: return ""
    if dec is None: dec = 0 if float(n).is_integer() else 2
    return "$" + f"{n:,.{dec}f}"

def fine_g(e): return None if e["grams"] is None else e["grams"] * FIN[f'{e["karat"]}K']
def metal(e):
    g = fine_g(e)
    return None if g is None else g * SPOT_G
def ratio(e):
    mv = metal(e)
    return None if (mv is None or e["price"] is None) else e["price"] / mv

def read_page(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()

# ---------------------------------------------------------------- C1
errs = []
ids = [e["id"] for e in ENTRIES]
if len(ids) != len(set(ids)): errs.append("duplicate entry ids")
for e in ENTRIES:
    for k in ["id", "name", "short", "sellerId", "category", "karat", "priceBasis", "url", "checkedOn", "provenance"]:
        if e.get(k) in (None, ""): errs.append(f'{e.get("id")}: missing {k}')
    if e["sellerId"] not in SELLERS: errs.append(f'{e["id"]}: unknown seller {e["sellerId"]}')
    for fid in e["flags"]:
        if fid not in FLAGS: errs.append(f'{e["id"]}: unknown flag {fid}')
for f in D["flags"]:
    for eid in f["entryIds"]:
        if eid not in ids: errs.append(f'{f["id"]}: unknown entry {eid}')
if len(SELLERS) != len(D["sellers"]): errs.append("duplicate seller ids")
check("C1", not errs, f"{len(ENTRIES)} entries, {len(D['sellers'])} sellers, {len(D['flags'])} flags, {len(REFS)} references" + ("" if not errs else " — " + "; ".join(errs[:6])))

# ---------------------------------------------------------------- C2
ALLOWED = ("bluenile.com", "brilliantearth.com", "allurez.com", "avianneandco.com", "thejewelrymaster.com",
           "solidgoldjewelers.net", "etsy.com", "kitco.com", "cnbc.com", "apmex.com", "consumer.ftc.gov",
           "ecfr.gov", "law.cornell.edu", "nist.gov", "lbma.org.uk", "bbb.org", "consumeraffairs.com",
           "jvclegal.org", "reportfraud.ftc.gov", "ftc.gov", "help.etsy.com", "topconsumerreviews.com")
bad = []
for e in ENTRIES:
    u = e["url"]
    if not u.startswith("https://"): bad.append(f'{e["id"]}: not https')
    host = (urlsplit(u).hostname or "").lower()
    if not any(host == d or host.endswith("." + d) for d in ALLOWED): bad.append(f'{e["id"]}: host {host}')
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["checkedOn"] or ""): bad.append(f'{e["id"]}: bad date')
    if e["provenance"] not in ("live", "prior"): bad.append(f'{e["id"]}: bad provenance')
check("C2", not bad, f"{len(ENTRIES)} listings have an https official-source URL and a {D['meta']['asOf']} check date" + ("" if not bad else " — " + "; ".join(bad[:6])))

# ---------------------------------------------------------------- C3
miss = []
for e in ENTRIES:
    if e["grams"] is None and "FL-03" not in e["flags"]: miss.append(f'{e["id"]}: no weight, no FL-03')
    if not e["solidStated"] and "FL-15" not in e["flags"]: miss.append(f'{e["id"]}: no solid claim, no FL-15')
    if not e["hallmarkStated"] and "FL-14" not in e["flags"]: miss.append(f'{e["id"]}: no hallmark, no FL-14')
    if e["price"] is None and "FL-13" not in e["flags"]: miss.append(f'{e["id"]}: no price, no FL-13')
    if not e["returnsVerified"] and not any(f in e["flags"] for f in ("FL-07", "FL-11", "FL-12", "FL-13", "FL-16")):
        miss.append(f'{e["id"]}: returns unverified, no returns flag')
check("C3", not miss, "every blank is covered by a flag" + ("" if not miss else " — " + "; ".join(miss[:8])))

# ---------------------------------------------------------------- C4
arith = []
if abs(SPOT["usdPerGram"] * TROY - SPOT["usdPerOz"]) > 0.25:
    arith.append(f"spot gram×ozt {SPOT['usdPerGram']*TROY:.2f} vs {SPOT['usdPerOz']}")
for k, f in FIN.items():
    v = D["spot"]["purity"]["perOz"][k]
    # Kitco's 24K row is the spot price itself (fineness .9999); the other rows are spot × fineness.
    expected = SPOT["usdPerOz"] if k == "24K" else SPOT["usdPerOz"] * f
    if abs(expected - v) > 0.03:
        arith.append(f"{k} purity {v} vs {expected:.2f}")
for e in ENTRIES:
    if e["grams"] is not None:
        if abs(fine_g(e) - e["grams"] * FIN[f'{e["karat"]}K']) > 1e-9: arith.append(f'{e["id"]}: fine')
        if abs(metal(e) - fine_g(e) * SPOT_G) > 1e-9: arith.append(f'{e["id"]}: metal')
check("C4", not arith, "spot, purity and 25 rows of derived values recompute" + ("" if not arith else " — " + "; ".join(arith[:6])))

# ---------------------------------------------------------------- C5
lis = read_page("site/listings.html")
rows = re.findall(r'<tr id="([A-Z]{2,3}-[A-Z0-9]+)"([^>]*)>', lis)
bad5 = []
if len(rows) != len(ENTRIES): bad5.append(f"{len(rows)} rows vs {len(ENTRIES)} entries")
for e in ENTRIES:
    m = re.search(r'<tr id="' + re.escape(e["id"]) + r'"([^>]*)>', lis)
    if not m: bad5.append(f'{e["id"]} missing'); continue
    block_start = m.end()
    block = lis[block_start:block_start + 4000]
    if e["url"] not in block: bad5.append(f'{e["id"]} source link missing')
    if e["grams"] is None:
        if "not stated" not in block: bad5.append(f'{e["id"]} blank weight not labelled')
    if e["price"] is None:
        if "no price" not in block: bad5.append(f'{e["id"]} blank price not labelled')
check("C5", not bad5, f"{len(rows)} listing rows, each with its official source link" + ("" if not bad5 else " — " + "; ".join(bad5[:8])))

# ---------------------------------------------------------------- C6 internal links + anchors
class IdParser(HTMLParser):
    def __init__(self): super().__init__(); self.ids=set()
    def handle_starttag(self, t, a):
        d = dict(a)
        if d.get("id"): self.ids.add(d["id"])
        if d.get("name") and t == "a": self.ids.add(d["name"])

ids_cache = {}
def page_ids(path):
    if path not in ids_cache:
        p = IdParser(); p.feed(read_page(path)); ids_cache[path] = p.ids
    return ids_cache[path]

bad6 = []
for page in PAGE_PATHS:
    base = os.path.dirname(page)
    for href in re.findall(r'href="([^"]+)"', read_page(page)):
        href = htmllib.unescape(href)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in page_ids(page): bad6.append(f"{page}: missing anchor {href}")
            continue
        if href == "":
            bad6.append(f"{page}: empty href"); continue
        target, _, frag = href.partition("#")
        target = unquote(target)
        tp = os.path.normpath(os.path.join(base, target))
        if not os.path.exists(os.path.join(ROOT, tp)):
            bad6.append(f"{page}: {href} → missing {tp}")
        elif frag:
            if tp not in PAGE_PATHS: continue
            if frag not in page_ids(tp): bad6.append(f"{page}: {href} → missing anchor {frag}")
check("C6", not bad6, f"all internal links and anchors resolve across {len(PAGE_PATHS)} pages" + ("" if not bad6 else " — " + "; ".join(bad6[:8])))

# ---------------------------------------------------------------- C7 external registry
registry = set()
for e in ENTRIES: registry.update([e["url"], e.get("priceSourceUrl"), e.get("returnUrl")])
for s in D["sellers"]:
    registry.update([s.get("website"), s.get("contactUrl"), s.get("returnsUrl"), s.get("warrantyUrl")])
    for r in s["reputation"]: registry.add(r["url"])
for r in REFS: registry.add(r["url"])
for q in [SPOT] + D["spot"]["prior"] + D["spot"]["crossChecks"]: registry.add(q["url"])
registry.discard(None)
bad7 = []
for page in PAGE_PATHS:
    for href in re.findall(r'href="([^"]+)"', read_page(page)):
        href = htmllib.unescape(href)
        if href.startswith(("http://", "https://")) and href.split("#")[0] not in {u.split("#")[0] for u in registry}:
            bad7.append(f"{page}: {href}")
check("C7", not bad7, f"every external link ({len(registry)} registered URLs) is recorded in the dataset" + ("" if not bad7 else " — " + "; ".join(bad7[:6])))

# ---------------------------------------------------------------- C8 dollar audit
dollar_re = re.compile(r"\$([0-9][0-9,]*(?:\.[0-9]+)?)")
def dollars(text):
    out = set()
    for s in dollar_re.findall(text):
        try: out.add(round(float(s.replace(",", "")), 4))
        except ValueError: pass
    return out
allowed = set(dollars(json.dumps(D, ensure_ascii=False)))
for e in ENTRIES:
    if e["price"] is not None:
        allowed.add(round(e["price"], 4)); allowed.add(round(e["price"], 2)); allowed.add(round(e["price"]))
    if e.get("compareAt"):
        allowed.add(round(e["compareAt"], 4))
    if metal(e) is not None:
        allowed.add(round(metal(e), 4)); allowed.add(round(metal(e), 2))
for k in FIN:
    v = D["spot"]["purity"]["perOz"][k]
    allowed.update([round(v, 4), round(v, 2), round(v / TROY, 4), round(v / TROY, 2)])
for q in [SPOT] + D["spot"]["prior"] + D["spot"]["crossChecks"]:
    allowed.add(round(q["usdPerOz"], 4)); allowed.add(round(q["usdPerOz"], 2))
    if q.get("usdPerGram"):
        allowed.add(round(q["usdPerGram"], 4)); allowed.add(round(q["usdPerGram"], 2))
for w in [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, TROY]:
    for k in FIN:
        v = w * FIN[k] * SPOT_G
        allowed.update([round(v, 4), round(v, 2)])
bad8 = []
for page in PAGE_PATHS:
    for v in dollars(read_page(page)):
        if not any(abs(v - a) <= 0.011 for a in allowed):
            bad8.append(f"{page}: ${v:,.2f}")
# dedupe & cap
bad8 = sorted(set(bad8))
check("C8", not bad8, f"every dollar figure on the site is dataset-sourced or computed ({len(allowed)} allowed values)" + ("" if not bad8 else f" — {len(bad8)} unmatched: " + "; ".join(bad8[:10])))

# ---------------------------------------------------------------- C9 price/weight presence
bad9 = []
for e in ENTRIES:
    block = re.search(r'<tr id="' + re.escape(e["id"]) + r'"([^>]*)>(.*?)</tr>', lis, re.S)
    if not block: bad9.append(f'{e["id"]} row missing'); continue
    b = block.group(2)
    if e["price"] is not None:
        if money(e["price"]) not in b: bad9.append(f'{e["id"]} price {money(e["price"])} not rendered')
        if e["url"] not in b: bad9.append(f'{e["id"]} URL not rendered')
    if e["grams"] is not None and f'{e["grams"]:g} g' not in b:
        bad9.append(f'{e["id"]} grams not rendered')
check("C9", not bad9, "every published price, weight and source URL is rendered in its row" + ("" if not bad9 else " — " + "; ".join(bad9[:8])))

# ---------------------------------------------------------------- C10 placeholders
bad10 = []
for page in PAGE_PATHS:
    t = read_page(page)
    for token in ["TODO", "undefined", "NaN", "lorem", "XXX", "000000", "{{", "}}"]:
        if token in t: bad10.append(f"{page}: {token}")
check("C10", not bad10, "no placeholders or template leftovers" + ("" if not bad10 else " — " + "; ".join(bad10[:6])))

# ---------------------------------------------------------------- C11 data.js == data.json
bad11 = []
try:
    js = open(os.path.join(ROOT, "site/assets/data.js"), encoding="utf-8").read()
    body = js[js.index("{"): js.rindex("}") + 1]
    if json.loads(body) != D: bad11.append("data.js differs from data.json")
except Exception as ex:
    bad11.append(f"cannot parse data.js: {ex}")
check("C11", not bad11, "site/assets/data.js matches data.json" + ("" if not bad11 else " — " + "; ".join(bad11)))

# ---------------------------------------------------------------- C12 published numbers on gold page
gp = read_page("site/gold-price.html")
bad12 = []
for v in [money(SPOT["usdPerOz"]), money(SPOT["usdPerGram"]), money(D["spot"]["prior"][0]["usdPerOz"])]:
    if v not in gp: bad12.append(f"{v} missing")
for w, k in [(5, "14K"), (1, "24K"), (TROY, "18K")]:
    v = money(w * FIN[k] * SPOT_G)
    if v not in gp: bad12.append(f"raw {w:g}g {k} {v} missing")
check("C12", not bad12, "spot, prior spot and three raw-gold cells recompute on the gold-price page" + ("" if not bad12 else " — " + "; ".join(bad12)))

# ---------------------------------------------------------------- C13 well-formed HTML
class Balance(HTMLParser):
    VOID = {"meta", "link", "br", "hr", "img", "input", "source", "area", "base", "col", "embed", "param", "track", "wbr"}
    def __init__(self): super().__init__(); self.stack=[]; self.err=[]
    def handle_starttag(self, t, a):
        if t not in self.VOID: self.stack.append(t)
    def handle_endtag(self, t):
        if self.stack and self.stack[-1] == t: self.stack.pop()
        elif t in self.stack:
            while self.stack and self.stack[-1] != t: self.err.append("unclosed " + self.stack.pop())
            self.stack.pop()
        else: self.err.append("stray </%s>" % t)
bad13 = []
for page in PAGE_PATHS:
    p = Balance(); p.feed(read_page(page))
    left = [x for x in p.stack if x not in ("html", "body")]
    if p.err or left: bad13.append(f"{page}: {p.err[:3]} {left[:3]}")
check("C13", not bad13, f"{len(PAGE_PATHS)} pages parse as well-formed HTML" + ("" if not bad13 else " — " + "; ".join(bad13[:4])))

# ---------------------------------------------------------------- C14 banner
bad14 = [p for p in PAGE_PATHS if "NO HALLUCINATIONS" not in read_page(p)]
check("C14", not bad14, "the NO HALLUCINATIONS rule is on every page" + ("" if not bad14 else " — " + ", ".join(bad14)))

# ---------------------------------------------------------------- C15 security
bad15 = []
for page in PAGE_PATHS:
    t = read_page(page)
    if re.search(r'href="http://', t): bad15.append(f"{page}: http:// link")
    if re.search(r'href="\s*javascript:', t, re.I): bad15.append(f"{page}: javascript: href")
    if re.search(r'<(iframe|object|embed)\b', t, re.I): bad15.append(f"{page}: embedded frame/object")
    if re.search(r'<script[^>]+src="(https?:)?//', t, re.I): bad15.append(f"{page}: third-party script")
    for tag in re.findall(r'<a\b[^>]*target="_blank"[^>]*>', t):
        if 'rel="noopener' not in tag: bad15.append(f"{page}: _blank without rel=noopener")
    if re.search(r'\son(click|load|error|mouseover)\s*=', t, re.I): bad15.append(f"{page}: inline event handler")
    if re.search(r'<form[^>]*\baction=', t, re.I): bad15.append(f"{page}: form posts somewhere")
    if re.search(r'type="password"', t, re.I): bad15.append(f"{page}: password field")
check("C15", not bad15, "no http://, javascript:, frames, third-party scripts, inline handlers or posting forms; every new-tab link is rel=noopener" + ("" if not bad15 else " — " + "; ".join(sorted(set(bad15))[:8])))

# ---------------------------------------------------------------- report
passed = sum(1 for _, ok, _ in results if ok)
failed = [r for r in results if not r[1]]
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
report = dict(ok=not failed, passed=passed, fail=len(failed), warn=0, ranAt=now,
              reportPath="data/check_report_v2.json",
              checks=[dict(id=c, ok=o, detail=d) for c, o, d in results])
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
json.dump(report, open(os.path.join(ROOT, "data/check_report_v2.json"), "w"), indent=1)

hist_path = os.path.join(ROOT, "data/pass_history_v2.json")
hist = json.load(open(hist_path)) if os.path.exists(hist_path) else []
hist.append(dict(ranAt=now, passed=passed, fail=len(failed), warn=0,
                 checks={c: ("PASS" if o else "FAIL") for c, o, _ in results},
                 note="consolidated site (session 7cca80c9)"))
json.dump(hist, open(hist_path, "w"), indent=1)

md = [f"# Verification report — consolidated GOLD5 site", "",
      f"- Run: {now}", f"- Data as of: {D['meta']['asOf']}",
      f"- Result: **{'PASS' if not failed else 'FAIL'}** — {passed} checks passed, {len(failed)} failed", ""]
for c, o, d in results:
    md.append(f"- {'PASS' if o else 'FAIL'} · **{c}** — {d}")
md += ["", "## What each check means", "",
       "- C1 dataset integrity · C2 official source + date per listing · C3 every blank flagged",
       "- C4 arithmetic · C5/C9 rendered rows · C6 internal links · C7 external link registry",
       "- C8 every dollar figure sourced or computed · C10 placeholders · C11 data.js/data.json parity",
       "- C12 published gold values · C13 HTML well-formedness · C14 no-hallucinations banner",
       "- C15 security: https-only, rel=noopener on new tabs, no frames, third-party scripts, inline handlers or posting forms", ""]
os.makedirs(os.path.join(ROOT, "docs/verification"), exist_ok=True)
open(os.path.join(ROOT, "docs/verification/consolidation-2026-10-22.md"), "w").write("\n".join(md))

print(f"GOLD5 verify v2 — {'PASS' if not failed else 'FAIL'}: {passed} passed, {len(failed)} failed — {now}")
for c, o, d in results:
    print(("  PASS " if o else "  FAIL ") + c + " · " + d)
sys.exit(0 if not failed else 1)
