# Przekazanie do Claude Code – Dynamic Visual Engine + wycinki i zdjęcia (9.11.2026)

Repo: `michalborecki-wq/Szko-a-klamala`, gałąź `claude/szkola-klamala-iug9g0`.
Ostatni commit z tej sesji: `e46ab98` („Dynamic Visual Engine 9.11: RGB, światło, głębia 2.5D…”).
Hierarchia zasad bez zmian: `CLAUDE.md` → skill `szkola-klamala-redakcja` → decyzje Michała → `docs/agent/kalendarz.md`.

---

## 1. Co zostało ZROBIONE i wypchnięte (commit e46ab98)

Brief Michała: „SKILL: SZKOŁA KŁAMAŁA – DYNAMIC VISUAL ENGINE” (ten sam, który 8.11 dał skill `szkola-klamala-dynamic-visual`). 9.11 rano Michał kazał go „dopracować (grafika, efekty specjalne), zapisać i wykorzystać”. Dopracowano istniejący skill i silnik – bez drugiej fabryki.

**`.claude/skills/szkola-klamala-grafiki/scripts/ruch.py`**
- otwarcie `rgb` – rozszczepienie kanałów w czerwieni #E53935 i niebieskim #2F6BFF marki: w 0 s (amp 16), drugie uderzenie 0,52 s z `kPunch` i wstrząsem, echo 1,45 s; w rotacji presetów KONTROWERSJA (pierwsze na liście), MOTORYZACJA, POLITYKA;
- przejście `swiatlo` – złote prześwietlenie (element `.leak`, `mix-blend-mode:screen`, przesuw przez kadr + brightness/blur treści); presety HISTORIA, KOSMOS, CIEKAWOSTKA, PRAWO; mocne – maks. 1–2 na rolkę;
- `fx.rgb` (domyślnie true w KONTROWERSJA/MOTORYZACJA/POLITYKA) – RGB przy każdym `impact()`; stop‑klatka na zwrocie zawsze dostaje RGB (amp 9);
- `fx.glebia` (true przy `moc: mocna`) – treść `perspective(1800px) rotateX(≤0,9°) rotateY(≤1,4°)` wg czasu globalnego `g`, tło `.fxbg` przesuwa się przeciwnie (paralaksa), obraz‑bohater okładki (`.hero-ill`) ma własne `scale`/`translate` (bliższy plan);
- `dokument`: po markerach najazd „kamery” na wyróżnienie (`window.__dolly`, origin = środek karty w poziomie i wyróżnienie w pionie, `amt` ograniczony tak, by karta została ≥50 px od krawędzi);
- `"wskaz"` w `dokument`: SVG‑łamana rysuje się (0,45 s) z dolnej krawędzi karty pod wyróżnieniem do żółtej etykiety `.doc-wsk` (linia NIE przecina tekstu dokumentu);
- poprawka starego błędu: w przejściu `warstwy` ramka `brk` jedzie z warstwą (`b.kid`), a w `warstwy`/`swiatlo` gaśnie `vis^3`;
- pomiar pozycji w `__layout` przy wyczyszczonej transformacji treści.

**`render.py`** – pole `"wskaz"` (2–4 słowa redakcji) w planszy `dokument` + CSS `.doc-wsk`.

**`.claude/skills/szkola-klamala-dynamic-visual/scripts/kontrola.py`** – pomiary automatyczne → `<id>_kontrola.json`: rozdzielczość, kl./s, audio, migotanie poza przejściami, czarne klatki, najdłuższy nieruchomy kadr (błąd > 4 s, bez ostatnich 3 s logo), ruch średni i 0–2 s, LUFS (błąd tylko dla plików `*muzyka*`/`*INSTAGRAM*`; TikTok/efekty celowo cichsze). Kod wyjścia 1 = „⚠ BŁĄD”. Test negatywny (kadr stoi 6 s) – wykryty.

**Skille:** `szkola-klamala-dynamic-visual/SKILL.md` (tabele efektów, presety, sekcja 7 Ograniczenia, sekcja 8 Historia zmian), `szkola-klamala-agent/SKILL.md` (dodano `"wskaz"` i interpretację kodu wyjścia kontroli).

**Demo (nie do publikacji):** `specs/demo_silnik/demo_dve.json` = ta sama treść co `demo.json` + nowe moduły. Render 1080p z muzyką ok. 8 min / 42 s. Wynik vs 8.11: ruch średni 1,03 → 1,32 (+28%), najdłuższy stojący kadr 0,43 s w obu, LUFS −14,0, kontrola bez błędów. **Uczciwie:** otwarcie `rgb` w pomiarze 0–2 s słabsze od `ramka` (2,39 vs 2,71) – dlatego tylko w rotacji, nie zamiast ramki. 4K z nowymi efektami jeszcze nierenderowane (pierwszy raz w dostawie 18:00 9.11).

