# Harmonogram automatycznych działań zespołu (od 26.11.2026)

Decyzja Michała 25.11: „Rozwiń zespół i zaprogramuj ich automatyczne działania”.

**Jak to działa:** zespół nie ma osobnego zadania cyklicznego (CLAUDE.md: jedno zadanie). Pracuje przy **przypomnieniach dostaw** (6:30, 10:30, 14:30), które co tydzień ustawia przypomnienie sobotnie 14:30. Każde przypomnienie odsyła do tego pliku. Sesja najpierw robi dostawę, potem uruchamia agentów z tabeli. Agenci tylko szkicują: nic nie publikują, nie wysyłają i nie płacą.

## Codziennie

| Pora | Kto (podagenci `zm-*`) | Co | Wynik |
|---|---|---|---|
| 6:30 (z dostawą 9:00) | `zm-zwiadowca-trendow` (już w dostawie: `pilne.py` + `sledczy.py`) → `zm-analityk-postow` | statystyki IG z ostatnich 24–48 h (Composio, odczyt) | `docs/zespol/petla/RRRR-MM-DD_wyniki.md`; rekord → wyzwalacz „REKORD” niżej |
| 10:30 (z karuzelą 13:00) | `zm-odpowiedzi-komentarze` → (`zm-eskalacja`, jeśli hejt lub zarzut błędu) | szkice odpowiedzi na nowe komentarze IG (Composio, odczyt) | `docs/zespol/spolecznosc/RRRR-MM-DD_odpowiedzi.md` |
| 14:30 (z rolką 18:00) | `zm-pytanie-dyskusji` (w opisie rolki) + `zm-przypominacz` | przypięty komentarz; terminy w CRM sponsorów | w `_opis.md` + `docs/zespol/sprzedaz/crm.md` |

## W wybrane dni

| Dzień | Kto | Co |
|---|---|---|
| poniedziałek 10:30 | `zm-obserwator-konkurencji` | co działa u konkurencji w niszy (prawo, policja, kierowcy) |
| środa 10:30 | `zm-profil-i-wyszukiwanie` | czy bio, wyróżnienia i przypięte rolki pasują do najlepszych wyników |
| piątek 10:30 | `zm-wspolprace-tworcy` | 5 propozycji współprac + szkice DM |
| sobota 14:30 | `zm-kampanie-i-akcje` | kalendarz okazji na kolejne 14 dni → tematy do kalendarza |
| niedziela 14:30 | `/zespol tydzien` (raport z `brand-director`, jeden plik) + `zm-reklama-platna` | raport tygodnia + propozycja promowania zwycięzcy z budżetem do decyzji Michała |
| 1. dzień miesiąca 10:30 | `/zespol promocja` (`zm-strateg-marki` → cały dział) | plan wizerunku i promocji na miesiąc |

## Wyzwalacze (od razu, poza harmonogramem)

- **REKORD:** rolka ≥ 5× mediana wyświetleń z ostatnich 14 dni (liczone w kodzie). Wtedy `zm-reklama-platna` przygotowuje propozycję promocji, `zm-pr-media` notkę dla mediów, a `zm-profil-i-wyszukiwanie` proponuje przypięcie rolki.
- **Sponsor/marka w komentarzach lub DM:** `zm-lowca-leadow` → `zm-ocena-leadow` → `zm-crm`.
- **Hejt, groźby, zarzut błędu:** `zm-eskalacja` (zapisz i zgłoś Michałowi w tej samej wiadomości).

## Co trafia do Michała („nie chcę bałaganu”)

Pod wiadomością z dostawą **najwyżej 3 linie „Zespół:”**, tylko gdy coś wymaga decyzji, np.:
- propozycja kampanii płatnej (kwota, czas, cel);
- gotowe teksty do profilu;
- szkic maila albo DM do wysłania.

Bez raportów pośrednich. Wszystko inne ląduje w plikach w `docs/zespol/`.
