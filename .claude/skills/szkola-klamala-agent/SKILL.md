---
name: szkola-klamala-agent
description: Autonomiczny agent „Szkoła kłamała” – 3 dostawy dziennie: 9:00 rolka (IG + TikTok), 13:00 karuzela 9:16 tylko na TikTok, 18:00 rolka. Każda rolka = 5 plików (IG 4K, TikTok 1080, okładka, wklejka do relacji, opis IG/TikTok z przypiętym komentarzem). Rano dodatkowo statystyki IG (Composio, odczyt) i research fabryki. Sprawdza fakty w 2 źródłach, pisze scenariusz (szablon C, haczyk „porównanie niesprawiedliwości”, pełne animacje), dobiera koszyk TikTok Shop, zapisuje w repozytorium. Nigdy nie publikuje – Michał publikuje ręcznie. Używaj przy uruchomieniu zadania cyklicznego albo gdy Michał prosi „zrób rolkę na dziś/jutro”, „uruchom agenta”.
---

# Agent „Szkoła kłamała” – cykl dzienny

## DOSTAWA – obowiązuje od 6.11 (decyzja Michała 5.11, ma pierwszeństwo przed krokami 3–8 poniżej)

„Zróbmy tak: dwie rolki plus jeden post koło 13.” (5.11; wcześniej 4.11: „Nie chcę bałaganu.”)

Zadanie uruchamia się 3 razy dziennie (7:23, 11:23, 16:23 Europe/Warsaw). Godzina startu < 10 → **dostawa 9:00** (rolka), < 14 → **dostawa 13:00** (post TikTok), inaczej → **dostawa 18:00** (rolka).

**13:00 – post tylko na TikTok:** karuzela zdjęć 9:16 z 4 slajdów (`"format": "vertical"`, typy cover → number → number/text → outro), wiedza ogólna w szablonie B (kosmos, ciało, mózg, rekordy), temat inny niż obie rolki dnia, bez policji, fakty w ≥2 źródłach jak zawsze. `dostawa.py` sam rozpozna format i odda `<TEMAT>_TIKTOK_01..04.jpg` + `_opis.md` (tylko opis TikTok + przypięty komentarz). Karuzela zdjęć nie ma koszyka TikTok Shop. Jeśli Michał przysłał zdjęcia produktu z Showcase, zamiast karuzeli zrób film produktowy (wzór: MAG5, `docs/tiktok-shop.md`) – tylko fakty z etykiety, oznaczenia jak przy koszyku.

1. Start (krok 0). Rano (dostawa 9:00) także kroki 1, 2 i 2a (statystyki, wnioski, research fabryki) – ich wyników **nie wysyłasz** Michałowi, tylko zapisujesz w repo (wyjątek: pobity rekord albo coś pilnego – 1 zdanie w wiadomości).
2. W `docs/agent/kalendarz.md` znajdź wiersz: dzisiejsza data + Twoja pora.
   - Źródło `spec: plik#post_id` → scenariusz gotowy, tylko render.
   - **NOWA** → wybierz 1 temat (kroki 3–5: fabryka/seria policyjna, fakty w ≥2 źródłach, szablon C, karta 20 pkt ≥15), zapisz spec w `publikacje/RRRR-MM-DD/spec_<id>.json` i wpisz go do kalendarza. **Tylko wersja A** – bez wariantu B i bez lektora.
   - Brak wiersza → dopisz go zgodnie z zasadą w nagłówku kalendarza i potraktuj jak NOWA.
   - Status „wysłane” → nic nie renderuj, nie wysyłaj drugi raz.
