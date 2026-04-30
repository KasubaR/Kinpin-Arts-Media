(function () {
  'use strict';

  function initPortfolioPage() {
    var root = document.getElementById('portfolio-root');
    var dataEl = document.getElementById('portfolio-data');
    if (!root || !dataEl) return;

    var items;
    try {
      items = JSON.parse(dataEl.textContent);
    } catch (e) {
      return;
    }

    var bySlug = {};
    items.forEach(function (p) {
      bySlug[p.slug] = p;
    });

    var behanceUrl = root.getAttribute('data-behance-url') || 'https://www.behance.net/KinpinArts';
    var contactUrl = root.getAttribute('data-contact-url') || '';
    var cards = root.querySelectorAll('.pf-card');
    var filterBtns = root.querySelectorAll('.filter-btn');
    var resultEl = document.getElementById('portfolio-result-count');
    var gridEl = document.getElementById('portfolio-grid');
    var emptyEl = document.getElementById('portfolio-empty');

    var backdrop = document.getElementById('portfolio-lightbox');
    var lbImg = document.getElementById('lb-img');
    var lbTitle = document.getElementById('lb-title');
    var lbDesc = document.getElementById('lb-desc');
    var lbTags = document.getElementById('lb-tags');
    var lbScope = document.getElementById('lb-scope');
    var lbDots = document.getElementById('lb-dots');
    var lbBehance = document.getElementById('lb-behance');
    var lbContact = document.getElementById('lb-contact');
    var lbDetail = document.getElementById('lb-detail');
    var lbPrev = document.getElementById('lb-prev');
    var lbNext = document.getElementById('lb-next');
    var lbClose = document.getElementById('lb-close');

    var activeFilter = 'All';
    var filteredSlugs = [];
    var activeIndex = 0;
    var lightboxOpen = false;

    function getVisibleSlugs() {
      var slugs = [];
      cards.forEach(function (card) {
        if (!card.classList.contains('is-filtered-out')) {
          slugs.push(card.getAttribute('data-slug'));
        }
      });
      return slugs;
    }

    function applyFilter(label) {
      activeFilter = label;
      var visible = 0;

      filterBtns.forEach(function (btn) {
        var f = btn.getAttribute('data-filter');
        btn.classList.toggle('active', f === label);
      });

      cards.forEach(function (card) {
        var raw = card.getAttribute('data-categories') || '';
        var cats = raw.split('|').filter(Boolean);
        var show =
          label === 'All' ||
          (cats.length > 0 && cats.indexOf(label) !== -1);
        card.classList.toggle('is-filtered-out', !show);
        if (show) visible++;
      });

      if (resultEl) {
        resultEl.textContent =
          visible +
          ' project' +
          (visible !== 1 ? 's' : '');
      }

      if (gridEl) gridEl.hidden = visible === 0;
      if (emptyEl) emptyEl.hidden = visible !== 0;

      closeLightbox();

      filteredSlugs = getVisibleSlugs();
    }

    function openLightbox(slug) {
      var item = bySlug[slug];
      if (!item || !backdrop) return;

      filteredSlugs = getVisibleSlugs();
      activeIndex = filteredSlugs.indexOf(slug);
      if (activeIndex < 0) activeIndex = 0;

      renderLightboxItem(item);
      backdrop.hidden = false;
      document.body.style.overflow = 'hidden';
      lightboxOpen = true;

      var multi = filteredSlugs.length > 1;
      if (lbPrev) lbPrev.hidden = !multi;
      if (lbNext) lbNext.hidden = !multi;
      if (lbDots) {
        if (multi) {
          lbDots.hidden = false;
          renderDots();
        } else {
          lbDots.innerHTML = '';
          lbDots.hidden = true;
        }
      }
    }

    function renderDots() {
      if (!lbDots) return;
      lbDots.innerHTML = '';
      filteredSlugs.forEach(function (slug, i) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'transition-all duration-200 rounded-full';
        dot.style.height = '0.4rem';
        dot.style.width = i === activeIndex ? '1.5rem' : '0.4rem';
        dot.style.background =
          i === activeIndex ? '#dd1c49' : 'rgba(255,255,255,0.2)';
        dot.setAttribute('aria-label', 'Go to project ' + (i + 1));
        dot.addEventListener('click', function () {
          activeIndex = i;
          var s = filteredSlugs[activeIndex];
          if (bySlug[s]) renderLightboxItem(bySlug[s]);
          renderDots();
        });
        lbDots.appendChild(dot);
      });
    }

    function renderLightboxItem(item) {
      if (!item) return;
      lbImg.src = item.image;
      lbImg.alt = item.title;
      lbTitle.textContent = item.title;
      lbDesc.textContent = item.description || '';

      var resolvedBehance =
        item.behance_url && String(item.behance_url).trim()
          ? String(item.behance_url).trim()
          : behanceUrl;

      if (lbScope) {
        lbScope.innerHTML = '';
        var scopes = item.scope || [];
        if (scopes.length) {
          lbScope.classList.add('is-visible');
          lbScope.setAttribute('aria-hidden', 'false');
          scopes.forEach(function (line) {
            var chip = document.createElement('span');
            chip.className = 'scope-chip font-body';
            chip.textContent = line;
            lbScope.appendChild(chip);
          });
        } else {
          lbScope.classList.remove('is-visible');
          lbScope.setAttribute('aria-hidden', 'true');
        }
      }

      lbTags.innerHTML = '';
      (item.categories || []).forEach(function (cat) {
        var span = document.createElement('span');
        span.className = 'cat-tag';
        span.textContent = cat;
        lbTags.appendChild(span);
      });
      var yearSpan = document.createElement('span');
      yearSpan.className = 'cat-tag';
      yearSpan.style.color = 'rgba(245,240,246,0.5)';
      yearSpan.style.background = 'rgba(255,255,255,0.06)';
      yearSpan.style.borderColor = 'rgba(255,255,255,0.1)';
      yearSpan.textContent = String(item.year);
      lbTags.appendChild(yearSpan);

      if (lbBehance) lbBehance.href = resolvedBehance;
      if (lbContact) lbContact.href = contactUrl;
      if (lbDetail) lbDetail.href = item.detail_url || '#';
    }

    function closeLightbox() {
      if (!backdrop) return;
      backdrop.hidden = true;
      document.body.style.overflow = '';
      lightboxOpen = false;
    }

    function step(delta) {
      if (filteredSlugs.length <= 1) return;
      activeIndex =
        (activeIndex + delta + filteredSlugs.length) %
        filteredSlugs.length;
      var slug = filteredSlugs[activeIndex];
      if (bySlug[slug]) renderLightboxItem(bySlug[slug]);
      renderDots();
    }

    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        applyFilter(btn.getAttribute('data-filter') || 'All');
      });
    });

    cards.forEach(function (card) {
      card.addEventListener('click', function () {
        var slug = card.getAttribute('data-slug');
        if (slug) openLightbox(slug);
      });
    });

    if (lbClose) lbClose.addEventListener('click', closeLightbox);
    if (lbPrev) lbPrev.addEventListener('click', function () { step(-1); });
    if (lbNext) lbNext.addEventListener('click', function () { step(1); });

    if (backdrop) {
      backdrop.addEventListener('click', function (e) {
        if (e.target === backdrop) closeLightbox();
      });
    }

    document.addEventListener('keydown', function (e) {
      if (!lightboxOpen) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    });

    function initScrollReveal() {
      var els = root.querySelectorAll('.reveal');
      if (!els.length) return;
      if (!('IntersectionObserver' in window)) {
        els.forEach(function (el) {
          el.classList.add('visible');
        });
        return;
      }
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add('visible');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.08 }
      );
      els.forEach(function (el) {
        observer.observe(el);
      });
    }

    applyFilter('All');
    initScrollReveal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPortfolioPage);
  } else {
    initPortfolioPage();
  }
})();
