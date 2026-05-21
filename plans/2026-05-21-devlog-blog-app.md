# Plan: DevLog — Blog „Cykl Tworzenia Aplikacji Webowej"

**Data:** 2026-05-21  
**Status:** Planowanie — zatwierdzone decyzje 2026-05-21  
**Temat bloga:** Cykl tworzenia aplikacji webowej (każdy post = jeden etap cyklu)  
**UI:** Terminal hybrid — wygląd terminala (ASCII-box, monospace, dark) + normalna nawigacja  

### Zatwierdzone decyzje projektowe
| # | Pytanie | Decyzja |
|---|---|---|
| 1 | Editor postów | **WYSIWYG** — django-markdownx (podgląd Markdown w czasie rzeczywistym) |
| 2 | Rejestracja | **Prosta** — bez weryfikacji email, konto aktywne od razu |
| 3 | RSS feed | **Per-category** — osobny feed dla każdej kategorii + jeden globalny |
| 4 | API write-access | **Tak** — `POST /api/posts/` i `PUT/PATCH/DELETE` dla zalogowanych autorów |

---

## 1. Streszczenie projektu

Aplikacja to w pełni funkcjonalny blog developerski o tematyce **cyklu tworzenia aplikacji webowej**. Każdy post dokumentuje jeden etap procesu: od planowania i wyboru tech-stacku, przez implementację backendu i frontendu, po deployment i monitoring.

Blog jest „na full wypasiony":
- terminal-style UI z ASCII-box kartami, monospace fontem i pseudopromptami
- System kont użytkowników (rejestracja, login, profil)
- Komentarze, tagi, kategorie, polecane posty
- Wysyłanie postów przez e-mail
- Wyszukiwanie pełnotekstowe
- RSS feed + XML sitemap
- REST API (Django REST Framework)
- Panel administracyjny

Materiał źródłowy: dokumenty `blog cz. I.docx` + `blog II.docx` (kurs Django).

---

## 2. Stos technologiczny

| Warstwa | Technologia |
|---|---|
| Język | Python 3.11+ |
| Framework | Django 4.2 LTS |
| Baza danych | SQLite (dev) → PostgreSQL (prod-ready) |
| Tagi | django-taggit 5.x |
| API | djangorestframework 3.15+ |
| Obrazy | Pillow |
| Markdown/WYSIWYG | django-markdownx (edytor + podgląd) + bleach (sanityzacja output) |
| Zmienne środowiskowe | python-decouple |
| Email | Django SMTP backend (konsola na dev) |
| RSS/Sitemap | django.contrib.syndication + sitemaps |
| Wyszukiwanie | Q-objects + icontains (SQLite) / SearchVector (Postgres) |
| CSS | Własny terminal.css (zero dependencji JS frameworków) |
| JS | Vanilla JS — typing effect, cursor blink, smooth scroll |
| Font | JetBrains Mono (CDN) lub system monospace fallback |

---

## 3. Struktura projektu

```
devlog/
├── devlog/                     ← konfiguracja projektu Django
│   ├── settings/
│   │   ├── base.py             ← wspólne ustawienia
│   │   ├── local.py            ← SQLite, DEBUG=True, email konsola
│   │   └── production.py       ← PostgreSQL, DEBUG=False, SMTP
│   ├── urls.py                 ← główny router URL
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── blog/                   ← core: posty, komentarze, tagi
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── feeds.py            ← RSS
│   │   ├── sitemaps.py
│   │   ├── templatetags/
│   │   │   └── blog_tags.py    ← custom template tags
│   │   └── migrations/
│   │
│   ├── accounts/               ← użytkownicy i profile
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── migrations/
│   │
│   └── api/                    ← REST API (DRF)
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── permissions.py
│
├── static/
│   ├── css/
│   │   └── terminal.css        ← terminal theme
│   ├── js/
│   │   └── terminal.js         ← typing effect, cursor blink
│   └── fonts/                  ← JetBrains Mono (opcjonalnie local)
│
├── media/                      ← przesyłane obrazy (cover images, avatary)
│
├── templates/
│   ├── base.html               ← terminal base layout
│   ├── partials/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   ├── pagination.html
│   │   └── sidebar.html        ← tag cloud, ostatnie posty, o autorze
│   ├── blog/
│   │   ├── post_list.html
│   │   ├── post_detail.html
│   │   ├── post_share.html
│   │   ├── post_search.html
│   │   └── category_list.html
│   └── accounts/
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       └── edit_profile.html
│
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
│
├── .env.example
├── .env                        ← gitignore
├── manage.py
└── README.md
```

