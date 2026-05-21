# SEO Backend — DevLog

Data: 2026-05-21

## Opis zadania
Implementacja backendu SEO dla bloga DevLog (Django 5.2). Dodanie pól SEO do modeli,
context processora, ustawień SEO/security, middleware nagłówków bezpieczeństwa,
rozszerzenie sitemap oraz robots.txt.

## Kryteria akceptacji
- `manage.py check` — 0 issues
- Migracja `seo_fields`: meta_description, meta_keywords, cover_image_alt, canonical_url (Post) + meta_description (Category)
- `Post.get_meta_description()` zwraca fallback z excerpt lub body
- `Post.get_canonical_url()` zwraca custom lub auto URL
- `apps.blog.seo_context.seo_defaults` jako context processor
- SITE_NAME, SITE_URL, SITE_DESCRIPTION, TWITTER_HANDLE, SITE_DEFAULT_OG_IMAGE w settings
- SecurityHeadersMiddleware dodaje CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy
- StaticSitemap w sitemaps dict (urls.py)
- robots.txt poprawny z {{ SITE_URL }} przez RobotsTxtView

## Pliki do utworzenia / modyfikacji
- MODYFIKACJA apps/blog/models.py — pola SEO + metody (Post), meta_description (Category)
- MODYFIKACJA apps/blog/admin.py — fieldsets SEO (Post), meta_description (Category)
- NOWY apps/blog/seo_context.py — context processor seo_defaults
- MODYFIKACJA devlog/settings/base.py — context processor, ustawienia SEO/security, middleware, pagination
- MODYFIKACJA devlog/settings/local.py — SITE_URL nadpisany na http://127.0.0.1:8000
- NOWY devlog/middleware.py — SecurityHeadersMiddleware
- MODYFIKACJA apps/blog/sitemaps.py — protocol https, select_related, StaticSitemap
- MODYFIKACJA devlog/urls.py — StaticSitemap w dict + RobotsTxtView z SITE_URL
- MODYFIKACJA templates/robots.txt — nowe disallow + {{ SITE_URL }}
- NOWA migracja blog/migrations/..._seo_fields.py

## DB changes
Czysto additive — nowe pola CharField/URLField z blank=True. Brak zmian destrukcyjnych,
brak zmian istniejących pól. Migracja bezpieczna do zastosowania na danych produkcyjnych.

## Error handling
get_meta_description czyści markdown przez regex; brak ścieżek błędów (operacje na stringach).
Middleware czyta ustawienia defensywnie przez getattr z fallbackiem.

## Edge cases
- Post bez excerpt i body → get_meta_description zwraca '' (strip pustego stringa)
- canonical_url puste + brak request → zwraca względny URL z get_absolute_url
- robots.txt renderuje SITE_URL z settings przez TemplateView context

## Ograniczenia (z zadania)
- NIE modyfikować views.py, urls.py poza dodaniem StaticSitemap/RobotsTxtView
- NIE ruszać templates/ poza robots.txt (równoległy agent)
