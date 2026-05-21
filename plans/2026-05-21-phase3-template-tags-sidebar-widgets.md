# Phase 3 — Custom Template Tags, Sidebar Widgets

**Date:** 2026-05-21
**Status:** In Progress

## Task Description

Extend the DevLog blog with custom inclusion tags (show_recent_posts, show_most_commented, show_tag_cloud), a reading_bar filter, widget partial templates, updated sidebar using those tags, and category_list.html.

## Acceptance Criteria

- [ ] `python manage.py check` — 0 issues
- [ ] Template tags `show_recent_posts`, `show_most_commented`, `show_tag_cloud` registered and working
- [ ] Filter `reading_bar` returns ASCII progress bar
- [ ] Sidebar uses inclusion tags (not static context variables for recent/tags)
- [ ] Widget partials in `templates/partials/`
- [ ] `templates/blog/category_list.html` exists (category view already uses post_list.html so this is supplementary)

## Files to Modify

- `apps/blog/templatetags/blog_tags.py` — ADD new tags/filters (preserve markdownify)
- `templates/partials/sidebar.html` — update sections to use inclusion tags
- `static/css/terminal.css` — append widget CSS

## Files to Create

- `templates/partials/widget_recent_posts.html`
- `templates/partials/widget_most_commented.html`
- `templates/partials/widget_tag_cloud.html`
- `templates/blog/category_list.html`

## Notes

- Views already exist: CategoryPostListView, AuthorPostListView — no view changes needed
- Sidebar currently uses context vars `posts` (sliced) and `popular_tags` from context_processor
- After change: recent posts and tag cloud sections use inclusion tags that query the DB themselves
- Categories section stays as-is (it uses `categories` from context_processor which is fine)
- The `show_most_commented` tag uses `django.db.models.Q` — must import models in blog_tags.py
- `show_tag_cloud` uses taggit's internal m2m table `taggit_taggeditem_items`

## Error Handling

- Inclusion tags return empty querysets gracefully (templates handle `{% empty %}`)
- reading_bar clamps to [0, 10] with `min(int(minutes), 10)`
