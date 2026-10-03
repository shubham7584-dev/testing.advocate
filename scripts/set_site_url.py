#!/usr/bin/env python3
"""Replace the public site base URL in canonical/Open Graph/schema markup.

Usage:
  python scripts/set_site_url.py --site-url https://USERNAME.github.io/REPOSITORY
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OLD = "https://shubham7584-dev.github.io/testing.advocate"


def normalize(value: str) -> str:
    value = value.strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment:
        raise argparse.ArgumentTypeError("--site-url must be an absolute http(s) URL without query/fragment")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", required=True, type=normalize)
    parser.add_argument("--from-url", default=DEFAULT_OLD, type=normalize)
    args = parser.parse_args()

    changed = 0
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        updated = text.replace(args.from_url, args.site_url)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    # Keep sitemap + robots aligned with the same public URL.
    print(f"Updated public URL in {changed} HTML files.")
    print("Run scripts/generate_sitemap.py --site-url <same-url> afterwards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
