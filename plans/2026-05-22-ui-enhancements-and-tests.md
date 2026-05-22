# Plan: UI Enhancements and Test Suite

## Tasks

### Task 1: Dark/Light Mode Toggle
- Add `.light-mode` CSS block in `terminal.css` after `:root`
- Add `.theme-toggle` button styles after `.nav-link-logout`
- Add `initThemeToggle()` function in `terminal.js` with localStorage persistence
- Add toggle button `<button id="theme-toggle">` in `base.html` navbar before auth block

### Task 2: Table of Contents from Markdown
- Add `render_toc` simple_tag in `apps/blog/templatetags/blog_tags.py`
- Add ToC CSS styles in `terminal.css` before `@media print`
- Add `initToc()` JS function with IntersectionObserver in `terminal.js`
- Add `.toc-link.toc-active` CSS rule
- Insert ToC in `post_detail.html` before `.post-body` div

### Task 3: Test Configuration
- Create `pytest.ini` in project root
- Create `apps/blog/tests/__init__.py` and `apps/blog/tests/test_models.py`
- Create `apps/accounts/tests/__init__.py` and `apps/accounts/tests/test_auth.py`
- Run tests and fix any errors

## Acceptance Criteria
- Toggle persists across page reloads (localStorage)
- Toggle respects `prefers-color-scheme` when no localStorage value
- ToC renders only when post has ≥3 headings
- ToC active link updates on scroll
- All test cases pass
