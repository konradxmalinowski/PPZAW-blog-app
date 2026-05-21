# Phase 5 — RSS Feeds & XML Sitemap

## Task Description

Add RSS feeds and XML sitemap to the DevLog blog. Also add `robots.txt` and update footer links.

## Acceptance Criteria

- [ ] `python manage.py check` — 0 issues
- [ ] `apps/blog/feeds.py` exists with `LatestPostsFeed` and `CategoryFeed`
- [ ] `apps/blog/sitemaps.py` exists with `PostSitemap` and `CategorySitemap`
- [ ] `/feed/` returns RSS XML (Content-Type: application/rss+xml)
- [ ] `/feed/category/<slug>/` returns RSS for a category
- [ ] `/sitemap.xml` returns valid XML sitemap
- [ ] `/robots.txt` returns text/plain
- [ ] Footer links in `base.html` point to real URLs

## Files to Create

- `apps/blog/feeds.py` — LatestPostsFeed, CategoryFeed
- `apps/blog/sitemaps.py` — PostSitemap, CategorySitemap
- `templates/robots.txt` — robots.txt content

## Files to Modify

- `apps/blog/urls.py` — add feed URL patterns
- `devlog/urls.py` — add sitemap.xml and robots.txt routes
- `templates/base.html` — update footer with real RSS/sitemap links

## API Contract

| Method | URL | Response |
|--------|-----|----------|
| GET | /feed/ | RSS XML |
| GET | /feed/category/<slug>/ | RSS XML |
| GET | /sitemap.xml | XML sitemap |
| GET | /robots.txt | text/plain |

## No DB Changes Needed

Feeds and sitemaps read from existing Post and Category models.

## Edge Cases

- CategoryFeed: 404 if category slug doesn't exist (handled by get_object_or_404)
- Posts without excerpt fall back to first 200 chars of body
- Authors without full_name fall back to username
- Empty sitemap is valid XML (no items)
