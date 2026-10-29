---
name: szkola-klamala-animacje
description: Animowane rolki „Szkoła kłamała” (@szkola_klamala) z oryginalną muzyką i efektami dźwiękowymi – kinetyczna typografia na poziomie profesjonalnego motion designera z biblioteką zróżnicowanych efektów (litery, zoom, marker, licznik-bandyta, pasek postępu, pieczątka MIT, iskry, wstrząs, tła gwiazdy/siatka/kule, przejścia smuga/zoom/paski/błysk), cięcia na bicie, rozmycie ruchu. Używaj ZAWSZE, gdy trzeba zrobić lub poprawić rolkę, Reel, film, wideo, animację, „ruszające się napisy”, muzykę albo dźwięk do rolki dla „Szkoła kłamała” – także przy „zrób z tego rolkę”, „ożyw te slajdy”, „wersja wideo”, „dodaj muzykę”. Wygląd plansz opisuje szkola-klamala-grafiki, napisy do nagranej mowy – szkola-klamala-napisy, montaż nagrań – szkola-klamala-montaz.
---

# Animacje i muzyka „Szkoła kłamała”

Rolka ma wyglądać i brzmieć, jakby zrobił ją profesjonalny motion designer: urozmaicone efekty z jednej palety marki, tekst zawsze czytelny, haczyk od pierwszej klatki, cięcia na bicie muzyki, dźwięk podkreślający każde ważne zdarzenie na ekranie.

Silnik: `.claude/skills/szkola-klamala-grafiki/scripts/render.py` + biblioteka ruchu `ruch.py` (ten sam katalog). Muzyka: `scripts/muzyka.py` w tym skillu. Treść i fakty – `CLAUDE.md`; wygląd plansz – `szkola-klamala-grafiki`.

## Jak pracować

1. Rozpisz Reel w JSON (`format: "reel"`, pola: `szkola-klamala-grafiki/references/spec-format.md`) i dodaj `"muzyka": {}` (nastrój i tempo dobiorą się same z przedmiotu). Typowy „jeden mit”: `cover` → `myth` albo `number` → `text`/`number`, `durations: [2.6, 4.4, 4.4]` – silnik dociągnie je do pełnych uderzeń tempa.
2. Szybki podgląd: `render.py spec.json --out out --video --draft` → arkusz klatek (`szkola-klamala-montaz/scripts/klatki.py out/<id>.mp4 --times …`) → Read. Poprawiaj treść, `durations`, ewentualnie `fx`.
3. Wersja finalna z muzyką – jedno polecenie:
   ```bash
   python3 .claude/skills/szkola-klamala-grafiki/scripts/render.py spec.json --out out --video --muzyka
   ```
   Wynik: `<id>_muzyka.mp4` (gotowy do publikacji, −14 LUFS), `<id>_efekty.mp4` (same efekty dźwiękowe – gdy Michał woli dźwięk z trendów TikToka), `<id>_zdarzenia.json` (oś czasu), okładka `<id>_reel_01.jpg`.
4. Zasada nr 8: obejrzyj gotowy film (arkusz klatek w momentach: 0 s, środek wejść, każde przejście, lądowanie liczby, koniec) i sprawdź raport głośności. Dopiero potem wyślij.

## Biblioteka efektów (`ruch.py`)

Każda rolka dostaje **inną kombinację** (wybór deterministyczny z `id` rolki – ten sam spec = ten sam film), a każda plansza inny wariant niż poprzednia. Paleta ruchów jest jedna – marka zostaje spójna, a widz nie widzi dwa razy tego samego.

| Grupa (`fx`) | Warianty | Co widać |
|---|---|---|
| `haczyk` (plansza 1) | `uderzenie`, `blysk` | tytuł widoczny od klatki 0; lekkie uderzenie skali albo połysk przelatujący przez litery |
| `naglowek` | `maska`, `litery`, `zoom`, `przesun` | słowa spod linii / litery spadają z obrotem / słowa z rozmytego zbliżenia / wjazd z pochyleniem |
| `tresc` | `rozmycie`, `marker` | słowa z rozmycia do ostrości; `**wyróżnienie**` zapala się na żółto albo dostaje żółty marker |
| `liczba` | `licznik`, `slot` | odliczanie od zera albo cyfry kręcące się jak w jednorękim bandycie; przy `%` pasek postępu; przy lądowaniu iskry, błysk i wstrząs kadru |
| `mit` | `kreska`, `pieczatka` | czerwone przekreślenie; dodatkowo pieczątka „MIT” wbijana obok etykiety ze wstrząsem |
| `tlo` | `gwiazdy`, `siatka`, `kule` | wg przedmiotu: KOSMOS – gwiazdy z paralaksą; nauki ścisłe i finanse – perspektywiczna siatka; reszta – dryfujące światła; zawsze wielki konturowy napis (liczba albo przedmiot) |
| `przejscie` | `smuga`, `zoom`, `paski`, `blysk` | pierwsze cięcie zawsze markową smugą, kolejne rotują |

