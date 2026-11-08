---
name: szkola-klamala-dynamic-visual
description: Dynamic Visual Engine „Szkoła kłamała” – ruch, animacje, przejścia, efekty specjalne i kontrola jakości rolek (dynamiczny montaż w stylu serwisu informacyjnego i dokumentu śledczego, przy niezmienionej palecie i logo marki). Używaj zawsze, gdy rolka ma być bardziej dynamiczna, „mniej jak slajdy”, gdy dobierasz otwarcie pierwszych 2 sekund, przejścia, akcenty na liczbach, oś czasu, cytat albo fragment dokumentu, gdy dodajesz nowy efekt do silnika (ruch.py/render.py) albo sprawdzasz pierwsze 2 sekundy i przejścia przed wysłaniem rolki – także gdy Michał mówi tylko „popraw grafikę”, „więcej ruchu”, „efekty”, „żeby wyglądało profesjonalnie”.
---

# Dynamic Visual Engine – „Szkoła kłamała”

Brief Michała (8.11.2026): materiały mają wyglądać jak nowoczesna, dynamiczna produkcja medialna (serwis informacyjny + dokument śledczy + explainer), a nie prezentacja plansz. **Tożsamość marki zostaje:** paleta (granat #0A0E18→#16203A, niebieski #2F6BFF, żółty #FFC727, czerwony #E53935), logo, kroje Inter / Inter Display Black Italic, znak „SZKOŁA KŁAMAŁA”, strefy bezpieczne. Zmieniamy sposób użycia tych elementów: ruch, głębię, rytm.

Silnik to istniejąca fabryka – `.claude/skills/szkola-klamala-grafiki/scripts/ruch.py` (efekty, JS liczony deterministycznie klatka po klatce) i `render.py` (plansze, render 4K, muzyka). Nie twórz drugiej fabryki; nowe efekty dodawaj modułowo (sekcja 6).

## 1. Zasady, które chronią widza i markę

- **Haczyk czytelny od klatki 0.** Otwarcie może ruszać kamerą, światłem i ramkami, ale nie może zamazać ani wypchnąć tekstu z kadru w pierwszej klatce – widz decyduje w 1–2 s (pominięcia 73–96% na koncie). Dlatego np. „cięcie” to rozjazd linii PO klatce 0, a nie wjazd z boku.
- **Ruch z treści, nie dekoracja.** Oś czasu tylko przy datach i etapach, cytat tylko dosłowny, ramka wokół liczby, która jest stawką rolki. Agresywne efekty (wstrząs, stop-klatka) – raz, w ważnym punkcie.
- **Prawdziwe materiały.** Karta dokumentu i cytat pokazują wyłącznie dosłowny tekst ze źródła (ISAP/API Sejmu, dokument, nagranie), skróty oznaczone „(…)”, nazwa aktu i jednostki w nagłówku. Nigdy fikcyjnych dokumentów, zrzutów ekranu, nagłówków prasowych ani zdjęć udających autentyczne. Ilustracja AI – tylko jawnie jako ilustracja.
- **Co 2–4 s istotna zmiana wizualna:** wejście planszy → drugi akcent (~1,6–2,2 s po wejściu) → przejście. Kadr nigdy nie stoi (`"moc": "mocna"`).

## 2. Katalog modułów (pola specu)

Ustawiane automatycznie przez preset; nadpisanie: `"fx": {...}` w poście (cała rolka) albo w planszy.

| Moduł | Pole | Warianty |
|---|---|---|
| Otwarcie (plansza 1) | `fx.otwarcie` | `uderzenie`, `blysk`, `zoomout`, `ciecie`, `skan`, `ramka`, `kinowe` |
| Wejście nagłówków | `fx.naglowek` | `maska`, `litery`, `zoom`, `przesun` |
| Tekst i wyróżnienia | `fx.tresc` | `rozmycie`, `marker` |
| Wielka liczba | `fx.liczba` (+ `"count": true`) | `licznik`, `slot` |
| Akcent na liczbie | `fx.akcent` | `ramka` (celownik), `ostrosc` (przesunięcie ostrości) |
| Przekreślenie mitu | `fx.mit` | `kreska`, `pieczatka` |
| Przejście DO planszy | `fx.przejscie` | `smuga`, `zoom`, `paski`, `blysk`, `kierunek` (obrót kamery + rozmycie ruchu), `przeslona` (okrąg), `warstwy` (elementy z różną prędkością) |
| Zwrot akcji | `fx.zwrot` | `stop` (domyślnie przy tagu TWIST/ZWROT: błysk, przyciemnienie tła, najazd), `brak` |
| Tło | `fx.tlo`, `fx.swiatlo` | `kule`, `gwiazdy`, `siatka`, `3d`; smuga światła i oddychający gradient |
| Moc | `"moc"` | `mocna` (najazd kamery, puls na bicie, drugi akcent) / `spokojna` |

Plansze z ruchem informacyjnym (render.py):
- `timeline` – oś czasu: `"items": [{"rok": "0 h", "tekst": "…"}, …]` (2–4), linia rysuje się, punkty wskakują.
- `quote` – cytat: `"cytat"` (dosłowny, `**wyróżnienie**` dostaje marker), `"kto"`.
- `dokument` – odsłonięcie dokumentu: `"naglowek"` (np. „Konstytucja RP · art. 41 ust. 3”), `"tekst"` (dosłowny fragment z `**wyróżnieniem**`), `"linie"` (0–3 szare linie kontekstu); karta wjeżdża w perspektywie, marker przechodzi po wyróżnieniach.
- istniejące: `cover`, `number`, `text`, `myth`, `bars` (animowany wykres), `versus`, `quiz`, `outro`.

## 3. Dobór do treści (presety)

`ruch.PRESETY` wybiera otwarcia, przejścia i akcent według pola posta `"ton"` albo przedmiotu (`subject`); seria „SPÓR” = KONTROWERSJA. W obrębie presetu wybór jest deterministyczny (hash id rolki), więc dwie rolki o tym samym temacie zaczynają się różnie.

| Preset | Charakter | Typowe plansze |
|---|---|---|
| PRAWO / POLITYKA | ramka, skan, kino; przejścia kierunkowe i warstwy | `dokument`, `quote`, `number` z ramką |
| HISTORIA | skan, kino; przesłona | `timeline`, `dokument` |
| NAUKA / KOSMOS | zoomout, kino, błysk; przesłona, zoom | `number` z `ostrosc`, `bars` |
| KONTROWERSJA | cięcie, uderzenie, ramka; kierunek, warstwy | `myth` z TWIST (stop-klatka), `versus` |
| CIEKAWOSTKA | zoomout, błysk, kino | `number`, `bars` |

Mapy i znaczniki lokalizacji: jeszcze nie ma modułu – dodawaj dopiero z prawdziwymi danymi geograficznymi (np. kontury z otwartych danych), nigdy „na oko”.

## 4. Dźwięk

Każdy efekt zgłasza zdarzenie (`start`, `uderzenie`, `pieczatka`, `marker`, `tik`, `pop`, `przejscie`…) do `<id>_zdarzenia.json`; `muzyka.py` układa pod nie efekty dźwiękowe i tnie plansze na bit. Nowy efekt = nowe zdarzenie istniejącego typu, żeby dźwięk zgrał się bez zmian w muzyce. Lektor (opcja) ma pierwszeństwo – podkład jest pod nim przyciszany.

## 5. Kontrola jakości (przed każdą wysyłką i po każdej zmianie silnika)

1. Render (podgląd szybciej: `--hd`; produkcja 4K przez `dostawa.py`).
2. `python3 .claude/skills/szkola-klamala-dynamic-visual/scripts/kontrola.py <rolka>_muzyka.mp4 [--przed <stara>.mp4]` → `_2s.jpg`, `_przejscia.jpg`, `_przed_po.jpg`; obejrzyj narzędziem Read.
3. Sprawdź: haczyk czytelny w KAŻDEJ klatce 0–2 s; nic nie wychodzi poza kadr i strefy UI; ramki i wyróżnienia nie zostają „w powietrzu” w przejściach; brak migotania; logo na końcu; −14 LUFS.
4. Jeśli efekt nie jest wyraźnie lepszy od poprzedniej wersji – popraw, nie wysyłaj.

## 6. Jak dodać nowy efekt (modułowo)

1. `ruch.py`: dopisz wariant do `WARIANTY` (i do odpowiednich `PRESETY`), keyframes do `css()`, logikę wejścia w `PREP` (gałąź w pętli elementów) albo ruch ciągły w `window.__setT` (czas lokalny `t`, globalny `g`).
2. Efekt zależny od czasu licz z `t` (deterministycznie), nie z `Date`/losowości – ten sam spec musi dać ten sam film.
3. Nowy typ planszy: szablon w `render.py → tpl()`, CSS w `css(f)`, klasy tekstu dopisz do skalowania w `FIT_AND_QA`.
4. Test: `specs/demo_silnik/demo.json` (wszystkie moduły), `specs/demo_silnik/otwarcia.json` (7 otwarć) + `kontrola.py`. Demo nigdy nie idzie do publikacji.

## 7. Ograniczenia (stan 8.11)

- 30 kl./s (60 kl./s podwaja czas renderu 4K).
- Bez map, wycinków prasowych i zdjęć z paralaksą – wymagają prawdziwych materiałów źródłowych; moduły do dodania, gdy będą dane.
- Opacity elementów sterowanych animacją CSS nie da się nadpisać w przejściu „warstwy” – pracuje tam przesunięcie i rozmycie.
