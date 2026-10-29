---
name: "instagram-mich-bor"
description: "Tygodniowy plan i szkice 5 materiałów „Szkoła kłamała” (konto Michała, Metricool) publikowanych na Instagramie, Facebooku i TikToku – ciekawostki i mity ze wszystkich dziedzin, 2 wideo + 3 karuzele, styl z logo, gotowe na reklamodawców. Używaj przy każdej prośbie o posty, Reelsy, TikToki, karuzele lub harmonogram „Szkoła kłamała”, także gdy pada tylko nazwa jednej sieci."
---

# „Szkoła kłamała” – tygodniowe szkice na Instagram, Facebook i TikTok

Konto Michała (dawniej @mich_bor_, docelowo @szkola_klamala) z ciekawostkami i obalaniem mitów ze **wszystkich dziedzin wiedzy**, po polsku, bez twarzy autora i bez treści o jego życiu prywatnym. Spoiwem marki nie jest jedna dziedzina, tylko obietnica: „to, czego szkoła nie powiedziała albo powiedziała źle”. Wszystko trafia do Metricool jako **szkic** – nic nie publikuje się bez akceptacji Michała (otwiera szkic w Metricool i go planuje).

## Dane techniczne

- Metricool: `blogId` zawsze odczytuj z `getBrandSettings` – to marka, której `networksData.instagramData` = `szkola_klamala` (stan na 22.10.2026: `7581117`, konto Metricool michalboria@proton.me). Strefa `Europe/Warsaw`. Handle do slajdów bierz z tego samego pola. Jeśli żadna marka nie ma tego konta albo jest ich kilka – nie zgaduj, opisz sytuację w raporcie i nie twórz szkiców.
- Przed planowaniem: `getBrandSettings`, `getScheduledPosts` na 7 dni naprzód i 4 tygodnie wstecz (bez powtórek tematów, kontrola rotacji przedmiotów), `getBestTimeToPostByNetwork` (instagram) – 5 slotów w różne dni, nigdy dwa posty jednego dnia.
- Wymagania konta: plan Metricool Starter (Google Drive, brak limitu 20 postów), Instagram typu **Firma** połączony ze stroną na Facebooku „Szkoła kłamała” i podłączony do Metricool przez Facebook Login (wymagane do muzyki w Reelsach); TikTok @szkola_klamala podłączony w tej samej marce Metricool.
- Instagram jest siecią główną (to pod nią planujesz tematy i godziny); Facebook i TikTok dostają te same materiały w wersji dopasowanej do sieci – szczegóły w sekcji „Facebook i TikTok”.

## Przedmioty („lekcje”) – rotacja

Każdy post ma przypisany przedmiot, widoczny na slajdzie/planszy 1 jako etykieta „SZKOŁA KŁAMAŁA · [PRZEDMIOT]”. To trzyma szeroką tematykę w jednej, rozpoznawalnej ramie (ten sam format, kąt i odbiorca – dorośli pamiętający polską szkołę) i ułatwia sprzedaż sponsoringu per przedmiot.

| Przedmiot | Przykładowe tematy | Naturalni reklamodawcy |
|---|---|---|
| Historia | mity historyczne, zapomniane wydarzenia, absurdy dawnych epok, historia Polski | wydawnictwa, muzea, VOD z dokumentami, turystyka |
| Geografia | dziwne granice, rekordy natury, „mapa kłamie” (odwzorowanie Merkatora), kraje i miasta | biura podróży, linie lotnicze, outdoor |
| Matematyka | paradoksy (Monty Hall, paradoks urodzin), sztuczki liczbowe, prawdopodobieństwo w życiu | aplikacje edukacyjne, korepetycje, gry logiczne |
| Fizyka | fizyka codzienności, mity („ciężkie spada szybciej”), zjawiska wyjaśnione prosto | kursy, gadżety naukowe, centra nauki |
| Chemia | chemia w kuchni i domu, mity o „chemii w jedzeniu” | AGD, marki kuchenne, centra nauki |
| Biologia i ciało | mity o zdrowiu i ciele (bez porad medycznych), zwierzęta, ewolucja | marki sportowe, zoo, wydawnictwa |
| Kosmos | skala Wszechświata, mity o kosmosie, misje kosmiczne | planetaria, teleskopy, VOD |
| Finanse | procent składany, inflacja, psychologia pieniądza, mity finansowe | banki, aplikacje finansowe, edukacja finansowa |
| Ekonomia | jak działają ceny, rynki, ciekawostki gospodarcze, historia pieniądza | media biznesowe, kursy, wydawnictwa |
| Psychologia | błędy poznawcze, efekty psychologiczne, nawyki, komunikacja | aplikacje do rozwoju, wydawnictwa, kursy |
| Język polski | pochodzenie słów, błędy językowe, „poprawna” polszczyzna, ciekawostki | wydawnictwa, aplikacje językowe |
| Technologia | jak działa internet/telefon, mity technologiczne, wynalazki | elektronika, operatorzy, aplikacje |

