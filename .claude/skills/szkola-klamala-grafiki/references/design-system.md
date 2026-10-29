# System wizualny „Szkoła kłamała”

Źródłem stylu jest logo Michała: białe i żółte pędzlowe litery, niebieskie smugi, czerwone podkreślenie i złota poświata na czarnym tle. Wszystko poniżej przekłada logo na siatkę, która pozostaje spójna w setkach postów.

## Kolory (tokeny w `TOK` w render.py)

| Token | Wartość | Użycie |
|---|---|---|
| bg0 / bg1 | `#0A0E18` / `#16203A` | tło: gradient radialny, jaśniejszy środek u góry |
| blue | `#2F6BFF` | smugi, cień nagłówków, etykiety FAKT/ZA, słupki |
| yellow | `#FFC727` | akcent: druga linia nagłówka, liczby, wyróżnienia, „przesuń” |
| red | `#E53935` | pędzel pod nagłówkiem, MIT/PRZECIW, skreślenie mitu, odpowiedź fałszywa |
| text | `#E8E8E8` | tekst ciągły (kontrast ok. 15:1 do tła) |
| muted | `#9AA3B5` | źródła, notki, handle |

Dlaczego tak mało kolorów: przy kilkuset postach każdy dodatkowy kolor rozmywa rozpoznawalność siatki profilu. Żółty działa tylko wtedy, gdy jest rzadki.

## Typografia

- Nagłówki: **Inter Display Black Italic**, wersaliki, lekko ujemny odstęp, twardy niebieski cień `0 7px 0` (nawiązanie do warstw logo). `text-wrap: balance` wyrównuje długość linii.
- Treść: **Inter Regular**, interlinia 1,32–1,38, `text-wrap: pretty` (bez pojedynczych słów w ostatniej linii).
- Skala 4:5: H1 118 / H2 74 / treść 44 / notka 30 / duża liczba 210. Skala 9:16: H1 124 / H2 86 / treść 54 / notka 34 / liczba 250.
- Minimum czytelności (QA): treść ≥ 36 px na 4:5 i ≥ 44 px na 9:16. Telefon wyświetla post w ok. 1/3 rozdzielczości, więc mniejsze litery przestają być czytelne w ruchu.

## Siatka i strefy bezpieczne

- 4:5 (1080×1350): margines 88 px, treść między 150 a 1200 px wysokości, pasek marki u góry, handle i „przesuń →” u dołu.
- 9:16 (1080×1920): treść w pasie 250–1490 px, lewy margines 90 px, prawy 150 px. Instagram i TikTok zasłaniają górę (nazwa konta, pasek postępu), dół (podpis, dźwięk, opis) i prawą krawędź (serce, komentarze, udostępnij).
- Treść jest wyśrodkowana pionowo w strefie bezpiecznej, quiz wyrównany do góry, żeby klatki odliczania się nie przesuwały.

## Elementy stałe

- Znak „SZKOŁA **KŁAMAŁA**” w lewym górnym rogu na slajdach wewnętrznych (na okładce zastępuje go etykieta przedmiotu).
- Kropki postępu zamiast „3/7”: dyskretne i czytelne na miniaturze.
- Pędzel (SVG o nierównych brzegach) pod nagłówkami okładki i outro, czyli czerwone podkreślenie z logo.
- Etykiety pochylone o −8°: żółta (przedmiot), czerwona (MIT/PRZECIW), niebieska (FAKT/ZA).
- Tło: gradient + 4 rozmyte smugi pod kątem −24° + winieta + delikatne ziarno 7%. Ziarno usuwa „plastikowy” efekt czystego gradientu i ogranicza pasy kompresji w JPEG i H.264.
- Karty (`versus`): półprzezroczyste, zaokrąglenie 22 px, cienka jasna ramka, miękki cień.

## Dodawanie nowego typu slajdu

Dodaj gałąź w `tpl()` w render.py, korzystając z istniejących klas (`chip`, `tag`, `h2`, `body`, `big`, `card`, `src`), żeby nowy typ dziedziczył skalę i strefy. Nowych kolorów nie dodawaj. Wyrenderuj `examples/przyklad.json` z nowym slajdem i sprawdź QA na obu formatach.
