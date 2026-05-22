# Plan: Matrix UI Redesign

**Data:** 2026-05-22  
**Gałąź:** main

## Problem

Obecny UI jest zbyt terminalowy (ASCII-boxy ┌─┐│└─┘) i nieczytelny przy długich postach. Użytkownik chce zachować klimat Matrix (zielony na czarnym) ale z lepszą czytelnością.

## Acceptance criteria

1. Nowa paleta kolorów: ciemnozielone tło, jasna zielona czytelna treść, neonowy zielony dla akcentów
2. Usunięte ASCII pseudo-boxy z kart postów — zastąpione czystym borderem / subtle glow
3. Navbar, breadcrumby i prompt-style elementy POZOSTAJĄ terminalne
4. JetBrains Mono wszędzie, ale lepszy line-height i font-size dla treści postów
5. Spójne kolory we wszystkich komponentach (sidebar, formularze, komentarze, admin-bar)
6. `manage.py check` bez błędów, serwer startuje, strona wyświetla się poprawnie

## Nowa paleta CSS

```css
--bg:           #0a0f0a      /* tło strony — bardzo ciemna zieleń */
--bg-card:      #0f1a0f      /* tło kart */
--bg-border:    #1e3d1e      /* obramowanie */
--bg-hover:     #152615      /* hover na kartach */
--text-primary: #b5f0b5      /* tekst główny — czytelna jasna zieleń */
--text-secondary: #6db86d    /* tekst drugorzędny */
--text-muted:   #3d7a3d      /* tekst wyciszony / placeholder */
--accent-green: #00ff41      /* neonowy Matrix — nagłówki, akcenty */
--accent-lime:  #39d353      /* łagodniejszy zielony — hover, secondary */
--accent-link:  #58d68d      /* linki */
--accent-warn:  #ffd700      /* ostrzeżenia (złoty — kontrast na zielonym tle) */
--accent-error: #ff4444      /* błędy */
--glow-green:   0 0 8px rgba(0,255,65,0.3)   /* subtelny glow */
```

## Zmiany

### Tylko frontend (static/css/terminal.css + ewentualne mikrozmiany w szablonach)

1. **CSS variables** — podmień obecną paletę na nową Matrix
2. **Post cards** — usuń `::before` ASCII-box, zastąp `border: 1px solid var(--bg-border)` + `border-radius: 4px` + opcjonalny `box-shadow: var(--glow-green)` on hover
3. **Sidebar boxes** — tak samo: prosty border zamiast ASCII
4. **Typografia treści** — `.post-body` / `.post-content`: `font-size: 1rem`, `line-height: 1.8`, `letter-spacing: 0.01em`
5. **Navbar** — ZACHOWAĆ prompt style (`~/blog$`), tylko zmienić kolory na nową paletę
6. **Linki** — `var(--accent-link)` (#58d68d), hover: `var(--accent-green)` z glow
7. **Formularze / przyciski** — dopasować do nowej palety
8. **Komentarze** — dopasować kolory
9. **Focus/hover states** — glow zamiast zwykłego outline (ale utrzymać dostępność WCAG)
10. **Scrollbar** — custom matrix-green scrollbar (webkit)

## Warstwa

- Frontend only: `static/css/terminal.css`
- Możliwe drobne zmiany w szablonach (np. usunięcie hard-coded kolorów)

## Agent

**frontend-agent** — czysto CSS, brak zmian backendowych ani schematów

## Nie robimy

- Nie zmieniamy prompt/breadcrumb stylu w navbar
- Nie dodajemy nowych pakietów (czyste CSS)
- Nie dotykamy modeli / API / migracji
