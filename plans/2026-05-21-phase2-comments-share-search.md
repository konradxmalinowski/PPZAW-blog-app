# Plan: DevLog Phase 2 — Comments, Email Share, Search

**Date:** 2026-05-21
**Status:** In progress

## Task Description

Implement Phase 2 of the DevLog blog: email sharing, comment system, and basic search.

## Acceptance Criteria

- [ ] `python manage.py check` — 0 issues
- [ ] `forms.py` exists with `EmailPostForm`, `CommentForm`, `SearchForm`
- [ ] View `post_share` works: GET shows form, POST sends email to console
- [ ] View `post_detail` handles POST with comment, saves to DB
- [ ] Comments display in terminal-style section on post detail
- [ ] Search `/search/?query=...` returns results
- [ ] Comment form auto-fills for authenticated users

## Files to Create

- `apps/blog/forms.py` — EmailPostForm, CommentForm, SearchForm

## Files to Modify

- `apps/blog/views.py` — add post_share, post_search, extend post_detail
- `apps/blog/urls.py` — add share and search URL patterns
- `templates/blog/post_detail.html` — add comments section + share link
- `templates/blog/post_share.html` — new template (terminal style)
- `templates/blog/post_search.html` — new template (terminal style)
- `static/css/terminal.css` — add form, comment, search result styles

## Model State (Phase 1 — existing)

Comment model already exists in `apps/blog/models.py` with:
- post (FK), user (FK nullable), name, email, body, created, updated, active
- Migration 0001_initial.py already includes Comment

No new migrations needed.

## API Contract

No new API endpoints (Phase 2 is template-based views only).

## Error Handling Strategy

- `post_share`: `get_object_or_404` for published post; form validation before send_mail
- `post_detail` comments: form validation; `commit=False` before assigning post FK
- `post_search`: graceful empty state when no results or no query

## Edge Cases

- Unauthenticated user posting comment: name/email required in form
- Authenticated user: auto-fill name/email from User model, readonly fields
- Empty search query: show form only, no results block
- Search with no results: show "0 results" message
- Share email failure: not handled in dev (console backend, always succeeds)
