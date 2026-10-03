# Step 8 — SEO foundation for GitHub Pages

## Changes
- Added `scripts/generate_sitemap.py` to generate a standards-based `sitemap.xml` from top-level HTML pages.
- The script requires the exact public site URL and supports GitHub Project Pages URLs that include the repository path.
- The script updates `robots.txt` with the absolute sitemap URL, replacing any older Sitemap directive instead of duplicating it.
- Added sitemap generation and Google Search Console submission instructions to `README.md`.
- Changed the blog article page title in `blog-corporate-lawyer.html` to `Corporate Lawyer Guide | Adv. Nikhil Shakarwal` to distinguish it from the Corporate Lawyer service page.
- Existing site design, page URLs, article data, blog card grid, search/filter/pagination, and legal-news-in-blog behavior are unchanged.

## Important deployment note
A production `sitemap.xml` has deliberately not been generated yet because the exact public GitHub Pages URL or custom domain is not confirmed. Do not publish a sitemap containing a placeholder domain. After confirming the live base URL, run one of:

```bash
python scripts/generate_sitemap.py --site-url https://USERNAME.github.io/REPOSITORY
```

For a custom domain, use that domain as the base URL instead. Then commit the generated `sitemap.xml` and updated `robots.txt`, deploy, and submit the deployed sitemap URL in Google Search Console.

## Validation
- Sitemap generator Python compilation passed.
- Tested generation in a temporary site: two HTML pages produced two sitemap URL entries, and `robots.txt` received the expected absolute Sitemap directive.
- Audit of the current 62 HTML pages found no missing title or meta description tags.
- Duplicate page-title issue identified and fixed for `blog-corporate-lawyer.html`.
- No live deployment or Google Search Console submission performed. No Git push performed.
