# „Szkoła kłamała” – kontekst projektu

Stan na 29.10.2026. Właściciel: Michał Borecki. Język pracy: **polski**.

## Czym jest projekt

- Konto edukacyjne **@szkola_klamala** (Instagram, TikTok): ciekawostki i obalanie mitów ze wszystkich dziedzin, bez twarzy autora i bez treści prywatnych. Obietnica marki: „to, czego szkoła nie powiedziała albo powiedziała źle”.
- Odbiorcy: dorośli, którzy pamiętają polską szkołę. Cel długoterminowy: zasięg, potem sponsoring per przedmiot (oznaczanie reklam zgodnie z rekomendacjami UOKiK).
- **Michał publikuje wszystko ręcznie** w aplikacjach IG i TikTok. **Nie używamy Metricool** (marka blogId 7581117 istnieje, ale nie tworzymy tam szkiców) ani Google Drive. **Facebook: crosspost z Instagrama jest włączony i daje ponad 90% wyświetleń rolek (statystyki 1.11)** – przy publikacji rolki zawsze zostawiać „Udostępnij na Facebooku”. Osobnych postów na FB nie robimy.

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

- **Instagram:** pon.–sob. codziennie 1 Reel „jeden mit”, **min. 4 plansze i min. 20 s** (decyzja 29.10). **Szablon od 1.11: B „stos liczb / rekord”** (skill `szkola-klamala-viral`): haczyk-stwierdzenie zaprzeczające oczywistej odpowiedzi (największy krój, od klatki 0) → wielka liczba → porównanie do Polski/ranking → mocniejsza liczba → „dlaczego” → pytanie-reakcja + „wyślij komuś…” + źródło; 5–6 plansz, maks. ok. 12 słów na planszę, 25–32 s. Szablon A „pętla ciekawości” (odpowiedź na 50–70%) zawieszony, dopóki pominięcia > ok. 60%. Każdy scenariusz oceniany kartą 20 pkt (min. 15) przed renderem. **Nacisk (decyzja 31.10): kilkukrotne obejrzenie (pętla, twist na końcu, liczba do sprawdzenia) i mocna kontrowersja – zawsze prawdziwa, ze źródłem i w granicach zakazanych tematów.** Długość z treści, nie z pustego czasu. **Tempo: każda plansza stoi tyle, by przeczytać całość jej informacji** (silnik liczy: wejście napisów + 0,3 s na słowo + 0,8 s i sam wydłuża planszę). Do tego 1 karuzela tygodniowo, jako **jeden** post.
- **TikTok:** 2–3 posty dziennie (ok. 15 tygodniowo): te same Reelsy jako wideo, karuzela w 9:16 i dodatkowe karuzele zdjęć 9:16 (4 slajdy). Godziny: 10:00, 13:00, 18:00.
- **Priorytet tematów:** najbardziej znane mity z szerokim zasięgiem (kosmos, ciało, mózg, medycyna, motoryzacja, prawo w codziennym życiu, pieniądze w codziennym życiu). Węższe tematy (język, ekonomia) rzadziej. Co tydzień co najmniej 3 z: prawo, finanse, motoryzacja, medycyna.
- Muzyka (decyzja 29.10): rolki mają **oryginalny podkład generowany w kodzie + efekty dźwiękowe** zsynchronizowane z animacją (`<id>_muzyka.mp4`, −14 LUFS), zamiast lektora. Dodatkowo `<id>_efekty.mp4` (same efekty), gdy Michał woli dźwięk z trendów w aplikacji. Nigdy cudzych plików MP3.
- **Dźwięk wg sieci (31.10):** Instagram – nasz podkład `<id>_muzyka.mp4`; TikTok – `<id>_efekty` w 1080 + dźwięk z trendów dodany w aplikacji (oryginał ok. 30%).
- **Serie:** numer „Szkoła kłamała #N” w opisie i małą etykietą na haczyku; serie tematyczne (Mit tygodnia, Prawo, którego nie znasz, Pieniądze bez ściemy).
- **Wyniki (od 2.11):** statystyki Instagrama pobieram sam przez **Composio** (konektor MCP, konto IG `szkola_klamala` połączone; narzędzia `INSTAGRAM_GET_IG_USER_MEDIA` i `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` z metrykami views, reach, likes, comments, shares, saved, ig_reels_avg_watch_time, reels_skip_rate; komentarze `INSTAGRAM_GET_IG_MEDIA_COMMENTS`) → `docs/wyniki.md` → korekta tematów i haczyków. Facebook w Composio – **decyzja Michała 2.11: nie łączymy**; wyświetlenia z Facebooka (crosspost) tylko ze zrzutu „Statystyki rolki” w aplikacji IG, gdy potrzebne. Composio nie publikuje – Michał publikuje ręcznie.
- Przekazanie materiałów: pliki post po poście (bez ZIP-ów i duplikatów), opisy IG i TikTok w blokach do skopiowania, źródła, propozycje dźwięków.