Nadpisanie: `"fx": {...}` w poście (cała rolka) albo w slajdzie (jedna plansza), np. `"fx": {"mit": "pieczatka", "przejscie": "paski"}`. Używaj, gdy treść czegoś wymaga (np. pieczątka przy bardzo znanym micie), nie dla zasady.

Zasady: jeden wariant na grupę na planszy; nie dokładaj efektów spoza biblioteki (3D, glitch, emoji, odbicia) – nowy efekt najpierw dopisz do `ruch.py` w stylu marki, sprawdź na arkuszu klatek i dopiero wtedy używaj.

## Muzyka i dźwięk (`muzyka.py`)

- **Oryginalny podkład generowany w kodzie** – bez praw autorskich osób trzecich, bez ryzyka wyciszenia. Nigdy nie wgrywaj cudzych MP3.
- Nastrój i tempo wg przedmiotu (`ruch.NASTROJ_PRZEDMIOTU`): `kosmos` 92 BPM (pad, dzwonki z echem), `elektro` 120 (nauki ścisłe, motoryzacja), `napiecie` 100 (historia, Spór tygodnia), `lekki` 120 (pozostałe, quiz), `spokojny` 90 (finanse, ekonomia, prawo). Nadpisanie: `"muzyka": {"nastroj": "...", "bpm": 110}`.
- Struktura: plansza 1 startuje uderzeniem i lżejszym rytmem, od planszy 2 pełny rytm; **każde cięcie na bicie**, przed nim narastanie, na nim świst + talerz + niskie „boom”.
- Efekty z osi zdarzeń animacji: uderzenie (liczba ląduje), stuk pieczątki, „szur” przekreślenia, marker, delikatne „pop” etykiet, tik odliczania quizu, buczek złej odpowiedzi. Uderzenia na moment ściszają podkład (ducking), więc są wyraźne.
- Miks pod telefon: subbas przycięty (głośniki telefonu nie grają < 80 Hz), −14 LUFS, szczyt ≤ −1,5 dBTP.
- Wersja `_efekty.mp4` jest celowo cichsza – gdy Michał dodaje dźwięk z trendów w aplikacji, efekty zostają pod spodem.

## Tempo i czytelność

- Napisy wchodzą w ok. 0,8–1,6 s, **potem tekst stoi** – ok. 0,25 s na słowo + 1 s zapasu. QA ostrzega, gdy plansza jest za krótka.
- Haczyk ok. 2,5 s, fakt 4–4,5 s, puenta 4–4,5 s. Cały „jeden mit”: 9–12 s.
- Liczby, które nie powinny się odliczać (rok „1958”, numer „01”), oznacz `"count": false`.
- Ostatnia plansza nie ma wyjścia – film zapętla się do haczyka.

## Lista kontrolna przed oddaniem

- Klatka 0: haczyk czytelny, bez pustego ekranu i bez logo na start.
- Nic nie jest ucięte ani zasłonięte (ogonki ą/ę, poświata, pieczątka nie wchodzi na tekst, tła nie konkurują z tekstem).
- Każdy tekst stoi wystarczająco długo, by przeczytać go dwa razy.
- Przejście w pełni zakrywa cięcie.
- Strefa bezpieczna 9:16 (góra 250, dół 430, prawo 150 px).
- Raport: 1080×1920, 30 kl./s, dźwięk, −14 LUFS ±1, szczyt ≤ −1 dB.
- Wysyłaj Michałowi jeden MP4 na rolkę (ten sam na IG i TikTok) + okładkę; opis IG i TikTok w blokach do skopiowania.

## Lektor (opcjonalnie)

`scripts/lektor.py` (Piper TTS, głos `mc_speech`, pole `"lektor"` w slajdach) zostaje jako opcja, ale **domyślnie rolki mają muzykę, nie lektora** (decyzja Michała). Gdy Michał nagra własny głos – to montaż (`szkola-klamala-montaz`).