---

## 4. Modele danych

### 4.1 `blog.Category`
```python
class Category(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color       = models.CharField(max_length=7, default='#7ee787')  # terminal accent
```

### 4.2 `blog.Post`
```python
class Post(models.Model):
    STATUS = [('draft', 'Draft'), ('published', 'Published')]

    title        = models.CharField(max_length=250)
    slug         = models.SlugField(max_length=250, unique_for_date='publish')
    author       = models.ForeignKey(User, on_delete=CASCADE, related_name='blog_posts')
    category     = models.ForeignKey(Category, on_delete=SET_NULL, null=True, related_name='posts')
    body         = models.TextField()                       # Markdown
    excerpt      = models.TextField(max_length=500, blank=True)
    cover_image  = models.ImageField(upload_to='posts/%Y/%m/', blank=True)
    tags         = TaggableManager()                        # django-taggit
    publish      = models.DateTimeField(default=timezone.now)
    created      = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)
    status       = models.CharField(max_length=10, choices=STATUS, default='draft')
    reading_time = models.PositiveIntegerField(default=0)   # auto-obliczany (save signal)

    objects   = models.Manager()
    published = PublishedManager()
```

### 4.3 `blog.Comment`
```python
class Comment(models.Model):
    post    = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    user    = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    name    = models.CharField(max_length=80)
    email   = models.EmailField()
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)
```

### 4.4 `accounts.UserProfile`
```python
class UserProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=CASCADE, related_name='profile')
    bio        = models.TextField(max_length=500, blank=True)
    avatar     = models.ImageField(upload_to='avatars/', blank=True)
    github_url = models.URLField(blank=True)
    website    = models.URLField(blank=True)
    # Auto-tworzony przez post_save signal na User
```

---

## 5. Widoki i URL-e

### 5.1 Aplikacja `blog`

| URL | Widok | Nazwa | Opis |
|---|---|---|---|
| `/` | `PostListView` (CBV) | `post_list` | Strona główna – lista opublikowanych postów |
| `/tag/<slug:tag_slug>/` | `post_list` (FBV) | `post_list_by_tag` | Posty filtrowane po tagu |
| `/category/<slug:cat_slug>/` | `CategoryPostListView` | `post_list_by_category` | Posty filtrowane po kategorii |
| `/author/<str:username>/` | `AuthorPostListView` | `post_list_by_author` | Posty danego autora |
| `/<int:year>/<int:month>/<int:day>/<slug:post>/` | `post_detail` | `post_detail` | Szczegóły posta |
| `/<int:post_id>/share/` | `post_share` | `post_share` | Formularz wysyłania posta emailem |
| `/search/` | `post_search` | `post_search` | Wyszukiwarka |
| `/feed/` | `LatestPostsFeed` | `post_feed` | RSS feed |

### 5.2 Aplikacja `accounts`

| URL | Widok | Nazwa | Opis |
|---|---|---|---|
| `/accounts/register/` | `register` | `register` | Rejestracja |
| `/accounts/login/` | `LoginView` (Django) | `login` | Logowanie |
| `/accounts/logout/` | `LogoutView` (Django) | `logout` | Wylogowanie |
| `/accounts/profile/` | `profile` | `profile` | Profil zalogowanego użytkownika |
| `/accounts/profile/edit/` | `edit_profile` | `edit_profile` | Edycja profilu |
| `/accounts/<str:username>/` | `public_profile` | `public_profile` | Publiczny profil autora |

### 5.3 Aplikacja `api`

