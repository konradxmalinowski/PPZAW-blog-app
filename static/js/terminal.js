/**
 * DevLog — terminal.js
 * Phase 7: enhanced terminal effects
 * - Fixed reading-progress bar (#reading-progress)
 * - ASCII reading bar (.reading-progress) on post detail
 * - Auto-dismiss Django messages
 * - Smooth scroll for anchor links
 */

(function () {
  'use strict';

  // ── Fixed reading progress bar (top of page, 2px green line) ──
  // Targets <div id="reading-progress"> in base.html.
  // Shows scroll percentage through the full page.
  function initReadingProgress() {
    var bar = document.getElementById('reading-progress');
    if (!bar) return;

    function onScroll() {
      var total = document.body.scrollHeight - window.innerHeight;
      var pct   = total > 0 ? (window.scrollY / total) * 100 : 0;
      bar.style.width = pct + '%';
    }

    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ── ASCII Reading Bar (.reading-progress on post detail) ──────
  // Shows filled/empty block chars that update as user scrolls.
  function initAsciiReadingBar() {
    var progressEl = document.querySelector('.reading-progress');
    if (!progressEl) return;

    var minutes = parseInt(progressEl.getAttribute('data-minutes') || '0', 10);
    if (minutes === 0) return;

    var FILLED = '█'; // █
    var EMPTY  = '░'; // ░
    var TOTAL  = 10;

    function buildBar(filled) {
      var bar = '';
      for (var i = 0; i < TOTAL; i++) {
        bar += i < filled ? FILLED : EMPTY;
      }
      return bar + ' ' + minutes + ' min';
    }

    function onScroll() {
      var scrollTop  = window.scrollY || document.documentElement.scrollTop;
      var docHeight  = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight <= 0) return;
      var ratio  = Math.min(scrollTop / docHeight, 1);
      var filled = Math.round(ratio * TOTAL);
      progressEl.textContent = buildBar(filled);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ── Auto-dismiss Django messages after 4 seconds ──────────────
  // Works with elements that have data-auto-dismiss attribute.
  // Fades out (CSS opacity transition) then removes from DOM.
  function initMessages() {
    document.querySelectorAll('[data-auto-dismiss]').forEach(function (el) {
      setTimeout(function () { el.style.opacity = '0'; }, 4000);
      setTimeout(function () {
        if (el.parentNode) { el.parentNode.removeChild(el); }
      }, 4500);
    });
  }

  // ── Smooth scroll for in-page anchor links ────────────────────
  // Intercepts clicks on href="#..." and uses scrollIntoView.
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var targetId = a.getAttribute('href');
        if (!targetId || targetId === '#') return;
        var target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  // ── Navbar brand: CSS handles blink animation ─────────────────
  // Mark as initialized so future JS phases can detect it.
  function initNavBrand() {
    var brand = document.querySelector('.navbar-brand, .prompt-link');
    if (brand && !brand.dataset.initialized) {
      brand.dataset.initialized = '1';
    }
  }

  // ── Lazy-load images (IntersectionObserver with native fallback) ──
  function initLazyLoading() {
    var lazyImgs = [].slice.call(document.querySelectorAll('img[data-src]'));
    if (!lazyImgs.length) return;
    if ('IntersectionObserver' in window) {
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var img = entry.target;
            img.src = img.dataset.src;
            if (img.dataset.srcset) img.srcset = img.dataset.srcset;
            img.removeAttribute('data-src');
            obs.unobserve(img);
          }
        });
      }, { rootMargin: '200px 0px' });
      lazyImgs.forEach(function (img) { obs.observe(img); });
    } else {
      lazyImgs.forEach(function (img) {
        img.src = img.dataset.src;
        if (img.dataset.srcset) img.srcset = img.dataset.srcset;
      });
    }
  }

  // ── Prefetch internal links on hover (speed perception) ────────
  function initPrefetch() {
    if (!('prefetch' in document.createElement('link').relList)) return;
    var prefetched = new Set();
    document.addEventListener('mouseover', function (e) {
      var a = e.target.closest('a[href]');
      if (!a) return;
      var href = a.href;
      if (!href || href.startsWith('#') || prefetched.has(href)) return;
      if (a.hostname !== location.hostname) return;
      prefetched.add(href);
      var link = document.createElement('link');
      link.rel = 'prefetch';
      link.href = href;
      document.head.appendChild(link);
    });
  }

  // ── External links — noopener + accessible label ────────────────
  function initExternalLinks() {
    document.querySelectorAll('a[href]').forEach(function (a) {
      if (a.hostname && a.hostname !== location.hostname) {
        a.setAttribute('rel', 'noopener noreferrer');
        if (!a.getAttribute('target')) a.setAttribute('target', '_blank');
        if (!a.querySelector('.sr-only')) {
          var hint = document.createElement('span');
          hint.className = 'sr-only';
          hint.textContent = ' (otwiera się w nowej karcie)';
          a.appendChild(hint);
        }
      }
    });
  }

  // ── Init ──────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initReadingProgress();
    initAsciiReadingBar();
    initMessages();
    initSmoothScroll();
    initNavBrand();
    initLazyLoading();
    initPrefetch();
    initExternalLinks();
  });

})();