---

## 2. Decyzja Michała 9.11 (10:51): wycinki i zdjęcia – wariant „bez kosztów”

Michał chciał wycinków i zdjęć z Google, PAP (Polska) i Reutersa (świat). Ustalono:
- **PAP i Reuters NIE są źródłem zdjęć** – obie agencje zastrzegają prawa (Reuters: zakaz kopiowania/ponownej publikacji bez pisemnej zgody; PAP – serwisy licencjonowane). Płatna licencja (PAP zdjęcia, Reuters Connect) – **odrzucona**, budżet 0 zł.
- **PAP (Polska) i Reuters (świat) = źródło faktów i nagłówków.** „Wycinek” = NASZA plansza z dosłownym, krótkim nagłówkiem agencji (cytat, prawo cytatu art. 29 pr. aut.), nazwą agencji zwykłym tekstem i datą; link w opisie. **Nie** podróbka zrzutu ekranu, **bez** logo i layoutu agencji.
- **Zdjęcia:** wyszukiwanie przez Google Grafika z filtrem „Prawa użytkowania → Licencje Creative Commons”, ale licencję zawsze weryfikuje się na stronie źródłowej (najczęściej Wikimedia Commons). Dozwolone: CC0, domena publiczna (np. NASA), CC BY, CC BY‑SA. **Odrzucać NC i ND** (konto ma sponsorów; zdjęcie przycinamy i nakładamy grafikę). Podpis na planszy: autor + licencja (+ serwis). Ilustracja AI zawsze z etykietą „Ilustracja – nie jest zdjęciem wydarzenia”.
- Do zapisania w `CLAUDE.md` (sekcja „Zasady treści”) jako decyzja 9.11 – **jeszcze nie zapisane**.

---

## 3. DO ZROBIENIA (przerwane w trakcie – nic z tego nie jest jeszcze w kodzie)

