#!/usr/bin/env python3
"""Fetch recent legal-news metadata from Google News RSS.

The site stores headlines, source names, dates and links only. Full article
text is not copied. Two independent publisher-scoped searches are used so a
single upstream/feed failure does not stop the other source from updating the
site. Existing data is preserved when no valid items can be fetched.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "news.json"
MAX_ITEMS = 18
NEWS_IMAGE_RULES = [
    (('supreme court',), 'images/blogs/supreme-court-lawyer.jpg'),
    (('high court',), 'images/blogs/civil-law.jpg'),
    (('property', 'real estate'), 'images/blogs/property-law.jpg'),
    (('divorce', 'matrimonial', 'family'), 'images/blogs/divorce-law.jpg'),
    (('child', 'custody'), 'images/blogs/child-custody.jpg'),
    (('criminal', 'murder', 'defamation', 'money laundering', 'ed custody'), 'images/blogs/criminal-law.jpg'),
    (('bail',), 'images/blogs/bail-law.jpg'),
    (('corporate', 'company', 'sail', 'steel'), 'images/blogs/corporate-law.jpg'),
    (('consumer',), 'images/blogs/consumer-law.jpg'),
    (('cheque', 'cheque bounce'), 'images/blogs/cheque-bounce-law.jpg'),
    (('medical', 'hospital', 'doctor'), 'images/blogs/medical-negligence.jpg'),
]
NEWS_IMAGE_FALLBACKS = [
    'images/blogs/civil-law.jpg',
    'images/blogs/legal-services.jpg',
    'images/blogs/corporate-law.jpg',
    'images/blogs/family-law.jpg',
    'images/blogs/court-marriage-law.jpg',
    'images/blogs/consumer-law.jpg',
]
ALLOWED_HOSTS = {"livelaw.in", "www.livelaw.in", "barandbench.com", "www.barandbench.com"}
FEED_QUERIES = [
    "site:livelaw.in India legal court law news",
    "site:barandbench.com India legal court law news",
]


def build_feed_url(query: str) -> str:
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode({
        "q": query,
        "hl": "en-IN",
        "gl": "IN",
        "ceid": "IN:en",
    })


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def parse_date(value: str | None) -> tuple[str, str]:
    if not value:
        return "", ""
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        parsed = parsed.astimezone(timezone.utc)
        return parsed.date().isoformat(), parsed.isoformat(timespec="seconds")
    except (TypeError, ValueError, OverflowError):
        return "", ""


def parse_feed(xml_bytes: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(xml_bytes)
    items: list[dict[str, str]] = []
    for item in root.findall(".//item"):
        title = clean_text(item.findtext("title"))
        url = (item.findtext("link") or "").strip()
        source_el = item.find("source")
        source = clean_text(source_el.text if source_el is not None else "") or "Legal news publisher"
        source_url = (source_el.attrib.get("url", "") if source_el is not None else "").strip()
        pub_date = item.findtext("pubDate")
        date, published_at = parse_date(pub_date)

        # Google News can wrap links in a Google-hosted redirect. Keep those
        # links (they lead to the original story) but accept only publisher
        # identities we explicitly scoped in the feeds above.
        publisher_host = urllib.parse.urlparse(source_url).netloc.lower()
        if not title or not url.startswith("https://"):
            continue
        if publisher_host and publisher_host not in ALLOWED_HOSTS:
            continue

        items.append({
            "title": title,
            "url": url,
            "source": source,
            "date": date,
            "publishedAt": published_at,
        })

    deduped: dict[str, dict[str, str]] = {}
    for item in items:
        key = re.sub(r"\W+", " ", item["title"].casefold()).strip()
        if key and key not in deduped:
            deduped[key] = item

    return sorted(deduped.values(), key=lambda entry: entry.get("publishedAt", ""), reverse=True)[:MAX_ITEMS]



def choose_news_image(title: str, index: int) -> str:
    text = (title or '').casefold()
    for keywords, image in NEWS_IMAGE_RULES:
        if any(keyword in text for keyword in keywords):
            return image
    return NEWS_IMAGE_FALLBACKS[index % len(NEWS_IMAGE_FALLBACKS)]


def fetch(url: str) -> list[dict[str, str]]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; AdvNikhilShakarwal-LegalNewsBot/2.0; +https://github.com/shubham7584-dev/testing.advocate)"
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"RSS request returned HTTP {response.status}")
        return parse_feed(response.read())


def main() -> int:
    collected: dict[str, dict[str, str]] = {}
    failures: list[str] = []

    for query in FEED_QUERIES:
        try:
            for item in fetch(build_feed_url(query)):
                key = re.sub(r"\W+", " ", item["title"].casefold()).strip()
                if key:
                    collected[key] = item
        except Exception as exc:  # one publisher failing must not stop the other
            failures.append(f"{query}: {exc}")

    items = sorted(collected.values(), key=lambda entry: entry.get("publishedAt", ""), reverse=True)[:MAX_ITEMS]
    for index, item in enumerate(items):
        item["image"] = choose_news_image(item.get("title", ""), index)
        item["imageAlt"] = f"Legal News – {item.get('source', 'Original publisher')}"
    if not items:
        details = "; ".join(failures) or "no valid items returned"
        print(f"Legal-news update failed; keeping existing data. Details: {details}", file=sys.stderr)
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} legal-news headlines to {OUTPUT.relative_to(ROOT)}")
    if failures:
        print("Some feeds failed but the remaining publisher feed(s) were used:")
        for failure in failures:
            print(f"- {failure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
