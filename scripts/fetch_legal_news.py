#!/usr/bin/env python3
"""Fetch short legal-news metadata from Google News RSS for selected publishers.

Only headlines, source names, dates and links are stored. Article text is not copied.
The workflow should fail rather than replace a working feed file with empty data.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "news.json"
FEED_URL = (
    "https://news.google.com/rss/search?"
    + urllib.parse.urlencode({
        "q": "(site:livelaw.in OR site:barandbench.com) India legal news",
        "hl": "en-IN",
        "gl": "IN",
        "ceid": "IN:en",
    })
)
MAX_ITEMS = 18


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
    seen: set[str] = set()
    for item in root.findall(".//item"):
        title = clean_text(item.findtext("title"))
        url = (item.findtext("link") or "").strip()
        source = clean_text(item.findtext("source")) or "Legal news publisher"
        pub_date = item.findtext("pubDate")
        date, published_at = parse_date(pub_date)
        if not title or not url.startswith("https://"):
            continue
        key = re.sub(r"\W+", " ", title.casefold()).strip()
        if key in seen:
            continue
        seen.add(key)
        items.append({
            "title": title,
            "url": url,
            "source": source,
            "date": date,
            "publishedAt": published_at,
        })
    items.sort(key=lambda entry: entry["publishedAt"], reverse=True)
    return items[:MAX_ITEMS]


def main() -> int:
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "AdvNikhilShakarwal-LegalNewsBot/1.0 (+GitHub Actions)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            if response.status != 200:
                raise RuntimeError(f"RSS request returned HTTP {response.status}")
            payload = response.read()
        items = parse_feed(payload)
        if not items:
            raise RuntimeError("The RSS feed returned no valid news items; keeping the existing file unchanged.")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {len(items)} legal-news headlines to {OUTPUT.relative_to(ROOT)}")
        return 0
    except Exception as exc:  # keep prior generated news if the upstream feed is unavailable
        print(f"Legal-news update failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
