#!/usr/bin/env python3
"""Generate sitemap.xml and keep robots.txt in sync for this static site.

Usage examples:
  python scripts/generate_sitemap.py --site-url https://USERNAME.github.io/REPOSITORY
  python scripts/generate_sitemap.py --site-url https://example.com

When --site-url is omitted in GitHub Actions, the script derives the URL from
GITHUB_REPOSITORY (for Project Pages). If a CNAME file exists, that custom
-domain URL is used instead.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, ElementTree, SubElement, register_namespace

ROOT = Path(__file__).resolve().parent.parent
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def normalize_site_url(value: str) -> str:
    value = value.strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("site URL must be an absolute http(s) URL")
    if parsed.query or parsed.fragment:
        raise argparse.ArgumentTypeError("site URL must not contain a query or fragment")
    return value


def detect_site_url() -> str | None:
    cname = ROOT / "CNAME"
    if cname.exists():
        domain = cname.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        if domain:
            return normalize_site_url(f"https://{domain}")

    repository = os.getenv("GITHUB_REPOSITORY", "").strip()
    if "/" in repository:
        owner, repo = repository.split("/", 1)
        if owner and repo:
            return normalize_site_url(f"https://{owner}.github.io/{repo}")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", type=normalize_site_url, help="Public base URL")
    args = parser.parse_args()

    base = args.site_url or detect_site_url()
    if not base:
        parser.error("provide --site-url or run in GitHub Actions with GITHUB_REPOSITORY/CNAME")

    pages = sorted(p for p in ROOT.glob("*.html") if p.is_file())
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

    print(f"Generated sitemap.xml with {len(pages)} HTML URLs.")
    print(f"Sitemap URL: {base}/sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
