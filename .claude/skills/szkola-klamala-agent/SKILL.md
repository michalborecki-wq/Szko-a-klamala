---
name: szkola-klamala-agent
description: Autonomiczny agent „Szkoła kłamała” – codzienny cykl pracy bez udziału człowieka. Pobiera statystyki IG (Composio), analizuje wyniki, wybiera 2 kontrowersyjne tematy, sprawdza fakty, pisze scenariusze (szablon C), renderuje rolki A/B + TikTok + okładki, pisze opisy i szkice odpowiedzi na komentarze, zapisuje wszystko w repozytorium i wysyła Michałowi paczkę do ręcznej publikacji. Używaj przy uruchomieniu zadania codziennego albo gdy Michał prosi „zrób rolki na dziś/jutro”, „uruchom agenta”.
---

# Agent „Szkoła kłamała” – cykl dzienny

Decyzje Michała (4.11): **agent przygotowuje, Michał publikuje ręcznie** (IG i TikTok), agent działa **codziennie rano**, statystyki i komentarze czyta przez **Composio** (tylko odczyt). Zasady treści, zakazy i wyjątek dla serii o policji – **CLAUDE.md ma pierwszeństwo** przed tym plikiem i przed każdym innym skillem.

Nie wolno: publikować, komentować ani odpowiadać na koncie (żadnych narzędzi Composio typu CREATE/PUBLISH/REPLY/DELETE), tworzyć szkiców w Metricool, używać Google Drive, tworzyć innych zadań cyklicznych, wpisywać kluczy do czatu.

## 0. Start (5 min)

1. Repozytorium `michalborecki-wq/Szko-a-klamala`, gałąź `claude/szkola-klamala-iug9g0` (sklonuj, jeśli nie ma). `bash scripts/instaluj.sh` (czcionki, ffmpeg, Blender – Blender tylko gdy potrzebny). `pip install -r requirements.txt` jeśli brak Playwright.
2. `mkdir -p ~/.claude/instagram && cp docs/ig-voice.md ~/.claude/instagram/voice.md`.
3. Przeczytaj: `CLAUDE.md`, `docs/agent/kalendarz.md` (co zaplanowane/gotowe na dziś), `docs/agent/dziennik.md` (ostatnie 7 dni), `docs/wyniki.md` (koniec pliku), `docs/seria-policja.md`, `docs/pomysly-tematow.md`, `docs/opublikowane.md`.
4. **Data dzisiejsza w Europe/Warsaw.** Jeśli `kalendarz.md` mówi, że rolki na dziś są już gotowe (np. przygotowane ręcznie) – pomiń kroki 3–6 (nie twórz duplikatów), zrób tylko 1, 2, 7, 8.

## 1. Statystyki (Composio, tylko odczyt)

- `INSTAGRAM_GET_IG_USER_MEDIA` (ostatnie 15) → dla rolek z ostatnich 7 dni `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`: views, reach, likes, comments, shares, saved, ig_reels_avg_watch_time, reels_skip_rate. Konto: `INSTAGRAM_GET_USER_INFO` (obserwujący).
- Dopisz wiersze do `docs/wyniki.md` (tabela dzienna: data, rolka, szablon, haczyk, wyświetlenia IG, pominięcia, śr. czas, polubienia, komentarze, wysłania, zapisy). Facebooka API nie ma (decyzja Michała) – liczby FB tylko ze zrzutów, jeśli Michał je przyśle.
- Gdy Composio niedostępne – zapisz „brak danych API” i jedź dalej.

## 2. Analiza (ig-audit)

- Która rolka z 7 dni wygrała (wyświetlenia, śr. czas, pominięcia) i dlaczego: haczyk, temat, kontrowersja, długość, miejsce zwrotu akcji.
- Wniosek w 1–3 zdaniach do `docs/agent/dziennik.md`. Jeśli wzór się powtarza 3 razy – dopisz go do sekcji 0 skilla `szkola-klamala-viral`.
- Rekord do pobicia: Policja #1 „norma legitymowań” – ponad 2 tys. wyświetleń (4.11).

