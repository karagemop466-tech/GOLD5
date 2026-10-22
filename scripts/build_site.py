#!/usr/bin/env python3
"""Build the dependency-free GitHub Pages artifact after evidence/link checks."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"
PAGES = ["index.html", "shortlist.html", "calculator.html", "sources.html", "flagged.html"]


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "audit.py")], cwd=ROOT, check=True)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for page in PAGES:
        shutil.copy2(ROOT / page, OUTPUT / page)
    for directory in ("assets", "data"):
        shutil.copytree(ROOT / directory, OUTPUT / directory)
    (OUTPUT / ".nojekyll").touch()
    print(f"Built static GitHub Pages artifact at {OUTPUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
