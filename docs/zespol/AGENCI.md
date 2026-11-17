# Zespół 36 agentów – lista (generowana)

> Plik generuje `scripts/zespol/generuj_agentow.py` – zmiany wprowadzaj tam, nie tutaj.

## Research – Zwiad i pisanie

| Agent | Schemat | Kiedy | Wynik |
|---|---|---|---|
| `zm-zwiadowca-trendow` – Zwiadowca trendów | Trend Scout | codziennie rano albo gdy brakuje tematu – gorące tematy z 48–72 h | `docs/zespol/research/RRRR-MM-DD_trendy.md` – 5 kandydatów z linkami |
| `zm-sluchacz-odbiorcow` – Słuchacz odbiorców | Audience Listener | raz w tygodniu albo po rolce z dużą liczbą komentarzy | `docs/zespol/research/RRRR-MM-DD_odbiorcy.md` |
| `zm-gornik-komentarzy` – Górnik komentarzy | Comment Miner | po zm-sluchacz-odbiorcow albo gdy Michał wklei komentarze | nowe wiersze w `docs/pomysly-tematow.md` |
| `zm-obserwator-konkurencji` – Obserwator konkurencji | Competitor Watch | raz w tygodniu (poniedziałek) albo przed nową serią | `BRAND_GROWTH/ANALYTICS/KONKURENCJA_RRRR-MM-DD.md` |
| `zm-scenarzysta` – Scenarzysta | Post Writer | gdy jest wybrany temat i trzeba scenariusza rolki albo karuzeli | `publikacje/RRRR-MM-DD/spec_<id>.json` + `<HHMM>_opis.md` (szkic) |
| `zm-autor-maili` – Autor maili | Email Writer | gdy trzeba napisać mail do marki, sponsora, instytucji (prośba o dane) albo odpowiedź na ofertę | `docs/zespol/sprzedaz/maile/RRRR-MM-DD_<adresat>.md` – szkic do wysłania przez Michała |

## Content – Produkcja

| Agent | Schemat | Kiedy | Wynik |
|---|---|---|---|
| `zm-grafik` – Grafik | Visual Designer | gdy jest zatwierdzony scenariusz – plansze, okładka, wklejka do relacji | podgląd `out/…_sheet.png` + poprawiony spec |
| `zm-karuzele` – Karuzele | Carousel Builder | post 13:00 na TikToku (4 slajdy 9:16) i karuzela tygodnia na IG (4:5) | `publikacje/RRRR-MM-DD/1300_TIKTOK_01..04.jpg` (+ IG 4:5 gdy karuzela tygodnia) |
| `zm-lektor` – Lektor | Voiceover | TYLKO na wyraźną prośbę Michała – test lektora jest wstrzymany (4.11) | `<id>_lektor.mp4` tylko na prośbę |
| `zm-montazysta` – Montażysta | Video Editor | render finalnej rolki: muzyka, efekty, logo, IG 4K + TikTok 1080 | `VIRAL_REELS_FACTORY/DOSTAWA/<data>_<HHMM>/` – 5 plików |
| `zm-straznik-marki` – Strażnik marki | Brand Check | przed każdą akceptacją – scenariusz, plansze, opis, odpowiedzi | `docs/zespol/kontrola/RRRR-MM-DD_<id>.md` – werdykt |
| `zm-biurko-akceptacji` – Biurko akceptacji | Approval Desk | ostatni krok przed przekazaniem Michałowi czegokolwiek (rolka, mail, odpowiedzi, oferta) | `docs/zespol/akceptacja.md` – kolejka: czeka / zaakceptowane / odrzucone |

## Publish – Paczki do ręcznej publikacji

| Agent | Schemat | Kiedy | Wynik |
|---|---|---|---|
| `zm-planista` – Planista | Scheduler | planowanie dnia i tygodnia; pilnuje godzin 9:00 / 13:00 / 18:00 | zaktualizowany kalendarz |
| `zm-paczka-tiktok` – Paczka TikTok | TikTok Poster | przygotowanie rolki na TikTok do ręcznej publikacji | sekcja TikTok w `<HHMM>_opis.md` |
| `zm-paczka-reels` – Paczka Reels | Reels Poster | przygotowanie rolki na Instagram do ręcznej publikacji | sekcja Instagram w `<HHMM>_opis.md` |
| `zm-paczka-karuzela` – Paczka karuzeli | Shorts Poster → karuzela 13:00 | post 13:00 na TikToku i karuzela tygodnia na IG (zamiast YouTube Shorts ze schematu – kanału nie prowadzimy) | `publikacje/RRRR-MM-DD/1300_opis.md` |
| `zm-paczka-relacja` – Paczka relacji | X Poster → relacja IG | relacja do każdej rolki (zamiast X ze schematu – konta X nie prowadzimy) | `_relacja.jpg` + linia „Relacja” w opisie |
| `zm-newsletter` – Newsletter (uśpiony) | Newsletter | TYLKO gdy Michał uruchomi newsletter – do tego czasu co tydzień najwyżej szkic | `docs/zespol/newsletter/RRRR-WW.md` (szkic) |

