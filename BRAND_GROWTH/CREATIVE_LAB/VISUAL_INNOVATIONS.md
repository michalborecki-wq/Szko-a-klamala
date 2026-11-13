# Innowacje wizualne – kolejka (priorytet = efekt / koszt)

Zasada premium: w jednej rolce najwyżej 1 nowy efekt i 2 rodzaje przejść. Wszystko w palecie i krojach marki.

| # | Pomysł | Do jakiego formatu | Jak (narzędzie) | Koszt | Status |
|---|---|---|---|---|---|
| V1 | **Kinetyczna typografia słowo po słowie** na pełnym kadrze (bez „planszy”) | CINEMATIC, POV, FAST | nowy typ `kinetyk` w `render.py`/`ruch.py` (słowa wjeżdżają w rytmie, kluczowe żółte i większe) | 2–3 h kodu | do zrobienia – najwyższy priorytet |
| V2 | **Okładka ze zdjęciem** (PD/CC) + pas żółty z haczykiem | DARK, DOC, CINEMATIC | `foto` jako cover (`uklad: pelny`) | 1–2 h | do zrobienia |
| V3 | **Animowany wykres liniowy / licznik rosnący w czasie** | EXPLAINER, BA | SVG `stroke-dashoffset` w `ruch.py` | 2 h | do zrobienia |
| V4 | **Przejście „dokument → liczba”**: zaznaczona fraza odkleja się i rośnie do wielkiej liczby | NEWS, DOC | wspólny element między planszami | 3 h | pomysł |
| V5 | **Podział ekranu góra/dół** „W SZKOLE / NAPRAWDĘ” z suwakiem | SVR, BA | wariant `versus` pionowy | 1–2 h | do zrobienia |
| V6 | **Mapa z trasą/zasięgiem** (Polska na tle Europy, puls punktu) | TOP, DOC, EXPLAINER | `mapa` + nowe punkty; ewentualnie `remotion-maps` | 1 h (silnik) | gotowe w silniku – nieużywane |
| V7 | **Tekstura papieru/akt** pod planszą-dokumentem (teczka, spinacz, stempel daty) | NEWS, DOC | CSS + SVG | 1 h | do zrobienia |
| V8 | **Subtelny glitch/RGB** tylko na słowie-kłamstwie w micie | MYTH | preset `rgb` zawężony do `.myth` | 30 min | do zrobienia |
| V9 | **Sceny 3D przedmiotu** (Blender, 5 s pętla) jako czołówka serii | serie | skill `szkola-klamala-3d` | ok. 40 min renderu na scenę | po wyborze serii |
| V10 | **Czołówka serii 1 s** (dżingiel + znak serii) | Co może policja, Śledztwo, Szkoła kłamała #N | `ruch.py` + `muzyka.py` | 2 h | do zrobienia |

Nieużywane możliwości silnika (zero kosztu – wdrożyć w planie rotacji): `quiz`, `bars`, `versus`, `timeline`, `mapa`, `foto`, `quote`, `wycinek`.
