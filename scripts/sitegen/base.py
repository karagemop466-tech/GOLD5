"""Shared helpers for the GOLD5 static-site generator."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

SEVERITY_LABEL = {"critical": "Critical", "warning": "Warning", "info": "Info"}

NAV = [
    ("index.html", "Overview", "overview"),
    ("pages/all-rings.html", "All rings", "all"),
    ("pages/solitaires.html", "Solitaires", "solitaire"),
    ("pages/halo-pave.html", "Halo &amp; pavé", "halo"),
    ("pages/18k.html", "18K gold", "18k"),
    ("pages/complete-rings.html", "Complete rings", "complete"),
    ("pages/sellers.html", "Sellers", "sellers"),
    ("pages/prices.html", "Gold price &amp; calculator", "prices"),
    ("pages/method.html", "Method", "method"),
    ("pages/flagged.html", "Flagged for review", "flagged"),
]


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def usd(value, decimals: int = 0) -> str:
    if value is None:
        return "—"
    return f"${value:,.{decimals}f}"


def short_host(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def badge(text: str, kind: str = "muted") -> str:
    return f'<span class="badge badge-{kind}">{esc(text)}</span>'


def ext(url: str, label: str, cls: str = "") -> str:
    if not url:
        return ""
    cls_attr = f' class="{cls}"' if cls else ""
    return (
        f'<a href="{esc(url)}"{cls_attr} target="_blank" rel="noopener noreferrer">{label}</a>'
    )


def nav_html(prefix: str, active: str) -> str:
    parts = []
    for href, label, key in NAV:
        cls = ' class="active"' if key == active else ""
        parts.append(f'<a href="{prefix}{href}"{cls}>{label}</a>')
    return "\n      ".join(parts)


def layout(prefix: str, title: str, description: str, active: str, body: str) -> str:
    meta = load("meta.json")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="{prefix}assets/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23122b1d'/%3E%3Ctext x='32' y='44' font-size='32' text-anchor='middle' fill='%23d8b45a'%3E%25C3%25A2%25C2%2597%25C2%2588%3C/text%3E%3C/svg%3E">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{prefix}index.html">
      <span class="brand-mark" aria-hidden="true">◈</span>
      <span class="brand-name">GOLD5</span>
      <span class="brand-sub">Gold engagement rings</span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Site">
      {nav_html(prefix, active)}
    </nav>
  </div>
</header>
<div class="rule-banner" role="note">
  <span><strong>No-hallucination rule.</strong> Every value is a verbatim field from an official page captured on
  {esc(meta['verified_on_display'])}, or arithmetic with the formula shown. If a seller did not publish a value, the cell is blank and flagged.</span>
  <a href="{prefix}pages/method.html">How verification works</a>
</div>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="footer-inner">
    <p><strong>GOLD5</strong> · verified {esc(meta['verified_on_display'])} · session {esc(meta['session_id'])} ·
      <a href="{esc(meta['repo'])}" target="_blank" rel="noopener noreferrer">repository</a></p>
    <p class="fine">Independent research, not financial, legal or appraisal advice. Prices change without notice — re-open every source link before buying.
      Nothing here guarantees authenticity. Always verify the physical ring with an independent jeweler and, ideally, XRF testing.</p>
  </div>
</footer>
<script src="{prefix}assets/app.js"></script>
</body>
</html>
"""
