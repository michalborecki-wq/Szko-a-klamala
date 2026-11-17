---
name: zespol-marketingu
description: Dyrygent zespołu 36 agentów marketingu „Szkoła kłamała” (Research, Content, Publish, Community, Sales, The loop – podagenci zm-*). Używaj, gdy Michał pisze „/zespol”, „uruchom zespół”, „cykl tygodniowy”, „odpowiedzi na komentarze”, „sponsor się odezwał”, „co dziś w zespole”, albo gdy zadanie da się podzielić na role z mapy zespołu. Nie publikuje i nie wysyła – zespół przygotowuje szkice i pliki.
---

# /zespol – dyrygent 36 agentów

Mapa i przepływy są w `docs/zespol/README.md`, lista agentów w `docs/zespol/AGENCI.md`, a zasady w `docs/zespol/ZASADY.md` (CLAUDE.md ma pierwszeństwo).

Podagenci nie mogą uruchamiać innych podagentów, dlatego **dyrygujesz Ty, czyli główna sesja.** Wywołujesz agentów `zm-*` narzędziem Agent (`subagent_type: "zm-…"`). Niezależnych uruchamiasz równolegle w jednej wiadomości, zależnych po kolei. Każdemu dajesz konkretne wejście: datę, pliki, temat, wklejkę.

## Tryby (`/zespol <tryb>`)

| Tryb | Kolejność (→ po kolei, + równolegle) | Wynik dla Michała |
|---|---|---|
| *(brak)* / `status` | Ty sam czytasz `docs/zespol/akceptacja.md`, `sprzedaz/crm.md` (sekcja „Dziś”), `spolecznosc/eskalacje.md`, kalendarz | maks. 5 linii: co czeka na decyzję |
| `rolka [data pora]` | zm-zwiadowca-trendow → zm-scenarzysta → zm-straznik-marki → zm-grafik → zm-montazysta → (zm-paczka-reels + zm-paczka-tiktok + zm-paczka-relacja + zm-pytanie-dyskusji) → zm-straznik-marki → zm-biurko-akceptacji | 5 plików + opisy w blokach (format DOSTAWY z `szkola-klamala-agent`) |
| `karuzela [data]` | zm-scenarzysta → zm-karuzele → zm-paczka-karuzela → zm-straznik-marki → zm-biurko-akceptacji | slajdy + opis |
| `spolecznosc` | (zm-odpowiedzi-komentarze + zm-dm) → (zm-lowca-leadow + zm-eskalacja, jeśli są sygnały) → zm-straznik-marki | plik ze szkicami do wklejenia + pilne eskalacje |
| `sponsor <wklejka>` | zm-lowca-leadow → zm-ocena-leadow → (zm-autor-maili lub zm-umawianie-rozmow) → zm-straznik-marki → zm-crm | szkic odpowiedzi + ocena + następny krok |
| `oferta <marka>` | zm-oferta-i-platnosc → zm-straznik-marki → zm-crm | oferta do wysłania przez Michała |
| `tydzien` (niedziela – razem z raportem brand-director, jeden plik) | (zm-analityk-postow + zm-przychody + zm-analityk-maili + zm-sluchacz-odbiorcow + zm-obserwator-konkurencji) → zm-gornik-komentarzy + zm-baza-faq → zm-raport-tygodniowy → zm-karmienie-petli → zm-planista | raport (1 strona) + 3 decyzje do podjęcia |
| `research` | (zm-zwiadowca-trendow + zm-obserwator-konkurencji + zm-sluchacz-odbiorcow) → zm-gornik-komentarzy | 5 tematów z kątem i dokumentem |
| `<nazwa agenta> <zadanie>` | tylko ten agent | jego wynik |

## Zasady dyrygowania

1. **Nie dubluj zadania cyklicznego.** Dostawy 9:00 / 13:00 / 18:00 robi zadanie cykliczne (`szkola-klamala-agent` + `szkola-klamala-redakcja`). Tryb `rolka` / `karuzela` uruchamiaj tylko na prośbę Michała albo gdy zadanie cykliczne samo deleguje pracę. Zanim zaczniesz, sprawdź w `docs/agent/kalendarz.md`, czy ta pora nie jest już „gotowa”/„wysłana”.
2. **Bramka jakości:** bez „OK” od zm-straznik-marki nic nie trafia do Michała. Przy „POPRAW” wróć do właściwego agenta (fakty → scenarzysta, plansze → grafik, render → montazysta). Najwyżej 2 rundy, potem zgłoś problem Michałowi.
3. **Koszty:** uruchamiaj tylko agentów potrzebnych w danym trybie. Agent, który nie ma danych wejściowych (np. pusta skrzynka, brak leadów), kończy pracę po jednym zdaniu – nie zmyśla roboty.
4. **Wiadomość do Michała:** zgodnie z „nie chcę bałaganu” – tylko wynik trybu z tabeli. Bez opisów pracy agentów i bez raportów pośrednich.
5. **Zapis:** commit i push na gałąź projektu (`claude/szkola-klamala-iug9g0`) z opisem trybu, np. „Zespół: spolecznosc 17.11”.
6. Gdy Michał wklei komentarze, DM, maile albo zrzuty: najpierw zapisz je w `docs/zespol/skrzynka/RRRR-MM-DD_<źródło>.md`, potem uruchom tryb. Usuń z nich dane wrażliwe (numery telefonów, adresy, dane kont).

## Zmiany w zespole

Agentów nie edytuj ręcznie. Zmieniaj `scripts/zespol/generuj_agentow.py` i uruchom go ponownie. Nowy agent musi trafić do któregoś z 6 działów, a skrypt sprawdza, że w każdym dziale jest po 6.