## Community – Społeczność (szkice)

| Agent | Schemat | Kiedy | Wynik |
|---|---|---|---|
| `zm-odpowiedzi-komentarze` – Odpowiedzi na komentarze | Comment Replier | w 1. godzinie po publikacji i codziennie wieczorem | `docs/zespol/spolecznosc/RRRR-MM-DD_odpowiedzi.md` – Michał wkleja sam |
| `zm-dm` – Wiadomości prywatne | DM Agent | gdy Michał wklei DM-y albo trzeba zaproponować współpracę z innym twórcą | `docs/zespol/spolecznosc/RRRR-MM-DD_dm.md` |
| `zm-baza-faq` – Baza FAQ | FAQ Builder | raz w tygodniu – z powtarzających się pytań | `docs/zespol/spolecznosc/faq.md` |
| `zm-pytanie-dyskusji` – Pytanie do dyskusji | Review Asker → pytanie do dyskusji | do każdej rolki – przypięty komentarz autora (zamiast prośby o opinie ze schematu) | linia „Przypięty komentarz” |
| `zm-lowca-leadow` – Łowca leadów | Lead Catcher | gdy w komentarzach/DM/mailach pojawia się marka, propozycja współpracy albo media | nowe wiersze w CRM |
| `zm-eskalacja` – Eskalacja | Escalation | hejt, groźby, zarzut błędu merytorycznego, sprawa prawna, prośba o usunięcie wizerunku | `docs/zespol/spolecznosc/eskalacje.md` + 1 zdanie do wiadomości dostawy, jeśli pilne |

## Sales – Sponsorzy i współprace

| Agent | Schemat | Kiedy | Wynik |
|---|---|---|---|
| `zm-ocena-leadow` – Ocena leadów | Lead Scorer | nowy wiersz w CRM albo przegląd tygodniowy | kolumny „ocena” i „następny krok” w CRM |
| `zm-umawianie-rozmow` – Umawianie rozmów | Call Booker | lead ≥ 7 pkt chce porozmawiać | `docs/zespol/sprzedaz/rozmowy/RRRR-MM-DD_<marka>.md` |
| `zm-przypominacz` – Przypominacz | Reminder | codziennie przy dostawie 9:00 – przegląd terminów w CRM | lista „dziś” w `docs/zespol/sprzedaz/crm.md` |
| `zm-follow-up` – Follow-up | Follow-up | brak odpowiedzi od marki po 5 dniach roboczych lub po rozmowie | szkic w `docs/zespol/sprzedaz/maile/` |
| `zm-oferta-i-platnosc` – Oferta i płatność | Payment Link | lead zaakceptował współpracę – oferta, umowa, faktura | `docs/zespol/sprzedaz/oferty/<marka>.md` |
| `zm-crm` – CRM | CRM Sync | po każdej zmianie u leada; porządek raz w tygodniu | `docs/zespol/sprzedaz/crm.md` |

## The loop – Pętla: wyniki → decyzje

| Agent | Schemat | Kiedy | Wynik |
|---|---|---|---|
| `zm-analityk-postow` – Analityk postów | Post Analyst | codziennie rano (statystyki z wczoraj) i w raporcie tygodniowym | wiersze w `docs/wyniki.md` |
| `zm-przychody` – Przychody | Revenue Tracker | raz w tygodniu albo gdy Michał przyśle zrzut prowizji/płatności | `docs/zespol/petla/przychody.md` |
| `zm-tracker-rozmow` – Notatki z rozmów | Call Tracker | po każdej rozmowie ze sponsorem (Michał podaje notatki lub nagranie) | notatka w `docs/zespol/sprzedaz/rozmowy/` |
| `zm-analityk-maili` – Analityk maili | Email Analyst | raz w tygodniu – skuteczność maili i DM do marek | sekcja „Sprzedaż” w raporcie tygodniowym |
| `zm-raport-tygodniowy` – Raport tygodniowy | Weekly Report | niedziela wieczorem / poniedziałek rano albo na prośbę Michała | `BRAND_GROWTH/REPORTS/RAPORT_RRRR-MM-DD.md` |
| `zm-karmienie-petli` – Karmienie pętli | Loop Feeder | po raporcie tygodniowym i po każdym nietypowym wyniku rolki | wpisy w `docs/agent/dziennik.md` + zaktualizowane pliki |