3. Opis: `publikacje/RRRR-MM-DD/<HHMM>_opis.md` – wyłącznie: **Instagram** (blok do skopiowania), **TikTok** (blok), **Przypięty komentarz** (1 linia), **Relacja** (1 linia). Gotowy tekst weź z pliku wskazanego w kalendarzu (bez linii o wersji B i lektorze); dla NOWEJ napisz go wg kroku 7. Sprawdź, czy daty i liczby w opisie są aktualne na dzień publikacji (np. „zostało N dni”) – popraw w Pythonie.
4. Render (w tle, jedna rolka): `python3 VIRAL_REELS_FACTORY/narzedzia/dostawa.py <spec> <post_id> --opis publikacje/RRRR-MM-DD/<HHMM>_opis.md` → `VIRAL_REELS_FACTORY/DOSTAWA/<data>_<HHMM>/` z 4 plikami. Kontrola: arkusz klatek (Read) – tekst w kadrze, żadnych urwanych słów, liczby, zwrot ≤14 s, logo; log: 2160×3840, −14 LUFS. Błąd → popraw spec i renderuj ponownie (zapas czasu ok. 1 h).
5. Wysyłka **od razu po kontroli** (zmiana 9.11: czekanie na 8:50/12:50/17:50 pętlą w tle kończyło sesję zadania przed wysyłką – karuzela 9.11 nie dotarła; Michał publikuje o pełnej godzinie sam). Jedna wiadomość:
   - SendUserFile (display: attach, status: proactive) – rolka: dokładnie 4 pliki w kolejności `_INSTAGRAM.mp4`, `_TIKTOK.mp4`, `_okladka.jpg`, `_opis.md`; post 13:00: slajdy `_TIKTOK_01..04.jpg` + `_opis.md`;
   - pod spodem: nagłówek „Rolka 9:00 – <haczyk>” (albo „Post 13:00”, „Rolka 18:00”), opis IG i opis TikTok w blokach kodu, przypięty komentarz, 1 linia przypomnienia („okładka ręcznie, Udostępnij na Facebooku, TikTok – dźwięk z trendów ok. 30%”). Nic więcej – bez tabel TOP 10, bez raportów, bez wariantów.
   - PushNotification: „<Rolka/Post> na <9:00/13:00/18:00> gotowy: <haczyk>”.
6. Zapis: kalendarz → „wysłane”, 1–2 zdania do `docs/agent/dziennik.md`, `docs/opublikowane.md` (temat jako „wysłany do publikacji”), commit + push (krok 8.2). Pliki wideo nie idą do gita.
6a. **TikTok Shop – koszyk w każdej rolce (decyzja Michała 5.11, `docs/tiktok-shop.md`):** wybierz 1 produkt z `docs/tiktok-shop-produkty.md`, który naturalnie pasuje do tematu (rolka o nawigacji → uchwyt; policja → etui na dokumenty, wideorejestrator; kosmos → luneta). Render z `--reklama "<marka>"` (etykieta tylko na pliku TikTok). Opis TikTok zaczyna się od „Reklama:”, a jego ostatnie zdanie łączy temat z produktem bez obietnic spoza karty produktu. W wiadomości 1 linia: „Koszyk: <produkt> – dodaj go przy publikacji i włącz Treści komercyjne”. Lista pusta albo nic nie pasuje → bez `--reklama`, bez „Reklama:”, a w wiadomości 1 linia „Koszyk: dodaj do Showcase <propozycja>”. Suplement diety: render z `--suplement` (ostrzeżenie na pliku TikTok), to samo ostrzeżenie w opisie TikTok, tylko oświadczenia z karty produktu, nigdy pod rolką o chorobach/leczeniu/medycynie. Nigdy produktów z listy „Nigdy”.
7. Nie da się zdążyć albo fakt się nie potwierdził → wyślij o czasie gotową rolkę zapasową z kalendarza (najbliższy wiersz ze `spec:` i statusem „do wysłania”) i napisz 1 zdanie, dlaczego. Nigdy nie wysyłaj niesprawdzonej rolki.

