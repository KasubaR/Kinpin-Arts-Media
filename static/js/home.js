(function () {
  'use strict';

  function initMobileNav() {
    var toggle = document.getElementById('site-nav-toggle');
    var menu = document.getElementById('site-mobile-menu');
    if (!toggle || !menu) return;

    function setOpen(open) {
      menu.classList.toggle('open', open);
      menu.classList.toggle('closed', !open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }

    toggle.addEventListener('click', function () {
      var open = menu.classList.contains('closed');
      setOpen(open);
    });

    menu.querySelectorAll('.site-mobile-link').forEach(function (link) {
      link.addEventListener('click', function () {
        setOpen(false);
      });
    });
  }

  function initPortfolioTabs() {
    var tabs = document.querySelectorAll('[data-portfolio-tab]');
    var items = document.querySelectorAll('[data-portfolio-item]');
    if (!tabs.length || !items.length) return;

    function activate(tab) {
      tabs.forEach(function (btn) {
        var isActive = btn.getAttribute('data-portfolio-tab') === tab;
        btn.classList.toggle('bg-crimson', isActive);
        btn.classList.toggle('border-crimson', isActive);
        btn.classList.toggle('text-white', isActive);
        btn.classList.toggle('font-medium', isActive);
        btn.classList.toggle('border-white/20', !isActive);
        btn.classList.toggle('text-white/50', !isActive);
        btn.classList.toggle('hover:border-crimson/40', !isActive);
        btn.classList.toggle('hover:text-white/80', !isActive);
      });

      items.forEach(function (item) {
        var raw = item.getAttribute('data-categories') || '';
        var cats = raw.split('|').filter(Boolean);
        var show =
          tab === 'All' || (cats.length > 0 && cats.indexOf(tab) !== -1);
        item.classList.toggle('hidden', !show);
      });
    }

    var initial = 'All';
    tabs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        initial = btn.getAttribute('data-portfolio-tab') || 'All';
        activate(initial);
      });
    });
    activate(initial);
  }

  function initScrollProgress() {
    var root = document.querySelector('.scroll-progress');
    var fill = root && root.querySelector('.scroll-progress__fill');
    if (!fill) return;

    var ticking = false;
    function update() {
      ticking = false;
      var el = document.documentElement;
      var scrollable = el.scrollHeight - el.clientHeight;
      var p = scrollable <= 0 ? 0 : el.scrollTop / scrollable;
      if (p < 0) p = 0;
      if (p > 1) p = 1;
      fill.style.transform = 'scaleX(' + p + ')';
    }

    function onViewportChange() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }

    window.addEventListener('scroll', onViewportChange, { passive: true });
    window.addEventListener('resize', onViewportChange, { passive: true });
    update();
  }

  function initScrollReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length || !('IntersectionObserver' in window)) {
      els.forEach(function (el) {
        el.classList.add('visible');
      });
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('visible');
            observer.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    els.forEach(function (el) {
      observer.observe(el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  function initAll() {
    initMobileNav();
    initPortfolioTabs();
    initScrollProgress();
    initScrollReveal();
  }
})();