## Przypomnienia dla Michała (z doświadczenia)

- Rolka na IG: **ustaw okładkę ręcznie** (Edytuj okładkę → Dodaj z galerii → `_okladka.jpg`) i zostaw włączone **„Udostępnij na Facebooku”** – stamtąd przychodzi ponad 90% wyświetleń.

- Karuzela = **jeden post** (zaznacz wszystkie zdjęcia naraz) i format **4:5** (ikona dwóch strzałek), inaczej IG przycina do kwadratu.
- TikTok: wysyłać tylko jedną wersję slajdu na sieć (podwójnie zapisane wersje w galerii dawały duplikat pierwszego zdjęcia).
- Promowanie na TikToku działa tylko dla filmów (TikTok Studio albo tiktok.com/promote/web/main), nie dla karuzel zdjęć. Najpierw 2–3 tygodnie regularnych publikacji, potem promować tylko zwycięzców, małym budżetem, cel „więcej obserwujących”.

## Wnioski z wyników (29.10)

- **1.11 (zrzut statystyk):** próg bazowy rolki 200–340 wyświetleń; rekordy po **1,1 tys.**: Francja – 12 stref czasowych i ISS – grawitacja. Wzór: wiedza ogólna typu rekord/zaskakująca odpowiedź, haczyk podważa oczywistą odpowiedź („nie ma Rosja”), jedna wielka liczba + ranking/porównanie, „dlaczego” na końcu. Prawo/finanse/święta – na progu (210–290). **Zero polubień, komentarzy i wysłań wszędzie** → każda rolka kończy się pytaniem, na które każdy zna swoją odpowiedź. Karuzele/zdjęcia/relacje na IG: 3–18. **Statystyki szczegółowe: >90% wyświetleń z Facebooka (crosspost), pominięcia 73–96%, średni czas 2–3 s → wszystko rozstrzyga pierwsza klatka; najlepszy haczyk to stwierdzenie zaprzeczające oczywistej odpowiedzi (Francja 73% pominięć), najgorszy – pytanie „…? Sprawdźmy.” (ISS 96%). Szablon B domyślny, A zawieszony; okładka zawsze ręcznie z `_okladka.jpg`.** Szczegóły: `docs/wyniki.md`. Cel Michała: 100 tys. wyświetleń – skill `szkola-klamala-viral` (sekcje 0, 0a; szablon B domyślny), silnik domyślnie w trybie `"moc": "mocna"` (kadr nigdy nie stoi, puls na bicie).
- Reel z jednym mitem (Merkury → Wenus najgorętsza) – 316 wyświetleń; karuzele i pojedyncze zdjęcia – 5–19; dwa inne posty 208 i 256 (prawdopodobnie Reelsy). Reel o urodzinach – 19: sam format nie wystarcza, potrzebny mocny, powszechny mit.

## Zadanie cykliczne – NIE DUBLOWAĆ

- W claude.ai działa zadanie „„Szkoła kłamała” – materiały tygodnia do ręcznej publikacji (IG, TikTok)”, id `trig_012NQ3c9krCrwpm1W16pPmbU`, niedziela 17:32 (Europe/Warsaw). Przygotowuje materiały na pon.–sob. według planu wyżej i wysyła push.
- **Nie twórz drugiego, równoległego zadania** – Michał dostałby podwójne materiały.
- **Tydzień 2–7.11: rolki IG przygotowane ręcznie 1.11 (`docs/plan-2-7.11.md`)** – zadanie tygodniowe w tym tygodniu nie robi nowych rolek. Dokłada tylko posty uzupełniające (karuzele TikTok, karuzela IG) i nie powtarza tych tematów.