**Viral – stałe zasady (decyzja Michała 6.11: „skup się na viralowych rolkach, kolorystyka zostaje, animacje, przede wszystkim kontrowersja”):**
- **Pakiet każdej rolki = 5 plików:** `_INSTAGRAM.mp4`, `_TIKTOK.mp4`, `_okladka.jpg`, **`_relacja.jpg`** (wklejka do relacji – `dostawa.py --relacja "nagłówek z *akcentem*|podtekst"`, nagłówek ≤6 słów, inny niż haczyk rolki), `_opis.md` (IG, TikTok, przypięty komentarz, ankieta do relacji, 3 szkice odpowiedzi na komentarze).
- **Haczyk – najpierw formuła „porównanie niesprawiedliwości”** (X surowiej niż Y, choć Y groźniejsze – wzór 6.11: „Mocną wiatrówkę rejestrujesz. Broń palną sprzed 1885 – nie.”), dopiero potem zaprzeczenie oczywistej odpowiedzi. Każdy człon porównania sprawdzony w tekście przepisu. 6 haczyków → karta 20 pkt → zwycięzca.
- **Styl wizualny od 9.11 (decyzja Michała 8.11: „Twórz rolki w takim stylu”) – Dynamic Visual Engine**, skill `szkola-klamala-dynamic-visual`: `"moc": "mocna"`, `"ton"` posta (PRAWO, POLITYKA, HISTORIA, KOSMOS, NAUKA, MOTORYZACJA, FINANSE, KONTROWERSJA, CIEKAWOSTKA) – preset sam dobiera otwarcie, przejścia i akcenty, więc **nie wpisuj na sztywno `fx.haczyk`/`fx.otwarcie`/`fx.przejscie`** (tylko gdy coś trzeba poprawić po kontroli); `"muzyka": {"nastroj": "napiecie", "bpm": 110}` dla prawa/policji; liczby `"count": true`; zwrot akcji jako plansza z tagiem/`myth_label` „TWIST” (stop-klatka). **W każdej rolce opartej na przepisie lub dokumencie – plansza `dokument`** z DOSŁOWNYM fragmentem (ISAP/API Sejmu/`zrodla/prawo/`), `**wyróżnieniem**` kluczowej frazy i nagłówkiem z aktem i artykułem (projekt oznacz „druk nr …”), plus `"wskaz"` – 2–4 słowa redakcji wskazujące stawkę (np. „Tu jest kara”; linia od dokumentu do etykiety, od 9.11); przy datach/terminach – `timeline`; cytat tylko dosłowny (`quote`). Nigdy fikcyjnych dokumentów. **Temat z newsa (decyzja 9.11):** plansza `wycinek` z DOSŁOWNYM nagłówkiem PAP (Polska) albo Reutersa (świat) – agencja i data zwykłym tekstem, link w opisie, maks. 20 słów; nagłówek sprawdzony na stronie artykułu (pap.pl blokuje automat → tytuł z Google News + drugie źródło, dopisek w `zrodla.md`). **Zdjęcie** – plansza `foto` tylko z `VIRAL_REELS_FACTORY/narzedzia/zdjecia.py` (CC0, domena publiczna/NASA, CC BY, CC BY-SA; nigdy NC/ND, nigdy zdjęcia ani logo agencji, nigdy zdjęcia bez autora i licencji); ilustracja AI tylko z `"ilustracja_ai": true`. Szukanie zdjęcia: `zdjecia.py --szukaj "fraza"` (najlepiej CC0/PD/CC BY; CC BY-SA tylko w całości, pełna atrybucja z linkiem do licencji w opisie). **Miejsce w temacie** (miasto, województwo, kraj) – plansza `mapa` z punktami ze współrzędnych ze źródła. Bez zdjęć ofiar, rannych, sprawców i miejsc tragedii. Spec z kalendarza (SPEC) bez pól `fx` dostaje nowy styl automatycznie; dodanie planszy `dokument` z dosłownym tekstem jest dozwolone (forma, nie zmiana tematu). **Przed wysyłką:** `python3 .claude/skills/szkola-klamala-dynamic-visual/scripts/kontrola.py <plik_TIKTOK.mp4> --zdarzenia <…_zdarzenia.json>` i obejrzyj `_2s.jpg` (haczyk czytelny w każdej klatce 0–2 s) oraz `_przejscia.jpg`; kod wyjścia 1 i „⚠ BŁĄD” w wydruku (migotanie, czarne klatki, kadr stoi > 4 s, zła rozdzielczość, brak audio) = popraw przed wysyłką.
- **Wyniki 9.11 (`docs/analiza-wynikow-2026-11-09.md`):** najmniej pominięć mają haczyki z obietnicą ukrytej stawki („…Jest haczyk.”, „Połowa – bezprawnie”, „…zostają dłużej”) – 63–74% wobec mediany 86%; same stwierdzenia lub gołe liczby („Pod szlabanem tracisz prawo jazdy”, „Ochroniarz…”) – 94–98%. Pierwsza rolka DVE (ZUS) – najlepsza na koncie. W IG 0 udostępnień i 0 zapisów: wezwanie „wyślij komuś” daj też na ostatniej planszy, nie tylko w opisie.
- **Slot NEWS / link od Michała:** skill `szkola-klamala-sledczy` (`python3 VIRAL_REELS_FACTORY/narzedzia/sledczy.py`).
- **Bez obrazów broni, emoji 🔫 i tagów #bron** – regulaminy IG/TikTok tną zasięg; temat broni tylko przez dokumenty i przepisy.
- Fakty: 1 agent-fact-checker (adwersaryjny) przed renderem rolki z nowym tematem; sporne interpretacje (np. proch) – nie na planszy.

