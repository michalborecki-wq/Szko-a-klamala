---
name: szkola-klamala-napisy
description: Spisywanie mowy i animowane napisy po polsku, słowo w słowo, w stylu marki „Szkoła kłamała” (@szkola_klamala) – transkrypcja faster-whisper z czasami każdego słowa, korekta, napisy z podświetlanym aktualnym słowem wypalone w pionowym wideo, plik SRT do wgrania. Używaj ZAWSZE, gdy film ma nagraną mowę albo lektora i trzeba: dodać napisy, „spisać, co mówię”, zrobić transkrypcję, napisy „jak na TikToku”, karaoke, SRT, poprawić napisy. Montaż całego nagrania (cięcie pauz, kadr, głośność) opisuje szkola-klamala-montaz; animowane plansze bez mowy – szkola-klamala-animacje.
---

# Napisy „Szkoła kłamała”

Większość ludzi ogląda Reelsy i TikToki bez dźwięku, więc napisy niosą film. Mają być **po polsku, słowo w słowo** (bez streszczania i „poprawiania” wypowiedzi), czytelne w ułamku sekundy i w stylu marki.

Skrypt: `.claude/skills/szkola-klamala-napisy/scripts/napisy.py`. Narzędzia: faster-whisper (darmowy, offline, model `medium` dla polskiego) i ffmpeg z libass. Instalacja: `bash scripts/instaluj.sh` w katalogu głównym repozytorium.

## Jak pracować

1. **Transkrypcja** (na kopii filmu, nigdy na oryginale):
   ```bash
   python3 .claude/skills/szkola-klamala-napisy/scripts/napisy.py transkrybuj film.mp4 --slownik "Kopernik, Merkator, ISS"
   ```
   Powstają `film.slowa.json` (każde słowo z czasem i pewnością) i `film.slowa.txt` (zdania z czasami). `--slownik` podpowiada nazwy własne i terminy z tematu odcinka.
2. **Korekta – obowiązkowa.** Przeczytaj `.txt` i popraw w `.slowa.json` tylko pole `"w"` źle usłyszanych słów. Skrypt wypisuje słowa o niskiej pewności – sprawdź je najpierw. Zasady:
   - słowo w słowo: nie usuwaj powtórzeń ani „yyy”, jeśli zostały w filmie (pauzy i gorsze podejścia wycina montaż, nie napisy);
   - nie zmieniaj czasów `start`/`end` i nie łącz słów;
   - liczby cyframi („90%”, „1569”), nazwy własne z wielkiej litery, polska ortografia i interpunkcja;
   - gdy nie da się ustalić słowa – zapytaj Michała, nie zgaduj.
3. **Wypalenie napisów:**
   ```bash
   python3 .claude/skills/szkola-klamala-napisy/scripts/napisy.py wypal film.mp4 --out film_napisy.mp4
   ```
   Powstają też `film.ass` (styl) i `film.srt` (do wgrania jako napisy w aplikacji, dla dostępności).
4. **Obejrzyj wynik** – `python3 .claude/skills/szkola-klamala-montaz/scripts/klatki.py film_napisy.mp4` i Read arkusza. Sprawdź listę kontrolną.

## Styl (wbudowany – nie zmieniaj bez powodu)

- Napisy renderują się w rozdzielczości filmu – w pionie 4K (2160×3840) są natywnie ostre (współrzędne w pliku ASS są w skali 1080×1920 i skalują się automatycznie).
- Fraza musi wisieć na ekranie tyle, by dało się ją przeczytać: krótkie frazy 1–3 słów nadążają za mową; gdy ktoś mówi bardzo szybko, łącz słowa w dłuższe frazy zamiast skracać czas wyświetlania.

- Inter Display Black Italic, wersaliki, biały tekst z ciemnym obrysem i **niebieskim cieniem przesuniętym w dół** – jak nagłówki marki.
- **Aktualnie wypowiadane słowo żółte** (#FFC727) z krótkim „pop” 108% → 100%. Nowa fraza wjeżdża lekko z dołu.
- 1–3 słowa, maks. ok. 15 znaków – zawsze **jedna linia**. Podział na pauzach i końcach zdań; przyimki, spójniki i „nie” („w”, „na”, „ze”, „że”, „nie”…) nigdy nie kończą frazy; „%” i interpunkcja trzymają się słowa.
- Pozycja: środek w poziomie strefy bezpiecznej, pionowo `y=1150` – nad podpisem i przyciskami aplikacji, w strefie bezpiecznej 9:16 (góra 250, dół 430, prawo 150 px). Gdy twarz lub ważny obiekt jest w tym miejscu, przesuń `--y` (np. 1350), ale nie poza strefę.
- Pierwsza fraza widoczna od klatki 0 (haczyk).

## Lista kontrolna

- Każde słowo zgadza się z tym, co słychać (sprawdź zwłaszcza nazwy własne, liczby i końcówki: „ziemskiej”, nie „ziemski”).
- Żadna fraza nie łamie się na dwie linie i nie wychodzi poza kadr.
- Napisy nie zasłaniają twarzy ani tekstu na planszach (wtedy zmień `--y`).
- Napisy nie wiszą w ciszy dłużej niż ok. 0,6 s.
- Gotowy film obejrzany jeszcze raz (arkusz klatek) przed oddaniem.