## Grafiki

- Silnik: skill `.claude/skills/szkola-klamala-grafiki/` (ładowany automatycznie przez Claude Code), `scripts/render.py` (Playwright + Pillow + ffmpeg), typy slajdów: cover / hero / myth / number / text / versus / bars / quiz / outro. Automatyczne dopasowanie tekstu, strefy bezpieczne 9:16 (góra 250, dół 430, prawo 150 px), minimalne rozmiary czcionek, limit słów, podglądy zbiorcze, MP4 z cichą ścieżką.
  Uruchamianie: `python3 .claude/skills/szkola-klamala-grafiki/scripts/render.py spec.json --out out --sheet --video` (katalog `out/` jest w `.gitignore`).
  Zależności Pythona: `pip install -r requirements.txt` (wersja Playwright zgodna z przeglądarką w `/opt/pw-browsers`; nie uruchamiaj `playwright install`).
- **taste-skill** (2.11, `.claude/skills/taste-skill/`, MIT, Leonxlnx/taste-skill v2.1.5, commit 12af471): art direction dla stron WWW, landingów i ekranów aplikacji (biblioteka kierunków, inspektor w przeglądarce). Do rolek i plansz nadal obowiązuje `szkola-klamala-grafiki`; taste-skill przydaje się np. do strony/linku w bio. Skrypty wymagają Node 22 i `CHROME_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`.
- **mcp-builder** (2.11, `.claude/skills/mcp-builder/`, anthropics/skills, commit ca45fc4, Apache 2.0): przewodnik budowy własnych serwerów MCP (Python FastMCP / TypeScript). Kandydaci: statystyki TikToka (brak gotowego konektora w Composio), lokalne narzędzie do weryfikacji aktów prawnych przez API Sejmu (ELI/ISAP). Klucze API zawsze w ustawieniach środowiska, nigdy w czacie.
- **claude-automation-recommender** (2.11, `.claude/skills/claude-automation-recommender/`, z wtyczki Anthropic `claude-code-setup`, claude-plugins-official commit a7ba5b9, Apache 2.0): tylko analizuje projekt i poleca automatyzacje (hooki, skille, serwery MCP, subagenci); niczego sam nie zmienia.
- **Agent skills (2.11)** w `.claude/skills/`:
  - z anthropics/skills (commit ca45fc4): frontend-design, canvas-design, algorithmic-art, theme-factory, web-artifacts-builder, webapp-testing, slack-gif-creator, doc-coauthoring, internal-comms, academy-guide, discernment-nudge (docx/pdf/pptx/xlsx/skill-creator są już w koncie; `brand-guidelines` pominięty – to marka Anthropic, nie nasza);
  - z vercel-labs/agent-skills (commit 1a2c79d): react-best-practices, composition-patterns, react-view-transitions, react-native-skills, web-design-guidelines, writing-guidelines, deploy-to-vercel, vercel-cli-with-tokens, vercel-optimize – tylko przy stronie WWW.
  - Paleta, kroje i styl rolek zawsze z `szkola-klamala-grafiki`; ogólne skille projektowe (frontend-design, canvas-design, theme-factory, taste-skill) nie nadpisują stylu marki.
