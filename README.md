# DevLog

Blog dokumentujący cykl tworzenia aplikacji webowej w Django. Terminal-style UI, DRF REST API, system kont z 2FA, RSS, newsletter, moderacja.

## Dokumentacja

| Plik | Opis |
|------|------|
| [docs/01-setup.md](docs/01-setup.md) | Instalacja, zmienne środowiskowe, testy, backup, logi |
| [docs/02-architecture.md](docs/02-architecture.md) | Stack, modele danych, URL namespaces, middleware |
| [docs/03-security.md](docs/03-security.md) | Brute-force, rate limiting, 2FA, XSS, CSRF, audit log |
| [docs/04-api.md](docs/04-api.md) | REST API — endpointy, autoryzacja, przykłady curl |
| [docs/05-frontend.md](docs/05-frontend.md) | CSS design system, JS, dark/light mode, komponenty |
| [docs/06-features.md](docs/06-features.md) | Funkcje: komentarze, 2FA, newsletter, panel autora, moderacja |

## Szybki start

```bash
git clone <repo-url>
cd DjangoProject

python3.14 -m venv venv
source venv/bin/activate

pip install -r requirements/local.txt

cp .env.example .env
# Uzupełnij SECRET_KEY, SUPERUSER_* i EMAIL_* w .env

DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py migrate
# Superuser i przykładowe posty tworzone automatycznie

DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py runserver
```

Aplikacja: **http://127.0.0.1:8000** | Admin: **http://127.0.0.1:8000/admin**

Pełna instrukcja: [docs/01-setup.md](docs/01-setup.md)

## Stack

- Python 3.14, Django 5.2
- SQLite (dev) — PostgreSQL-ready
- Django REST Framework, django-taggit, django-markdownx
- pyotp (2FA TOTP), django-axes (brute-force), django-ratelimit, bleach (XSS)
- Terminal dark theme (własny CSS), JetBrains Mono, Vanilla JS

## Testy

```bash
DJANGO_SETTINGS_MODULE=devlog.settings.local venv/bin/pytest -v
```
