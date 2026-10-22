#!/usr/bin/env python3
"""Negative tests for tools/check_report.py — proves the gate actually catches hallucinations.

Each test plants a plausible error, runs the checker, requires a FAIL, then restores the file.
If any planted error slips through, this script exits non-zero.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "verification", "data.json")
# the suite's landing page moved to report/index.html when the integrated root dashboard
# took over the repo root; plant the HTML error there, where the checker looks
INDEX = os.path.join(ROOT, "report", "index.html")
CHECK = [sys.executable, os.path.join(ROOT, "tools", "check_report.py")]


def run():
    p = subprocess.run(CHECK, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def with_data(mutate, label):
    shutil.copy(DATA, DATA + ".bak")
    try:
        with open(DATA, encoding="utf-8") as f:
            d = json.load(f)
        mutate(d)
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
        rc, out = run()
        hits = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL:")]
        return rc, hits
    finally:
        shutil.move(DATA + ".bak", DATA)


def t_price(d):
    for r in d["listings"]:
        if r["id"] == "A01":
            r["priceUsd"] = 999
            r["priceText"] = "$999"


def t_weight(d):
    for r in d["listings"]:
        if r["id"] == "A07":
            r["weightG"] = 4.2


def t_flag(d):
    for r in d["listings"]:
        if r["id"] == "A01":
            r["flags"].append("G-MADE-UP")


def t_currency(d):
    for r in d["listings"]:
        if r["id"] == "A09":
            r["priceText"] = "$950.00"


def t_drop_token(d):
    for r in d["listings"]:
        if r["id"] == "A05":
            r["tokens"] = [t for t in r["tokens"] if "2.3 grams" not in t]


def t_bad_url(d):
    d["listings"][0]["url"] = "https://example.com/fake-ring"


def t_flag_amount(d):
    for f in d["flags"]:
        if f["id"] == "G-VERA-RETURN-FEES":
            f["detail"] = f["detail"].replace("$20", "$420")


def t_ref_quote(d):
    for r in d["references"]:
        if r["id"] == "R-FTC":
            r["quotes"][0] = "Nobody ever made a rule about karat marks"


def t_html():
    shutil.copy(INDEX, INDEX + ".bak")
    try:
        with open(INDEX, encoding="utf-8") as f:
            s = f.read()
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(s.replace("<h1>", "<p>Best ring: $999.99</p><h1>", 1))
        rc, out = run()
        hits = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL:")]
        return rc, hits
    finally:
        shutil.move(INDEX + ".bak", INDEX)


TESTS = [
    ("Invented price in the data (A01 $1,085 → $999)", lambda: with_data(t_price, "price")),
    ("Invented weight for a row that publishes none (A07 → 4.2 g)", lambda: with_data(t_weight, "weight")),
    ("Row points at a flag that does not exist", lambda: with_data(t_flag, "flag")),
    ("Price text silently changed (A09 EUR page → fake $950.00)", lambda: with_data(t_currency, "currency")),
    ("Evidence token removed (the 2.3 g claim)", lambda: with_data(t_drop_token, "token")),
    ("Product URL replaced with a non-official domain", lambda: with_data(t_bad_url, "url")),
    ("Hand-typed price in the HTML ($999.99)", lambda: t_html()),
    ("Flag detail invents an amount ($20 restocking → $420)", lambda: with_data(t_flag_amount, "flagamount")),
    ("Reference quote that is not on the cited page", lambda: with_data(t_ref_quote, "refquote")),
]


def main():
    print("GOLD5 security tests — planting errors to prove the checker catches them\n")
    passed = 0
    for name, fn in TESTS:
        rc, hits = fn()
        caught = rc != 0
        print(f"[{'CAUGHT' if caught else 'MISSED'}] {name}")
        for h in hits[:3]:
            print("          " + h)
        passed += 1 if caught else 0
    print(f"\n{passed}/{len(TESTS)} planted errors caught")
    rc, out = run()
    print("clean-state check:", "PASS" if rc == 0 else "FAIL")
    return 0 if passed == len(TESTS) and rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
