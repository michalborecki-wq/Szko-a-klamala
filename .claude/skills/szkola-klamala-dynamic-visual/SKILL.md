---
name: szkola-klamala-dynamic-visual
description: Dynamic Visual Engine „Szkoła kłamała” – ruch, animacje, przejścia, efekty specjalne (RGB, światło, głębia 2.5D, najazd na dokument, wskazanie szczegółu, wycinki agencji PAP/Reuters, zdjęcia na wolnych licencjach z paralaksą) i kontrola jakości rolek z pomiarami (dynamiczny montaż w stylu serwisu informacyjnego i dokumentu śledczego, przy niezmienionej palecie i logo marki). Używaj zawsze, gdy rolka ma być bardziej dynamiczna, „mniej jak slajdy”, gdy dobierasz otwarcie pierwszych 2 sekund, przejścia, akcenty na liczbach, oś czasu, cytat albo fragment dokumentu, gdy dodajesz nowy efekt do silnika (ruch.py/render.py) albo sprawdzasz pierwsze 2 sekundy i przejścia przed wysłaniem rolki – także gdy Michał mówi tylko „popraw grafikę”, „więcej ruchu”, „efekty”, „żeby wyglądało profesjonalnie”, „dodaj wycinek z PAP/Reutersa”, „wstaw zdjęcie”, „skąd wziąć zdjęcie do rolki”.
---

# Dynamic Visual Engine – „Szkoła kłamała”