Zasady rotacji:
- 5 postów tygodniowo = 5 różnych przedmiotów; pełny cykl 12 przedmiotów w ok. 2,5 tygodnia. Żaden przedmiot nie wraca częściej niż raz na tydzień, dopóki statystyki nie pokażą wyraźnego lidera.
- Po 4–6 tygodniach sprawdź `getAnalyticsDataByMetrics` w podziale na przedmioty i formaty. Główna miara: **udostępnienia (sends) na zasięg**, potem wyświetlenia i czas oglądania; zapisy pomocniczo. Przedmioty z najlepszym wynikiem dostają 2 sloty w tygodniu, najsłabsze rzadziej. Opisz zmianę w raporcie.
- Gdy jest okazja (święto, rocznica, głośne wydarzenie naukowe, sezon), podmień jeden post na treść okolicznościową z pasującego przedmiotu.

## Tygodniowy miks 5 postów (2 Reelsy + 3 karuzele)

Reelsy najlepiej docierają do osób spoza obserwujących – dla nowego konta to główne źródło wzrostu. Karuzele pogłębiają relację i dają zapisy.

| # | Format | Przykład | Cel |
|---|---|---|---|
| 1 | Reel „Ciekawostka tygodnia” (8–20 s) | „Kleopatra żyła bliżej iPhone'a niż piramid” | zasięg do nowych osób, udostępnienia |
| 2 | Karuzela „Mit vs fakt” (5 mitów, 7 slajdów) | „5 mitów o kosmosie, w które wierzysz” | udostępnienia, zapisy |
| 3 | Karuzela „wyjaśniam” albo „opowieść” (naprzemiennie co tydzień) | „Dlaczego mapa świata kłamie” / „Człowiek, który przeżył dwie bomby atomowe” | zapisy, czas oglądania |
| 4 | Karuzela „Spór tygodnia” | „Kopernik – Polak czy Niemiec?” | komentarze, dyskusja |
| 5 | Reel „Quiz w piątek” (pytanie → 3 s na odpowiedź → rozwiązanie, 10–20 s) | „Który z tych faktów jest fałszywy?” | czas oglądania, powtórne obejrzenia |

- **Trial Reels:** jeden z dwóch Reelsów utwórz jako `TRIAL_REEL` (pokazywany najpierw tylko nieobserwującym). Jeśli Metricool odrzuci typ (funkcja niedostępna na koncie) – utwórz zwykły `REEL` i odnotuj w raporcie raz.
- Najsilniejszy mit z karuzeli może wrócić jako Reel w kolejnym tygodniu (inne ujęcie, nie kopia).

## Kontrowersja – trzy poziomy

1. **Zaskakująca prawda** (posty 1, 2, 3, 5) – fakty sprzeczne z intuicją lub szkolną wiedzą, twardo udokumentowane. Rdzeń marki.
2. **Spór tygodnia** (post 4, dokładnie 1 na tydzień) – pytanie, w którym specjaliści naprawdę się spierają albo odpowiedź zależy od definicji. Przykłady: „Kopernik – Polak czy Niemiec?”, „Pluton – planeta czy nie?”, „Czy Kolumb odkrył Amerykę?”, „Czy pieniądze dają szczęście?”, „Czy pomidor to owoc?”, „Kto naprawdę wynalazł żarówkę?”.
3. **Kontrowersje światopoglądowe – nigdy:** polityka, religia, szczepionki i spory medyczne, płeć, migracja, teorie spiskowe, atakowanie konkretnych osób, grup lub instytucji (także konkretnych szkół, nauczycieli, podręczników i wydawców). Gdy temat sporu choćby ociera się o te obszary – wybierz inny.