| Endpoint | Metoda | Opis |
|---|---|---|
| `/api/` | GET | API root (DRF browsable) |
| `/api/posts/` | GET | Lista opublikowanych postów |
| `/api/posts/<slug>/` | GET | Szczegóły posta |
| `/api/posts/<slug>/comments/` | GET, POST | Komentarze posta (POST wymaga auth) |
| `/api/tags/` | GET | Lista tagów |
| `/api/categories/` | GET | Lista kategorii |
| `/api/posts/` | POST | Tworzenie posta (wymaga auth + rola author/admin) |
| `/api/posts/<slug>/` | PUT, PATCH | Edycja posta (tylko własne lub admin) |
| `/api/posts/<slug>/` | DELETE | Usunięcie posta (tylko własne lub admin) |
| `/api/auth/token/` | POST | Pobranie tokenu auth (DRF TokenAuth) |

### 5.4 System i inne

| URL | Opis |
|---|---|
| `/admin/` | Panel Django Admin |
| `/sitemap.xml` | XML sitemap (django.contrib.sitemaps) |
| `/robots.txt` | Robots.txt (prosty widok TemplateView) |

---

## 6. Formularze

| Formularz | Klasa bazowa | Pola | Zastosowanie |
|---|---|---|---|
| `EmailPostForm` | `forms.Form` | name, email, to, comments | Wysyłanie posta emailem |
| `CommentForm` | `forms.ModelForm(Comment)` | name, email, body | Dodawanie komentarza (auto-fill z usera) |
| `SearchForm` | `forms.Form` | query | Wyszukiwanie pełnotekstowe |
| `RegisterForm` | `UserCreationForm` | username, email, password1, password2 | Rejestracja |
| `UserProfileForm` | `forms.ModelForm(UserProfile)` | bio, avatar, github_url, website | Edycja profilu |

---

## 7. Custom Template Tags (`blog/templatetags/blog_tags.py`)

| Tag/Filter | Typ | Opis |
|---|---|---|
| `{% get_recent_posts count=5 %}` | inclusion_tag | Widget: ostatnie posty w sidebarze |
| `{% get_most_commented count=5 %}` | inclusion_tag | Widget: najkomentowansze posty |
| `{% get_tag_cloud %}` | inclusion_tag | Chmura tagów z wagami (Count) |
| `{% markdown body %}` | filter | Konwersja Markdown → HTML (+ bleach sanitize) |
| `{% reading_time body %}` | filter | Szacowany czas czytania w minutach |

---

## 8. RSS Feed i Sitemap

### RSS (`blog/feeds.py`) — globalny + per-category
```python
class LatestPostsFeed(Feed):
    title       = "DevLog — Cykl tworzenia aplikacji webowej"
    link        = "/feed/"
    description = "Najnowsze wpisy o tworzeniu aplikacji webowych"

    def items(self):
        return Post.published.order_by('-publish')[:10]

class CategoryFeed(Feed):
    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)

    def title(self, obj):
        return f"DevLog — kategoria: {obj.name}"

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self, obj):
        return Post.published.filter(category=obj).order_by('-publish')[:10]
```

**URL-e feedów:**
- `/feed/` — globalny
- `/feed/category/<slug>/` — per-category

### Sitemap (`blog/sitemaps.py`)
```python
class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority   = 0.9

    def items(self):
        return Post.published.all()
```

---

## 9. Wyszukiwanie pełnotekstowe

**Dev (SQLite)** — Q-objects:
```python
from django.db.models import Q

results = Post.published.filter(
    Q(title__icontains=query) |
    Q(body__icontains=query) |
    Q(excerpt__icontains=query) |
    Q(tags__name__icontains=query)
).distinct()
```

**Prod (PostgreSQL)** — SearchVector:
```python
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
search_query  = SearchQuery(query)
results = Post.published.annotate(
    search=search_vector,
    rank=SearchRank(search_vector, search_query)
).filter(search=search_query).order_by('-rank')
```

Przełączanie przez ustawienie `USE_POSTGRES_SEARCH = True` w `settings/production.py`.

---

## 10. REST API — serializery

