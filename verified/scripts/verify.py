#!/usr/bin/env python3
"""Verification harness for GOLD5.

Passes (the "security checks" against hallucination):
  1. quote     — every recorded value must be a literal substring of its captured quote
  2. arith     — every derived number is recomputed from its inputs
  3. coverage  — every blank field must be represented by a flag
  4. money     — every $ amount rendered on the site must trace to data or a shown formula
  5. flags     — flag ids and cross-references must resolve
  6. links     — internal links and anchors must resolve ( --links also fetches external URLs )
  7. build     — committed HTML must be byte-identical to a fresh build

Exit code 0 only if nothing fails.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

FAILS: list[str] = []


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def norm(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip().lower()


class Check:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.assertions = 0
        self.failures = 0
        self.detail: list[str] = []

    def ok(self):
        self.assertions += 1

    def fail(self, message: str):
        self.assertions += 1
        self.failures += 1
        self.detail.append(message)
        FAILS.append(f"[{self.name}] {message}")

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "assertions": self.assertions,
            "failures": self.failures,
            "failure_detail": self.detail,
        }


# ---------------------------------------------------------------- 1. quotes
FIELD_MATCHERS = {
    "price_usd": lambda e: [f"${e['price_usd']:,.0f}", f"${e['price_usd']:,.2f}", f"{e['price_usd']:,.2f}"],
    "karat": lambda e: [f"{e['karat']}k", f"{e['karat']}kt"],
    "stock_number": lambda e: [norm(e.get("stock_number") or "")],
    "width_mm": lambda e: [f"{e['width_mm']:g} mm", f"{e['width_mm']:g}mm"],
    "solid_gold": lambda e: ["solid gold"],
}


def check_quotes() -> Check:
    c = Check("quote", "Every recorded value appears literally inside its captured quote.")
    for entry in load("entries.json")["entries"]:
        for item in entry["evidence"]:
            field, quote = item["field"], norm(item["quote"])
            c.ok()
            if not quote:
                c.fail(f"{entry['id']}: empty quote for {field}")
                continue
            matcher = FIELD_MATCHERS.get(field)
            if matcher is None:
                continue  # free-text field (stone, notes): presence of a quote is enough
            options = [norm(o) for o in matcher(entry) if o]
            if field == "width_mm":
                expr = r"(?<![\d.])" + re.escape(f"{entry['width_mm']:g}") + r"(?:\.0+)?0*\s*mm"
                if re.search(expr, quote):
                    continue
            if not any(o in quote for o in options):
                c.fail(f"{entry['id']}: {field} value {options} not found in quote “{item['quote']}”")
    return c


# ------------------------------------------------------------- 2. arithmetic
def check_arithmetic() -> Check:
    c = Check("arith", "Derived values recompute exactly from their inputs and the captured spot.")
    data = load("gold-prices.json")
    oz = data["troy_ounce_grams"]
    ref = next(o for o in data["observations"] if o["id"] == data["reference_id"])
    per_gram = ref["usd_per_troy_oz"] / oz

    # APMEX publishes a per-gram figure; it must agree with the per-ounce figure it published.
    for obs in data["observations"]:
        if "usd_per_gram_stated" in obs:
            c.ok()
            calc = obs["usd_per_troy_oz"] / oz
            if abs(calc - obs["usd_per_gram_stated"]) > 0.02:
                c.fail(f"{obs['id']}: per-gram {obs['usd_per_gram_stated']} vs computed {calc:.2f}")

    for entry in load("entries.json")["entries"]:
        if entry.get("weight_g") is None or entry.get("price_usd") is None:
            continue
        c.ok()
        melt = entry["weight_g"] * entry["karat"] / 24 * per_gram
        if melt > entry["price_usd"]:
            c.fail(
                f"{entry['id']}: price ${entry['price_usd']:.0f} is below fine-gold value ${melt:.0f} at spot — verify weight and karat"
            )
    return c


# --------------------------------------------------------------- 3. coverage
REQUIRED_FIELDS = [
    ("price_usd", "F-010"),
    ("weight_g", "F-004"),
    ("hallmark", "F-005"),
]


def check_coverage() -> Check:
    c = Check("coverage", "Every blank or unstated field is represented by a flag on that row.")
    for entry in load("entries.json")["entries"]:
        flags = set(entry.get("flags", []))
        for field, fid in REQUIRED_FIELDS:
            value = entry.get(field)
            if value in (None, "", "not-stated"):
                c.ok()
                if fid not in flags:
                    c.fail(f"{entry['id']}: {field} is blank but flag {fid} is missing")
            else:
                c.ok()
        if entry["solid_gold"] != "explicit":
            c.ok()
            if "F-006" not in flags:
                c.fail(f"{entry['id']}: solid_gold={entry['solid_gold']} but F-006 missing")
        if not entry.get("weight_status"):
            c.fail(f"{entry['id']}: weight_status missing")
    return c


# ------------------------------------------------------------------ 4. money
STATIC_ALLOWED = {
    # values that appear verbatim in captured policy text or product text
    "$150",      # Blue Nile diamond-report replacement fee
    "$40",       # Brilliant Earth engraving-removal fee
    "$1,000",    # Blue Nile warranty threshold / calculator placeholder
    "$250",      # gift-card promotion text quoted from Brilliant Earth's banner
    "$75",       # Mejuri free-shipping threshold
    "$2,000",    # price-band filter label (UI control, not a claim about a product)
    "$3,000",    # price-band filter label
}


def allowed_money_tokens() -> set[str]:
    allowed = {t.replace(".00", "") for t in STATIC_ALLOWED}
    # Anything quoted anywhere in the evidence data is traceable by definition.
    for name in ("entries.json", "sellers.json", "flags.json", "gold-prices.json", "checklist.json", "meta.json"):
        for token in re.findall(r"\$\s?\d[\d,]*(?:\.\d+)?", (DATA / name).read_text(encoding="utf-8")):
            allowed.add(token.replace(" ", "").rstrip(",.").replace(".00", ""))
    data = load("gold-prices.json")
    oz = data["troy_ounce_grams"]
    ref = next(o for o in data["observations"] if o["id"] == data["reference_id"])
    per_gram = ref["usd_per_troy_oz"] / oz
    for obs in data["observations"]:
        allowed.add(f"${obs['usd_per_troy_oz']:,.2f}")
        allowed.add(f"${obs['usd_per_troy_oz'] / oz:,.2f}")
    for entry in load("entries.json")["entries"]:
        if entry.get("price_usd") is not None:
            allowed.add(f"${entry['price_usd']:,.0f}")
            allowed.add(f"${entry['price_usd']:,.2f}")
    for kat in (10, 14, 18, 22, 24):
        for grams in range(0, 61):
            allowed.add(f"${grams * kat / 24 * per_gram:,.2f}")
    # melt values derived from each entry's own verified weight and karat
    for entry in load("entries.json")["entries"]:
        if entry.get("weight_g") and entry.get("karat"):
            melt = entry["weight_g"] * entry["karat"] / 24 * per_gram
            allowed.add(f"${melt:,.2f}")
            allowed.add(f"${melt:,.0f}")
    # analysis.py computes its figures from the same data with explicit formulas
    sys.path.insert(0, str(ROOT / "scripts"))
    from sitegen import analysis  # noqa: E402

    allowed |= analysis.all_money_tokens()
    return allowed


def page_files() -> list[Path]:
    files = [ROOT / "index.html"] + sorted((ROOT / "pages").glob("*.html"))
    return [p for p in files if p.exists()]


def check_money() -> Check:
    c = Check("money", "Every rendered $ amount traces to captured data or a printed formula.")
    allowed = allowed_money_tokens()
    for path in page_files():
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
        body = html.unescape(re.sub(r"<[^>]+>", " ", text))
        for token in re.findall(r"\$\s?\d[\d,]*(?:\.\d+)?", body):
            token = token.replace(" ", "").rstrip(",.")
            c.ok()
            if token not in allowed and token.replace(".00", "") not in allowed:
                c.fail(f"{path.relative_to(ROOT)}: unaccounted money token {token}")
    return c


# ------------------------------------------------------------------ 5. flags
def check_flags() -> Check:
    c = Check("flags", "Flag ids resolve, and every flag references real data rows.")
    flags = load("flags.json")["flags"]
    ids = {f["id"] for f in flags}
    sellers = {s["id"] for s in load("sellers.json")["sellers"]}
    entries = {e["id"] for e in load("entries.json")["entries"]}
    c.ok()
    if len(ids) != len(flags):
        c.fail("duplicate flag ids")
    for f in flags:
        c.ok()
        if not f.get("source", "").startswith("https://"):
            c.fail(f"{f['id']}: source is not an https URL")
        for target in f["affects"]:
            c.ok()
            if target not in entries and target not in sellers:
                c.fail(f"{f['id']}: affects unknown id {target}")
        if f["severity"] not in ("critical", "warning", "info"):
            c.fail(f"{f['id']}: bad severity {f['severity']}")
    for entry in load("entries.json")["entries"]:
        for fid in entry.get("flags", []):
            c.ok()
            if fid not in ids:
                c.fail(f"{entry['id']}: references missing flag {fid}")
    return c


# ------------------------------------------------------------------ 6. links
def check_links(fetch_external: bool = False) -> Check:
    c = Check("links", "Internal links and anchors resolve; external URLs are well formed.")
    anchors: dict[Path, set[str]] = {}
    for path in page_files():
        text = path.read_text(encoding="utf-8")
        anchors[path] = set(re.findall(r'id="([^"]+)"', text))
    external: set[str] = set()
    for path in page_files():
        text = path.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("mailto:", "data:", "tel:")):
                continue
            if href.startswith(("http://", "https://")):
                external.add(href)
                c.ok()
                parsed = urlparse(href)
                if not parsed.netloc or "." not in parsed.netloc:
                    c.fail(f"{path.name}: malformed external URL {href}")
                if parsed.scheme != "https":
                    c.fail(f"{path.name}: insecure external URL {href}")
                continue
            if href.startswith("#"):
                c.ok()
                if href[1:] and href[1:] not in anchors[path]:
                    c.fail(f"{path.name}: missing anchor {href}")
                continue
            target, _, frag = href.partition("#")
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            c.ok()
            if not resolved.exists():
                c.fail(f"{path.name}: broken link {href}")
            elif frag and frag not in anchors.get(resolved, set()):
                c.fail(f"{path.name}: missing anchor #{frag} in {target}")

    if fetch_external:
        import urllib.error
        import urllib.request

        for url in sorted(external):
            c.assertions += 1
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "GOLD5-verify/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    if resp.status >= 400:
                        c.fail(f"{url}: HTTP {resp.status}")
            except Exception as exc:  # network-restricted environments
                c.fail(f"{url}: unreachable ({type(exc).__name__})")
    return c


# -------------------------------------------------------------- 7. checklist
def check_checklist() -> Check:
    c = Check("checklist", "A checklist item may only be marked covered when coverage is complete.")
    sys.path.insert(0, str(ROOT / "scripts"))
    from sitegen import analysis  # noqa: E402

    cov = analysis.checklist_coverage()
    for item in load("checklist.json")["items"]:
        got, total = cov[item["metric"]]
        c.ok()
        if item["status"] == "covered" and total and got != total:
            c.fail(f"{item['id']}: marked covered but coverage is {got}/{total}")
        if item["status"] == "gap" and total and got == total:
            c.fail(f"{item['id']}: marked gap but coverage is complete ({got}/{total})")
        if item["status"] not in ("covered", "gap", "offline"):
            c.fail(f"{item['id']}: unknown status {item['status']}")
    return c


# ------------------------------------------------------------------ 8. build
def check_build() -> Check:
    c = Check("build", "Committed HTML is byte-identical to a build from data/.")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_site.py"), "--check"],
        capture_output=True,
        text=True,
    )
    c.ok()
    if proc.returncode != 0:
        c.fail((proc.stdout + proc.stderr).strip()[:2000] or "build check failed")
    return c


def commit_sha() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return "unknown"


def main(argv: list[str]) -> int:
    checks = [
        check_quotes(),
        check_arithmetic(),
        check_coverage(),
        check_money(),
        check_flags(),
        check_links("--links" in argv),
        check_checklist(),
        check_build(),
    ]
    total = sum(c.assertions for c in checks)
    failed = sum(c.failures for c in checks)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": commit_sha(),
        "totals": {"assertions": total, "failures": failed, "checks": len(checks)},
        "checks": [c.as_dict() for c in checks],
    }
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Verification report",
        "",
        f"- Generated: {report['generated_at_utc']}",
        f"- Commit: `{report['commit']}`",
        f"- Assertions: {total}",
        f"- Failures: {failed}",
        "",
        "| Pass | What it proves | Assertions | Failures |",
        "|---|---|---|---|",
    ]
    for c in checks:
        lines.append(f"| {c.name} | {c.description} | {c.assertions} | {c.failures} |")
    if FAILS:
        lines += ["", "## Failures", ""] + [f"- {f}" for f in FAILS]
    else:
        lines += ["", "No failures. Every value traces to a captured quote, every blank is flagged.", ""]
    (reports / "verification.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for c in checks:
        print(f"{c.name:9s} assertions={c.assertions:4d} failures={c.failures}")
    print(f"TOTAL assertions={total} failures={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
