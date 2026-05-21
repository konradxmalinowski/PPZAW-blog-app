# Faza 6 — REST API (Django REST Framework)

Data: 2026-05-21

## Opis zadania

Zaimplementować pełne REST API dla DevLog z użyciem DRF. Endpointy dla postów,
komentarzy, kategorii, tagów oraz uzyskiwania tokenu uwierzytelniającego.

## Kryteria akceptacji

- `python manage.py check` — 0 issues
- `GET /api/posts/` — paginowana lista JSON (PageNumberPagination, PAGE_SIZE=10)
- `GET /api/posts/<slug>/` — szczegóły z komentarzami i similar_posts
- `POST /api/posts/` z tokenem — tworzy post (201)
- `DELETE /api/posts/<slug>/` bez autora — 403
- `GET /api/categories/`, `GET /api/tags/` — działają
- `POST /api/auth/token/` — zwraca token
- Permission `IsAuthorOrReadOnly` działa

## Pliki do utworzenia / modyfikacji

- `apps/api/serializers.py` (NOWY)
- `apps/api/permissions.py` (NOWY)
- `apps/api/views.py` (NADPISANY — scaffold)
- `apps/api/urls.py` (NOWY)
- `devlog/urls.py` (DODANIE jednej linii `path('api/', ...)`)

NIE modyfikować: `apps/blog/`, `apps/accounts/`.

## Kontrakt API

| Metoda | Ścieżka | Auth | Opis | Kod sukcesu |
|--------|---------|------|------|-------------|
| GET | /api/posts/ | brak | lista (search, ordering, tag, category) | 200 |
| POST | /api/posts/ | token | utwórz post | 201 |
| GET | /api/posts/<slug>/ | brak | szczegóły | 200 |
| PUT/PATCH | /api/posts/<slug>/ | author/admin | edycja | 200 |
| DELETE | /api/posts/<slug>/ | author/admin | usunięcie | 204 |
| GET | /api/posts/<slug>/comments/ | brak | komentarze aktywne | 200 |
| POST | /api/posts/<slug>/comments/ | auth | dodaj komentarz | 201 |
| GET | /api/categories/ | brak | kategorie | 200 |
| GET | /api/tags/ | brak | tagi z liczbą | 200 |
| POST | /api/auth/token/ | brak | uzyskaj token | 200 |

## Zmiany w DB

Brak. `rest_framework.authtoken` już zmigrowany (sprawdzić w check).

## Strategia obsługi błędów

DRF domyślnie zwraca ustrukturyzowany JSON (400/401/403/404). Nie eksponujemy
stack trace (DEBUG=True na dev, ale produkcja zwraca 500 bez detali). Walidacja
przez serializery DRF (typy, długości, wymagane pola).

## Uwagi techniczne (wykryte z kodu)

- `djangorestframework-taggit` NIE jest osobno zainstalowany, ale `taggit`
  6.1.0 zawiera własny moduł `taggit.serializers` z `TaggitSerializer` oraz
  `TagListSerializerField` — import ze spec działa.
- W taggit 6.1.0 `TaggableManager.set(tags)` przyjmuje LISTĘ, nie `*args`.
  Spec używa `post.tags.set(*tags)` — to stare API i jest BŁĘDNE dla >1 tagu.
  Poprawka: `instance.tags.set(tags)`.
- `Comment` nie ma managera `filter_active`. PostDetailSerializer używa
  `SerializerMethodField` filtrującego `comments.filter(active=True)`.
- Pagination jest globalna (REST_FRAMEWORK w base.py), więc listy są
  automatycznie paginowane — żadnej dodatkowej konfiguracji nie trzeba.

## Edge cases

- Post o statusie 'draft' — niewidoczny w API (queryset `Post.published`).
- Komentarz pod nieistniejącym/draft postem — 404.
- POST posta bez tagów — pusta lista tagów (required=False).
- similar_posts dla posta bez tagów — pusta lista.
- DELETE/PUT przez nie-autora niebędącego adminem — 403.
