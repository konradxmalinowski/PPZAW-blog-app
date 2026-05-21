# DevLog

Blog dokumentujący cykl tworzenia aplikacji webowej w Django. Terminal-style UI, DRF REST API, system kont użytkowników, RSS, sitemap.

## Wymagania

- Python 3.14+
- pip

## Uruchomienie (dev)

### 1. Sklonuj repozytorium

```bash
git clone <repo-url>
cd DjangoProject
```

### 2. Utwórz i aktywuj środowisko wirtualne

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements/local.txt
```

### 4. Skonfiguruj zmienne środowiskowe

```bash
cp .env.example .env
```

Edytuj `.env` — wystarczą wartości domyślne na dev (SQLite, email na konsolę).

### 5. Zastosuj migracje i utwórz superusera

```bash
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py migrate
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py createsuperuser
```

### 6. Uruchom serwer

```bash
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py runserver
```

Aplikacja dostępna pod: **http://127.0.0.1:8000**

Panel admina: **http://127.0.0.1:8000/admin**

---

## Adresy

| Adres | Opis |
|---|---|
| `/` | Lista postów |
| `/blog/<rok>/<mies>/<dzień>/<slug>/` | Szczegół posta |
| `/search/` | Wyszukiwarka |
| `/accounts/register/` | Rejestracja |
| `/accounts/login/` | Logowanie |
| `/accounts/profile/` | Profil użytkownika |
| `/api/` | REST API (DRF) |
| `/api/posts/` | Lista/tworzenie postów |
| `/api/auth/token/` | Token autoryzacyjny |
| `/sitemap.xml` | Sitemap XML |
| `/robots.txt` | Robots.txt |
| `/blog/feed/` | RSS (wszystkie posty) |
| `/admin/` | Panel administracyjny |

## REST API — szybki start

Uzyskaj token:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "twoj_user", "password": "twoje_haslo"}'
```

Utwórz post:

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Nowy post", "body": "Treść...", "status": "published"}'
```

## Testy

```bash
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py test apps.api
```

## Stack

- Python 3.14, Django 5.2
- django-taggit, djangorestframework, django-markdownx, Pillow, bleach, python-decouple
- SQLite (dev) — PostgreSQL-ready
- Terminal CSS (własny, dark #0d1117, JetBrains Mono)
