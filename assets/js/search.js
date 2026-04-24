// ============================================================================
// Simple people search.
//
// Fetches /people.json (generated at build time from _data/people.yml) and
// filters it client-side as you type. No external dependencies.
// ============================================================================
(function () {
  const input   = document.getElementById('q');
  const results = document.getElementById('results');
  if (!input || !results) return;

  let people = null;        // loaded lazily on first focus
  let loading = null;       // in-flight fetch promise, prevents duplicate loads
  const MAX_RESULTS = 8;

  // Derive the site's base URL from a known asset link so search still works
  // when the site is deployed to a subpath (e.g. https://org.github.io/yearbook/).
  function indexUrl() {
    const link = document.querySelector('link[rel="stylesheet"][href*="/assets/css/main.css"]');
    if (link) return link.getAttribute('href').replace(/\/assets\/css\/main\.css.*$/, '/people.json');
    return '/people.json';
  }

  function load() {
    if (people) return Promise.resolve(people);
    if (loading) return loading;
    loading = fetch(indexUrl())
      .then(r => { if (!r.ok) throw new Error('people.json not found'); return r.json(); })
      .then(data => { people = data; return people; })
      .catch(err => { console.warn('Search index failed to load:', err); people = []; return people; });
    return loading;
  }

  function render(matches) {
    if (!matches.length) {
      results.hidden = true;
      results.innerHTML = '';
      return;
    }
    results.innerHTML = matches.map(p =>
      `<li><a href="${p.url}"><span class="r-name">${escapeHtml(p.name)}</span>` +
      (p.meta ? `<span class="r-meta">${escapeHtml(p.meta)}</span>` : '') +
      `</a></li>`
    ).join('');
    results.hidden = false;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[c]));
  }

  // Preload on first focus so results feel instant on first keystroke
  input.addEventListener('focus', load, { once: true });

  input.addEventListener('input', async () => {
    const q = input.value.trim().toLowerCase();
    if (q.length < 2) { render([]); return; }
    const data = await load();
    const matches = data
      .filter(p => p.search.includes(q))
      .slice(0, MAX_RESULTS);
    render(matches);
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.site-search')) results.hidden = true;
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { input.value = ''; render([]); }
  });
})();
