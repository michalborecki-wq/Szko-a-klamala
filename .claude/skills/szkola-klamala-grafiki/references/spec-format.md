# Format pliku JSON (spec)

```json
{
  "handle": "@szkola_klamala",
  "posts": [ { …post… }, { …post… } ]
}
```

## Post

| Pole | Wymagane | Opis |
|---|---|---|
| `id` | tak | Nazwa plików, np. `pon_kosmos_wenus` (bez spacji i polskich znaków). |
| `format` | tak | `carousel` (1080×1350, Instagram), `vertical` (1080×1920, TikTok-zdjęcia / Stories) albo `reel` (plansze 1080×1920 + MP4). |
| `vertical_copy` | nie | Tylko przy `carousel`: `true` = dorób natywną wersję 9:16 dla TikToka (pliki `<id>_916_NN.jpg`). |
| `series` | nie | Domyślnie `SZKOŁA KŁAMAŁA`. Dla sporu: `SPÓR TYGODNIA`, dla quizu: `QUIZ W PIĄTEK`. |
| `subject` | tak | Przedmiot wersalikami: `HISTORIA`, `KOSMOS`, `PRAWO`, `MOTORYZACJA`, `MEDYCYNA`, `FINANSE`… |
| `durations` | przy `reel` | Lista sekund na planszę (tyle elementów, ile slajdów). |
| `animate` | nie | Tylko `reel`: domyślnie `true` – animowane napisy w MP4; `false` = prosty pokaz plansz. |
| `muzyka` | nie | Tylko `reel`: `{}` = podkład i efekty dźwiękowe dobrane do przedmiotu; `{"nastroj": "kosmos|elektro|napiecie|lekki|spokojny", "bpm": 110}` nadpisuje. Obecność pola włącza cięcia na bicie. |
| `fx` | nie | Tylko `reel`: nadpisanie wariantów efektów dla całej rolki (lista w skillu `szkola-klamala-animacje`); to samo pole w slajdzie – dla jednej planszy. |
| `slides` | tak | Lista slajdów (niżej). |

Pliki wynikowe: `<id>_NN.jpg` (4:5), `<id>_916_NN.jpg` (9:16), `<id>_reel_NN.jpg` + `<id>.mp4`, podglądy `_podglad_<id>_<format>.jpg`, raport `qa_report.txt`.

## Formatowanie tekstu w każdym polu

- `**tekst**` → żółte wyróżnienie (liczby, słowa-klucze; maks. 1–2 na slajd),
- `\n` → nowa linia (rzadko potrzebne – szablon sam łamie tekst),
- twarde spacje po jednoliterowych wyrazach i przed jednostkami dodają się automatycznie,
- nie wpisuj HTML – zostanie pokazany jako tekst.

## Typy slajdów i pola

**cover** – `title`, `accent` (żółta druga linia), `sub`, opcjonalnie `note`.
```json
{"type": "cover", "title": "5 mitów o kosmosie,", "accent": "w które wierzysz", "sub": "Ostatni zaskakuje najbardziej."}
```

**hero** – `big` (1–4 znaki: liczba/słowo), `title`, `accent`, `sub`, `source`. Wyśrodkowany.
```json
{"type": "hero", "big": "12", "title": "stref czasowych", "accent": "ma Francja", "sub": "Więcej niż Rosja i USA.", "source": "timeanddate.com"}
```

**myth** – `myth` (przekreślony), `fact`, opcjonalnie `num` („01”), `source`, `myth_label`/`fact_label` (domyślnie MIT/FAKT).
```json
{"type": "myth", "num": "01", "myth": "Na ISS nie ma grawitacji.", "fact": "Jest – ok. **90%** ziemskiej.", "source": "NASA"}
```

**number** – `big` (do ~9 znaków), `title`, `accent`, `body`, opcjonalnie `tag` (`FAKT`/`MIT`/`ZA`/`PRZECIW`), `note`, `source`.

**text** – `title`, `accent`, `body`, opcjonalnie `tag`, `note`, `source`.

**versus** – `side` (`za`/`przeciw`), `label` (np. „ZA: OWOC”), `title`, `accent`, `body` (w karcie), `source`.

**bars** – `title`, `accent`, opcjonalnie `body` (1 zdanie nad wykresem), `rows`: lista `[etykieta, wartość_liczbowa, opis_wartości]`, `label_width` (px, domyślnie 240), `note`, `source`. Wartości liczbowe policz w kodzie przed wpisaniem.
```json
{"type": "bars", "title": "Ranking", "rows": [["Francja", 12, "12"], ["Rosja", 11, "11"], ["USA", 11, "11"]], "label_width": 200}
```

**quiz** – `options` (2–4 zdania), `question` (napis w etykiecie, domyślnie „KTÓRY FAKT JEST FAŁSZYWY?”), `countdown` (3/2/1 – duża cyfra pod opcjami), `reveal` (indeks fałszywej odpowiedzi od 0 – podświetla ją na czerwono, resztę przyciemnia, etykieta robi się czerwona). W klatkach odliczania podawaj identyczne `options`, żeby nic nie skakało w wideo.

Pola animacji (każdy slajd Reela, opcjonalne): `count` (`false` = duża liczba nie odlicza się od zera, np. przy roku „1569”), `enter` (`false` = plansza bez wejścia napisów; ustawiane automatycznie dla klatek odliczania i rozwiązania quizu).

**outro** – `question` (otwarte pytanie), `sub`, `sources` („Źródła: …”), `partner_slot` (domyślnie `true` – puste miejsce na logo partnera).

## Typowe układy

- **Karuzela „Mit vs fakt” (7):** cover → 5× myth (z `num`) → outro.
- **Karuzela „wyjaśniam” (6–8):** cover → number (drugi haczyk) → 2–4× text/bars → outro.
- **Spór tygodnia (8):** cover (`series: "SPÓR TYGODNIA"`) → number (kontekst) → 2× versus za → 2× versus przeciw → text (`tag: "ŹRÓDŁA"`, „Co mówią źródła”) → outro.
- **Reel „jeden mit” (min. 4 plansze, min. 20 s; zwykle 5–6 plansz):** cover (mit jako haczyk) → myth (FAKT z liczbą) → number (drugi fakt) → text (skąd mit / jak sprawdzono) → outro (pytanie + źródła, `partner_slot: false`). `durations: [2.6, 4.4, 4.2, 4.4, 4.4, 3.8]`, `muzyka: {}`.
- **Reel „Quiz w piątek”:** cover → quiz → quiz `countdown` 3 → 2 → 1 → quiz `reveal` (+ opcjonalnie text z wyjaśnieniem). `durations: [2.4, 3.0, 1, 1, 1, 4.0]`.
- **TikTok zdjęcia (4):** hero lub cover → 2× text/number → outro; `format: "vertical"`.
