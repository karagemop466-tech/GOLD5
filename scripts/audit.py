#!/usr/bin/env python3
"""Dependency-free evidence, link, and static-security checks for GOLD."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_HOSTS = {"www.bluenile.com", "www.ecfr.gov", "www.bbb.org", "www.quince.com", "quince.com", "www.lbma.org.uk"}
HTML_PAGES = ["index.html", "shortlist.html", "calculator.html", "sources.html", "flagged.html"]


class MarkupCheck(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, dict[str, str]]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        if tag in {"a", "link", "script"}:
            key = "href" if tag in {"a", "link"} else "src"
            url = attributes.get(key, "")
            if url:
                self.links.append((url, attributes))
        for name in attributes:
            if name.lower().startswith("on"):
                self.errors.append(f"inline event handler found: {name}")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_json(name: str):
    with (ROOT / "data" / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    products = load_json("products.json")
    sources = load_json("sources.json")
    flags = load_json("flags.json")
    if not isinstance(products, list) or not products:
        fail("product ledger is missing or is not a non-empty list")
    if not isinstance(sources, list) or not sources:
        fail("source register is missing or is not a non-empty list")
    source_map = {source.get("id"): source for source in sources}
    if len(source_map) != len(sources) or None in source_map:
        fail("source IDs are missing or duplicated")

    for source in sources:
        parsed = urlparse(source.get("url", ""))
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            fail(f"source is not HTTPS on an approved official/seller domain: {source.get('url')}")
        if not source.get("accessed") or not source.get("supports") or not source.get("title"):
            fail(f"source record missing title/date/scope: {source.get('id')}")

    if not isinstance(flags, list) or not flags:
        fail("flag register is missing or empty")
    seen_flag_ids = set()
    for flag in flags:
        if not flag.get("id") or flag["id"] in seen_flag_ids:
            fail("flag IDs are missing or duplicated")
        seen_flag_ids.add(flag["id"])
        if not flag.get("category") or not flag.get("title") or not flag.get("detail"):
            fail(f"flag missing category/title/detail: {flag.get('id')}")
        if not flag.get("sources"):
            fail(f"flag has no source links: {flag['id']}")
        for item in flag["sources"]:
            if item.get("id") not in source_map or not item.get("label"):
                fail(f"flag source missing or unlabeled: {flag['id']}")

    required = {
        "id", "name", "seller", "productType", "listedKarat", "listedMetal",
        "explicitSolidGold", "hallmark", "makerMark", "goldAlloyWeightGrams",
        "priceUsd", "priceScope", "priceObserved", "returnTerms", "sourceId",
        "returnSourceId", "reputationSourceIds", "sellerReputation", "independentTestingTerms", "status", "notes",
    }
    unknown_fields = ("explicitSolidGold", "hallmark", "makerMark", "goldAlloyWeightGrams", "independentTestingTerms")
    for product in products:
        missing_keys = required - product.keys()
        if missing_keys:
            fail(f"product {product.get('id')} missing schema fields: {sorted(missing_keys)}")
        product_source = source_map.get(product["sourceId"])
        if not product_source:
            fail(f"product {product['id']} has no product source")
        if product.get("returnSourceId") and product["returnSourceId"] not in source_map:
            fail(f"product {product['id']} has no return-policy source")
        for reputation_id in product.get("reputationSourceIds", []):
            if reputation_id not in source_map:
                fail(f"product {product['id']} has a missing reputation source: {reputation_id}")
        if product.get("sellerReputation") and not product.get("reputationSourceIds"):
            fail(f"product {product['id']} reputation summary has no independent source")
        if product.get("sellerReputation"):
            reputation_evidence = " ".join(source_map[sid]["supports"] for sid in product["reputationSourceIds"]).lower()
            for numeric_claim in re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", product["sellerReputation"]):
                if numeric_claim.lower() not in reputation_evidence:
                    fail(f"seller reputation number {numeric_claim} lacks matching BBB evidence for {product['id']}")
        if not product_source["url"].startswith("https://"):
            fail(f"product {product['id']} source is not HTTPS")
        for key in unknown_fields:
            if product.get(key) not in (None, ""):
                fail(f"unverified field {key} must stay blank for {product['id']}")
        price = product.get("priceUsd")
        if price is not None:
            if not isinstance(price, (int, float)) or price <= 0:
                fail(f"invalid product price for {product['id']}")
            if not product.get("priceScope") or not product.get("priceObserved"):
                fail(f"price lacks scope/date for {product['id']}")
            expected = f"${price:,.0f}"
            if expected not in product_source["supports"]:
                fail(f"price {expected} is not stated in linked seller evidence for {product['id']}")
        if not str(product.get("status", "")).startswith("Flagged"):
            fail(f"listing {product['id']} must remain flagged until all checks and independent test are complete")
        if not product.get("notes"):
            fail(f"product {product['id']} needs a limitations note")

    for page in HTML_PAGES:
        path = ROOT / page
        if not path.is_file():
            fail(f"required page missing: {page}")
        parser = MarkupCheck()
        parser.feed(path.read_text(encoding="utf-8"))
        if parser.errors:
            fail(f"{page}: {'; '.join(parser.errors)}")
        for raw_url, attrs in parser.links:
            url = raw_url.strip()
            if url.startswith(("#", "mailto:", "tel:")):
                continue
            parsed = urlparse(url)
            if parsed.scheme:
                if parsed.scheme != "https":
                    fail(f"insecure/non-HTTPS external link in {page}: {url}")
                if attrs.get("target") == "_blank" and not {"noopener", "noreferrer"}.issubset(set(attrs.get("rel", "").split())):
                    fail(f"new-tab external link missing noopener/noreferrer in {page}: {url}")
                continue
            local = (ROOT / parsed.path.split("#", 1)[0]).resolve()
            if not local.exists():
                fail(f"broken local link/reference in {page}: {url}")

    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    if "@import" in css or re.search(r"url\(\s*['\"]?https?://", css, re.I):
        fail("remote CSS import/asset is not allowed")
    for script in (ROOT / "assets" / "site.js", ROOT / "assets" / "calculator.js"):
        text = script.read_text(encoding="utf-8")
        if re.search(r"\beval\s*\(|\bnew\s+Function\s*\(", text):
            fail(f"unsafe dynamic code execution in {script.name}")
    if "textContent" not in (ROOT / "assets" / "calculator.js").read_text(encoding="utf-8"):
        fail("calculator should render user-provided data with safe text APIs")

    print(f"PASS: {len(products)} listing(s) have linked, scoped evidence; prices are traceable and unknown facts remain blank.")
    print(f"PASS: {len(flags)} flagged findings each link to at least one source-register entry.")
    print(f"PASS: {len(sources)} HTTPS sources use approved seller, government, or independent-review domains and have observation dates.")
    print(f"PASS: {len(HTML_PAGES)} pages have resolvable local references; no insecure external links, inline event handlers, remote assets, or eval/new Function found.")
    print("NOTE: This is a project-specific static evidence/security audit, not a professional penetration test or independent assay.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
