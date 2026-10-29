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

- **Instagram:** pon.–sob. codziennie 1 Reel „jeden mit”, 8–12 s, 3 plansze: MIT → FAKT z liczbą → puenta + źródło. Do tego 1 karuzela tygodniowo, jako **jeden** post.
- **TikTok:** 2–3 posty dziennie (ok. 15 tygodniowo): te same Reelsy jako wideo, karuzela w 9:16 i dodatkowe karuzele zdjęć 9:16 (4 slajdy). Godziny: 10:00, 13:00, 18:00.
- **Priorytet tematów:** najbardziej znane mity z szerokim zasięgiem (kosmos, ciało, mózg, medycyna, motoryzacja, prawo w codziennym życiu, pieniądze w codziennym życiu). Węższe tematy (język, ekonomia) rzadziej. Co tydzień co najmniej 3 z: prawo, finanse, motoryzacja, medycyna.
- Muzykę Michał dodaje ręcznie w aplikacji. Pliki MP4 mają cichą ścieżkę AAC.
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

- Silnik: skill `szkola-klamala-grafiki`, `scripts/render.py` (Playwright + Pillow + ffmpeg), typy slajdów: cover / hero / myth / number / text / versus / bars / quiz / outro. Automatyczne dopasowanie tekstu, strefy bezpieczne 9:16 (góra 250, dół 430, prawo 150 px), minimalne rozmiary czcionek, limit słów, podglądy zbiorcze, MP4 z cichą ścieżką.
  Uruchamianie: `python scripts/render.py spec.json --out out --sheet --video`.
  **Pliki silnika nie są jeszcze w tym repozytorium** – trzeba je dodać z paczki (wraz z `legacy/gen.py` i `examples/przyklad.json`).
- Styl: tło #0A0E18→#16203A, niebieskie smugi #2F6BFF, żółte akcenty #FFC727, czerwony pędzel #E53935, Inter Display Black Italic w nagłówkach, Inter w treści, ziarno 7%, kropki postępu, znak „SZKOŁA KŁAMAŁA” u góry, handle @szkola_klamala.
- Wymaga czcionki Inter / Inter Display z Black Italic: `fc-list | grep -i "Inter Display"`.

## Dokumenty

- `docs/opublikowane.md` – tematy już opublikowane i odrzucone (nie powtarzać w tym samym formacie).
- `docs/zrodla.md` – sprawdzone fakty i źródła do ponownego użycia.
- `docs/profil.md` – bio, teksty TikTok, ustawienia konta.
- `docs/otwarte-sprawy.md` – lista zadań na później.
