# Plan wzrostu – 2.11.2026

## Stan (Instagram API przez Composio, 2.11)

- Konto: 19 obserwujących, 23 posty.
- Rolki na IG: 7–128 wyświetleń. Pominięcia w pierwszych 3 s: 69–96%. Średni czas oglądania: 1,6–6 s. Komentarzy, wysłań i zapisów: 0.
- Facebook (crosspost): większość wyświetleń (ok. 1 tys. przy 2 rolkach), dane tylko ze zrzutów.
- Nowa okładka z obrazem (ochroniarz, 2.11): 50 wyświetleń, pominięcia 95,6%, 1,6 s – po kilku godzinach bez poprawy. Do oceny po tygodniu.
- Pierwsza dyskusja w komentarzach: TikTok, granica z Czechami.

## Diagnoza

Rolki odpadają w 1–2 s. Widz na pierwszej klatce widzi planszę z tekstem, a nie „film”. Konto jest bardzo małe, więc algorytm testuje każdą rolkę na garstce obcych osób, a przy ~95% pominięć nie daje drugiej fali.

## Co wdrożone (1–2.11)

1. Haczyk-stwierdzenie największym krojem od klatki 0 (szablon B domyślny).
2. Obraz-bohater na okładce + pieczątka + żółty układ (`obrazy.py`): polska, torba, suwak, dowod, monety, opona.
3. Silnik „moc: mocna”: kadr nigdy nie stoi, puls na bicie.
4. Statystyki IG pobierane przez Composio (bez zrzutów).
5. Tematy sezonowe (opony teraz, Black Friday 20–27.11) – bank `docs/pomysly-tematow.md`.
6. Pytanie-reakcja na końcu każdej rolki i w opisie.

## Testy do decyzji Michała (łamią obecne reguły, więc wymagają zgody)

| Test | Po co | Reguła, którą narusza |
|---|---|---|
| **Krótka rolka 8–12 s** (2–3 plansze: haczyk z odpowiedzią + liczba + pytanie), zapętlona | przy średnim oglądaniu 1,6 s krótszy film ma większy % obejrzeń do końca i ponowne odtworzenia | min. 4 plansze i 20 s (decyzja 29.10) |
| **Lektor na pierwszych 3 s** (sam haczyk wypowiedziany, dalej muzyka) | dźwięk mowy zatrzymuje część osób oglądających z dźwiękiem | „muzyka zamiast lektora” (29.10) |
| **Ruchomy obraz zamiast planszy na start** (3D z Blendera lub darmowe nagrania) | feed to wideo – plansza wygląda jak reklama | brak (koszt: czas renderu 3D ok. 40 min) |

## Działania Michała (bez kosztów)

1. **Trial Reels** (Rolki próbne) – ta sama rolka z dwoma haczykami do osób nieobserwujących; zwycięzcę publikować normalnie.
2. **Odpowiedź w 1. godzinie** na każdy komentarz, zawsze z pytaniem zwrotnym (TikTok: odpowiedź filmem).
3. **Komentarze pod dużymi kontami** z tej niszy (ciekawostki, prawo, finanse, motoryzacja): 5–10 merytorycznych komentarzy dziennie, w pierwszych minutach po publikacji – to darmowy ruch na profil.
4. **Wspólne posty („Zaproś współtwórcę”)** – realne dopiero przy kilkuset obserwujących; najpierw kontakt przez komentarze.
5. Okładka ręcznie, „Udostępnij na Facebooku” włączone, TikTok tego samego dnia.