```python
# api/serializers.py

class TagSerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.SerializerMethodField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = ['id', 'name', 'body', 'created']
        read_only_fields = ['id', 'created']

class PostListSerializer(serializers.ModelSerializer):
    tags     = TagSerializer(many=True)
    category = CategorySerializer()
    author   = serializers.StringRelatedField()

    class Meta:
        model  = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 'tags',
                  'excerpt', 'publish', 'reading_time']

class PostDetailSerializer(PostListSerializer):
    body_html       = serializers.SerializerMethodField()
    similar_posts   = PostListSerializer(many=True)
    comments_count  = serializers.IntegerField(source='comments.count')

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['body_html', 'similar_posts', 'comments_count']

class PostWriteSerializer(serializers.ModelSerializer):
    """Używany przy POST/PUT/PATCH — przyjmuje Markdown w polu body."""
    tags = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model  = Post
        fields = ['title', 'category', 'body', 'excerpt', 'cover_image', 'tags',
                  'publish', 'status']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(*tags)
        return post
```

**Uprawnienia API (permissions.py):**
- `IsAuthenticatedOrReadOnly` — domyślne dla wszystkich endpoints
- `IsAuthorOrReadOnly` — własny permission: edycja/usunięcie tylko przez autora posta lub admina

---

## 11. Terminal UI — System Designu

### 11.1 Paleta kolorów

| Token | Hex | Zastosowanie |
|---|---|---|
| `--bg` | `#0d1117` | Tło strony |
| `--bg-card` | `#161b22` | Tło kart/komponentów |
| `--bg-border` | `#30363d` | Obramowania ASCII-box |
| `--text-primary` | `#c9d1d9` | Tekst główny |
| `--text-secondary` | `#8b949e` | Metadane, daty, opisy |
| `--accent-green` | `#7ee787` | Komendy, nagłówki, akcenty |
| `--accent-blue` | `#79c0ff` | Linki, nazwy tagów |
| `--accent-yellow` | `#d29922` | Ostrzeżenia, kategorie |
| `--accent-red` | `#f85149` | Błędy, status draft |
| `--accent-purple` | `#bc8cff` | Autorzy, tagi specjalne |

### 11.2 Typografia

```css
font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
font-size: 15px;
line-height: 1.65;
```

### 11.3 Mockupy komponentów ASCII

**Nawigacja (navbar):**
```
┌─────────────────────────────────────────────────────────────────┐
│  [~] devlog$ _          [HOME] [POSTY] [TAGI] [SZUKAJ] [login]  │
└─────────────────────────────────────────────────────────────────┘
```

**Karta posta (post_list):**
```
┌─[ POST #042 ]────────────────────────────────────────────────────┐
│                                                                  │
│  > Konfiguracja środowiska Django i virtualenv                   │
│    ─────────────────────────────────────────────                 │
│    📁 setup  ·  @jan_kowalski  ·  2024-01-15  ·  ~4 min         │
│    Tagi: #django  #python  #setup  #backend                      │
│                                                                  │
│    Lorem ipsum dolor sit amet, consectetur adipiscing...         │
│    tworzyć izolowane środowisko Pythona za pomocą...             │
│                                                                  │
│    [>> CZYTAJ DALEJ ]                                            │
└──────────────────────────────────────────────────────────────────┘
```

**Szczegóły posta (breadcrumb + header):**
```
~/blog/posty/2024/01/15/konfiguracja-django$ cat post.md
────────────────────────────────────────────────────
  Konfiguracja środowiska Django i virtualenv
  autor: @jan_kowalski | 2024-01-15 | ████░░ 4 min
────────────────────────────────────────────────────
```

**Pasek wyszukiwania:**
```
┌─[ SZUKAJ ]─────────────────────────────────────────┐
│  $ grep -r "_" ./posts/                            │
└────────────────────────────────────────────────────┘
```

**Sekcja komentarzy:**
```
┌─[ KOMENTARZE (3) ]────────────────────────────────┐
│                                                   │
│  >> anna_dev @ 2024-01-16 10:23                   │
│  ┊  Świetny artykuł! Bardzo pomocne...            │
│                                                   │
│  >> marek_123 @ 2024-01-17 08:45                  │
│  ┊  Miałem problem z virtualenv na Windows...     │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Sidebar — tag cloud:**
```
┌─[ TAG CLOUD ]──────────────────┐
│  #django [12]  #python [9]     │
│  #api [7]  #setup [5]          │
│  #deployment [4]  #testing [3] │
└────────────────────────────────┘
```

**Footer:**
```
────────────────────────────────────────────────────────────
  devlog v1.0  |  RSS  |  sitemap  |  [GitHub]  |  2024
  "Code is poetry, and the terminal is its stage."
