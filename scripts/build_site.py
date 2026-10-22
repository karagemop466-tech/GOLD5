"""Build the GOLD5 site from data/*.json. Deterministic: --check compares output."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitegen.base import ROOT, load  # noqa: E402
from sitegen import pages  # noqa: E402

OUTPUTS = {
    "index.html": pages.overview_page,
    "pages/all-rings.html": pages.all_rings_page,
    "pages/solitaires.html": lambda: pages.category_page("solitaire-setting"),
    "pages/halo-pave.html": lambda: pages.category_page("halo-pave-setting"),
    "pages/18k.html": lambda: pages.category_page("18k-gold"),
    "pages/complete-rings.html": lambda: pages.category_page("complete-ring"),
    "pages/sellers.html": pages.sellers_page,
    "pages/prices.html": pages.prices_page,
    "pages/method.html": pages.method_page,
    "pages/flagged.html": pages.flagged_page,
}


def render_all() -> dict[str, str]:
    return {name: fn() for name, fn in OUTPUTS.items()}


def main(argv: list[str]) -> int:
    check = "--check" in argv
    rendered = render_all()
    stale = []
    for name, content in rendered.items():
        path = ROOT / name
        if check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if check:
        if stale:
            print("STALE (rebuild needed): " + ", ".join(stale))
            return 1
        print(f"OK: {len(rendered)} pages match data/*.json")
        return 0
    print(f"Built {len(rendered)} pages: " + ", ".join(rendered))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