Zasady „Sporu tygodnia”:
- Spór musi być realny i merytoryczny – po obu stronach stoją wiarygodne źródła lub uznani specjaliści. Nie wolno sztucznie robić sporu z faktu ustalonego.
- Struktura karuzeli (maks. 10 slajdów): okładka z pytaniem → kontekst → „ARGUMENTY ZA” (2 slajdy) → „ARGUMENTY PRZECIW” (2 slajdy) → „Co mówią źródła” (stan wiedzy, bez wyroku) → ostatni slajd z otwartym pytaniem merytorycznym.
- **Bez formuł typu „wpisz A albo B”, „oznacz znajomego”, „daj like jeśli…”** – Instagram traktuje je jako engagement bait i nie poleca takich postów. Zamiast tego otwarte pytanie: „Który argument jest dla Ciebie najmocniejszy – i dlaczego?”, „Znasz źródło, które to rozstrzyga?”.
- Obie strony uczciwie i w równej objętości, każdy argument ze źródłem. Konto nie ogłasza zwycięzcy; może wskazać, w którą stronę skłania się większość badaczy, jeśli tak jest.
- Etykieta okładki: „SPÓR TYGODNIA · [PRZEDMIOT]”. Etykiety slajdów: „ZA” niebieska `#2F6BFF`, „PRZECIW” czerwona `#E53935` (pochylone jak MIT/FAKT).
- Przedmiot sporu też podlega rotacji – nie dwa tygodnie z rzędu z tego samego przedmiotu.
- W raporcie zaznacz, że post jest „Sporem tygodnia”, i krótko uzasadnij, dlaczego temat jest bezpieczny (poziom 2, nie 3). Przy tematach narodowościowych (np. Kopernik) przypomnij o filtrze komentarzy (Ukryte słowa).

## Oryginalność – warunek polecania

Od kwietnia 2026 r. Instagram nie poleca nieobserwującym kont, które w ciągu ok. miesiąca publikują głównie cudze lub nieprzetworzone treści – dotyczy to także karuzel i zdjęć. Podanie źródła ani znak wodny nie wystarczają.
- Każdy tekst pisany od zera, własnymi słowami i w głosie marki; nigdy przeklejanie zdań ze źródeł, cudzych list „10 faktów” ani tłumaczenie gotowych postów z zagranicznych kont.
- Własne grafiki z szablonu; zdjęcia archiwalne tylko jako element własnego projektu, z licencją (domena publiczna lub CC z atrybucją autor/licencja/link w podpisie).
- Rozpoznawalny głos: stałe zwroty marki („Szkoła mówiła… A naprawdę…”), ten sam układ, ta sama etykieta.
- Raz w miesiącu przypomnij Michałowi w raporcie o sprawdzeniu „Stanu konta” (Ustawienia → Stan konta) – czy konto jest kwalifikowane do polecania.

## Haczyki, podpisy, hashtagi

- Plansza/slajd 1 i pierwsza linia podpisu = haczyk: kontrast („Szkoła mówiła… Nie.”), liczba („5 mitów…”), oskarżenie w duchu marki („Tego w szkole Ci nie powiedzieli”), luka ciekawości („Dlaczego…?”). Haczyk musi się uczciwie spełnić.
- **Slajd 2 karuzeli musi działać samodzielnie jako drugi haczyk** – Instagram pokazuje karuzelę ponownie, zaczynając od slajdu 2.
- Każdy post buduj wokół jednego twierdzenia, które chce się **wysłać komuś** („muszę to pokazać…”) – udostępnienia w wiadomościach to najsilniejszy sygnał dotarcia do nowych osób.
- Podpis 400–1000 znaków: rozwinięcie jednego najciekawszego wątku + źródło („Źródło: …”) + co najwyżej jedno naturalne wezwanie (np. „Zapisz na później” albo merytoryczne pytanie), bez próśb o oznaczanie znajomych czy lajki.
- **SEO:** w pierwszych zdaniach podpisu naturalne polskie frazy, których ktoś mógłby szukać (np. „ciekawostki historyczne”, „mity o kosmosie”). Do każdego obrazu tekst alternatywny (`mediaAltText`) opisujący treść slajdu. Publiczne posty kont profesjonalnych trafiają do Google.
- **Hashtagi: 3–5 na końcu podpisu (`text`), nie w pierwszym komentarzu** (Metricool nie dodaje pierwszego komentarza pod Reelsami; Instagram dopuszcza maks. 5). Zestaw: #szkolaklamala + 1 szeroki (#ciekawostki, #wiedza) + 1–3 pod przedmiot i temat.
- Ton: przystępny, zadziorny, z humorem, bez wykładu i bez atakowania nauczycieli, maks. 3 emoji.
- Polska typografia: półpauza (–), cudzysłów „…”, w HTML twarde spacje ( ) po jednoliterowych spójnikach i przyimkach.

