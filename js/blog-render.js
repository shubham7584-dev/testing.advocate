/* Shared article-card renderer for the homepage and blog listing.
   Data lives in data/articles.json so both pages use the same source. */
(() => {
  'use strict';

  const grid = document.querySelector('[data-blog-grid]');
  if (!grid) return;

  const mode = grid.dataset.blogGrid;
  const isListing = mode === 'listing';
  const searchInput = isListing ? document.getElementById('articleSearch') : null;
  const categorySelect = isListing ? document.getElementById('articleCategory') : null;
  const resetButton = isListing ? document.getElementById('resetArticleFilters') : null;
  const resultsCount = isListing ? document.getElementById('articleResultsCount') : null;
  const pagination = isListing ? document.getElementById('articlePagination') : null;
  const pageSize = 9;
  let allArticles = [];
  let currentPage = 1;

  function makeElement(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function makeLink(url, label, className, external = false) {
    const link = makeElement('a', className, label);
    link.href = url;
    if (external) {
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
    }
    return link;
  }

  function formatDate(value) {
    if (!value) return '';
    const parsed = new Date(`${value}T00:00:00`);
    if (Number.isNaN(parsed.getTime())) return '';
    return parsed.toLocaleDateString('en-IN', {
      day: 'numeric', month: 'short', year: 'numeric'
    });
  }

  function makeImage(article, listing) {
    const img = document.createElement('img');
    img.src = article.image;
    img.alt = article.imageAlt || `${article.category || 'Legal'} article`;
    img.loading = 'lazy';
    img.decoding = 'async';
    img.onerror = () => { img.style.display = 'none'; };
    if (listing) {
      const wrapper = makeLink(article.url, '', 'blog-image', Boolean(article.external));
      wrapper.setAttribute('aria-label', article.external
        ? `Read news at ${article.source || 'publisher'}: ${article.title} (opens in a new tab)`
        : `Read article: ${article.title}`);
      wrapper.appendChild(img);
      return wrapper;
    }
    const zoom = makeElement('div', 'zoom');
    zoom.appendChild(img);
    return zoom;
  }

  function makeCard(article, listing) {
    const card = makeElement(listing ? 'article' : 'div', 'blog-card');
    if (listing) {
      card.appendChild(makeImage(article, true));
      const body = makeElement('div', 'blog-body');
      body.appendChild(makeElement('span', 'blog-category', article.category || 'Legal Guides'));
      const titleLink = makeLink(article.url, '', 'blog-title-link', Boolean(article.external));
      titleLink.appendChild(makeElement('h2', '', article.title));
      body.appendChild(titleLink);
      body.appendChild(makeElement('p', '', article.description || 'Read this legal guide for general information and practical considerations.'));
      const dateText = formatDate(article.date);
      if (dateText || article.source) {
        const meta = makeElement('div', 'blog-meta');
        if (dateText) meta.appendChild(makeElement('span', '', dateText));
        if (dateText && article.source) meta.appendChild(makeElement('span', '', ' · '));
        if (article.source) meta.appendChild(makeElement('span', '', article.source));
        body.appendChild(meta);
      }
      const readMore = makeLink(article.url, article.external ? 'Read News at Source ' : 'Read More ', 'read-more-link', Boolean(article.external));
      const arrow = makeElement('span', '', '→');
      arrow.setAttribute('aria-hidden', 'true');
      readMore.appendChild(arrow);
      body.appendChild(readMore);
      card.appendChild(body);
      return card;
    }

    card.appendChild(makeImage(article, false));
    const body = makeElement('div', 'blog-content');
    body.appendChild(makeElement('span', '', article.category || 'Legal Guides'));
    body.appendChild(makeElement('h3', '', article.title));
    body.appendChild(makeElement('p', '', article.description || ''));
    body.appendChild(makeLink(article.url, 'Read More →', 'read-btn'));
    card.appendChild(body);
    return card;
  }

  function populateCategories(articles) {
    if (!categorySelect) return;
    const categories = [...new Set(articles.map(article => (article.category || 'Legal Guides').trim()))]
      .filter(Boolean).sort((a, b) => a.localeCompare(b));
    categories.forEach(category => {
      const option = makeElement('option', '', category);
      option.value = category;
      categorySelect.appendChild(option);
    });
  }

  function getFilteredArticles() {
    const query = (searchInput?.value || '').trim().toLocaleLowerCase();
    const category = categorySelect?.value || '';
    return allArticles.filter(article => {
      const searchable = [article.title, article.description, article.category, article.source].join(' ').toLocaleLowerCase();
      return (!query || searchable.includes(query)) && (!category || (article.category || 'Legal Guides') === category);
    });
  }

  function renderPagination(totalPages) {
    if (!pagination) return;
    pagination.replaceChildren();
    if (totalPages <= 1) return;

    const addButton = (label, page, options = {}) => {
      const button = makeElement('button', '', label);
      button.type = 'button';
      button.disabled = Boolean(options.disabled);
      if (options.current) button.setAttribute('aria-current', 'page');
      if (options.label) button.setAttribute('aria-label', options.label);
      button.addEventListener('click', () => {
        currentPage = page;
        renderListing(true);
      });
      pagination.appendChild(button);
    };

    addButton('Previous', Math.max(1, currentPage - 1), { disabled: currentPage === 1, label: 'Previous page' });
    for (let page = 1; page <= totalPages; page += 1) {
      addButton(String(page), page, { current: page === currentPage, label: `Page ${page}` });
    }
    addButton('Next', Math.min(totalPages, currentPage + 1), { disabled: currentPage === totalPages, label: 'Next page' });
  }

  function renderListing(scrollToGrid = false) {
    if (!isListing) return;
    const filtered = getFilteredArticles();
    const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
    currentPage = Math.min(currentPage, totalPages);
    const start = (currentPage - 1) * pageSize;
    const visible = filtered.slice(start, start + pageSize);

    grid.replaceChildren();
    if (!visible.length) {
      grid.appendChild(makeElement('p', 'blog-empty-state', 'No blog posts or legal news match your search. Try a different keyword or clear the filters.'));
    } else {
      visible.forEach(article => grid.appendChild(makeCard(article, true)));
    }

    if (resultsCount) {
      const summary = filtered.length
        ? `Showing ${start + 1}–${Math.min(start + pageSize, filtered.length)} of ${filtered.length} items`
        : 'No matching items found';
      resultsCount.textContent = summary;
    }
    renderPagination(totalPages);
    if (scrollToGrid) grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  const articlesRequest = fetch('data/articles.json').then(response => {
    if (!response.ok) throw new Error(`Article data request failed (${response.status})`);
    return response.json();
  });
  // Legal news is included only in the full Blogs listing, not as a separate page/section.
  // If the scheduled feed has not populated yet, ordinary articles still render normally.
  const newsRequest = isListing
    ? fetch('data/news.json').then(response => response.ok ? response.json() : []).catch(() => [])
    : Promise.resolve([]);

  Promise.all([articlesRequest, newsRequest])
    .then(([articles, newsItems]) => {
      if (!Array.isArray(articles)) throw new Error('Article data must be a list');
      const unique = [];
      const seen = new Set();
      for (const article of articles) {
        if (!article || !article.url || seen.has(article.url)) continue;
        seen.add(article.url);
        unique.push(article);
      }

      if (isListing && Array.isArray(newsItems)) {
        for (const item of newsItems) {
          if (!item || !item.title || typeof item.url !== 'string' || !item.url.startsWith('https://') || seen.has(item.url)) continue;
          seen.add(item.url);
          unique.push({
            title: item.title,
            url: item.url,
            category: 'Legal News',
            date: item.date || (item.publishedAt || '').slice(0, 10),
            image: 'images/blogs/supreme-court-lawyer.jpg',
            imageAlt: 'Legal news and court developments',
            description: `Latest legal development reported by ${item.source || 'the original publisher'}. Open the source report for full details.`,
            source: item.source || 'Original source',
            publishedAt: item.publishedAt || item.date || '',
            external: true
          });
        }
      }

      unique.sort((a, b) => (b.publishedAt || b.date || '').localeCompare(a.publishedAt || a.date || '') || (a.title || '').localeCompare(b.title || ''));
      allArticles = unique;

      if (isListing) {
        populateCategories(allArticles);
        searchInput?.addEventListener('input', () => { currentPage = 1; renderListing(); });
        categorySelect?.addEventListener('change', () => { currentPage = 1; renderListing(); });
        resetButton?.addEventListener('click', () => {
          if (searchInput) searchInput.value = '';
          if (categorySelect) categorySelect.value = '';
          currentPage = 1;
          renderListing();
          searchInput?.focus();
        });
        renderListing();
        return;
      }

      const visible = mode === 'home' ? unique.slice(0, 3) : unique;
      grid.replaceChildren();
      if (!visible.length) {
        grid.appendChild(makeElement('p', 'blog-data-status', 'No articles are available right now. Please check back soon.'));
        return;
      }
      visible.forEach(article => grid.appendChild(makeCard(article, false)));
    })
    .catch(error => {
      console.error('Unable to load legal articles:', error);
      grid.replaceChildren(makeElement('p', 'blog-data-status', 'Articles could not be loaded. Please refresh the page or use the Blogs menu to try again.'));
      if (resultsCount) resultsCount.textContent = 'Articles could not be loaded.';
    });
})();