Brief Michała (8.11.2026): materiały mają wyglądać jak nowoczesna, dynamiczna produkcja medialna (serwis informacyjny + dokument śledczy + explainer), a nie prezentacja plansz. **Tożsamość marki zostaje:** paleta (granat #0A0E18→#16203A, niebieski #2F6BFF, żółty #FFC727, czerwony #E53935), logo, kroje Inter / Inter Display Black Italic, znak „SZKOŁA KŁAMAŁA”, strefy bezpieczne. Zmieniamy sposób użycia tych elementów: ruch, głębię, rytm.

Silnik to istniejąca fabryka – `.claude/skills/szkola-klamala-grafiki/scripts/ruch.py` (efekty, JS liczony deterministycznie klatka po klatce) i `render.py` (plansze, render 4K, muzyka). Nie twórz drugiej fabryki; nowe efekty dodawaj modułowo (sekcja 6).

## 1. Zasady, które chronią widza i markę

- **Haczyk czytelny od klatki 0.** Otwarcie może ruszać kamerą, światłem i ramkami, ale nie może zamazać ani wypchnąć tekstu z kadru w pierwszej klatce – widz decyduje w 1–2 s (pominięcia 73–96% na koncie). Dlatego np. „cięcie” to rozjazd linii PO klatce 0, a nie wjazd z boku.
- **Ruch z treści, nie dekoracja.** Oś czasu tylko przy datach i etapach, cytat tylko dosłowny, ramka wokół liczby, która jest stawką rolki. Agresywne efekty (wstrząs, stop-klatka) – raz, w ważnym punkcie.
- **Prawdziwe materiały.** Karta dokumentu i cytat pokazują wyłącznie dosłowny tekst ze źródła (ISAP/API Sejmu, dokument, nagranie), skróty oznaczone „(…)”, nazwa aktu i jednostki w nagłówku. Nigdy fikcyjnych dokumentów, zrzutów ekranu, nagłówków prasowych ani zdjęć udających autentyczne. Ilustracja AI – tylko jawnie jako ilustracja (`"ilustracja_ai": true` → etykieta „Ilustracja – nie jest zdjęciem wydarzenia”).
- **Wycinki i zdjęcia (decyzja Michała 9.11, wariant bez kosztów).** PAP (Polska) i Reuters (świat) to źródło faktów i nagłówków, **nie zdjęć** – obie agencje zastrzegają prawa, płatnej licencji nie kupujemy. „Wycinek” to nasza plansza z dosłownym, krótkim nagłówkiem (prawo cytatu, art. 29 pr. aut.), nazwą agencji zwykłym tekstem i datą – bez logo i layoutu agencji, link w opisie. Zdjęcia tylko na licencjach CC0, domena publiczna (np. NASA), CC BY, CC BY-SA – NC i ND odrzucamy (konto ma sponsorów, zdjęcie przycinamy i nakładamy grafikę); podpis: autor + licencja (+ serwis). Google Grafika z filtrem „Licencje Creative Commons” służy tylko do szukania – licencję potwierdza strona źródłowa.
- **Co 2–4 s istotna zmiana wizualna:** wejście planszy → drugi akcent (~1,6–2,2 s po wejściu) → przejście. Kadr nigdy nie stoi (`"moc": "mocna"`).

## 2. Katalog modułów (pola specu)

Ustawiane automatycznie przez preset; nadpisanie: `"fx": {...}` w poście (cała rolka) albo w planszy.

| Moduł | Pole | Warianty |
|---|---|---|
| Otwarcie (plansza 1) | `fx.otwarcie` | `uderzenie`, `blysk`, `zoomout`, `ciecie`, `skan`, `ramka`, `kinowe`, `rgb` (rozszczepienie czerwień/niebieski marki w 0 s, drugie uderzenie z „punchem” w 0,52 s, echo w 1,45 s) |
| Wejście nagłówków | `fx.naglowek` | `maska`, `litery`, `zoom`, `przesun` |
| Tekst i wyróżnienia | `fx.tresc` | `rozmycie`, `marker` |
| Wielka liczba | `fx.liczba` (+ `"count": true`) | `licznik`, `slot` |
| Akcent na liczbie | `fx.akcent` | `ramka` (celownik), `ostrosc` (przesunięcie ostrości) |
| Przekreślenie mitu | `fx.mit` | `kreska`, `pieczatka` |
| Przejście DO planszy | `fx.przejscie` | `smuga`, `zoom`, `paski`, `blysk`, `kierunek` (obrót kamery + rozmycie ruchu), `przeslona` (okrąg), `warstwy` (elementy z różną prędkością; ramka jedzie z warstwą), `swiatlo` (złote prześwietlenie jak poświata logo – mocne, maks. 1–2 na rolkę) |
| Zwrot akcji | `fx.zwrot` | `stop` (domyślnie przy tagu TWIST/ZWROT: błysk, przyciemnienie tła, najazd, rozszczepienie RGB), `brak` |
| Rozszczepienie RGB | `fx.rgb` | `true` w presetach KONTROWERSJA, MOTORYZACJA, POLITYKA – przy każdym uderzeniu liczby; gaśnie w ~0,3 s |
| Głębia 2.5D | `fx.glebia` | `true` przy `moc: mocna` – treść pochylona w perspektywie (≤1,4°, wolno), tło w przeciwną stronę (paralaksa), obraz-bohater okładki na bliższym planie (najeżdża szybciej niż tekst) |
| Tło | `fx.tlo`, `fx.swiatlo` | `kule`, `gwiazdy`, `siatka`, `3d`; smuga światła i oddychający gradient |
| Moc | `"moc"` | `mocna` (najazd kamery, puls na bicie, drugi akcent) / `spokojna` |

Plansze z ruchem informacyjnym (render.py):
- `timeline` – oś czasu: `"items": [{"rok": "0 h", "tekst": "…"}, …]` (2–4), linia rysuje się, punkty wskakują.
- `quote` – cytat: `"cytat"` (dosłowny, `**wyróżnienie**` dostaje marker), `"kto"`.
- `dokument` – odsłonięcie dokumentu: `"naglowek"` (np. „Konstytucja RP · art. 41 ust. 3”), `"tekst"` (dosłowny fragment z `**wyróżnieniem**`), `"linie"` (0–3 szare linie kontekstu); karta wjeżdża w perspektywie, marker przechodzi po wyróżnieniach, potem „kamera” najeżdża na wyróżnienie (najazd liczony tak, żeby karta została ≥50 px od krawędzi kadru). Opcjonalnie `"wskaz"` – etykieta 2–4 słowa (np. „Termin z Konstytucji”, „Tu jest kara”): żółta linia rysuje się z dolnej krawędzi karty pod wyróżnieniem do etykiety (wskazanie szczegółu, wypełnia pustą dolną część kadru). Etykieta to komentarz redakcji, nie cytat – nie może zmieniać sensu przepisu.
- `wycinek` – nagłówek agencji jako wycinek z gazety (papier, taśma, pochylenie): `"agencja"` (PAP | Reuters), `"data"`, `"naglowek"` (DOSŁOWNIE, `**wyróżnienie**`, maks. 20 słów), `"link"` (idzie do opisu, nie na planszę), opcjonalnie `"tlumaczenie"` (Reuters → „tłum. red.: …”), `"wskaz"`, `"tag"`, `"title"/"accent"`, `"source"` (domyślnie „Źródło: {agencja}, {data}”). Ruch jak `dokument` (wjazd w perspektywie, marker, najazd kamery, wskazanie). Brak agencji/daty/nagłówka/linku albo > 20 słów = błąd renderu. Nagłówek sprawdź na stronie artykułu; gdy strona blokuje pobieranie (pap.pl), tytuł z Google News + temat w drugim niezależnym źródle i dopisek „nagłówek z RSS” w `zrodla.md`.
- `foto` – zdjęcie na wolnej licencji: `"zdjecie"` (ścieżka względem repo, np. `zrodla/zdjecia/<slug>.jpg`; metadane z `<slug>.json` obok – robi je `VIRAL_REELS_FACTORY/narzedzia/zdjecia.py`), ręcznie `"autor"`, `"licencja"`, `"zrodlo"`, `"serwis"`; `"uklad"`: `ramka` (odbitka z taśmą, odsłonięcie maską + błysk) albo `pelny` (pełny kadr pod tekstem, zdjęcie min. 1600 px wysokości – inaczej silnik sam przełącza na ramkę). Ruch: dwie warstwy – tył rozmyty i wolny (1,08→1,14), przód ostry z maską i szybszy (1,00→1,10, przesuw) → głębia; razem z `fx.glebia`. Plus `"tag"`, `"title"/"accent"`, `"body"`. Brak autora/licencji/źródła albo licencja NC/ND = błąd renderu.
  - `zdjecia.py --commons "File:…"` (Wikimedia Commons: licencja z API, odrzuca NC/ND), `--nasa <nasa_id>` (images.nasa.gov, domena publiczna; zdjęcia z dopiskiem o prawach osób trzecich odrzuca), `--plik <jpg> --autor … --licencja … --zrodlo …` (gdy Michał pobierze sam). Zapisuje maks. 2400 px.
- istniejące: `cover`, `number`, `text`, `myth`, `bars` (animowany wykres), `versus`, `quiz`, `outro`.

## 3. Dobór do treści (presety)

`ruch.PRESETY` wybiera otwarcia, przejścia i akcent według pola posta `"ton"` albo przedmiotu (`subject`); seria „SPÓR” = KONTROWERSJA. W obrębie presetu wybór jest deterministyczny (hash id rolki), więc dwie rolki o tym samym temacie zaczynają się różnie.

| Preset | Charakter | Typowe plansze |
|---|---|---|
| PRAWO / POLITYKA | ramka, skan, kino (POLITYKA także rgb); przejścia kierunkowe, warstwy, światło | `dokument` z `wskaz`, `quote`, `number` z ramką |
| HISTORIA | skan, kino; przesłona, światło | `timeline`, `dokument` |
| NAUKA / KOSMOS | zoomout, kino, błysk; przesłona, zoom | `number` z `ostrosc`, `bars` |
| KONTROWERSJA | rgb, cięcie, uderzenie, ramka; kierunek, warstwy; RGB na uderzeniach | `myth` z TWIST (stop-klatka + RGB), `versus` |
| CIEKAWOSTKA | zoomout, błysk, kino | `number`, `bars` |

Mapy i znaczniki lokalizacji: jeszcze nie ma modułu (wycinki agencji i zdjęcia – plansze `wycinek` i `foto`, sekcja 2) – dodawaj dopiero z prawdziwymi danymi geograficznymi (np. kontury z otwartych danych), nigdy „na oko”.

## 4. Dźwięk

Każdy efekt zgłasza zdarzenie (`start`, `uderzenie`, `pieczatka`, `marker`, `tik`, `pop`, `przejscie`…) do `<id>_zdarzenia.json`; `muzyka.py` układa pod nie efekty dźwiękowe i tnie plansze na bit. Nowy efekt = nowe zdarzenie istniejącego typu, żeby dźwięk zgrał się bez zmian w muzyce. Lektor (opcja) ma pierwszeństwo – podkład jest pod nim przyciszany.

## 5. Kontrola jakości (przed każdą wysyłką i po każdej zmianie silnika)

1. Render (podgląd szybciej: `--hd`; produkcja 4K przez `dostawa.py`).
2. `python3 .claude/skills/szkola-klamala-dynamic-visual/scripts/kontrola.py <rolka>_muzyka.mp4 [--przed <stara>.mp4]` → `_2s.jpg`, `_przejscia.jpg`, `_przed_po.jpg` (obejrzyj narzędziem Read) oraz `_kontrola.json` z pomiarami: rozdzielczość, kl./s, ścieżka audio, migotanie poza przejściami, czarne klatki, najdłuższy nieruchomy kadr (limit 4 s), średni ruch całości i 0–2 s, LUFS (cel −14). Kod wyjścia 1 = „⚠ BŁĄD” – nie wysyłaj, popraw. Pomiar ruchu liczy jasność, więc efekty barwne (RGB) zaniża – porównuj go między wersjami tej samej rolki, nie jako ocenę estetyki.
3. Sprawdź: haczyk czytelny w KAŻDEJ klatce 0–2 s; nic nie wychodzi poza kadr i strefy UI; ramki i wyróżnienia nie zostają „w powietrzu” w przejściach; brak migotania; logo na końcu; −14 LUFS.
4. Jeśli efekt nie jest wyraźnie lepszy od poprzedniej wersji – popraw, nie wysyłaj.

## 6. Jak dodać nowy efekt (modułowo)

1. `ruch.py`: dopisz wariant do `WARIANTY` (i do odpowiednich `PRESETY`), keyframes do `css()`, logikę wejścia w `PREP` (gałąź w pętli elementów) albo ruch ciągły w `window.__setT` (czas lokalny `t`, globalny `g`).
2. Efekt zależny od czasu licz z `t` (deterministycznie), nie z `Date`/losowości – ten sam spec musi dać ten sam film.
3. Nowy typ planszy: szablon w `render.py → tpl()`, CSS w `css(f)`, klasy tekstu dopisz do skalowania w `FIT_AND_QA`.
4. Test: `specs/demo_silnik/demo.json` (stan 8.11), `specs/demo_silnik/demo_dve.json` (ta sama treść + moduły 9.11), `specs/demo_silnik/otwarcia.json` (otwarcia) + `kontrola.py --przed`. Demo nigdy nie idzie do publikacji.

## 7. Ograniczenia (stan 9.11)

- 30 kl./s (60 kl./s podwaja czas renderu 4K). Render demo 1080p z muzyką ok. 8 min na 42 s; 4K ok. 2–3× dłużej.
- Bez map – wymagają prawdziwych konturów z otwartych danych; moduł do dodania, gdy będą dane.
- Wikimedia Commons z chmury: metadane i licencja działają, ale pobieranie pliku z upload.wikimedia.org bywa blokowane (HTTP 429 dla wspólnego adresu IP chmury). Wtedy: zdjęcie z NASA (`--nasa`) albo Michał pobiera plik i agent dopisuje go przez `--plik` z danymi licencji ze strony Commons.
- pap.pl blokuje pobieranie stron automatem (Incapsula) – dosłowny nagłówek PAP bierzemy z Google News (tytuł strony), potwierdzenie treści z drugiego źródła.
- Opacity elementów sterowanych animacją CSS nie da się nadpisać w przejściu „warstwy” – pracuje tam przesunięcie i rozmycie.
- Otwarcie `rgb` nie jest „mocniejsze” od `ramka` w pomiarze ruchu 0–2 s (2,4 wobec 2,7) – daje inny bodziec w klatce 0 (kolorowy rozjazd), dlatego jest w rotacji tylko w presetach kontrowersji, motoryzacji i polityki, a nie zamiast ramki.

## 8. Historia zmian

- **9.11 (po południu)** – plansze `wycinek` (PAP/Reuters: dosłowny nagłówek na „papierze” z taśmą, walidacja pól i długości cytatu) i `foto` (zdjęcia CC0/PD/CC BY/CC BY-SA z podpisem; ramka albo pełny kadr, paralaksa dwóch warstw, walidacja licencji), narzędzie `zdjecia.py` (Commons, NASA, plik ręczny), kanały PAP i Reuters w porannym researchu (`zrodla_rss.json`, strony tagów PAP pomijane). Demo: `specs/demo_silnik/demo_wycinek_foto.json` (nagłówek PAP z 6.11, zdjęcie NASA AS17-148-22727). Poprawka błędu: wyróżnione słowo na jasnej karcie (`dokument`, `wycinek`) było niewidoczne przez ok. 0,8 s przed markerem (jasny kolor tekstu na jasnym papierze) – teraz `kMarkerDoc` trzyma ciemny tekst od początku.

- **9.11** – otwarcie `rgb`, przejście `swiatlo`, rozszczepienie RGB na uderzeniach i zwrocie, głębia 2.5D (pochylenie treści + paralaksa tła i obrazu-bohatera), najazd kamery na wyróżnienie w `dokument` z ograniczeniem do kadru, `wskaz` (linia od dokumentu do etykiety), ramka jedzie z warstwą w przejściu „warstwy” (wcześniej zostawała w powietrzu), pomiary automatyczne w `kontrola.py`. Demo: `specs/demo_silnik/demo_dve.json` (ta sama treść co `demo.json`). Wynik porównania: średni ruch całej rolki 1,03 → 1,32 (+28%), najdłuższy stojący kadr 0,43 s w obu, pusta dolna połowa planszy dokumentu wypełniona wskazaniem.
- **8.11** – pierwsza wersja (7 otwarć, presety, `dokument`, `timeline`, `quote`, stop-klatka, `kontrola.py`).