## Rzetelność – twardo

Największe ryzyko reputacyjne konta to własny błąd („konto o kłamstwach szkoły kłamie”).
- Każdy fakt sprawdzony w wiarygodnym źródle (encyklopedia, publikacja naukowa, instytucja publiczna, uczelnia, muzeum, renomowane media) w trakcie przygotowania – nie z pamięci. Źródło w podpisie i w raporcie.
- Fakt sporny lub źródła się różnią – pomiń albo napisz „według…”, „szacuje się”.
- Matematyka i fizyka: każde obliczenie i wynik policz w kodzie przed publikacją.
- **Finanse i ekonomia: wyłącznie pojęcia i mechanizmy** (procent składany, inflacja, historia pieniądza, błędy poznawcze w finansach). **Nigdy nie wymieniaj ani nie sugeruj konkretnych instrumentów** – spółek, ETF-ów, funduszów, obligacji konkretnych emitentów, kryptowalut – nawet jako przykładu; nawet pośrednia sugestia może być rekomendacją inwestycyjną w rozumieniu MAR, a dopisek „to nie porada” przed tym nie chroni. Dopisek „To nie jest porada inwestycyjna” zostaje jako uzupełnienie. Liczby (inflacja, stopy) tylko aktualne i ze źródłem (GUS, NBP).
- Biologia i ciało: bez porad medycznych, diet i suplementacji; mity zdrowotne tylko z oficjalnym źródłem (WHO, NFZ, publikacje).
- Psychologia: tylko efekty potwierdzone badaniami; bez diagnoz i porad terapeutycznych.
- Zero polityki bieżącej i tematów światopoglądowych, zero treści o tragediach, w których żyją bliscy ofiar, bez szokowania przemocą.
- Bez kopiowania cudzych tekstów, grafik, memów i muzyki spoza biblioteki IG.
- Gdy po publikacji wyjdzie błąd – w raporcie zaproponuj korektę (edycja podpisu + komentarz przypięty „Poprawka: …”).

## Gotowość na reklamodawców

- **Brand safety jako warunek:** bez polityki, wulgaryzmów, drastycznych obrazów, teorii spiskowych i kontrowersji religijnych. Prowokacja tylko w nazwie i haczykach, treść rzetelna.
- **Sponsoring per przedmiot:** tabela przedmiotów wyżej podaje naturalnych reklamodawców; dobieraj część tematów tak, żeby każdy przedmiot miał serię postów, którą da się zaoferować jednej marce („Lekcja finansów z…”). Niczego nie reklamuj przed umową.
- **Stałe serie:** „Ciekawostka tygodnia”, „Mit vs fakt”, „Spór tygodnia”, „Quiz w piątek”, „Polecam przeczytać” (rekomendacja książki/dokumentu na końcu karuzeli, na start bez sponsora). Ostatni slajd ma zarezerwowane miejsce na logo partnera (na razie puste).
- **Dane do media kitu:** w pierwszą niedzielę miesiąca dołącz podsumowanie z `getAnalyticsDataByMetrics`: obserwujący i przyrost, średnie wyświetlenia, udostępnienia, zapisy i zaangażowanie na post, top 3 posty, ranking przedmiotów i formatów. Po ok. 5 tys. obserwujących lub średnich wyświetleniach stabilnie powyżej 10 tys. zaproponuj media kit i listę marek do własnego kontaktu (na tym etapie marki rzadko zgłaszają się same).
- **Oznaczanie reklam (rekomendacje Prezesa UOKiK):** wyraźnie i na początku – „Reklama” / „Współpraca reklamowa z [marka]” na slajdzie 1 lub w pierwszej linii podpisu, plus „Oznaczenie płatnego partnerstwa” na Instagramie. Dotyczy też barteru, prezentów i linków afiliacyjnych. Nigdy w ukryciu.
- **Żadnej oferty współpracy nie przyjmuj automatycznie** – przekaż Michałowi.

