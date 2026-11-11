# Głęboka analiza 11.11.2026 – dlaczego rolki są przewijane i co zmieniono

Dane: Composio (`INSTAGRAM_GET_IG_MEDIA_INSIGHTS`, tylko odczyt), 11.11 ok. 20:30. Tylko Instagram (Facebook – ponad 90% wyświetleń – jest niewidoczny w API). Małe próbki: traktować jako sygnał.

| Data | Haczyk | Wyśw. IG | Pominięcia w 3 s | Śr. czas |
|---|---|---|---|---|
| 11.11 wiecz. | „+51 km/h na krajówce i 3 miesiące pieszo.” | 38 | **97%** | 1,2 s |
| 11.11 rano | „Wielkiego Muru nie widać z Księżyca. Szkoła kłamała.” (tło wideo) | 5 | 66,7% | 7,7 s |
| 10.11 wiecz. | „„Pilny komunikat skarbówki” to nie kara. To telefon.” | 9 | 77,8% | 2,9 s |
| 10.11 rano | „500 zł miesięcznie przez 30 lat to nie 180 tys. zł.” | 36 | 91,4% | 3,4 s |
| 9.11 wiecz. | „Mandat? Możesz powiedzieć „nie”.” | 6 | 100% | 1,2 s |
| 9.11 rano | „ZUS daruje 315 mln zł. Jest haczyk.” | 109 | **66,3%** | 3,8 s |

Wszystkie: 0 udostępnień, 0 zapisów.

## Diagnoza

1. **Haczyk – wzór zwycięzców i przegranych (17 rolek z 9.11 + 6 nowych).**
   - Trzyma (≤ 75% pominięć): znany PODMIOT + wielka kwota/liczba + otwarta pętla – „ZUS daruje 315 mln zł. Jest haczyk.”, „2000 zł mandatu. Połowa – bezprawnie”, obalenie zdania, które każdy zna ze szkoły – „Wielkiego Muru nie widać z Księżyca”, „Francja ma 12 stref”.
   - Przegrywa (≥ 90%): żargon i symbole w 1. linii („+51 km/h na krajówce”), pytanie na początku („Mandat?”), zdanie, które trzeba policzyć („500 zł … to nie 180 tys.”), sucha reguła bez stawki („Kontroluje Cię policjant tej samej płci”).
   - **Reguła:** haczyk ≤ 7 słów, zaczyna się od podmiotu znanego każdemu (ZUS, policja, mandat, szkoła, bank, sąsiad), ma jedną liczbę albo jedno zaprzeczenie i kończy się otwartą pętlą („Jest haczyk.”, „Połowa – bezprawnie.”, „Szkoła kłamała.”). Bez znaków „+”, skrótów i gwary kierowców w 1. linii.
2. **Pierwsza klatka – wszystkie okładki wyglądały tak samo.** Zestawienie 6 ostatnich pierwszych klatek: to samo ciemne tło, mała płaska ikona, napis średniej wielkości, ok. 40% kadru puste. W feedzie Facebooka (skąd jest ponad 90% wyświetleń) rolka wygląda jak „ta sama co wczoraj” → przewinięcie w 1 s.
3. **Środek rolki – małe litery na pustym, ciemnym tle.** Plansza zwrotu akcji (najważniejszy moment) była szarym, drobnym przekreślonym tekstem. Outro – zwykły tekst; wezwanie „wyślij komuś” niewidoczne (0 udostępnień od początku konta).
4. **Długość.** Rolka 11.11 wyszła 39 s (cytat przepisu 32 słowa). Cel 20–24 s.
5. **Tło wideo** (Mur, 11.11 rano) – najdłuższy średni czas na koncie (7,7 s), ale przy 5 wyświetleniach; do potwierdzenia.

## Zmiany wprowadzone 11.11 (silnik `render.py`, obowiązują od rolki 12.11)

- **Okładki na zmianę: żółta / ciemna** (automatycznie, gdy rolka nie ma tła wideo i spec nie podaje `"uklad"`) – pierwsza klatka przestaje być „tą samą rolką”.
- **Tekst rośnie, aż wypełni kadr** (do ×1,45) – koniec z planszami w połowie pustymi.
- **TWIST na czerwono**: mit dużym, przekreślonym grubą czerwoną linią krojem nagłówka; fakt dużym białym tekstem z żółtym markerem; czerwona poświata tła i czerwone smugi.
- **Kolor niesie znaczenie**: plansza z liczbą – niebieska poświata, zwrot – czerwona, outro – jaśniejszy niebieski.
- **Outro**: pytanie krojem nagłówka + żółty przycisk „➤ Wyślij komuś, kto…” (wezwanie obrazem, nie tylko w opisie).
- Zakres liczb i liczba z jednostką nie łamią się między wierszami („51–60 km/h”, „1500 zł”).

## Reguły scenariusza (dopisane do `docs/agent/lekcje.md`)

- Haczyk wg wzoru z pkt 1; karta 20 pkt – haczyk niespełniający wzoru = max 12 pkt (nie przechodzi).
- Cytat w `dokument` ≤ 18 słów; plansza ≤ 12 słów; rolka 20–26 s.
- Zwrot akcji zawsze jako `myth` (`myth`/`fact`), najpóźniej na 3. planszy z 5.
- Co druga rolka z tłem wideo (zasoby AI z etykietą) – pomiar: śr. czas vs rolki bez tła.
- Pomiar co 3 dni tym samym układem tabeli; cel etapowy: pominięcia < 75% w 3 rolkach z rzędu.
