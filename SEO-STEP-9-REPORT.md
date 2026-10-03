# SEO Step 9 — Structured Data + Live Feed Reliability

## Implemented

1. **Absolute canonical and Open Graph URLs**
   - Updated all 62 HTML pages to use absolute URLs for the current test GitHub Pages site:
     `https://shubham7584-dev.github.io/testing.advocate/`
   - Individual blog pages now use `og:type=article` and include published-time/section metadata.

2. **LegalService + Person structured data on the homepage**
   - Replaced the minimal `Person` JSON-LD block with a JSON-LD graph containing `LegalService` and `Person` entities.
   - Included public phone, email, Delhi service area, opening hours, social profiles, and relationship between the firm and advocate.

3. **BlogPosting structured data on all 25 article pages**
   - Added `BlogPosting` JSON-LD with headline, description, image, publication date, author, publisher, category, language, canonical URL, and main entity URL.

4. **Sitemap and robots synchronization**
   - `sitemap.xml` contains 62 HTML page URLs for the test GitHub Pages URL.
   - `robots.txt` points to the same sitemap.
   - `scripts/generate_sitemap.py` can now derive a GitHub Pages project URL automatically from `GITHUB_REPOSITORY`, or a custom domain from `CNAME`.

5. **Legal-news reliability**
   - Seeded `data/news.json` with 8 recent legal-news cards so the Legal News category is populated immediately.
   - Improved `scripts/fetch_legal_news.py` to query LiveLaw and Bar & Bench separately, deduplicate results, validate publisher identity, and preserve existing data if both upstream searches fail.
   - Existing architecture remains the same: legal news appears as cards inside `blog.html`; there is no separate news page or homepage news section.

6. **Automation workflow**
   - Updated `.github/workflows/update-legal-news.yml` to refresh both the legal-news data and sitemap/robots automatically every 6 hours and on manual dispatch.
   - The workflow commits generated changes only when needed.

7. **Site URL helper**
   - Added `scripts/set_site_url.py` so the final production repo can replace the temporary testing URL in canonical/Open Graph/schema markup before the production push.

## Validation

- HTML pages: 62
- Unique page titles: 62
- Non-empty meta descriptions: 62
- JSON-LD blocks: 26
- BlogPosting schemas: 25
- Site article records: 25
- Seed legal-news items: 8
- Sitemap URLs: 62
- robots.txt sitemap directive: verified
- JavaScript syntax: verified with Node
- Python scripts: verified with `py_compile`
- JSON-LD parsing: verified for all pages

## Current test URL

`https://shubham7584-dev.github.io/testing.advocate/`

## Important production note

Before the final production repository is pushed, run:

```powershell
python scripts/set_site_url.py --site-url https://shubham7584-dev.github.io/Adv.Nikhil.shakarwal
python scripts/generate_sitemap.py --site-url https://shubham7584-dev.github.io/Adv.Nikhil.shakarwal
```

The production URL should be used only when that repository is actually the final public deployment.
