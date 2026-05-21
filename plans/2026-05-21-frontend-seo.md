# Plan: Frontend SEO — OG Tags, Schema.org, Semantic HTML, WCAG AAA

**Date:** 2026-05-21  
**Task slug:** frontend-seo

## Task Description

Implement comprehensive frontend SEO for the DevLog Django blog with terminal-style UI:
- Rewrite `<head>` in `base.html` with full meta/OG/Twitter/Schema.org
- Enhance `post_detail.html` with BlogPosting JSON-LD, BreadcrumbList, visible breadcrumb nav, semantic HTML improvements
- Enhance `post_list.html` with pagination SEO (rel=prev/next), semantic article/time elements
- Add accessibility CSS (skip link, focus-visible, sr-only, reduced motion, print styles, breadcrumb styles)
- Add Core Web Vitals JS (lazy loading fallback, prefetch on hover, external link attributes)

## Acceptance Criteria

- `python manage.py check` — 0 issues
- `<head>`: charset, viewport, title, description, robots, canonical, hreflang, OG (6+ tags), Twitter Card, Schema.org WebSite with SearchAction
- post_detail.html: BlogPosting JSON-LD, BreadcrumbList JSON-LD, visible breadcrumb HTML with microdata
- Template blocks: `meta_description`, `canonical_url`, `og_title`, `schema_extra`, `schema_breadcrumb`
- Skip link as first child of body, `id="main-content"` on `<main>`
- `@media (prefers-reduced-motion: reduce)` in terminal.css
- `.sr-only` and `:focus-visible` styles in terminal.css
- Print styles in terminal.css
- post_list.html: rel="prev"/"next" in head, `<article>` for each post, `<time datetime>` for dates
- Lazy loading on images, noopener noreferrer on external links

## Files to Modify

1. `templates/base.html` — rewrite `<head>`, add skip link, add `id="main-content"` to `<main>`
2. `templates/blog/post_detail.html` — add `extra_head` block with SEO meta/schema, visible breadcrumb, semantic improvements
3. `templates/blog/post_list.html` — add `extra_head` for pagination SEO, `<time datetime>` for dates
4. `static/css/terminal.css` — append accessibility/print/breadcrumb styles
5. `static/js/terminal.js` — append lazy loading, prefetch, external links

## Backend Context Variables (provided by backend agent)

- `SITE_NAME`, `SITE_URL`, `SITE_DESCRIPTION`, `SITE_DEFAULT_IMAGE`, `TWITTER_HANDLE` via context processor
- `post.meta_description` / `post.get_meta_description()` on Post
- `post.cover_image_alt`, `post.canonical_url` on Post
- `category.meta_description` on Category
- Using `{{ SITE_NAME|default:"DevLog" }}` pattern to work before backend commit

## Constraints

- Do NOT modify any files in `apps/` (models, views, URLs)
- Do NOT change existing terminal UI layout (navbar, footer, colors, fonts)
- Only append to CSS/JS files, never overwrite existing styles