- **Marketing (2.11)** – skille z wtyczki Anthropic `marketing` (anthropics/knowledge-work-plugins, commit 2574e29, Apache 2.0): content-creation, draft-content, campaign-plan, brand-review, competitive-brief, performance-report, seo-audit, email-sequence. Konektory wtyczki (HubSpot, Ahrefs, Similarweb itd.) nie są podpięte; Canva i Notion działają z konta. Zasady treści, zakazane tematy i plan publikacji z tego pliku mają pierwszeństwo przed ogólnymi poradami marketingowymi (np. bez wezwań typu „wpisz A albo B”).
- **Canva skills (2.11)** – oficjalne skille Canvy (canva-sdks/canva-skills, commit 906e8e0, Apache 2.0) w `.claude/skills/canva-*`: edit-design, implement-feedback, design-feedback, brand-check, resize-for-social-media, bulk-create. Działają przez konektor Canva z konta (już połączony). Edycje w Canvie są szkicem do zatwierdzenia – zatwierdzać dopiero po akceptacji Michała. Rolki i plansze nadal renderuje nasz silnik; Canva służy do analizy, poprawek i wersji pod inne formaty.
- **Social Media (2.11)** – skill `social` z coreyhaines31/marketingskills (commit 88c79f6, MIT), `.claude/skills/social/`: posty, karuzele, scenariusze krótkich wideo, recykling treści, kalendarz, nasłuch. Część o publikowaniu przez agenta i narzędzia do planowania (np. Postiz) **nie dotyczy nas** – Michał publikuje ręcznie. Przy konflikcie obowiązuje ten plik i skill `szkola-klamala-viral`.
  Z tej samej kolekcji: `video` (produkcja wideo – u nas silnik `render.py`/Blender, bez awatarów AI i bez twarzy autora; płatne usługi tylko po zgodzie Michała, klucze w ustawieniach środowiska), `influencer-marketing` (współprace – reklamy oznaczane wg UOKiK), `community-marketing` (budowanie społeczności, bez engagement bait).
- **Projektowanie graficzne (2.11)** – skille z wtyczki Anthropic `design` (anthropics/knowledge-work-plugins, commit 2574e29, Apache 2.0): design-critique (recenzja plansz i okładek), design-system (spisanie systemu marki), accessibility-review (kontrast, czytelność), ux-copy, design-handoff, user-research, research-synthesis. Razem z canvas-design, frontend-design, theme-factory, taste-skill i skillami Canvy; styl marki zawsze z `szkola-klamala-grafiki`.
- **Finanse (2.11)** – skille z wtyczki Anthropic `finance` (anthropics/knowledge-work-plugins, commit 2574e29, Apache 2.0): księgowość firmowa (financial-statements, variance-analysis, reconciliation, journal-entry, journal-entry-prep, close-management, audit-support, sox-testing; standardy głównie USA). **Nie są źródłem do rolek** – rolki finansowe dalej wg zasad z tego pliku: tylko mechanizmy, polskie źródła (KNF, GUS, NBP, ISAP), dopisek „To nie jest porada inwestycyjna”.
- **Prawo (2.11)** – skille z wtyczki Anthropic `legal` (anthropics/knowledge-work-plugins, commit 2574e29, Apache 2.0): review-contract (umowy sponsorskie), compliance-check (np. oznaczanie reklam wg UOKiK, RODO), legal-risk-assessment, legal-response, triage-nda, brief, meeting-briefing, vendor-check, signature-request (konektory e-podpisu niepodłączone). To narzędzia pomocnicze, nie porada prawna; wzorce są ogólne/amerykańskie, więc prawo polskie zawsze z ISAP/API Sejmu. **Nie są źródłem do rolek** – rolki prawne dalej wg zasad z tego pliku (artykuł + ustawa, „To nie jest porada prawna”).
- `legacy/` – starszy generator (`gen.py`, `mkreel.py`, `spec_tt.py`) i specyfikacje postów z tygodnia 26–31.10 wraz z tekstami (`TEKSTY_tydzien_26-31.10.md`).
- **Okładki rolek (1.11, analiza w Canvie):** nigdy sam tekst – obraz-bohater tematu (`"obraz"`: polska/torba/suwak/dowod/monety, `scripts/obrazy.py`), pieczątka (`"pieczatka"`) i zmienny układ (`"uklad": "zolty"`). Folder w Canvie: „Szkoła kłamała – rolki (analiza)”.
- Styl: tło #0A0E18→#16203A, niebieskie smugi #2F6BFF, żółte akcenty #FFC727, czerwony pędzel #E53935, Inter Display Black Italic w nagłówkach, Inter w treści, ziarno 7%, kropki postępu, znak „SZKOŁA KŁAMAŁA” u góry, handle @szkola_klamala.
- Wymaga czcionki Inter / Inter Display z Black Italic: `fc-list | grep -i "Inter Display"`.

