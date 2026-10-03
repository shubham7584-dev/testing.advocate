#!/usr/bin/env python3
"""Generate a sitemap.xml for this static site and add its URL to robots.txt.

Usage:
  python scripts/generate_sitemap.py --site-url https://username.github.io/repository

For a custom domain, pass the public site origin instead, e.g. https://example.com.
For GitHub Project Pages, include the repository path in --site-url.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, ElementTree

ROOT = Path(__file__).resolve().parent.parent
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def normalize_site_url(value: str) -> str:
    value = value.strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("--site-url must be an absolute http(s) URL")
    if parsed.query or parsed.fragment:
        raise argparse.ArgumentTypeError("--site-url must not contain a query or fragment")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", required=True, type=normalize_site_url,
                        help="Public base URL; include /repository for GitHub Project Pages")
    args = parser.parse_args()
    base = args.site_url

    pages = sorted(p for p in ROOT.glob("*.html") if p.is_file())
    from xml.etree.ElementTree import register_namespace
    register_namespace("", SITEMAP_NS)
    urlset = Element(f"{{{SITEMAP_NS}}}urlset")
    for page in pages:
        entry = SubElement(urlset, f"{{{SITEMAP_NS}}}url")
        loc = SubElement(entry, f"{{{SITEMAP_NS}}}loc")
        loc.text = f"{base}/{page.name}"

    sitemap_path = ROOT / "sitemap.xml"
    ElementTree(urlset).write(sitemap_path, encoding="utf-8", xml_declaration=True)

    robots_path = ROOT / "robots.txt"
    existing = robots_path.read_text(encoding="utf-8") if robots_path.exists() else "User-agent: *\nAllow: /\n"
    lines = [line for line in existing.splitlines() if not line.strip().lower().startswith("sitemap:")]
    while lines and not lines[-1].strip():
        lines.pop()
    lines.extend(["", f"Sitemap: {base}/sitemap.xml", ""])
    robots_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Generated {sitemap_path.name} with {len(pages)} HTML URLs.")
    print(f"Updated robots.txt with Sitemap: {base}/sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
