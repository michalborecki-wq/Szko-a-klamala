# „Szkoła kłamała” – kontekst projektu

Stan na 29.10.2026. Właściciel: Michał Borecki. Język pracy: **polski**.

## Czym jest projekt

- Konto edukacyjne **@szkola_klamala** (Instagram, TikTok): ciekawostki i obalanie mitów ze wszystkich dziedzin, bez twarzy autora i bez treści prywatnych. Obietnica marki: „to, czego szkoła nie powiedziała albo powiedziała źle”.
- Odbiorcy: dorośli, którzy pamiętają polską szkołę. Cel długoterminowy: zasięg, potem sponsoring per przedmiot (oznaczanie reklam zgodnie z rekomendacjami UOKiK).
- **Michał publikuje wszystko ręcznie** w aplikacjach IG i TikTok. **Nie używamy Metricool** (marka blogId 7581117 istnieje, ale nie tworzymy tam szkiców) ani Google Drive. Facebook nie jest podłączony – pomijamy.

## Zasady treści

- Każdy fakt sprawdzony w wiarygodnym źródle w trakcie przygotowania, nie z pamięci. Obliczenia w kodzie. Źródło na slajdzie (krótko) i w podpisie (pełne).
- Teksty pisane od zera, własnymi słowami (od 04.2026 Instagram nie poleca kont z cudzymi lub nieprzetworzonymi treściami).
- **Zakazane:** polityka, religia, szczepionki i spory medyczne, płeć, migracja, teorie spiskowe, atakowanie osób i instytucji, drastyczne treści.
- **Finanse:** tylko mechanizmy; nigdy nazwy instrumentów, banków, funduszy ani kryptowalut. Dopisek „To nie jest porada inwestycyjna”.
- **Prawo:** stan prawny z artykułem i ustawą (ISAP, UOKiK, gov.pl), dopisek „To nie jest porada prawna”, bez polityki.
- **Motoryzacja:** mity kierowców i ciekawostki techniczne (przepisy, ADAC, PZM, ITS), bez reklam marek.
- **Medycyna:** tylko oficjalne źródła (WHO, NFZ, GIS, NHS, CDC, publikacje). Bez porad, dawek, diet, suplementów i szczepionek. Dopisek „To nie jest porada medyczna – w sprawach zdrowia pytaj lekarza”.
- **Wezwania:** najwyżej 1, z powodem („zapisz – przyda się, gdy…”, „wyślij komuś, kto…”) plus prawdziwe otwarte pytanie. Bez „wpisz A albo B”, próśb o polubienia i oznaczania znajomych (engagement bait).
- **Typografia:** półpauza (–), „cudzysłów”, twarde spacje po jednoliterowych wyrazach.

## Plan publikacji (decyzja Michała 29.10)

- **Instagram:** pon.–sob. codziennie 1 Reel „jeden mit”, **min. 4 plansze i min. 20 s** (zwykle 5–6 plansz, 20–25 s; decyzja 29.10): MIT → FAKT z liczbą → rozwinięcie (drugi fakt, skąd mit, jak to sprawdzono) → puenta/pytanie + źródło. Długość z treści, nie z pustego czasu. **Tempo: każda plansza stoi tyle, by przeczytać całość jej informacji** (silnik liczy: wejście napisów + 0,3 s na słowo + 0,8 s i sam wydłuża planszę). Do tego 1 karuzela tygodniowo, jako **jeden** post.
- **TikTok:** 2–3 posty dziennie (ok. 15 tygodniowo): te same Reelsy jako wideo, karuzela w 9:16 i dodatkowe karuzele zdjęć 9:16 (4 slajdy). Godziny: 10:00, 13:00, 18:00.
- **Priorytet tematów:** najbardziej znane mity z szerokim zasięgiem (kosmos, ciało, mózg, medycyna, motoryzacja, prawo w codziennym życiu, pieniądze w codziennym życiu). Węższe tematy (język, ekonomia) rzadziej. Co tydzień co najmniej 3 z: prawo, finanse, motoryzacja, medycyna.
- Muzyka (decyzja 29.10): rolki mają **oryginalny podkład generowany w kodzie + efekty dźwiękowe** zsynchronizowane z animacją (`<id>_muzyka.mp4`, −14 LUFS), zamiast lektora. Dodatkowo `<id>_efekty.mp4` (same efekty), gdy Michał woli dźwięk z trendów w aplikacji. Nigdy cudzych plików MP3.
- Przekazanie materiałów: pliki post po poście (bez ZIP-ów i duplikatów), opisy IG i TikTok w blokach do skopiowania, źródła, propozycje dźwięków.

## Przypomnienia dla Michała (z doświadczenia)

- Karuzela = **jeden post** (zaznacz wszystkie zdjęcia naraz) i format **4:5** (ikona dwóch strzałek), inaczej IG przycina do kwadratu.
- TikTok: wysyłać tylko jedną wersję slajdu na sieć (podwójnie zapisane wersje w galerii dawały duplikat pierwszego zdjęcia).
- Promowanie na TikToku działa tylko dla filmów (TikTok Studio albo tiktok.com/promote/web/main), nie dla karuzel zdjęć. Najpierw 2–3 tygodnie regularnych publikacji, potem promować tylko zwycięzców, małym budżetem, cel „więcej obserwujących”.

## Wnioski z wyników (29.10)