## Wideo: animacje, napisy, montaż

- Narzędzia (darmowe): ffmpeg z libass, faster-whisper (spisywanie mowy offline, model `medium`), auto-editor, Playwright, numpy/scipy (generator muzyki), Piper TTS (lektor – opcja, domyślnie nie używamy). Kontener jest ulotny – na początku sesji z wideo: `bash scripts/instaluj.sh`.
- Skille (`.claude/skills/`): `szkola-klamala-animacje` (animowane rolki: biblioteka efektów `ruch.py` + muzyka `muzyka.py`), `szkola-klamala-napisy` (transkrypcja + napisy PL słowo w słowo w stylu marki), `szkola-klamala-montaz` (montaż nagrań), `szkola-klamala-grafiki` (slajdy i silnik).
- **3D (31.10):** Blender 4.2 (darmowy, `scripts/instaluj.sh`), skill `szkola-klamala-3d` – sceny 3D w palecie marki renderowane Cycles na CPU (ok. 40 min na 23 s) i podkładane pod plansze polem `"tlo3d"` w poście. Higgsfield (płatny, AI) wymaga konektora albo kluczy `HF_API_KEY`/`HF_API_SECRET` w ustawieniach środowiska – jeszcze niepodłączony.
- **Rozdzielczość: grafika i napisy zawsze w 4K** (decyzja 29.10): rolki i TikTok 2160×3840, karuzele 4:5 2160×2700 – silnik renderuje z podwójną gęstością pikseli przy tym samym układzie 1080 px CSS; `--hd`/`--draft` tylko do podglądów.
- **Wyjątek TikTok** (29.10): edytor TikToka po wczytaniu pionowego filmu 4K wyświetla obraz podwójnie (jeden pod drugim). Na TikTok zawsze idzie `<id>_tiktok_1080.mp4` (1080×1920 z mastera 4K, H.264 High@4.1) – `muzyka.py` robi go automatycznie. Instagram – plik 4K `<id>_muzyka.mp4`; gdyby IG pokazał ten sam błąd, też dać wersję 1080.
- **Tempo czytania** (decyzja 29.10): człowiek musi zdążyć przeczytać całość informacji ze slajdu – plansza nigdy krótsza niż czas przeczytania całości (0,3 s/słowo z etykietą i źródłem, z zapasem; silnik liczy i wydłuża sam). Dlatego w rolce maks. ok. 15 słów na planszę – rolka 6 plansz ma wtedy 25–30 s.
- **Logo twórcy na końcu każdego filmu** (decyzja 30.10): ok. 2,8 s animowanego outro z logo „Szkoła kłamała” (`.claude/skills/szkola-klamala-grafiki/assets/logo.png`) i handle @szkola_klamala – `render.py --video` dokleja je automatycznie (`logo_outro.py`), muzyka zgrywa uderzenie z wejściem logo. Wyłączenie tylko na wyraźną prośbę: `"logo": false` w poście.
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
- `docs/pomysly-tematow.md` – bank tematów z haczykami (finanse – mechanizmy; prawo – „co mogą, a czego nie mogą” policja i ochrona), ze statusem sprawdzenia; brać stąd tematy do planu tygodnia.
- `docs/profil.md` – bio, teksty TikTok, ustawienia konta.
- `docs/otwarte-sprawy.md` – lista zadań na później.
- `docs/analiza-konkurencji-2026-10.md` – konkurencja i sygnały algorytmów IG/TikTok (podstawa szablonu pętli ciekawości).
- `docs/wyniki.md` – wyniki rolek (temat, haczyk, długość, wyświetlenia, wysłania, czas oglądania).
- `docs/KONTEKST_szkola_klamala.md` – oryginalny dokument przekazania projektu (29.10).
- `docs/archiwum/instagram-mich-bor_SKILL_metricool.md` – dawna wersja skilla treści (z Metricool). **Przy konflikcie obowiązuje ten plik (CLAUDE.md):** bez Metricool i Google Drive, plan publikacji jak wyżej.
