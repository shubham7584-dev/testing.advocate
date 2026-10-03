# Adv. Nikhil Shakarwal — Website

Static HTML/CSS/JS site. No build step, no server required.

## Deploy on GitHub Pages

1. Create a new GitHub repository (public, unless you have GitHub Pro/Team for a private Pages site).
2. Upload **everything in this folder** to the repo root (`index.html`, `css/`, `js/`, `images/`, etc. all at the top level — not inside an extra subfolder).
3. In the repo, go to **Settings → Pages**.
4. Under "Build and deployment", set **Source** to `Deploy from a branch`, pick the `main` branch and the `/ (root)` folder, then **Save**.
5. GitHub will give you a URL like `https://<your-username>.github.io/<repo-name>/` — it usually goes live within a minute or two.


## SEO sitemap

- Generate `sitemap.xml` only after confirming the exact public GitHub Pages URL or custom domain.
- For GitHub Project Pages, include the repository path in the URL. Example: `python scripts/generate_sitemap.py --site-url https://USERNAME.github.io/REPOSITORY`.
- For a user/organization Pages site or custom domain, pass its public base URL without a trailing slash.
- The script lists the site's top-level HTML pages and adds the absolute sitemap URL to `robots.txt`. Re-run it if the public URL changes or new HTML pages are added.
- Submit the deployed `sitemap.xml` URL in Google Search Console. A sitemap helps discovery but does not guarantee indexing or rankings.

## Legal news automation

- Legal-news headlines appear as regular cards inside `blog.html`, under the `Legal News` category. They are not shown in a separate news page or separate homepage section.
- `data/news.json` is a generated static data file. The site does not fetch third-party feeds directly in the visitor's browser.
- `scripts/fetch_legal_news.py` reads a Google News RSS search scoped to LiveLaw and Bar & Bench, stores headline/source/date/link metadata only, and does not copy full article text.
- GitHub Actions runs `.github/workflows/update-legal-news.yml` every six hours and can also be run manually from **Actions → Update legal news → Run workflow**.
- To populate the feed for local preview, run `python scripts/fetch_legal_news.py` from the project root while connected to the internet, then refresh `blog.html` and choose the `Legal News` category if desired.
- If the upstream feed is unavailable or returns no valid items, the updater exits without overwriting the existing `data/news.json` file.
- Before enabling the workflow on the live repository, check the publishers' terms and attribution requirements. Headlines link to the source; full article text is not republished.

## Using a custom domain (optional)

If you point a domain you own at this site, add a file named `CNAME` (no extension) to the repo root containing just your domain, e.g.:

```
www.yourdomain.com
```

Then follow GitHub's instructions to add the matching DNS records at your domain registrar.

## Notes

- `.nojekyll` is included so GitHub serves the files as-is.
- All links between pages are relative, so the site works the same whether it's hosted at the root domain or at `username.github.io/repo-name/`.