## Grafiki – styl z logo „Szkoła kłamała”

Logo Michała: białe i żółte pędzlowe litery, niebieskie smugi, czerwone podkreślenie, złota poświata na czarnym tle. Karuzele i plansze Reelsów mają z nim tworzyć spójną siatkę.

- Karuzele: 1080 × 1350 px (4:5), **maks. 10 slajdów** (limit Metricool), HTML + Playwright, **eksport do JPEG (sRGB, jakość ~92)** – Instagram przyjmuje JPEG.
- Font Inter (nagłówki 900 italic, wersaliki; tekst merytoryczny 400 prosty).
- Tło: `radial-gradient(ellipse at 50% 35%, #16203A 0%, #0A0E18 70%)` + dwie ukośne niebieskie smugi `#2F6BFF` (lewy górny i prawy dolny róg, `rotate(-24deg)`, przezroczystość 0,4–0,55).
- Nagłówki białe z cieniem `0 6px 0 #2F6BFF`; drugi wiersz/akcent żółty `#FFC727` z poświatą `0 0 40px rgba(255,199,39,.35)`; pod tytułem okładki czerwone podkreślenie `#E53935` (16 px, zaokrąglone, `rotate(-3deg)`).
- Etykiety pochylone (`skew(-8deg)`): „MIT” czerwona `#E53935`, „FAKT” niebieska `#2F6BFF`. Mit przekreślony cienko (4 px, czerwony), tekst mitu szary `#BFC3CC`.
- Duże numery 01–05 żółte, 900 italic, z poświatą. Tekst merytoryczny `#E8E8E8`, 42 px.
- Stałe elementy: żółta belka i „n/N” u góry, handle w lewym dolnym rogu (`#9AA3B5`), „przesuń →” żółte w prawym (poza ostatnim slajdem). Etykieta okładki: „SZKOŁA KŁAMAŁA · [PRZEDMIOT]”.
- Maks. ~30 słów na slajd; slajd 1 = haczyk; slajd 2 = drugi haczyk; ostatni = pytanie (+ puste miejsce na logo partnera).
- Obejrzyj każdy slajd (Read) przed użyciem: ucięty tekst, sieroty, czytelność.
- Wykresy i schematy (matematyka, fizyka, finanse) rysuj w tym samym stylu, dane policzone w kodzie.
- **Ilustracje AI tylko w wyraźnie ilustracyjnym, niefotorealistycznym stylu**, jako tło lub dodatek; nigdy fotorealistyczne wizerunki postaci historycznych ani „zdjęcia” wydarzeń; wtedy `isAiGenerated: true`. Brak wymyślonego „prowadzącego” – konto nie może wyglądać jak persona AI.

## Reelsy – specyfikacja

- 1080 × 1920, MP4 H.264, 30 kl./s, `-movflags +faststart`, **z cichą ścieżką AAC** (np. `anullsrc`) – część systemów odrzuca wideo bez ścieżki audio; przy muzyce z biblioteki ustaw `videoVolume: 0`.
- Długość 8–20 s; haczyk tekstowy widoczny od pierwszej klatki (bez intro, bez logo na początku); 3–5 plansz w stylu z logo, każda na tyle długo, by dało się przeczytać (ok. 2,5–4 s), dynamiczne przejścia; ostatnia plansza z puentą, która zachęca do ponownego obejrzenia lub wysłania.
- Okładka: `videoCoverMilliseconds` na planszy z haczykiem albo `videoThumbnailUrl` z osobnym JPEG 1080×1920 z tytułem (ważne dla siatki profilu).

## Podkład muzyczny