### 3.1 Plansza `wycinek` (render.py + ruch.py)
Pola: `agencja` („PAP” | „Reuters”), `data` („8.11.2026”), `naglowek` (DOSŁOWNIE z artykułu, `**wyróżnienie**`), `link` (do opisu, nie renderowany), opcjonalnie `tlumaczenie` (Reuters po angielsku → „tłum. red.: …”), `wskaz`, `tag`, `title/accent`, `source` (domyślnie „Źródło: {agencja}, {data}”).
Walidacja w Pythonie (twardy błąd `ValueError`): brak `agencja`/`data`/`link`; `naglowek` > 20 słów (prawo cytatu – krótko).
Plan HTML: `<div class='doc wyc'><div class='wyc-k'>NAGŁÓWEK · {agencja} · {data}</div><div class='doc-t wyc-t' data-fit>„…”</div>[<div class='wyc-tl'>tłum. red.: …</div>]</div>` – klasy `doc` + `.doc-t` dają za darmo wjazd `kDocIn`, markery, najazd kamery i `wskaz` z ruch.py (gałąź `el.matches('.doc')`).
Styl `.wyc`: papier gazetowy (#F2EEE3, delikatne linie), poszarpane krawędzie `clip-path`, pochylenie przez **`rotate: -1.6deg`** (właściwość indywidualna – `transform` nadpisuje animacja), pasek taśmy `::before` (półprzezroczysty żółty). `.wyc-k` – małe kapitaliki Inter 700, szary #5B6170; `.wyc-t` – Georgia bold, ok. `body*1.25`, line-height 1.2. Dodać `.wyc-t` do listy dopasowania w `FIT_AND_QA` (jest tam `.doc-t`).

### 3.2 Plansza `foto`
Pola: `zdjecie` (ścieżka względem katalogu repo albo bezwzględna, np. `zrodla/zdjecia/<slug>.jpg`) – metadane czytane automatycznie z pliku obok `<slug>.json` (autor, licencja, zrodlo/URL, serwis); ręcznie: `autor`, `licencja`, `zrodlo`. `uklad`: `ramka` (domyślnie – zdjęcie jako odbitka/karta z taśmą, odsłonięcie maską) albo `pelny` (pełny kadr z paralaksą; QA: zdjęcie min. ok. 1600 px wysokości, inaczej ostrzeżenie/zmiana na `ramka`). `ilustracja_ai: true` → etykieta zamiast podpisu autora. Plus zwykłe `tag`, `title/accent`, `body`, `wskaz`.
Walidacja: brak licencji/autora/źródła → `ValueError`; licencja z NC/ND → `ValueError`.
Obraz osadzać jako `data:` URI (base64) – strona idzie przez `pg.set_content`. Korzeń repo ze ścieżki skryptu: `Path(__file__).resolve().parents[3]`.
Ruch (ruch.py, `__setT`): dwie warstwy – tył (rozmyty, większy, wolniejszy: scale 1,08→1,14, Y −10→+10 px) i przód (ostry, z maską gradientową, szybszy: scale 1,00→1,10, X 0→−30, Y +20→−30 px) → złudzenie głębi; razem z `fx.glebia`. Odsłonięcie fotografii: maska (clip-path inset) + krótki błysk. Pełny kadr: warstwę zdjęcia wstawić w `body` obok `.bg` (nie w `.content` – `.content` ma marginesy stref bezpiecznych i transformacje), np. przez dodatkowy fragment HTML zwracany z `tpl` (dziś `tpl` składa stronę w liniach ~345–349: `<div class='bg'>…<div class='content {cls}'>{b}</div>`). Podpis „Fot. … · CC BY‑SA 4.0” w strefie bezpiecznej (nad dolnym marginesem 430 px).
Do demo (bez sieci w sesji): `/usr/local/lib/python3.13/dist-packages/skimage/data/astronaut.png` (NASA, domena publiczna; 512×512 → tylko `uklad: ramka`) lub `matplotlib/mpl-data/sample_data/grace_hopper.jpg` (US Navy, domena publiczna).

### 3.3 Narzędzie `VIRAL_REELS_FACTORY/narzedzia/zdjecia.py`
- `--commons "File:Nazwa.jpg"` lub URL strony Commons → API `https://commons.wikimedia.org/w/api.php?action=query&titles=…&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=2400&format=json` → `extmetadata.LicenseShortName/Artist/LicenseUrl/AttributionRequired`, odrzuć NC/ND, pobierz miniaturę 2400 px do `zrodla/zdjecia/<slug>.jpg` + `<slug>.json` (autor bez HTML, licencja, url licencji, strona źródłowa, data pobrania);
- `--nasa <nasa_id>` → `https://images-api.nasa.gov/asset/<id>` + metadata (domena publiczna; uwaga na zdjęcia z dopiskiem o prawach osób trzecich);
- `--plik <lokalny> --autor --licencja --zrodlo` – gdy Michał sam pobierze; ta sama walidacja;
- User‑Agent zwykły (bez e‑maila Michała). Testować offline na spreparowanym JSON (ta sesja nie ma sieci – `curl` → 403 na proxy); środowisko agenta dziennego sieć miało (RSS 4.11 działał).

### 3.4 Nagłówki agencji w porannym researchu
`VIRAL_REELS_FACTORY/narzedzia/zrodla_rss.json` – dodać (typ „agencja”):
- `https://news.google.com/rss/search?q=site:pap.pl&hl=pl&gl=PL&ceid=PL:pl` (PAP; bezpośredni RSS PAP padał 4.11: „mismatched tag” – blokada Incapsula),
- `https://news.google.com/rss/search?q=site:reuters.com&hl=en-US&gl=US&ceid=US:en` (Reuters – świat).
Tytuł z RSS to tylko punkt wyjścia: przed wycinkiem agent sprawdza dosłowny nagłówek i datę na stronie artykułu (WebFetch). Jeden cytat na źródło, < 15–20 słów.

### 3.5 Dokumentacja i zasady
- `szkola-klamala-dynamic-visual/SKILL.md`: typy `wycinek`, `foto`, `zdjecia.py`, zasady licencji; usunąć z „Ograniczeń” zdania o braku wycinków/zdjęć (mapy dalej brak); historia zmian.
- `szkola-klamala-agent/SKILL.md` i `szkola-klamala-redakcja/SKILL.md` (sekcja 7a, dowody): kiedy `wycinek` (temat z newsa – PAP/Reuters), kiedy `foto`; zakaz zdjęć bez licencji, zakaz zdjęć/logo agencji.
- `CLAUDE.md` → „Zasady treści”: decyzja 9.11 (patrz pkt 2).
- Demo: `specs/demo_silnik/demo_wycinek_foto.json`, render `--video --hd --muzyka`, `kontrola.py` (+ obejrzeć `_2s.jpg`, `_przejscia.jpg`), poprawki, commit + push na `claude/szkola-klamala-iug9g0`.

---

## 4. Jak uruchamiać (przypomnienie)

```bash
python3 .claude/skills/szkola-klamala-grafiki/scripts/render.py specs/demo_silnik/demo_dve.json --out /tmp/out --video --hd --muzyka
python3 .claude/skills/szkola-klamala-dynamic-visual/scripts/kontrola.py /tmp/out/DEMO_silnik_prawo_muzyka.mp4 --przed <stara>.mp4
```
Pakietów nie instalować w sesjach bez sieci; Playwright z `/opt/pw-browsers`. Produkcja zawsze 4K (`--hd` tylko podglądy). Nie publikować niczego – Michał publikuje ręcznie. Jedno zadanie cykliczne (`trig_01SeXEiKGkqsPEVp6gZ8TnTi`) – nie tworzyć drugiego.
