# Instalacja i uruchomienie

## Wymagania

| Zależność | Wersja |
|-----------|--------|
| Python | 3.14+ |
| pip | najnowsza |
| Git | dowolna |

## Szybki start (dev)

```bash
# 1. Sklonuj repozytorium
git clone <repo-url>
cd DjangoProject

# 2. Utwórz środowisko wirtualne
python3.14 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 3. Zainstaluj zależności
pip install -r requirements/local.txt

# 4. Skonfiguruj środowisko
cp .env.example .env
# Edytuj .env — patrz docs/02-configuration.md

# 5. Zastosuj migracje (tworzy też superusera i przykładowe posty automatycznie)
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py migrate

# 6. Uruchom serwer
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py runserver
```

Aplikacja: **http://127.0.0.1:8000**  
Panel admina: **http://127.0.0.1:8000/admin**

---

## Zmienne środowiskowe

Plik `.env` — kopiuj z `.env.example`:

| Zmienna | Domyślnie (dev) | Opis |
|---------|-----------------|------|
| `SECRET_KEY` | — | Klucz Django (wymagany) |
| `DEBUG` | `True` | Tryb debugowania |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Dozwolone hosty |
| `SUPERUSER_USERNAME` | `admin` | Login superusera (tworzony automatycznie) |
| `SUPERUSER_EMAIL` | — | Email superusera |
| `SUPERUSER_PASSWORD` | — | Hasło superusera |
| `EMAIL_BACKEND` | smtp | Backend poczty |
| `EMAIL_HOST` | `smtp.gmail.com` | Serwer SMTP |
| `EMAIL_PORT` | `587` | Port SMTP |
| `EMAIL_HOST_USER` | — | Login SMTP |
| `EMAIL_HOST_PASSWORD` | — | App Password (Gmail) |
| `DEFAULT_FROM_EMAIL` | — | Adres nadawcy |
| `SITE_DEFAULT_OG_IMAGE` | — | Domyślny obraz OG (URL) |

### Gmail App Password

1. Wejdź na [myaccount.google.com](https://myaccount.google.com) → Bezpieczeństwo
2. Włącz weryfikację dwuetapową
3. Wygeneruj **App Password** dla aplikacji "DevLog"
4. Wklej 16-znakowy kod do `.env` jako `EMAIL_HOST_PASSWORD`

---

## Struktura katalogów

```
DjangoProject/
├── devlog/                  # Konfiguracja projektu
│   ├── settings/
│   │   ├── base.py          # Wspólne ustawienia
│   │   ├── local.py         # Dev (DEBUG=True, SQLite)
│   │   └── production.py    # Prod (HTTPS, HSTS, secure cookies)
│   └── urls.py
├── apps/
│   ├── blog/                # Posty, komentarze, tagi, kategorie, newsletter
│   │   ├── management/commands/backup_db.py
│   │   ├── profanity.py     # Filtr przekleństw
│   │   └── templatetags/blog_tags.py
│   ├── accounts/            # Rejestracja, logowanie, 2FA, profile
│   └── api/                 # DRF REST API
├── templates/               # Wszystkie szablony (nie w apps/)
│   ├── base.html
│   ├── partials/
│   ├── blog/
│   └── accounts/
├── static/
│   ├── css/terminal.css     # Terminal dark theme
│   └── js/terminal.js
├── backups/db/              # Backupy bazy danych (gitignored)
├── logs/                    # Logi aplikacji (gitignored)
├── docs/                    # Ta dokumentacja
└── reports/                 # Raporty security
```

---

## Testy

```bash
# Wszystkie testy
DJANGO_SETTINGS_MODULE=devlog.settings.local venv/bin/pytest -v

# Konkretna app
DJANGO_SETTINGS_MODULE=devlog.settings.local venv/bin/pytest apps/blog/tests/ -v
DJANGO_SETTINGS_MODULE=devlog.settings.local venv/bin/pytest apps/accounts/tests/ -v

# Z coverage
DJANGO_SETTINGS_MODULE=devlog.settings.local venv/bin/pytest --cov=apps -v
```

---

## Backup bazy danych

```bash
# Jednorazowy backup
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py backup_db

# Trzymaj tylko ostatnie 10
DJANGO_SETTINGS_MODULE=devlog.settings.local python manage.py backup_db --keep 10
```

Backupy zapisywane w `backups/db/db_YYYYMMDD_HHMMSS.sqlite3`.

---

## Logi

Logi zapisywane w `logs/`:
- `logs/django.log` — błędy aplikacji (WARNING+), rotacja 5 MB × 5 plików
- `logs/security.log` — zdarzenia security (INFO+), rotacja 5 MB × 10 plików
