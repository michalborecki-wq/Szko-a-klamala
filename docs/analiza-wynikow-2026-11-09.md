# Analiza wyników Instagrama – 9.11.2026 (deep dive)

Dane: Composio, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` (tylko odczyt), 9.11 ok. 12:30. **Tylko Instagram** – wyświetlenia z Facebooka (crosspost, wg zrzutu 1.11 ponad 90% całości) API nie zwraca (`facebook_views` → błąd 400), więc liczby poniżej to mały wycinek zasięgu. Dla Policji #1 IG pokazuje 8 wyświetleń, a Michał widział ponad 2 tys. – reszta to Facebook.

| Data | Rolka | Szablon | Wyśw. IG | Zasięg IG | Śr. czas [s] | Pominięcia [%] |
|---|---|---|---|---|---|---|
| 9.11 rano | ZUS daruje 315 mln zł. Jest haczyk. | nowy styl DVE + `dokument` | 52 | 48 | 4.9 | 63.3 |
| 8.11 wiecz. | Pod szlabanem tracisz prawo jazdy | C | 41 | 39 | 1.6 | 94.9 |
| 8.11 rano | Mózg: 2% masy, 20% energii | B | 92 | 85 | 3.3 | 77.6 |
| 7.11 wiecz. | Saturn pływałby w wodzie | B | 43 | 41 | 3.5 | 82.5 |
| 7.11 rano | Kasyno nie oszukuje. Ma jedno zero. | B | 51 | 44 | 2.9 | 86.4 |
| 6.11 wiecz. | Wiatrówka vs broń czarnoprochowa | C (porównanie niesprawiedliwości) | 38 | 30 | 4.4 | 86.7 |
| 6.11 rano | Punkty karne zostają dłużej | C | 16 | 17 | 2.4 | 68.8 |
| 5.11 wiecz. | Policja #4 – kontrola osobista | C | 53 | 52 | 1.9 | 97.9 |
| 5.11 rano | IKE – 28 260 zł przepada | C | 22 | 19 | 3.3 | 85.0 |
| 4.11 wiecz. | Nawigacja w telefonie – 500 zł | C | 51 | 51 | 2.7 | 93.8 |
| 4.11 rano | 2000 zł mandatu. Połowa – bezprawnie | C | 21 | 20 | 3.1 | 73.7 |
| 3.11 | Policja #1 – norma legitymowań | C | 8 | 7 | 6.2 | 87.5 |
| 2.11 wiecz. | Zimowe opony nie są obowiązkowe | B | 100 | 94 | 4.0 | 78.7 |
| 2.11 | IKZE – 3617 zł | B | 56 | 53 | 2.0 | 98.0 |
| 2.11 rano | Ochroniarz nie przeszuka torby | B | 55 | 51 | 1.8 | 94.0 |
| 1.11 wiecz. | Najdłuższa granica – Czechy | B | 129 | 121 | 1.7 | 95.9 |
| 1.11 rano | Lokata 6% – podatek Belki | B | 19 | 17 | 3.1 | 82.4 |

Wszystkie rolki: **0 udostępnień i 0 zapisów** w IG. Mediana pominięć: 86.4%, mediana śr. czasu: 3.1 s.

## Wnioski

1. **Pierwsza rolka w nowym stylu (ZUS, Dynamic Visual Engine) ma najniższy odsetek pominięć na koncie: 63,3%** (mediana 86.4%) i drugi najdłuższy średni czas (4,9 s). Próbka mała (52 wyświetlenia, kilka godzin po publikacji) – to sygnał, nie dowód. Do potwierdzenia na kolejnych 5 rolkach w nowym stylu.
2. **Najgorsze haczyki (pominięcia ≥ 94%)**: „Pod szlabanem tracisz prawo jazdy”, „Kontroluje Cię policjant tej samej płci”, „Państwo odda Ci 3617 zł”, „Ochroniarz…”, „Najdłuższa granica…”, „Nawigacja – 500 zł”. Wspólne: pierwsza plansza to stwierdzenie bez napięcia albo liczba bez kontekstu. Najlepsze (≤ 75%): ZUS „…Jest haczyk.”, „Punkty karne zostają dłużej”, „2000 zł mandatu. Połowa – bezprawnie” – obietnica ukrytego haczyka/niesprawiedliwości w pierwszej klatce.
3. **Zero udostępnień i zapisów** mimo wezwań „wyślij komuś…” – wezwanie w opisie nie działa. Propozycja: wezwanie na ostatniej planszy obrazem (np. „Wyślij temu, kto…” z ikoną) i pytanie, na które łatwo odpowiedzieć jednym słowem w komentarzu (bez „wpisz A/B”).
4. **Kanał**: IG daje 16–129 wyświetleń na rolkę; zasięg robi Facebook (crosspost). Przy publikacji zawsze „Udostępnij na Facebooku” – to bez zmian najważniejsza czynność.
5. **Godzina**: rolki poranne i wieczorne nie różnią się wyraźnie w IG (za mało danych); decyzji 9:00/18:00 nie zmieniać.

## Rekomendacje do agenta (od 10.11)
- Haczyk w formule „X. Jest haczyk.” / „Połowa – bezprawnie” (ukryta stawka) – priorytet w karcie 20 pkt.
- Każda rolka w stylu DVE z planszą-dowodem (`dokument`, `wycinek`, `mapa`) – sprawdzić na 5 kolejnych rolkach, czy pominięcia zostają < 75%.
- Co tydzień ten sam pomiar (ten plik jako wzór); Facebook – zrzut „Statystyki rolki” od Michała, gdy chce porównania.
