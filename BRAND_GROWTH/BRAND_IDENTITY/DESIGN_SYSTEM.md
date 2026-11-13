# System projektowy (stan silnika 13.11.2026)

## Płótno i strefy
- Rolka i TikTok: 2160×3840 (układ 1080×1920 CSS ×2); TikTok dostaje plik 1080×1920. Karuzela IG 4:5: 2160×2700.
- Strefy bezpieczne 9:16: góra 250 px, dół 430 px, prawo 150 px (w układzie 1080). Nic ważnego poza nimi.

## Klocki (typy plansz `render.py`)
| Typ | Rola | Uwagi |
|---|---|---|
| cover | haczyk + obraz + pieczątka | żółta/ciemna na zmianę; z `tlo3d` zawsze ciemna |
| number | jedna wielka liczba | `count: true` tylko dla czystej liczby |
| myth | mit przekreślony → fakt | TWIST: czerwona poświata, pola `myth`/`fact` |
| dokument | dosłowny cytat z markerem | ≤ 18 słów, `wskaz` jako dopisek |
| wycinek | dosłowny nagłówek agencji | ≤ 20 słów, data, bez logo |
| versus | dwie kolumny | SCHOOL VS REALITY, BEFORE/AFTER |
| bars | słupki/ranking | TOP 5, porównania |
| timeline | oś czasu | DOCUMENTARY, DARK HISTORY |
| mapa | kontury + punkty | Polska, Europa, świat |
| foto | zdjęcie z podpisem licencji | `ramka` albo `pelny` z paralaksą |
| quote | cytat osoby/instytucji | zawsze ze źródłem |
| quiz | pytanie + opcje + odliczanie | INTERACTIVE |
| text / hero | zdanie albo ogromna liczba | oddech między planszami |
| outro | pytanie + żółty przycisk „Wyślij” + źródła | pytanie o ocenę zasady |

## Ruch (`ruch.py`)
- `"moc": "mocna"`: kadr nigdy nie stoi, puls na bicie. Presety wg `"ton"` (otwarcie, przejścia, akcent).
- Zasady: jedno wejście prowadzi, reszta dołącza z opóźnieniem ≤ 0,3 s; stop-klatka na zwrocie; marker rysuje się po przeczytaniu zdania; nie więcej niż 2 rodzaje przejść w rolce.
- Tempo czytania: 0,3 s na słowo + zapas; silnik sam wydłuża planszę. Cel rolki 20–26 s.

## Dźwięk
Podkład generowany w kodzie + efekty zsynchronizowane (uderzenie na zwrocie i na logo), −14 LUFS. TikTok: wersja z efektami + dźwięk z trendów dodany w aplikacji.

## Kontrola
`kontrola.py` + arkusz klatek z GOTOWEGO wideo (pierwsza klatka, zwrot, outro). Lista z sekcji 8 skilla `brand-growth-director`.

## Luki systemu (do `CREATIVE_LAB/VISUAL_INNOVATIONS.md`)
Brak: napisów słowo w słowo bez plansz (styl „talking captions”), sceny pełnoekranowego zdjęcia z kinetycznym tekstem, animowanego wykresu liniowego, przejścia „z dokumentu w liczbę”, okładki ze zdjęciem.