Kroki poniżej (0–8) opisują, JAK robić research, fakty, scenariusz i opis. Tam, gdzie mówią o 2 rolkach, wariancie B, lektorze, raporcie TOP 10 albo godzinach 12:00/19:00 lub 17:00 – obowiązuje sekcja DOSTAWA.

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

## 2a. Fabryka – research i ranking (codziennie, VIRAL_REELS_FACTORY)

1. `cd VIRAL_REELS_FACTORY/narzedzia && python3 research.py` → `RESEARCH/<data>/naglowki.md` (RSS z 72 h).
2. Z nagłówków i z WebSearch wybierz ok. 12–15 kandydatów we wszystkich kategoriach A–E (A: bieżące decyzje i absurdy prawa – **polityka tylko jako fakty**; B: ciekawostki; C: pieniądze, praca, codzienność; D: technologia i AI; E: dylematy, podwójne standardy). Dla każdego: oceny 1–10 (emocje, dyskusja, aktualność, zaskoczenie, film, udostępnienia), źródła z datami, `weryfikacja`, `rodzaj`, `granice` → `TOPICS/<data>/tematy.json` (wzór: `TOPICS/2026-11-04/tematy.json`).
3. `python3 ranking.py` → `TOP10.md` + `top3.json`. Do produkcji tylko tematy dopuszczone (fakt, ≥2 niezależne źródła, w granicach). Nie wymyślaj aktualności; strona niedostępna (np. 403) = szukaj innego źródła albo odrzuć.
4. Dla TOP 3: `python3 nowa_rolka.py <nazwa> --tytul "…" [--lektor]` (lektor: 1 rolka dziennie, decyzja 4.11) → wypełnij `scenariusz.md` (3 warianty: kontrowersyjny / ciekawostkowy / emocjonalny + rekomendacja + karta 20 pkt + tekst lektorski), `spec.json` (A, `_wariantB`, opcjonalnie `_lektor`), `opis.md`, `zrodla.md`, `meta.json`. Wzory: `SCRIPTS/2026-11-04_*`.
5. Produkcja: `python3 produkcja.py <rid>` w tle, rolka po rolce (2 rolki na dziś; trzecia – scenariusz na zapas). Gotowe paczki: `READY_TO_PUBLISH/<rid>/` (pliki, okładki, opis, LISTA.md).
6. Statystyki: wpisz wyniki z Composio i zrzutów (`python3 analityka.py dodaj …` albo `import`), raz w tygodniu `python3 analityka.py raport` → wnioski do kroku 2.

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
