/**
 * DevLog — terminal.js
 * Minimal vanilla JS: cursor blink (CSS handles animation),
 * ASCII reading-progress bar on post detail.
 */

(function () {
  'use strict';

  // ── Cursor is handled by CSS animation (blink keyframe) ──
  // Nothing extra needed for the navbar cursor.

  // ── ASCII Reading Progress Bar ────────────────────────────
  // On post_detail, if the user scrolls, update the reading
  // progress bar based on scroll position vs. article length.
  function initReadingProgress() {
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
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight <= 0) return;
      var ratio = Math.min(scrollTop / docHeight, 1);
      var filled = Math.round(ratio * TOTAL);
      progressEl.textContent = buildBar(filled);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    // Set initial value from CSS — no change needed on load.
  }

  // ── Hover highlight for post cards ───────────────────────
  // CSS transitions already handle this — no JS needed.

  // ── Init ──────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initReadingProgress();
  });

})();