- **Reelsy – automatycznie z licencjonowanej biblioteki Instagrama:** w `instagramData` ustaw `audioConfiguration` z `audioId` = fraza wyszukiwania (tytuł/wykonawca) albo numeryczny ID; reszta pól uzupełnia się sama. `videoVolume: 0`, `audioVolume` domyślnie. Gdy fraza pasuje do kilku utworów, wybierz z listy zwróconej przez Metricool i ponów z ID. Utwór zaczyna się od 0 s – wybieraj takie z mocnym wejściem.
- **Dobór nastroju do przedmiotu:** historia/opowieść – filmowy, tajemniczy; spór tygodnia – napięcie; matematyka/fizyka/technologia – elektroniczny, rytmiczny; kosmos – ambient; quiz – lekki, zabawny; finanse/ekonomia – spokojny, nowoczesny. Unikaj wokalu zagłuszającego czytanie.
- **Wymaganie:** konto Firma połączone ze stroną na Facebooku i Metricool przez Facebook Login; biblioteka dla kont firmowych jest węższa (utwory do użytku komercyjnego). Gdy Metricool odrzuci `audioConfiguration` z tego powodu – utwórz szkic bez muzyki, a w raporcie podaj proponowany utwór i przypomnij o wymaganiu (jednorazowo).
- **Karuzele:** API nie pozwala dodać muzyki. W raporcie przy każdej karuzeli podaj 1 proponowany utwór – Michał dodaje go w aplikacji po publikacji (post → ⋯ → Edytuj → audio). Muzyka może dodatkowo kwalifikować karuzelę do kanału Reels.
- **Nigdy** nie wgrywaj własnych plików MP3/muzyki spoza biblioteki Instagrama – ryzyko wyciszenia, blokady i naruszenia praw autorskich.

## Facebook i TikTok

Każdy z 5 materiałów tygodnia trafia na trzy sieci jako **osobne szkice** – osobny post w Metricool na sieć, bo każda wymaga innego tekstu i ustawień (TikTok nie obsługuje łamania wierszy, liczba hashtagów jest różna). To nie narusza zasad oryginalności: publikujesz własny materiał z czystych plików źródłowych, bez znaków wodnych innej platformy (Instagram obniża zasięg materiałów ze znakiem wodnym TikToka). Jeśli `getBrandSettings` nie pokazuje danej sieci (niepodłączona albo połączenie wygasło), pomiń ją i napisz o tym raz w raporcie.

### Facebook (strona „Szkoła kłamała”)

Odbiorcy Facebooka są starsi (35+), chętniej czytają dłuższe teksty i komentują, ale ostrzej się kłócą – dlatego tu najlepiej działają „Spór tygodnia” i „opowieść”, a moderacja komentarzy jest ważniejsza niż na Instagramie.
- Karuzele → `facebookData: {"type": "POST"}` z tymi samymi JPEG 4:5 (do 35 zdjęć; nie mieszaj zdjęć z wideo w jednym poście).
- Reelsy → `facebookData: {"type": "REEL"}` z tym samym MP4 (3–90 s, 9:16). Metricool nie dodaje muzyki do Reelsów na Facebooku – publikuj z cichą ścieżką; w raporcie podaj utwór, gdyby Michał chciał dodać go ręcznie.
- Tekst: ten sam co na Instagramie (z łamaniem wierszy), ale tylko 2–3 hashtagi. Facebook pozwala na klikalne linki – pełny link do źródła daj w `firstCommentText` („Źródło: …”), żeby nie obniżać zasięgu samego posta.
- Godzina: ten sam dzień co na Instagramie, slot z `getBestTimeToPostByNetwork` dla `facebook`.

### TikTok (@szkola_klamala)