────────────────────────────────────────────────────────────
```

### 11.4 Efekty JS (minimalne, vanilla)

- **Blinking cursor**: `::after` pseudo-element z CSS animation (`blink 1s step-end infinite`)
- **Typing effect**: nagłówek na homepage wpisuje się litera po literze (opcjonalne, max 500ms)
- **Highlight on hover**: karty lekko jaśnieją przy hover (CSS transition `background-color`)
- **ASCII progress bar**: czas czytania jako `████░░░░ 4 min`

---

## 12. Panel administracyjny (Django Admin)

```python
# blog/admin.py

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display   = ('title', 'category', 'author', 'publish', 'status', 'reading_time')
    list_filter    = ('status', 'category', 'created', 'publish', 'author')
    search_fields  = ('title', 'body', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields  = ('author',)
    date_hierarchy = 'publish'
    ordering       = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display   = ('name', 'email', 'post', 'created', 'active')
    list_filter    = ('active', 'created', 'updated')
    search_fields  = ('name', 'email', 'body')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
```

---

## 13. Fazy implementacji

### Faza 1 — Core blog (fundament z dokumentów)
1. Setup projektu Django: `devlog/`, split settings, `.env`
2. Model `Category` + migracja
3. Model `Post` (rozszerzony względem doc 1) + `PublishedManager` + signal `reading_time`
4. Admin dla `Post` i `Category`
5. Widoki: `post_list` (CBV ListView), `post_detail`
6. URL-e + `get_absolute_url()`
7. Szablony: `base.html` + `post_list.html` + `post_detail.html`
8. Stronicowanie (`pagination.html`)
9. Terminal CSS (podstawowy)

### Faza 2 — Email + komentarze + tagi (z dokumentów)
10. `EmailPostForm` + widok `post_share` + szablon `post_share.html`
11. Model `Comment` + `CommentForm` + integracja w `post_detail`
12. django-taggit: integracja, filtrowanie po tagu, tag URL
13. Podobne posty (`Count` aggregation)
14. Admin dla `Comment`

### Faza 3 — Rozszerzenia bloga
15. Custom template tags: `get_recent_posts`, `get_most_commented`, `get_tag_cloud`
16. Sidebar (`partials/sidebar.html`)
17. Filter Markdown: `{{ post.body|markdown }}`
18. Widoki po kategorii i autorze

### Faza 4 — System kont
19. Model `UserProfile` + `post_save` signal
20. Formularze: `RegisterForm`, `UserProfileForm`
21. Widoki: `register`, `login`/`logout` (Django built-in), `profile`, `edit_profile`, `public_profile`
22. Integracja komentarza z zalogowanym userem (auto-fill name/email)

### Faza 5 — Wyszukiwanie
23. `SearchForm` + widok `post_search`
24. Implementacja SQLite (Q-objects)
25. Szablon wyników wyszukiwania

### Faza 6 — RSS + Sitemap
26. `LatestPostsFeed` (django.contrib.syndication)
27. `PostSitemap` + `CategorySitemap` (django.contrib.sitemaps)
28. `robots.txt` (TemplateView)

### Faza 7 — REST API (DRF)
29. Instalacja DRF, konfiguracja w `settings`
30. Serializers: Tag, Category, Comment, PostList, PostDetail
31. Views: `PostListAPIView`, `PostDetailAPIView`, `CommentListCreateAPIView`
32. URL-e API
33. Token authentication
34. Pagination w API

### Faza 8 — Terminal UI dopieszczenie
35. Pełny `terminal.css` z wszystkimi tokenami
36. `terminal.js`: cursor blink, ASCII progress bar
37. Responsywność (mobile terminal look)
38. Dark theme consistency w Admin (opcjonalnie: django-jazzmin)

---

## 14. Zależności (requirements/base.txt)

```
Django>=4.2,<5.0
django-taggit>=5.0
djangorestframework>=3.15
Pillow>=10.0
django-markdownx>=4.0
bleach>=6.0
python-decouple>=3.8
```

```
# requirements/local.txt
-r base.txt
django-debug-toolbar>=4.0
```

```
# requirements/production.txt
-r base.txt
psycopg2-binary>=2.9
gunicorn>=21.0
whitenoise>=6.5
```

---

## 15. Zmienne środowiskowe (.env.example)

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_SETTINGS_MODULE=devlog.settings.local

# Database (tylko dla produkcji)
DATABASE_URL=postgresql://user:password@localhost/devlog

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Media
MEDIA_ROOT=/path/to/media
```

---

## 16. Przykładowe posty (plan treści bloga)

| # | Tytuł | Kategoria | Tagi | Opis |
|---|---|---|---|---|
| 1 | Planowanie aplikacji webowej — od pomysłu do szkicu | Planowanie | #planning #requirements #ux | Zbieranie wymagań, wireframy, wybór stacku |
| 2 | Konfiguracja środowiska Django i virtualenv | Setup | #django #python #setup | virtualenv, pip, startproject |
| 3 | Projektowanie modeli danych w Django | Backend | #django #orm #models | Model Post, relacje, migracje |
| 4 | Django Admin — panel zarządzania treścią | Backend | #django #admin | ModelAdmin, customizacja |
| 5 | Widoki i URL-e — routing w Django | Backend | #django #views #urls | FBV vs CBV, path(), namespace |
| 6 | System szablonów Django | Frontend | #django #templates #html | Dziedziczenie, bloki, filtry |
| 7 | Formularze Django — wysyłanie, walidacja | Backend | #django #forms #validation | Form, ModelForm, CSRF |
| 8 | System komentarzy — ModelForm w praktyce | Backend | #django #comments #forms | commit=False, relacje FK |
| 9 | Tagowanie postów z django-taggit | Backend | #django #taggit #packages | Integracja paczek zewnętrznych |
| 10 | Django REST Framework — API dla bloga | API | #drf #api #rest | Serializers, ViewSets, auth |
| 11 | Wyszukiwanie pełnotekstowe w Django | Backend | #django #search #postgresql | Q objects, SearchVector |
| 12 | Deployment aplikacji Django | Deployment | #deployment #gunicorn #nginx | Gunicorn, Nginx, collectstatic |

---

## 17. Kryteria akceptacji (Definition of Done)

- [ ] Wszystkie modele mają migracje i są zarejestrowane w admin
- [ ] Strona główna wyświetla listę postów ze stronicowaniem (3 per page)
- [ ] Szczegóły posta: treść Markdown, komentarze, podobne posty, tagi
- [ ] Formularz komentarza działa (walidacja, CSRF)
- [ ] Formularz wysyłania posta emailem działa
- [ ] Filtrowanie po tagu, kategorii i autorze
- [ ] Rejestracja i logowanie użytkownika
- [ ] Profil publiczny autora
- [ ] Wyszukiwanie zwraca sensowne wyniki
- [ ] RSS feed zwraca poprawny XML
- [ ] `/sitemap.xml` zawiera wszystkie posty
- [ ] API endpoints zwracają JSON (GET /api/posts/, GET /api/posts/\<slug\>/)
- [ ] UI jest spójny terminalowo (dark bg, monospace, ASCII-box karty)
- [ ] Terminal CSS nie psuje się na mobile (min 320px)
- [ ] Brak błędów w Django debug toolbar (brak N+1 queries)
- [ ] Admin panel jest w pełni skonfigurowany dla wszystkich modeli
- [ ] `python manage.py check` przechodzi bez błędów

---

## 18. Następne kroki

Po zatwierdzeniu planu, implementacja pójdzie w kolejności faz (1→8).

Każda faza = osobne zadanie do delegacji do `fullstack-orchestrator`.

**Wszystkie pytania rozstrzygnięte — plan gotowy do implementacji.**

Kolejny krok: `implement-feature Faza 1 — Core blog (setup projektu, modele, widoki, szablony)`
