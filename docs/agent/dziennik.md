# Dziennik agenta

Każdy dzień: data, statystyki (najlepsza i najsłabsza rolka), wnioski, co przygotowano, problemy.

## 4.11.2026 (start, ręcznie)
- Rekord konta: Policja #1 „norma legitymowań” – ponad 2 tys. wyświetleń (Michał). Śr. czas 5 s, pominięcia 83% (zrzut 3.11).
- Wniosek: szablon C + mocna kontrowersja wokół policji działa najlepiej; zwrot akcji przed 14 s (na #1 widzowie odpadali ok. 17 s).
- Przygotowano rolki do 8.11 (specs/tydzien_4-8.11_*.json, opisy w paczce dla Michała).
- Zadanie codzienne: `trig_01SeXEiKGkqsPEVp6gZ8TnTi` (7:13 Europe/Warsaw, nowa sesja przy każdym uruchomieniu, push). Stare tygodniowe `trig_012NQ3c9krCrwpm1W16pPmbU` usunięte.
- Konektor Composio dodany do zadania przez Michała 4.11 (claude.ai → Scheduled tasks → zadanie → Edit → Connectors) – sprawdzone: zadanie go widzi.

## 4.11 wieczorem – zmiana trybu
Decyzja Michała: 2 dostawy dziennie (ok. 9:00 i 17:00), każda = 1 rolka + opis IG i TikTok, bez wariantów B i lektora. Zadanie: starty 7:23 i 15:23, narzędzie `dostawa.py`, kalendarz przepisany na pory 9:00/17:00 (5–10.11 z gotowych scenariuszy, od 11.11 nowe).

## 5.11
- 9:00 – IKE wysłane do Michała; push z sesji zadania nie przeszedł (403, zadanie bez podpiętego repozytorium) – status poprawiony ręcznie.
- Decyzja Michała: 3 dostawy (9:00 rolka, 13:00 karuzela 9:16 na TikTok, 18:00 rolka), od 5.11 wieczór o 18:00.

## 9.11
- 9:00 – ZUS (nowy styl, plansza `dokument`) wysłane 8.11 wieczorem z sesji głównej. Błąd silnika wykryty 9.11: wyróżnione słowo na jasnej karcie niewidoczne ok. 0,8 s przed markerem – poprawione (`kMarkerDoc`).
- 13:00 – sesja zadania (11:23) zrobiła karuzelę „Antarktyda – największa pustynia”, ale ustawiła czekanie na 12:50 w tle i zakończyła się o 11:27 → **wysyłka przepadła**; push 403 (zadanie bez podpiętego repozytorium: `sources: []`, `add_repo` niedostępne w sesji zadania). Karuzelę odtworzono i wysłano z sesji głównej (fakty ponownie sprawdzone: Live Science, Guinness World Records, Wikipedia).
- Naprawa: polecenie zadania i skille – wysyłka od razu po kontroli, bez czekania w tle; instrukcja instalacji zależności (venv). Do zrobienia przez Michała: dodać repozytorium do zadania (claude.ai → Zaplanowane zadania → zadanie → Edytuj → Repozytoria), inaczej commity z sesji zadania giną.
- Silnik: plansze `wycinek`, `foto`, `mapa`; `zdjecia.py` (Openverse, Commons, NASA).
- 18:00 – sesja zadania (16:24) skończyła się po 46 s: w poleceniu brakowało nazwy repozytorium (usunięta przy zmianie 13:19), a sesja nie ma go sklonowanego → nic nie zrobiła. Rolkę „Mandat? Możesz powiedzieć »nie«” zrobiono w sesji głównej i wysłano ok. 18:40 (spóźnienie). Polecenie zadania poprawione: pełna nazwa repo + `git clone` (repo publiczne).
