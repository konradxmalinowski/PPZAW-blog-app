# Phase 7 — Terminal UI Polish

**Date:** 2026-05-21
**Scope:** Static files + templates only. No model/view/URL changes.

## Task description

Final polish pass on the terminal-style UI. Ensure all CSS tokens, JS effects,
and template structures are complete, consistent, and production-ready.

## Acceptance criteria

- [ ] `python manage.py check` — 0 issues
- [ ] `terminal.css` contains all CSS tokens (`:root { --bg: #0d1117; ... }`)
- [ ] `--bg-card-hover` token present (alias for `--bg-hover`)
- [ ] `#reading-progress` fixed top bar CSS + div in base.html
- [ ] `.alert` / `.alert-success` / `.alert-error` classes in CSS
- [ ] JetBrains Mono loaded in base.html
- [ ] RSS `<link>` in base.html `<head>`
- [ ] Messages rendered as `.alert` with `data-auto-dismiss`
- [ ] JS: fixed reading progress bar, auto-dismiss messages, smooth scroll
- [ ] `post_list.html` — classes already correct, no change needed
- [ ] `CLAUDE.md` has implementation status table
- [ ] `collectstatic` works without errors

## Components to modify

1. `static/css/terminal.css` — add missing tokens/classes
2. `static/js/terminal.js` — replace with enhanced version
3. `templates/base.html` — add reading-progress div, RSS link, update messages
4. `CLAUDE.md` — add status table

## What's already in place (DO NOT change)

- All CSS variables `:root { --bg, --bg-card, --bg-border, ... }`
- Full navbar, post card, sidebar, footer, form, comment CSS
- ASCII reading progress (ASCII bar scrolling in `.reading-progress` element)
- `post_list.html` — already has `.post-card`, `.post-card-meta`, `.tag`, etc.
- `base.html` — has JetBrains Mono, messages, footer with RSS link

## What needs adding

1. `terminal.css`:
   - `--bg-card-hover` token (currently named `--bg-hover`)
   - `#reading-progress` fixed 2px top bar
   - `.alert`, `.alert-success`, `.alert-error` classes
   - `.sidebar-title` class alias
   - `.tag-list` class alias (currently `.post-card-tags` / `.tag-cloud`)

2. `terminal.js`:
   - `initReadingProgress()` — fixed top bar (`#reading-progress`)
   - `initMessages()` — auto-dismiss `.alert[data-auto-dismiss]` after 4s
   - `initSmoothScroll()` — smooth scroll for anchor links
   - Keep existing ASCII reading bar logic

3. `base.html`:
   - `<div id="reading-progress"></div>` after `<body>`
   - `<link rel="alternate" type="application/rss+xml" ...>` in `<head>`
   - Messages: add `.alert` wrapper + `data-auto-dismiss` attribute

4. `CLAUDE.md`:
   - Implementation Status table for all 7 phases

## Error handling strategy

- No API calls, no data fetching — pure CSS/JS/template changes
- Run `manage.py check` to verify no Django errors introduced
- Run `collectstatic` to verify static file collection works