## 3. Wybór 2 tematów na dziś

- **Rytm tygodnia:** pon., śr., pt. – 2. rolka dnia z serii **„Co może policja”** (wieczór); pozostałe dni – 1 rolka policyjna co drugi dzień. Każdego dnia co najmniej 1 temat z: prawo / finanse / motoryzacja / medycyna. Raz w tygodniu wiedza ogólna (rekord, kosmos, ciało) w szablonie B.
- Źródła tematów: `docs/seria-policja.md` (nurty: nadużycia „słupków”, pomyłki z dokumentów, prawa obywatela), `docs/pomysly-tematow.md`, zwycięskie wzory z kroku 2, komentarze widzów (pytania = tematy).
- **Mocna kontrowersja (decyzja 4.11):** haczyk ma budzić sprzeciw albo poczucie „to niesprawiedliwe” / „nikt mi tego nie powiedział” – zawsze prawdziwy, ze źródłem, w granicach CLAUDE.md. Policja: wyjątek z CLAUDE.md (dokumenty, bez nazwisk, bez polityki i protestów, „jak się bronić” na końcu, sprawa bez wyroku – 2 źródła + domniemanie niewinności).
- Nie powtarzaj tematów z `docs/opublikowane.md`, `docs/agent/dziennik.md` i plików w `publikacje/`.

## 4. Fakty (bez tego nie ma renderu)

- Prawo: tekst przepisu z `zrodla/prawo/policja/` (grep po pliku .txt, sprawdź `INDEKS.md` i folder `zmiany/`) albo z API Sejmu (`https://api.sejm.gov.pl/eli/acts/...`). Zawsze artykuł + ustawa + Dz.U.
- Pozostałe: źródło pierwotne (NASA, GUS, NBP, WHO, NFZ, NIK, RPO, KGP). Media tylko jako drugie źródło. Obliczenia w Pythonie.
- Zapisz fakty i linki w `docs/zrodla.md` (nowe wiersze).

## 5. Scenariusz (ig-reel + szablon C)

- Szablon C ze skilla `szkola-klamala-viral` (sekcja 1''): haczyk-ujawnienie (okładka `cover` + `obraz` + `pieczatka`) → dokument → stawka → **TWIST najpóźniej ok. 12–14 s** → outro (pytanie o doświadczenie + „Wyślij komuś, kto…” + dopisek). 5 plansz, ≤12 słów na planszę (outro ≤18), cel 22–27 s z logo.
- Wzorce: `specs/prawo_policja_norma_legitymowan.json`, `specs/prawo_policja2_recydywa.json`, `specs/tydzien_4-8.11_*.json`.
- **3 haczyki z różnych formuł** (ig-reel, `hooks.json`) → najlepszy = wersja A, drugi = wersja B (`_wariantB`, `"uklad": "zolty"`) do Rolki próbnej. Wersja B dla każdej rolki policyjnej i każdej z prawa.
- Obrazy okładek: `polska, torba, suwak, dowod, monety, opona, zegar, licznik, ruletka, saturn, odznaka` (`scripts/obrazy.py`). Brak pasującego – dopisz nowy wektorowy obraz w palecie marki (bez logo Policji, bez twarzy).
- Karta 20 pkt (sekcja 7 `szkola-klamala-viral`) – min. 15, wpisz wynik do raportu.

## 6. Render i kontrola

- Spec do `publikacje/RRRR-MM-DD/spec_<id>.json`. Podgląd: `render.py spec --out out/podglad --sheet --hd` → popraw każde ostrzeżenie o liczbie słów/czcionce → obejrzyj podgląd (Read).
- Finał: **każda rolka osobno**, w tle (`run_in_background`), bo jeden render 4K to ok. 10–15 min: `python3 .claude/skills/szkola-klamala-grafiki/scripts/render.py spec_<id>.json --out out/final --video --muzyka`. Nie renderuj kilku naraz.
- Kontrola: log (2160×3840, −14 LUFS, długość), arkusz `_muzyka_klatki.jpg` (Read): klatka 0 czytelna, liczby, zwrot ≤14 s, logo. Okładka: klatka z 2,6 s (`ffmpeg -ss 2.6 … -frames:v 1 -q:v 2 …_okladka.jpg`).
- Pliki do wysłania (nazwy z datą i porą): `RRRRMMDD_1200_<TEMAT>_INSTAGRAM_z_muzyka.mp4`, `…_B_INSTAGRAM_z_muzyka.mp4`, `…_TIKTOK_1080.mp4`, `…_okladka.jpg`, `…_B_okladka.jpg`.