- Reel z jednym mitem (Merkury → Wenus najgorętsza) – 316 wyświetleń; karuzele i pojedyncze zdjęcia – 5–19; dwa inne posty 208 i 256 (prawdopodobnie Reelsy). Reel o urodzinach – 19: sam format nie wystarcza, potrzebny mocny, powszechny mit.

## Zadanie cykliczne – NIE DUBLOWAĆ

- W claude.ai działa zadanie „„Szkoła kłamała” – materiały tygodnia do ręcznej publikacji (IG, TikTok)”, id `trig_012NQ3c9krCrwpm1W16pPmbU`, niedziela 17:32 (Europe/Warsaw). Przygotowuje materiały na pon.–sob. według planu wyżej i wysyła push.
- **Nie twórz drugiego, równoległego zadania** – Michał dostałby podwójne materiały.

## Grafiki

- Silnik: skill `.claude/skills/szkola-klamala-grafiki/` (ładowany automatycznie przez Claude Code), `scripts/render.py` (Playwright + Pillow + ffmpeg), typy slajdów: cover / hero / myth / number / text / versus / bars / quiz / outro. Automatyczne dopasowanie tekstu, strefy bezpieczne 9:16 (góra 250, dół 430, prawo 150 px), minimalne rozmiary czcionek, limit słów, podglądy zbiorcze, MP4 z cichą ścieżką.
  Uruchamianie: `python3 .claude/skills/szkola-klamala-grafiki/scripts/render.py spec.json --out out --sheet --video` (katalog `out/` jest w `.gitignore`).
  Zależności Pythona: `pip install -r requirements.txt` (wersja Playwright zgodna z przeglądarką w `/opt/pw-browsers`; nie uruchamiaj `playwright install`).
- `legacy/` – starszy generator (`gen.py`, `mkreel.py`, `spec_tt.py`) i specyfikacje postów z tygodnia 26–31.10 wraz z tekstami (`TEKSTY_tydzien_26-31.10.md`).
- Styl: tło #0A0E18→#16203A, niebieskie smugi #2F6BFF, żółte akcenty #FFC727, czerwony pędzel #E53935, Inter Display Black Italic w nagłówkach, Inter w treści, ziarno 7%, kropki postępu, znak „SZKOŁA KŁAMAŁA” u góry, handle @szkola_klamala.
- Wymaga czcionki Inter / Inter Display z Black Italic: `fc-list | grep -i "Inter Display"`.

## Wideo: animacje, napisy, montaż

- Narzędzia (darmowe): ffmpeg z libass, faster-whisper (spisywanie mowy offline, model `medium`), auto-editor, Playwright, numpy/scipy (generator muzyki), Piper TTS (lektor – opcja, domyślnie nie używamy). Kontener jest ulotny – na początku sesji z wideo: `bash scripts/instaluj.sh`.
- Skille (`.claude/skills/`): `szkola-klamala-animacje` (animowane rolki: biblioteka efektów `ruch.py` + muzyka `muzyka.py`), `szkola-klamala-napisy` (transkrypcja + napisy PL słowo w słowo w stylu marki), `szkola-klamala-montaz` (montaż nagrań), `szkola-klamala-grafiki` (slajdy i silnik).
- **Rozdzielczość: grafika i napisy zawsze w 4K** (decyzja 29.10): rolki i TikTok 2160×3840, karuzele 4:5 2160×2700 – silnik renderuje z podwójną gęstością pikseli przy tym samym układzie 1080 px CSS; `--hd`/`--draft` tylko do podglądów.
- **Tempo czytania** (decyzja 29.10): człowiek musi zdążyć przeczytać całość informacji ze slajdu – plansza nigdy krótsza niż wejście napisów + 0,3 s/słowo (z etykietą i źródłem) + 0,8 s.
- Poziom: rolki mają wyglądać jak od profesjonalnego grafika / motion designera – urozmaicone efekty (każda rolka inna kombinacja), ale z jednej palety marki; cięcia na bicie muzyki.
- **Zasady montażu (obowiązują przy każdym filmie):**
  1. Na start zapytaj, gdzie trafi film i co ma zrobić widz.
  2. Nigdy nie ruszaj oryginału. Pracuj na kopii.
  3. Wytnij pauzy i gorsze podejścia.
  4. Napisy po polsku, słowo w słowo.
  5. Kolory i krój pisma z plików marki.
  6. Napisy, ikony i plansze zawsze w kadrze.
  7. Pion 9:16 w **4K (2160×3840)**, głośność −14 LUFS.
  8. Zanim powiesz, że skończyłeś, obejrzyj gotowy film jeszcze raz.

## Dokumenty

- `docs/opublikowane.md` – tematy już opublikowane i odrzucone (nie powtarzać w tym samym formacie).
- `docs/zrodla.md` – sprawdzone fakty i źródła do ponownego użycia.
- `docs/profil.md` – bio, teksty TikTok, ustawienia konta.
- `docs/otwarte-sprawy.md` – lista zadań na później.
- `docs/KONTEKST_szkola_klamala.md` – oryginalny dokument przekazania projektu (29.10).
- `docs/archiwum/instagram-mich-bor_SKILL_metricool.md` – dawna wersja skilla treści (z Metricool). **Przy konflikcie obowiązuje ten plik (CLAUDE.md):** bez Metricool i Google Drive, plan publikacji jak wyżej.
