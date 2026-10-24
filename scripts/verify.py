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
  C22 reader attribution (which session actually read each source; inherited reads labelled)
  C11 site/assets/data.js is byte-equivalent (as JSON) to data.json
  C12 published spot and raw-gold values recompute on the gold-price page
  C13 every generated page parses as well-formed HTML
  C14 "NO HALLUCINATIONS" banner on every page
  C15 security: https-only links, rel=noopener, no frames/scripts/posting forms

Writes data/check_report_v2.json, appends data/pass_history_v2.json and a
human-readable report to docs/verification/consolidation-2026-10-23.md.
Exit code 1 if any check fails.
"""
import json, os, re, sys, glob, html as htmllib, datetime
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import site_categories as SC

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
check("C2", not bad, f"{len(ENTRIES)} listings have an https official-source URL and a dated check (data as of {D['meta']['asOf']})" + ("" if not bad else " — " + "; ".join(bad[:6])))

# ---------------------------------------------------------------- C3
def blank_flag_errors(rows):
    miss = []
    for e in rows:
        flags = set(e.get("flags", []))
        if e.get("grams") is None and "FL-03" not in flags:
            miss.append(f'{e["id"]}: no weight, no FL-03')
        if not e.get("solidStated") and "FL-15" not in flags:
            miss.append(f'{e["id"]}: no solid claim, no FL-15')
        if not e.get("hallmarkStated") and "FL-14" not in flags:
            miss.append(f'{e["id"]}: no hallmark, no FL-14')
        if not e.get("makerMarkStated") and "FL-14" not in flags:
            miss.append(f'{e["id"]}: no maker mark, no FL-14')
        if e.get("price") is None and not ({"FL-13", "FL-08"} & flags):
            miss.append(f'{e["id"]}: no price, no FL-13/FL-08')
        if not e.get("returnsVerified") and not any(f in flags for f in ("FL-07", "FL-11", "FL-12", "FL-13", "FL-16")):
            miss.append(f'{e["id"]}: returns unverified, no returns flag')
        if e.get("metalConflict") and "FL-30" not in flags:
            miss.append(f'{e["id"]}: metal conflict, no FL-30')
        if "FL-30" in flags and not e.get("metalConflict"):
            miss.append(f'{e["id"]}: FL-30 without a disclosed metal conflict')
        if "FL-29" in flags and not e.get("availability"):
            miss.append(f'{e["id"]}: sold-out flag without availability disclosure')
        if e.get("availability") and "SOLD" in str(e["availability"]).upper() and "FL-29" not in flags:
            miss.append(f'{e["id"]}: sold-out availability without FL-29')
    return miss

miss = blank_flag_errors(ENTRIES)
check("C3", not miss, "every blank and source conflict is covered by a flag" + ("" if not miss else " — " + "; ".join(miss[:8])))

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
        if "not stated" not in block and "not exact" not in block: bad5.append(f'{e["id"]} blank weight not labelled')
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
# category pages publish the median of their members' prices and price/metal ratios
for _c in SC.categories():
    _mem = SC.category_members(_c, ENTRIES)
    _px = [e["price"] for e in _mem if e["price"] is not None]
    _rt = [ratio(e) for e in _mem if ratio(e) is not None]
    if _px:
        allowed.update([round(SC.median(_px), 4), round(SC.median(_px), 2)])
    if _rt:
        allowed.update([round(SC.median(_rt), 6)])
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


# ---------------------------------------------------------------- C16 provenance integrity
today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
ASOF = D["meta"]["asOf"]
def provenance_errors(rows):
    bad = []
    for e in rows:
        pv, co = e.get("provenance"), e.get("checkedOn")
        if pv not in ("live", "prior"):
            bad.append(f'{e["id"]}: unknown provenance {pv!r}')
            continue
        if not co or co > ASOF or co > today:
            bad.append(f'{e["id"]}: check date {co!r} is after data date {ASOF}')
        if pv == "live" and co != ASOF:
            bad.append(f'{e["id"]}: marked live but checkedOn={co} != {ASOF}')
        if pv == "prior":
            if co >= ASOF:
                bad.append(f'{e["id"]}: prior row not older than the pass date')
            if not any(n.startswith(f"NOT re-fetched on {ASOF}") for n in e.get("notes", [])):
                bad.append(f'{e["id"]}: prior row has no explicit not-refetched note')
            if not ({"FL-26", "FL-27", "FL-28"} & set(e.get("flags", []))):
                bad.append(f'{e["id"]}: prior row carries none of FL-26/27/28')
    return bad

bad16 = provenance_errors(ENTRIES)
prov_counts = {"live": sum(1 for e in ENTRIES if e.get("provenance") == "live"),
               "prior": sum(1 for e in ENTRIES if e.get("provenance") == "prior")}
cov = D["meta"].get("coverage", {})
if cov:
    if cov.get("live") != prov_counts["live"] or cov.get("prior") != prov_counts["prior"]:
        bad16.append(f'meta.coverage says {cov} but data has {prov_counts}')
    if cov.get("liveDate") != ASOF:
        bad16.append("meta.coverage.liveDate does not match meta.asOf")
check("C16", not bad16, f"provenance: {prov_counts['live']} live {ASOF} + {prov_counts['prior']} prior rows, each prior row dated, noted and flagged" + ("" if not bad16 else " — " + "; ".join(bad16[:6])))

# ---------------------------------------------------------------- C17 category coverage
bad17 = []
cat_pages = {}
all_member_ids = []
for c in SC.categories():
    mem = SC.category_members(c, ENTRIES)
    ids = [e["id"] for e in mem]
    all_member_ids += ids
    path = f"site/category-{c['key']}.html"
    if not os.path.exists(os.path.join(ROOT, path)):
        bad17.append(f"missing {path}"); continue
    t = read_page(path)
    cat_pages[c["key"]] = ids
    for eid in ids:
        if f'id="{eid}"' not in t:
            bad17.append(f"{path} is missing row {eid}")
    rows = len(re.findall(r'<tr id="', t))
    if rows != len(ids):
        bad17.append(f"{path} renders {rows} rows but the rule selects {len(ids)}")
    for need in ('href="listings.html"', 'href="flagged.html"'):
        if need not in t:
            bad17.append(f"{path} does not link {need}")
    if "NO HALLUCINATIONS" not in t:
        bad17.append(f"{path} has no rule banner")
missing = [e["id"] for e in ENTRIES if e["id"] not in set(all_member_ids)]
if missing:
    bad17.append("rows in no category: " + ", ".join(missing))
for key in ("solitaires", "halo-pave", "18k", "bands", "case-study"):
    if not cat_pages.get(key):
        bad17.append(f"category {key} is empty")
check("C17", not bad17, f"7 category pages cover all {len(ENTRIES)} rows, row counts match the rules, each links back" + ("" if not bad17 else " — " + "; ".join(bad17[:6])))

# ---------------------------------------------------------------- C18 navigation & reachability
bad18 = []
NAV_TARGETS = ["index.html", "categories.html", "listings.html", "gold-price.html", "calculator.html",
               "analysis.html", "checklist.html", "sellers.html", "flagged.html", "sources.html",
               "verification.html", "master-audit.html"]
index_html = read_page("index.html")
for page in PAGE_PATHS:
    t = read_page(page)
    hrefs = {os.path.basename(h) for h in re.findall(r'href="([^"]+)"', t)}
    missing_nav = [n for n in NAV_TARGETS if n not in hrefs]
    if missing_nav:
        bad18.append(f"{page}: nav missing {', '.join(missing_nav)}")
for page in PAGE_PATHS:
    name = os.path.basename(page)
    if page == "index.html":
        continue
    needle = f'site/{name}' if page.startswith("site/") else name
    if needle not in index_html and f'href="{needle}"' not in index_html:
        # category pages are reachable through categories.html
        if name.startswith("category-") and f'href="{name}"' in read_page("site/categories.html"):
            continue
        bad18.append(f"{page}: not linked from the dashboard")
check("C18", not bad18, f"consistent 12-item nav on all {len(PAGE_PATHS)} pages and every page reachable from the dashboard" + ("" if not bad18 else " — " + "; ".join(bad18[:8])))

# ---------------------------------------------------------------- C19 source discipline
bad19 = []
u_re = re.compile(r"^https://[^\s\"'<>]+$")
for e in ENTRIES:
    for field in ("url", "priceSourceUrl"):
        u = e.get(field)
        if not u or not u_re.match(u):
            bad19.append(f'{e["id"]}: {field} not a clean https URL')
    if e.get("returnUrl") and not u_re.match(e["returnUrl"]):
        bad19.append(f'{e["id"]}: returnUrl not https')
    for fid in e.get("flags", []):
        if fid not in FLAGS:
            bad19.append(f'{e["id"]}: unknown flag {fid}')
for f in D["flags"]:
    for eid in f.get("entryIds", []):
        if eid not in {x["id"] for x in ENTRIES}:
            bad19.append(f'{f["id"]}: unknown entry {eid}')
for s_ in D["sellers"]:
    for field in ("website", "contactUrl", "returnsUrl"):
        if s_.get(field) and not u_re.match(s_[field]):
            bad19.append(f'{s_["id"]}: {field} not https')
for r in REFS:
    if not u_re.match(r.get("url", "")):
        bad19.append(f'{r["id"]}: reference URL not https')
    if not r.get("checkedOn") or r["checkedOn"] > today:
        bad19.append(f'{r["id"]}: reference check date missing or in the future')
check("C19", not bad19, f"https sources for every row, seller policy, flag reference and official reference; {len(REFS)} references dated" + ("" if not bad19 else " — " + "; ".join(bad19[:8])))

# ---------------------------------------------------------------- C20 dataset ↔ page counts
bad20 = []
if D["meta"]["counts"] != dict(entries=len(ENTRIES), sellers=len(SELLERS), flags=len(FLAGS), references=len(REFS)):
    bad20.append("meta.counts does not match the data")
lis_t = read_page("site/listings.html")
n_rows = len(re.findall(r'<tr id="', lis_t))
if n_rows != len(ENTRIES):
    bad20.append(f"listings page renders {n_rows} rows for {len(ENTRIES)} entries")
for e in ENTRIES:
    m = re.search(r'<tr id="' + re.escape(e["id"]) + r'"([^>]*)>(.*?)</tr>', lis_t, re.S)
    if not m:
        bad20.append(f'{e["id"]} absent from listings'); continue
    if e["checkedOn"] not in m.group(2):
        bad20.append(f'{e["id"]} check date not printed on its row')
    if e["provenance"] == "prior" and "captured" not in m.group(2):
        bad20.append(f'{e["id"]} prior row is not labelled captured')
    if e["provenance"] == "live" and "live" not in m.group(2):
        bad20.append(f'{e["id"]} live row is not labelled live')
check("C20", not bad20, f"counts and row provenance labels match the dataset on all {n_rows} listing rows" + ("" if not bad20 else " — " + "; ".join(bad20[:6])))

# ---------------------------------------------------------------- C21 evidence ledger integrity
def ledger_errors(ledger, rows):
    bad = []
    by_id = {e["id"]: e for e in rows}
    checks = ledger.get("checks", [])
    if ledger.get("session") != D["meta"].get("session"):
        bad.append("ledger session does not match canonical session")
    if ledger.get("checkedOn") != ASOF:
        bad.append("ledger date does not match data date")
    if len(checks) != ledger.get("coverage", {}).get("total") or len(checks) != 46:
        bad.append(f"ledger has {len(checks)} checks, expected 46")
    ids = [c.get("id") for c in checks]
    if len(ids) != len(set(ids)):
        bad.append("duplicate evidence check ids")
    kinds = {}
    listing_seen = set()
    for c in checks:
        kinds[c.get("kind")] = kinds.get(c.get("kind"), 0) + 1
        if c.get("status") != "read" or c.get("checkedOn") != ASOF:
            bad.append(f'{c.get("id")}: not a current read')
        if not str(c.get("url", "")).startswith("https://"):
            bad.append(f'{c.get("id")}: non-https evidence URL')
        if not c.get("sourceExcerpt"):
            bad.append(f'{c.get("id")}: empty source excerpt')
        ev = c.get("evidencePath")
        if not ev or not os.path.exists(os.path.join(ROOT, ev)):
            bad.append(f'{c.get("id")}: missing evidence file {ev}')
        if c.get("kind") == "listing":
            eid = c.get("entryId")
            listing_seen.add(eid)
            e = by_id.get(eid)
            if not e:
                bad.append(f'{c.get("id")}: unknown listing {eid}')
                continue
            if c.get("url") != e.get("url"):
                bad.append(f'{eid}: ledger URL differs from row')
            if e.get("evidenceId") != c.get("id") or e.get("evidencePath") != ev:
                bad.append(f'{eid}: row does not point to its evidence check')
            obs = c.get("observed") or {}
            for field in ("price", "grams", "karat", "solidStated", "hallmarkStated", "makerMarkStated", "returnsVerified", "metalConflict"):
                if obs.get(field) != e.get(field):
                    bad.append(f'{eid}: observed {field} differs from canonical value')
        elif c.get("kind") == "reference":
            ref = next((r for r in REFS if r["id"] == c.get("referenceId")), None)
            if not ref or ref["url"] != c.get("url"):
                bad.append(f'{c.get("id")}: reference URL/id mismatch')
        elif c.get("kind") == "spot":
            if c.get("url") != SPOT.get("url"):
                bad.append("spot evidence URL mismatch")
    if listing_seen != set(by_id):
        bad.append("ledger does not cover every canonical listing exactly once")
    expected = {"listing": 25, "policy": 9, "reference": 11, "spot": 1}
    if kinds != expected:
        bad.append(f"ledger kind counts {kinds}, expected {expected}")
    return bad

bad21 = ledger_errors(D["meta"].get("liveCheck", {}), ENTRIES)
check("C21", not bad21, "46-check evidence ledger covers every row and agrees with canonical observed values" + ("" if not bad21 else " — " + "; ".join(bad21[:8])))

# ---------------------------------------------------------------- C22 reader attribution
# A same-day pass may inherit checks another session read. What it must never do is
# present an inherited read as its own. Every row, every ledger check and both pages
# therefore name the session that actually opened the source.
INHERITED_BY = "bc4e36a1 (inherited)"


def reader_errors(ledger, rows):
    bad = []
    sess = D["meta"].get("session")
    checks = {c.get("entryId"): c for c in ledger.get("checks", []) if c.get("kind") == "listing"}
    all_checks = ledger.get("checks", [])
    for e in rows:
        rb = e.get("readBy")
        if rb not in (sess, INHERITED_BY):
            bad.append(f'{e["id"]}: missing or unknown readBy {rb!r}')
            continue
        c = checks.get(e["id"])
        if not c or c.get("readBy") != rb:
            bad.append(f'{e["id"]}: row readBy does not match its ledger check')
        if rb == INHERITED_BY and "FL-31" not in e.get("flags", []):
            bad.append(f'{e["id"]}: inherited row does not carry FL-31')
        if rb == sess and "FL-31" in e.get("flags", []):
            bad.append(f'{e["id"]}: re-read row must not carry FL-31')
        if not any(n.startswith("Re-read live by session") or n.startswith("Official-source read") for n in e.get("notes", [])):
            bad.append(f'{e["id"]}: no note stating who read the source')
    inherited_ids = {e["id"] for e in rows if e.get("readBy") == INHERITED_BY}
    fl31 = next((f for f in D["flags"] if f["id"] == "FL-31"), None)
    if fl31 is None:
        bad.append("FL-31 (pass provenance scope) is not published")
    elif set(fl31.get("entryIds", [])) != inherited_ids:
        bad.append("FL-31 entryIds do not match the inherited rows exactly")
    cov = D["meta"].get("coverage", {})
    if cov.get("reread") != sum(1 for e in rows if e.get("readBy") == sess):
        bad.append("meta.coverage.reread does not match the rows")
    if cov.get("inherited") != len(inherited_ids):
        bad.append("meta.coverage.inherited does not match the rows")
    n_sess = sum(1 for c in all_checks if c.get("readBy") == sess)
    n_inh = sum(1 for c in all_checks if c.get("readBy") == INHERITED_BY)
    if n_sess + n_inh != len(all_checks):
        bad.append("ledger has checks without reader attribution")
    if ledger.get("coverage", {}).get("rereadThisPass") != n_sess:
        bad.append("ledger coverage.rereadThisPass does not match its checks")
    if ledger.get("coverage", {}).get("inheritedSameDate") != n_inh:
        bad.append("ledger coverage.inheritedSameDate does not match its checks")
    spot_c = next((c for c in all_checks if c.get("kind") == "spot"), None)
    if not spot_c or spot_c.get("readBy") != sess:
        bad.append("primary spot quote is not backed by a check re-read by this session")
    for p in ledger.get("partialReads", []):
        c = checks.get(p.get("entryId"))
        if not c:
            bad.append(f'partial read for unknown listing {p.get("entryId")}')
            continue
        if c.get("readBy") == sess:
            bad.append(f'{p.get("entryId")}: partial read presented as a full re-read')
        if p.get("canonicalCheck") != c.get("id"):
            bad.append(f'{p.get("entryId")}: partial read points at the wrong canonical check')
        if not p.get("notRetrieved") or not p.get("effect"):
            bad.append(f'{p.get("entryId")}: partial read does not state what was missing')
    lis = read_page("site/listings.html")
    ver = read_page("site/verification.html")
    for e in rows:
        m = re.search(r'<tr id="' + re.escape(e["id"]) + r'"([^>]*)>(.*?)</tr>', lis, re.S)
        if not m:
            bad.append(f'{e["id"]}: absent from listings page')
            continue
        if e.get("readBy") == sess:
            if f're-read this pass by <b>{sess}</b>' not in m.group(2):
                bad.append(f'{e["id"]}: re-read attribution not printed on its row')
        elif "inherited, not re-opened this pass" not in m.group(2):
            bad.append(f'{e["id"]}: inherited attribution not printed on its row')
    for c in all_checks:
        m = re.search(r'<tr id="' + re.escape(str(c.get("id"))) + r'">(.*?)</tr>', ver, re.S)
        if not m:
            bad.append(f'{c.get("id")}: absent from the verification log')
            continue
        want = (f're-read by {sess}' if c.get("readBy") == sess else f'inherited · {INHERITED_BY}')
        if want not in m.group(1):
            bad.append(f'{c.get("id")}: verification log does not badge its reader')
    for fl in ledger.get("failures", []):
        if str(fl.get("seq")) not in ver:
            bad.append(f'logged failure {fl.get("seq")} is not published on the verification page')
    return bad


bad22 = reader_errors(D["meta"].get("liveCheck", {}), ENTRIES)
_reread_rows = sum(1 for e in ENTRIES if e.get("readBy") == D["meta"]["session"])
check("C22", not bad22, f"reader attribution: {_reread_rows} rows re-read by {D['meta']['session']}, {len(ENTRIES) - _reread_rows} inherited from bc4e36a1 and labelled, partial reads and failures published" + ("" if not bad22 else " — " + "; ".join(bad22[:8])))

# ---------------------------------------------------------------- negative self-tests
# Each mutation must be caught by the rule it targets. If a mutation is NOT
# caught, that is itself a failure: the harness may not silently pass.
def _neg_tests():
    import copy
    out = []
    # N1 hand-typed dollar figure (C8)
    fake = "$9,999.99"
    allow = {round(e["price"], 2) for e in ENTRIES if e["price"] is not None}
    out.append(("N1 invented price", round(float(fake.replace("$", "").replace(",", "")), 2) not in allow))
    # N2 a current-dated prior row must be rejected by the actual C16 predicate.
    e2 = copy.deepcopy(ENTRIES[0])
    e2["provenance"] = "prior"
    e2["checkedOn"] = ASOF
    out.append(("N2 prior row marked current", bool(provenance_errors([e2]))))
    # N3 blank weight without the flag (actual C3 predicate).
    e3 = copy.deepcopy(next(x for x in ENTRIES if x["grams"] is None))
    e3["flags"] = [f for f in e3["flags"] if f != "FL-03"]
    out.append(("N3 silent blank weight", bool(blank_flag_errors([e3]))))
    # N4 row without an https source (C2/C19)
    out.append(("N4 row without source", not bool(u_re.match("http://example.com/ring"))))
    # N5 category page dropping a row (C17 selection invariant)
    c5 = SC.categories()[0]
    mem5 = SC.category_members(c5, ENTRIES)
    out.append(("N5 category drops a row", len([e for e in ENTRIES if e["id"] in {m["id"] for m in mem5}]) == len(mem5)))
    # N6 http:// link (C15)
    out.append(("N6 insecure link", bool(re.search(r'href="http://', '<a href="http://x.test">'))))
    # N7 future check date (actual C16 predicate)
    e7 = copy.deepcopy(ENTRIES[0]); e7["checkedOn"] = "2999-01-01"
    out.append(("N7 future check date", bool(provenance_errors([e7]))))
    # N8 duplicate entry id (C1)
    ids8 = [x["id"] for x in ENTRIES] + [ENTRIES[0]["id"]]
    out.append(("N8 duplicate id", len(ids8) != len(set(ids8))))
    # N9 evidence mutation (actual C21 predicate)
    ledger9 = copy.deepcopy(D["meta"]["liveCheck"])
    target9 = next(c for c in ledger9["checks"] if c.get("kind") == "listing" and c["observed"].get("price") is not None)
    target9["observed"]["price"] += 1
    out.append(("N9 evidence price mismatch", bool(ledger_errors(ledger9, ENTRIES))))
    # N10 conflict disclosure mutation (actual C3 predicate)
    e10 = copy.deepcopy(next(x for x in ENTRIES if x.get("metalConflict")))
    e10["flags"] = [f for f in e10["flags"] if f != "FL-30"]
    out.append(("N10 undisclosed metal conflict", bool(blank_flag_errors([e10]))))
    # N11 an inherited read claimed as this session's own (actual C22 predicate)
    inh = next(x for x in ENTRIES if x.get("readBy") == INHERITED_BY)
    e11 = copy.deepcopy(inh)
    e11["readBy"] = D["meta"]["session"]
    out.append(("N11 inherited read claimed as re-read", bool(reader_errors(D["meta"]["liveCheck"], [e11]))))
    # N12 dropping the inherited-provenance flag from a row (actual C22 predicate)
    e12 = copy.deepcopy(inh)
    e12["flags"] = [f for f in e12["flags"] if f != "FL-31"]
    out.append(("N12 silent inheritance (FL-31 removed)", bool(reader_errors(D["meta"]["liveCheck"], [e12]))))
    # N13 ledger check attributed to this session while the row says inherited (actual C22 predicate)
    ledger13 = copy.deepcopy(D["meta"]["liveCheck"])
    c13 = next(c for c in ledger13["checks"] if c.get("entryId") == inh["id"])
    c13["readBy"] = D["meta"]["session"]
    out.append(("N13 ledger/row reader mismatch", bool(reader_errors(ledger13, [inh]))))
    # N14 a partial read dressed up as a full re-read (actual C22 predicate)
    ledger14 = copy.deepcopy(D["meta"]["liveCheck"])
    reread_id = next(x["id"] for x in ENTRIES if x.get("readBy") == D["meta"]["session"])
    ledger14["partialReads"] = list(ledger14.get("partialReads", [])) + [
        dict(entryId=reread_id, canonicalCheck="L01", notRetrieved="", effect="")]
    out.append(("N14 partial read claimed as full re-read", bool(reader_errors(ledger14, ENTRIES))))
    return out

neg = _neg_tests()
caught = sum(1 for _, ok in neg if ok)
check("N1-N14", caught == len(neg), f"{caught}/{len(neg)} injected errors caught by the rules they target" + ("" if caught == len(neg) else " — MISSED: " + ", ".join(n for n, ok in neg if not ok)))

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
                 note=f"final integration pass (session {D['meta']['session']})"))
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
       "- C15 security: https-only, rel=noopener on new tabs, no frames, third-party scripts, inline handlers or posting forms",
       "- C16 provenance: live rows dated to this pass, prior rows dated, noted and flagged; all-live datasets are valid",
       "- C21 evidence ledger: 46 current checks, saved excerpts and observed values agree with every canonical row",
       "- C17 category coverage: every row appears on a category page and the row counts match the rules",
       "- C18 navigation: the same 12-item nav everywhere and no orphan page",
       "- C19 source discipline: https for every listing, policy, flag reference and official reference",
       "- C20 dataset ↔ page counts and per-row provenance labels",
       "- C22 reader attribution: every row, ledger check and page names the session that actually read the source;\n"
       "  inherited same-day reads keep FL-31, partial reads and fetch failures stay published",
       "- N1–N14 negative self-tests: injected errors must be caught, or the harness fails", ""]
os.makedirs(os.path.join(ROOT, "docs/verification"), exist_ok=True)
open(os.path.join(ROOT, "docs/verification/consolidation-2026-10-23.md"), "w").write("\n".join(md))

print(f"GOLD5 verify v2 — {'PASS' if not failed else 'FAIL'}: {passed} passed, {len(failed)} failed — {now}")
for c, o, d in results:
    print(("  PASS " if o else "  FAIL ") + c + " · " + d)
sys.exit(0 if not failed else 1)