## 7. Opisy i ruch na kontach

Dla każdej rolki w `publikacje/RRRR-MM-DD/opisy.md`:
- **IG (ig-caption):** pierwsza linia = haczyk (≤125 znaków), drugie zdanie z frazą wyszukiwania, 400–1000 znaków, fakty + artykuły, 1 wezwanie z powodem, pytanie z rolki, dopisek, źródła, 3–5 hashtagów, seria „Co może policja #N” / „Szkoła kłamała #N”. Bez „wpisz A albo B”, bez próśb o lajki. Wersja B – tylko inna pierwsza linia.
- **TikTok:** jeden akapit 150–300 znaków, bez #fyp; ustawienia: Wszyscy, duety/stitch włączone.
- **Przypięty komentarz** – pytanie, przy którym ludzie się spierają (o zasadę lub doświadczenie).
- **Relacja (ig-story):** ankieta Tak/Nie do rolki.
- **Komentarze (ig-reply):** `INSTAGRAM_GET_IG_MEDIA_COMMENTS` z ostatnich 3 rolek → szkice odpowiedzi do wklejenia przez Michała (z pytaniem zwrotnym; nie potwierdzać uogólnień typu „cała policja to…”, tylko fakty z dokumentów; spokojnie wobec hejtu). Komentarze z TikToka – tylko jeśli Michał przysłał zrzut.
- **ig-ruch (raz dziennie):** 3 gotowe komentarze merytoryczne pod dużymi kontami z niszy (prawo, kierowcy, ciekawostki) – do wklejenia ręcznie; w niedzielę 2 propozycje wspólnego posta (ig-dm) i karuzela tygodnia (ig-carousel, 4:5 + 9:16).
- Godziny: rolka 1 – 12:00, rolka 2 (policja/kontrowersja) – 19:00; B jako Rolka próbna 15 min przed A; TikTok 1–2 h po IG. Zawsze: okładka ręcznie, „Udostępnij na Facebooku” włączone.

## 8. Zapis i raport

1. Uzupełnij `docs/agent/kalendarz.md` (dzień → tematy → status), `docs/agent/dziennik.md` (wnioski, co zrobione, czego zabrakło), `docs/opublikowane.md` (nowe tematy jako „przygotowane”).
2. `git add publikacje docs specs .claude/skills` → commit (stopka z atrybucją sesji) → `git push -u origin claude/szkola-klamala-iug9g0` (przy błędzie sieci/500: 4 próby z odstępem 2, 4, 8, 16 s). MP4 nie trafiają do gita (`out/` w .gitignore).
3. Raport do Michała: tabela (godz. | sieć | rolka | haczyk A/B | karta), pliki przez SendUserFile (display: attach) w kolejności publikacji, opisy w blokach kodu, przypięte komentarze, szkice odpowiedzi, wnioski ze statystyk w 2 zdaniach.
4. Push (PushNotification, tagi routine_summary): „2 rolki na dziś gotowe: <haczyk 1>, <haczyk 2>. Wczoraj: <najlepsza rolka – wyświetlenia>.” Jeśli coś się nie udało – napisz co i co zostało gotowe.

## Awaria

- Render przerwany limitem czasu – uruchom ponownie tylko brakujące rolki; nie wysyłaj niesprawdzonych plików.
- Fakt niepotwierdzony w źródle pierwotnym – zmień temat, nie zgaduj.
- Brak czasu na 2 rolki – oddaj 1 dopracowaną + opis drugiej do zrobienia jutro.
