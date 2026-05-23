'use strict';

function initReadingProgress() {
  const bar = document.getElementById('reading-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const total = document.body.scrollHeight - window.innerHeight;
    bar.style.width = total > 0 ? `${(window.scrollY / total) * 100}%` : '0%';
  }, { passive: true });
}

function initMessages() {
  document.querySelectorAll('[data-auto-dismiss]').forEach(el => {
    setTimeout(() => { el.style.opacity = '0'; }, 4000);
    setTimeout(() => { el.parentNode?.removeChild(el); }, 4500);
  });
}

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
  });
}

function initLazyLoading() {
  const imgs = [...document.querySelectorAll('img[data-src]')];
  if (!imgs.length) return;
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const img = entry.target;
        img.src = img.dataset.src;
        if (img.dataset.srcset) img.srcset = img.dataset.srcset;
        img.removeAttribute('data-src');
        obs.unobserve(img);
      });
    }, { rootMargin: '200px 0px' });
    imgs.forEach(img => obs.observe(img));
  } else {
    imgs.forEach(img => {
      img.src = img.dataset.src;
      if (img.dataset.srcset) img.srcset = img.dataset.srcset;
    });
  }
}

function initPrefetch() {
  if (!('prefetch' in document.createElement('link').relList)) return;
  const prefetched = new Set();
  document.addEventListener('mouseover', e => {
    const a = e.target.closest('a[href]');
    if (!a || !a.href || a.href.startsWith('#') || prefetched.has(a.href)) return;
    if (a.hostname !== location.hostname) return;
    prefetched.add(a.href);
    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.href = a.href;
    document.head.appendChild(link);
  });
}

function initExternalLinks() {
  document.querySelectorAll('a[href]').forEach(a => {
    if (!a.hostname || a.hostname === location.hostname) return;
    a.setAttribute('rel', 'noopener noreferrer');
    if (!a.getAttribute('target')) a.setAttribute('target', '_blank');
    if (!a.querySelector('.sr-only')) {
      const hint = document.createElement('span');
      hint.className = 'sr-only';
      hint.textContent = ' (opens in new tab)';
      a.appendChild(hint);
    }
  });
}

function initThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;

  const stored = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isLight = stored === 'light' || (!stored && !prefersDark);

  if (isLight) {
    document.body.classList.add('light-mode');
    btn.textContent = '[dark]';
  } else {
    btn.textContent = '[light]';
  }

  btn.addEventListener('click', () => {
    const light = document.body.classList.toggle('light-mode');
    localStorage.setItem('theme', light ? 'light' : 'dark');
    btn.textContent = light ? '[dark]' : '[light]';
  });
}

function initNavToggle() {
  const toggle = document.getElementById('navbar-toggle');
  const navbar = document.querySelector('.navbar');
  if (!toggle || !navbar) return;

  toggle.addEventListener('click', () => {
    const open = navbar.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? '[×]' : '[≡]';
  });

  navbar.querySelectorAll('a.nav-link, button.nav-link-logout').forEach(el => {
    el.addEventListener('click', () => {
      navbar.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = '[≡]';
    });
  });

  document.addEventListener('click', e => {
    if (navbar.classList.contains('nav-open') && !navbar.contains(e.target)) {
      navbar.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = '[≡]';
    }
  });
}

function initToc() {
  const links = document.querySelectorAll('.toc-link');
  if (!links.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove('toc-active'));
        const active = document.querySelector(`.toc-link[href="#${entry.target.id}"]`);
        if (active) active.classList.add('toc-active');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });

  document.querySelectorAll('.post-body h2, .post-body h3').forEach(h => {
    if (h.id) observer.observe(h);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initReadingProgress();
  initMessages();
  initSmoothScroll();
  initLazyLoading();
  initPrefetch();
  initExternalLinks();
  initThemeToggle();
  initNavToggle();
  initToc();
});