TikTok najsilniej ze wszystkich sieci nagradza dźwięk i oglądalność do końca, a pokazuje treści głównie osobom spoza obserwujących – dla nowego konta to największa szansa na zasięg.
- **Wideo (oba Reelsy)** → ten sam MP4 (3 s–10 min). Przez API nie da się wybrać utworu do wideo, a wideo bez modnego dźwięku na TikToku traci zasięg, dlatego ustaw `autoPublish: false`: o godzinie publikacji Metricool wyśle Michałowi powiadomienie, a on w aplikacji TikTok doda dźwięk z trendów i opublikuje. W raporcie podaj 1–2 proponowane dźwięki (nastrój + przykład).
- **Karuzele** → tryb zdjęć TikToka (do 35 zdjęć, JPEG). Wygeneruj wersję slajdów **1080 × 1920 (9:16)**: slajd 4:5 wycentrowany na tle w kolorach marki, z etykietą „SZKOŁA KŁAMAŁA · [PRZEDMIOT]” nad nim i handle pod nim – bez pustych czarnych pasów. Ustaw `tiktokData.autoAddMusic: true` (TikTok sam dobiera muzykę do zdjęć), `photoCoverIndex: 0`, `title` = haczyk (krótko, do ok. 90 znaków). Tu zostaw `autoPublish: true`, bo muzyka do zdjęć działa tylko przy automatycznej publikacji.
- **Tekst:** jeden akapit bez łamania wierszy (API TikToka ich nie obsługuje), 150–300 znaków: haczyk + jedno zdanie rozwinięcia + krótkie źródło („wg Encyklopedii PWN”) + 3–5 hashtagów (#szkolaklamala, #ciekawostki, #wiedza + 1–2 pod temat). Bez #fyp i podobnych – nic nie dają, a wyglądają na spam.
- **Ustawienia `tiktokData`:** `privacyOption: "PUBLIC_TO_EVERYONE"`, komentarze, duety i stitch włączone (stitch to darmowy zasięg), `isAigc: true` tylko przy wideo z ilustracjami AI (etykieta AI na TikToku działa wyłącznie dla wideo), `commercialContentThirdParty` / `commercialContentOwnBrand` = `false` – `true` tylko przy prawdziwej współpracy reklamowej, razem z oznaczeniem zgodnym z UOKiK w tekście.
- Te same zasady co na Instagramie: bez „wpisz A albo B” i próśb o oznaczanie znajomych, ta sama rzetelność, te same granice tematów.
- Godzina: slot z `getBestTimeToPostByNetwork` dla `tiktok`, ten sam dzień co na Instagramie albo następny.

## Media i szkic w Metricool

- Metricool wymaga publicznego URL mediów. Wgraj pliki do Google Drive Michała – „Mój dysk”, folder „Instagram” (nie dysk współdzielony) – i użyj linków; Metricool sam je pobiera. Działa po połączeniu Drive w Metricool (plan Starter). Jeśli połączenie wygasło – zgłoś w raporcie („Planowanie → multimedia → Drive → retry”).
- `createScheduledPost` z `blogId` odczytanym z `getBrandSettings`, w `info`: `draft: true`, `autoPublish: true`, `providers: [{"network":"instagram"}]`, `instagramData` z `type` `"POST"` (karuzela = kilka URL-i w `media`), `"REEL"` lub `"TRIAL_REEL"` (wideo, `audioConfiguration`, okładka), `isAiGenerated` gdy dotyczy; `mediaAltText` dla obrazów; `publicationDate` ze slotu w `Europe/Warsaw`; `text` (z hashtagami na końcu); `firstCommentText: ""`.
- Facebook i TikTok: osobne wywołania `createScheduledPost` z `providers: [{"network":"facebook"}]` + `facebookData`, albo `[{"network":"tiktok"}]` + `tiktokData` (pola jak w sekcji „Facebook i TikTok”), zawsze `draft: true`; w każdym poście tylko dane tej jednej sieci.
- Gdy mediów nie da się dołączyć albo Metricool odrzuci szkic – nie ponawiaj w kółko; dostarcz pliki i treść w raporcie do ręcznego dodania.

## Raport dla Michała

Krótko: tabela 5 materiałów (dzień, przedmiot, format, temat, haczyk, utwór) ze statusem i godziną osobno dla Instagrama, Facebooka i TikToka, lista źródeł faktów, pliki JPEG/MP4 (SendUserFile, także wersje 9:16 dla TikToka), przypomnienie „otwórz szkice w Metricool i zaplanuj, żeby się opublikowały” oraz „przy wideo na TikToku przyjdzie powiadomienie – dodaj dźwięk w aplikacji i opublikuj”, i jedno zdanie o tym, który post, przedmiot i format z poprzedniego tygodnia miał najwięcej udostępnień i wyświetleń (jeśli są dane). W pierwszą niedzielę miesiąca – podsumowanie dla reklamodawców w podziale na sieci (która sieć rośnie najszybciej) i przypomnienie o sprawdzeniu „Stanu konta” oraz dostępności Trial Reels i monetyzacji w panelu profesjonalnym.