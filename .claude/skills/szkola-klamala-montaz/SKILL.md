---
name: szkola-klamala-montaz
description: Montaż nagrań wideo dla „Szkoła kłamała” (@szkola_klamala) według 8 zasad montażu – kopia oryginału, wycięcie pauz i gorszych podejść, pion 9:16 w 4K (2160×3840), napisy po polsku słowo w słowo, kolory i krój marki, wszystko w kadrze, głośność −14 LUFS, ponowne obejrzenie gotowego filmu. Używaj ZAWSZE, gdy Michał przysyła nagranie (głos, ekran, kamera, lektor) do zmontowania, skrócenia, „wycięcia ciszy”, przerobienia na Reel/TikTok, wyrównania głośności albo przygotowania do publikacji – także przy „zmontuj”, „przytnij”, „zrób z tego rolkę”.
---

# Montaż „Szkoła kłamała”

Skrypt: `.claude/skills/szkola-klamala-montaz/scripts/montaz.py` (ffmpeg + faster-whisper), podgląd: `scripts/klatki.py`. Napisy – skill **szkola-klamala-napisy**; animowane plansze i przerywniki – **szkola-klamala-animacje**. Instalacja narzędzi: `bash scripts/instaluj.sh` w katalogu głównym repozytorium.

## Zasady montażu (8)

1. **Na start zapytaj, gdzie trafi film i co ma zrobić widz.** Zanim cokolwiek utniesz: sieć (Reel IG / TikTok / oba), cel (obejrzeć do końca, zapisać, wysłać komuś, wejść na profil) i ewentualny limit długości. Od tego zależą haczyk, tempo, długość i ostatnia plansza. Jeśli Michał już to napisał – nie pytaj drugi raz.
2. **Nigdy nie ruszaj oryginału. Pracuj na kopii.** `montaz.py przygotuj` kopiuje plik do katalogu pracy i sprawdza sumę SHA-256; wszystkie etapy (`1_ciete`, `2_pion`, `3_napisy`, `GOTOWE`) to osobne pliki. Nie nadpisuj i nie usuwaj niczego w miejscu, z którego przyszło nagranie.
3. **Wytnij pauzy i gorsze podejścia.** Skrypt na podstawie transkrypcji proponuje cięcia: pauzy dłuższe niż ok. 0,45 s (z oddechem 0,12 s) i wcześniejsze podejścia, gdy zdanie zostało powtórzone (zostaje ostatnie). Przejrzyj `ciecia.json` i listę ✂ – popraw, jeśli skrypt uciął coś potrzebnego. Na łączeniach są mikro-przenikania dźwięku (bez trzasków).
4. **Napisy po polsku, słowo w słowo.** Transkrypcja po cięciach + obowiązkowa korekta + wypalenie – według skilla `szkola-klamala-napisy`.
5. **Kolory i krój pisma z plików marki.** Wyłącznie tokeny marki: granat #0A0E18/#16203A, niebieski #2F6BFF, żółty #FFC727, czerwony #E53935, Inter Display Black Italic w nagłówkach i napisach, Inter w treści (`szkola-klamala-grafiki/references/design-system.md`). Plansze, okładki i przerywniki rób silnikiem grafik/animacji, nie ręcznie.
6. **Napisy, ikony i plansze zawsze w kadrze.** Strefa bezpieczna 9:16: góra 250 px, dół 430 px, prawo 150 px (interfejs IG/TikToka). Poziome nagranie: `--kadr blur` (całe ujęcie na rozmytym tle marki) albo `--kadr crop` (wypełnienie, gdy ważny obiekt jest w środku). Sprawdź na arkuszu klatek, że nic nie jest ucięte.
7. **Pion 9:16 w 4K (2160×3840), głośność −14 LUFS.** Zasada Michała: grafika i napisy zawsze w 4K – słabsze nagranie skaluje się filtrem lanczos, a napisy i plansze renderują się natywnie w 4K. `montaz.py wykoncz` normalizuje dźwięk dwuprzebiegowo (EBU R128) do −14 LUFS ±1, szczyt poniżej −1 dBTP, i raportuje wynik. Film bez dźwięku dostaje cichą ścieżkę AAC; muzyka – oryginalny podkład z `szkola-klamala-animacje/scripts/muzyka.py` albo dźwięk z trendów dodany w aplikacji. Nigdy cudzych MP3.
8. **Zanim powiesz, że skończyłeś, obejrzyj gotowy film jeszcze raz.** Wynik `kontrola` (wymiary, kl./s, dźwięk, LUFS) + arkusz klatek przeczytany narzędziem Read. Szukaj: uciętych słów na cięciach, napisów rozjeżdżających się z mową, czegokolwiek poza kadrem, czarnych klatek. Dopiero potem wyślij plik (SendUserFile, jeden MP4 na sieć, bez ZIP-ów).

## Polecenia

```bash
M=.claude/skills/szkola-klamala-montaz/scripts
python3 $M/montaz.py przygotuj nagranie.mov --praca praca/odcinek1     # kopia + transkrypcja + propozycja cięć
#   → przejrzyj praca/odcinek1/ciecia.json
python3 $M/montaz.py zloz praca/odcinek1 --kadr blur                   # cięcia + pion + transkrypcja do napisów
#   → popraw praca/odcinek1/2_pion.slowa.json, potem polecenie „wypal” wypisane przez skrypt
python3 $M/montaz.py wykoncz praca/odcinek1                            # −14 LUFS + kontrola + arkusz klatek
python3 $M/montaz.py kontrola dowolny_film.mp4                         # sama kontrola gotowego pliku
```

Katalog `praca/` trzymaj poza repozytorium albo w `out/` (jest w `.gitignore`) – nagrania nie trafiają do gita.

## Raport dla Michała

Krótko: co wycięto (ile sekund, które podejścia), długość przed/po, wynik kontroli (4K 2160×3840, LUFS), plik gotowy do publikacji, proponowany dźwięk z biblioteki IG / trendów TikToka, opis IG i TikTok w blokach do skopiowania (zasady treści – `CLAUDE.md`).
