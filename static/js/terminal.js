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

  // ── Init ──────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initReadingProgress();
    initAsciiReadingBar();
    initMessages();
    initSmoothScroll();
    initNavBrand();
  });

})();
