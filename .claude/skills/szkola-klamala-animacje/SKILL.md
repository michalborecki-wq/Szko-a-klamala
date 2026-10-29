---
name: szkola-klamala-animacje
description: Animowane napisy i ruch w Reelsach i filmach TikTok „Szkoła kłamała” (@szkola_klamala) – kinetyczna typografia na poziomie profesjonalnego motion designera: słowa wysuwane spod maski, rysowane przekreślenie mitu, odliczane liczby, markowe przejścia, rozmycie ruchu. Używaj ZAWSZE, gdy trzeba zrobić lub poprawić rolkę, Reel, film, wideo, animację, „ruszające się napisy”, planszę wideo albo MP4 dla „Szkoła kłamała” – także przy „zrób z tego rolkę”, „ożyw te slajdy”, „wersja wideo”. Wygląd plansz opisuje skill szkola-klamala-grafiki, napisy do nagranej mowy – szkola-klamala-napisy, montaż nagrań – szkola-klamala-montaz.
---

# Animacje „Szkoła kłamała”

Rolka ma wyglądać, jakby zrobił ją profesjonalny motion designer: jeden spójny język ruchu, nic przypadkowego, tekst zawsze da się spokojnie przeczytać, haczyk widać od pierwszej klatki.

Silnik jest wspólny z grafikami: `.claude/skills/szkola-klamala-grafiki/scripts/render.py`. Ten skill opisuje, **jak** go używać do wideo i jakie decyzje podejmować. Treść i fakty – `instagram-mich-bor` / `CLAUDE.md`; wygląd plansz – `szkola-klamala-grafiki`.

## Jak pracować

1. Rozpisz Reel w JSON (`format: "reel"`, format pól: `szkola-klamala-grafiki/references/spec-format.md`). Typowy „jeden mit”: `cover` (mit jako haczyk) → `number` (fakt z liczbą) → `text` (puenta + źródło), `durations: [2.6, 4.2, 3.8]`.
2. Szybki podgląd układu i tempa:
   ```bash
   python3 .claude/skills/szkola-klamala-grafiki/scripts/render.py spec.json --out out --video --draft
   ```
3. Obejrzyj klatki (`python3 .claude/skills/szkola-klamala-montaz/scripts/klatki.py out/<id>.mp4` → arkusz JPEG, potem Read). Sprawdź listę kontrolną niżej. Popraw treść / `durations` i powtórz.
4. Wersja finalna (z rozmyciem ruchu, ok. 1,5–2 min na 10 s): to samo polecenie bez `--draft`.
5. Przed oddaniem obejrzyj gotowy film jeszcze raz (arkusz klatek + `ffprobe`) – zasada nr 8 montażu.

## Język ruchu (wbudowany w silnik – nie dokładaj innych efektów)

| Element | Ruch | Po co |
|---|---|---|
| Nagłówek (`h1`, `h2`) | słowa wysuwają się spod niewidocznej linii (maska), lekko obrócone, po kolei | klasyczna kinetyczna typografia, prowadzi wzrok słowo po słowie |
| Haczyk na planszy 1 | **widoczny od klatki 0**, tylko delikatne „uderzenie” (skala 1,12 → 1) | okładka i pierwsze 0,3 s decydują, czy ktoś zostanie |
| Etykieta (chip, MIT/FAKT) | wjazd z lewej z pochyleniem | zapowiada, co zaraz przeczytasz |
| Pędzel pod tytułem | rysuje się od lewej | „ręczny” akcent marki |
| Duża liczba (`big`) | wyskakuje i **odlicza się od zera**, na końcu błysk | liczba jest bohaterem – widz czeka na wynik |
| MIT | pojawia się, potem czerwona linia **przekreśla go na oczach widza** | najmocniejszy moment „szkoła kłamała” |
| Tekst treści | słowa wchodzą z rozmycia do ostrości; `**wyróżnienia**` po chwili zapalają się na żółto | czytelność + jeden akcent na zdanie |
| Wykres (`bars`) | słupki rosną, wartości się odliczają | dane „dzieją się” |
| Quiz | opcje wjeżdżają raz; cyfry 3-2-1 wyskakują; zła odpowiedź drga na czerwono, reszta gaśnie | napięcie bez skakania układu |
| Przejście między planszami | markowa niebieska smuga z żółtymi paskami przecina ekran (0,22 s + 0,22 s) | jeden, rozpoznawalny „stinger” marki zamiast losowych przejść |
| Tło | smugi lekko dryfują, ziarno filmowe żyje, powolny najazd kamery (treść 1 → 1,025) | brak martwych klatek |
| Całość | rozmycie ruchu (2 podklatki na klatkę) | płynność jak z programu do animacji |

Wszystkie ruchy mają tę samą krzywą (szybki start, miękkie lądowanie). Nie dodawaj obrotów 3D, odbić, wirujących liter, emoji, efektów „glitch” ani przejść innych niż smuga – mieszanie stylów to pierwszy znak amatorskiego montażu.

## Tempo

- Napisy wchodzą w ok. 0,8–1,6 s; **potem tekst musi stać** – licz ok. 0,25 s na słowo treści + 1 s zapasu. QA w `qa_report.txt` ostrzega, gdy plansza jest za krótka na wejście i czytanie – wtedy wydłuż `durations` albo skróć tekst.
- Haczyk 2,4–3 s, fakt 4–4,5 s, puenta 3,5–4 s. Cały „jeden mit”: 9–12 s (krótkie filmy oglądane do końca i powtarzane są promowane).
- Ostatnia plansza nie ma wyjścia – film zapętla się płynnie do haczyka.
- Liczby, które nie powinny się odliczać (rok „1569”, numer „01”), oznacz w slajdzie `"count": false`.

## Lista kontrolna przed oddaniem

- Klatka 0: haczyk czytelny, bez pustego ekranu i bez logo na start.
- Żadne słowo nie jest ucięte (ogonki ą/ę, poświata liczb) – w trakcie wjazdu i po nim.
- Każdy tekst stoi nieruchomo wystarczająco długo, by przeczytać go dwa razy.
- Przejście w pełni zakrywa ekran w momencie cięcia (nie widać „przeskoku”).
- Napisy, liczby i źródła w strefie bezpiecznej 9:16 (góra 250, dół 430, prawo 150 px) – silnik tego pilnuje, ale sprawdź wzrokiem.
- `ffprobe`: 1080×1920, 30 kl./s, H.264 + ścieżka AAC, długość zgodna z sumą `durations`.
- Wysyłaj Michałowi jeden MP4 na Reel (ten sam plik na IG i TikTok) oraz okładkę `<id>_reel_01.jpg`.
