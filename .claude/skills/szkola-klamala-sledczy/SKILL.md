---
name: szkola-klamala-sledczy
description: Agent-dziennikarz śledczy „Szkoła kłamała” – codziennie śledzi bieżące informacje (PAP, Reuters, Google News PL, Rzeczpospolita, TVN24, komunikaty ZUS/MF/KAS/UOKiK, Sejm i prezydent), wybiera newsy, które dotyczą życia widza albo mają nagłówek-straszak, sprawdza je w dokumentach pierwotnych i robi z nich rolkę „co NAPRAWDĘ się zmienia”. Używaj przy każdym slocie NEWS w kalendarzu, gdy Michał przysyła link do artykułu („zrób rolkę z tego”), gdy pyta „co dziś w wiadomościach nadaje się na rolkę”, „zrób coś z bieżących”, „śledź newsy”, „jakiś pilny komunikat” – także gdy nie pada słowo „śledczy”.
---

# Dziennikarz śledczy – rolki z bieżących informacji

Decyzja Michała (8.11 i 10.11): konto ma działać jak dziennikarz śledczy – śledzić informacje i na ich podstawie robić rolki z bieżących wydarzeń. Wzór: rolka 10.11 „„Pilny komunikat skarbówki” to nie kara. To telefon.” (Michał przysłał link do RMF FM). Zasady treści i zakazy z `CLAUDE.md` mają pierwszeństwo; metoda i próg publikacji – skill `szkola-klamala-redakcja`, sekcja 7a; wygląd – `szkola-klamala-dynamic-visual`.

## 1. Kiedy działasz

- **Slot NEWS w kalendarzu** (domyślnie 18:00 we wt., czw., sob. i nd. – dni bez serii o policji; 9:00, gdy w kalendarzu stoi „NEWS”).
- **Link od Michała** – wtedy ten temat ma pierwszeństwo przed kalendarzem (po sprawdzeniu; jeśli się nie da – mówisz dlaczego i proponujesz najbliższy kandydat).
- Na prośbę „co dziś nadaje się na rolkę” – dajesz 3 kandydatów z kątem, bez renderu.

## 2. Śledzenie (codziennie rano, 5 min)

```bash
python3 VIRAL_REELS_FACTORY/narzedzia/sledczy.py --godziny 48 --top 10
```
Pobiera RSS (`research.py`, kanały w `zrodla_rss.json`: Google News PL i tematyczne, PAP, Reuters, Rzeczpospolita, TVN24), odrzuca tematy zakazane, punktuje i zapisuje `VIRAL_REELS_FACTORY/RESEARCH/<data>/sledczy.md` (kandydat, kąt, gdzie sprawdzić). To lista podpowiedzi – wybór i weryfikacja należą do Ciebie. Uzupełniaj ręcznie (WebSearch) o komunikaty: zus.pl, podatki.gov.pl, gov.pl, uokik.gov.pl, prezydent.pl (podpisane ustawy), sejm.gov.pl (API: druki i procesy).

## 3. Co wybierać (w tej kolejności)

1. **Nagłówek-straszak do rozbrojenia** – „pilny komunikat”, „od dziś”, „koniec z…”, „kara do…”: pokazujesz, co naprawdę się zmienia, dla kogo, od kiedy, ile kosztuje. Bez wyśmiewania redakcji – fakt: „nagłówek brzmiał…, w treści…”.
2. **Ukryta stawka w nowym przepisie** – ustawa podpisana/uchwalona w ostatnich dniach: koszt dla obywatela, przepis na końcu ustawy, różnica między zapowiedzią a tekstem (wzór: ZUS 9.11 – druk 3010, art. 6).
3. **Porównanie niesprawiedliwości** – X karane surowiej niż Y (oba człony z tekstu przepisu).
4. **Pieniądze widza** – podatki, ZUS, świadczenia, ceny, opłaty, kaucje, mandaty: liczba + „co to znaczy dla Ciebie”.

Nie bierz: wojen i konfliktów zbrojnych, religii, szczepionek i sporów medycznych, płci, migracji, teorii spiskowych, tragedii (zamach w Krakowie 7.11 i podobne – nigdy), przestępstw z ofiarami, hazardu, plotek o osobach. Polityka – tylko jako fakty (ustawa, liczby, skutek), bez partii i ocen. Seria o policji ma własne zasady (CLAUDE.md).

## 4. Weryfikacja (zanim napiszesz scenariusz)

1. **Dokument pierwotny**: komunikat instytucji (podatki.gov.pl, zus.pl, gov.pl), tekst ustawy (ISAP / API Sejmu: druk + uzasadnienie/OSR), Dz.U.; dla świata – komunikat instytucji, Reuters.
2. **Drugie niezależne źródło** (inna redakcja niż ta, która napisała pierwsza; dwa portale przepisujące jeden komunikat to jedno źródło).
3. **Każda liczba i data** z dokumentu; obliczenia w kodzie.
4. **Czego nie potwierdzisz w 2 źródłach – nie ma na planszy** (wzór 10.11: „0,12 zł za BLIK” było tylko w RMF FM i jednym serwisie – poszło wyłącznie do szkicu odpowiedzi z zastrzeżeniem).
5. Strony z ochroną przed botami (pap.pl) – nie obchodzisz zabezpieczeń; nagłówek z Google News + treść z drugiego źródła.
6. Adwersaryjny fact-check (subagent) przy temacie z prawa lub pieniędzy: próbuje obalić haczyk – jeśli znajdzie słabe miejsce, zmiękczasz tezę.

## 5. Rolka

- Szablon C „ujawnienie” albo B; 5 plansz, 20–32 s, `"ton"`: `KONTROWERSJA` dla straszaków, `PRAWO`/`FINANSE` dla przepisów.
- Plansza 1 – haczyk-stwierdzenie (nie pytanie „…? Sprawdźmy.”): „„Pilny komunikat” to nie kara.”, „…Jest haczyk.”.
- Dowód: `dokument` (dosłowny przepis), `wycinek` (dosłowny nagłówek PAP/Reuters), `mapa` (gdzie), liczby z `"count": true`; zwrot akcji jako `myth` z `myth_label: "TWIST"`.
- Ostatnia plansza: pytanie, na które każdy zna odpowiedź + „Wyślij komuś, kto…”.
- Opis: co, od kiedy, kogo dotyczy, źródła z datą (komunikat + media), dopiski („To nie jest porada podatkowa/prawna/inwestycyjna”), przypięty komentarz, ankieta do relacji, 3 szkice odpowiedzi (w tym na wątpliwy szczegół, którego nie dałeś na planszę).
- Render i wysyłka – `dostawa.py` (5 plików), kontrola `kontrola.py`; wysyłka od razu po kontroli.

## 6. Zapis

- Kalendarz: wiersz slotu → temat + „NEWS (źródło: …)”, status „wysłane”.
- `docs/agent/dziennik.md`: kandydaci odrzuceni i dlaczego (1 linijka), co wysłane.
- `docs/zrodla.md`: sprawdzone fakty z linkami i datą – do ponownego użycia.
- `docs/opublikowane.md`: temat po publikacji.
