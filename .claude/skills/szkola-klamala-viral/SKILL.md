---
name: szkola-klamala-viral
description: Scenariusze rolek „Szkoła kłamała” (@szkola_klamala) pisane pod maksymalne wyświetlenia na Instagramie i TikToku – pętla ciekawości (odpowiedź na końcu), biblioteka haczyków po polsku, budżet słów i długości, serie, powody do wysłania, SEO, strategia dźwięku, ocena scenariusza przed renderem i pętla uczenia się na statystykach. Używaj ZAWSZE przed napisaniem lub zatwierdzeniem scenariusza rolki, przy prośbach „żeby to był viral”, „więcej wyświetleń”, „lepszy haczyk”, „zweryfikuj scenariusz”, oraz przy analizie wyników rolek. Fakty i granice tematów – CLAUDE.md; grafika i ruch – szkola-klamala-grafiki i szkola-klamala-animacje.
---

# Scenariusze pod zasięg

Oparte na analizie z 31.10.2026 i wynikach rolek (rekord: ISS, 1100 wyświetleń) (`docs/analiza-konkurencji-2026-10.md`). Najważniejsze sygnały: **Instagram** – czas oglądania i **wysłania** (sends) na zasięg; **TikTok** – **obejrzenie do końca** i **ponowne obejrzenia**, potem zapisy i udostępnienia. Wszystko poniżej służy tym czterem liczbom. Rzetelność i granice tematów z `CLAUDE.md` są nadrzędne – haczyk może być prowokujący, treść zawsze prawdziwa.

## 0. Wnioski z wyników (aktualizuj co tydzień; pełna tabela w `docs/wyniki.md`)

**Stan 1.11 – statystyki szczegółowe (pełne dane w `docs/wyniki.md`):**
- **Ponad 90% wyświetleń przychodzi z Facebooka** (crosspost z IG). ISS: 1051 z FB, 57 z IG. Francja: 1038 z FB, 19 z IG. Crosspost na FB zawsze włączony. Pierwsze zdanie opisu pisz też pod Facebooka (dorośli, 35+).
- **Widzowie odpadają w 1–2 s:** pominięcia 73–96%, średni czas oglądania 2–3 s. Prawie nikt nie widzi drugiej planszy, więc **wszystko rozstrzyga pierwsza klatka**.
- **Najlepszy haczyk** (73% pominięć, najniżej): **stwierdzenie zaprzeczające oczywistej odpowiedzi** – „Najwięcej stref czasowych nie ma Rosja. Ani USA.”
- **Najgorszy** (96%): pytanie z „Sprawdźmy.” („Na ISS nie ma grawitacji? Sprawdźmy.”). Akapit tekstu na pierwszej klatce (szkło): 89%.
- Prawo, finanse i święta: 210–290 wyświetleń. Karuzele i zdjęcia: 3–19. Polubienia, komentarze i wysłania: prawie 0.

Zasady, które z tego wynikają (obowiązują od 1.11):
1. **Haczyk = stwierdzenie, nie pytanie.** Zaprzecza temu, co widz „wie”: „Najwięcej X nie ma Y.”, „Z dalej: Z”, „X wcale nie robi Y”. Mieści się w 3–8 słowach, jest napisany największym krojem (silnik: klasa `hook`, 1,35× nagłówka) i czytelny od klatki 0. Pod nim co najwyżej 1–3 słowa dopowiedzenia („Ani USA.”). Nigdy akapit.
2. **Szablon B jest domyślny.** Pierwsza wielka liczba stoi na planszy 2. Szablon A (odpowiedź na 50–70%) zawieszony, dopóki pominięcia nie spadną poniżej ok. 60%.
3. **Okładka zawsze ręcznie** z `_okladka.jpg`, czyli z planszy haczyka. Okładka ISS na profilu to klatka przejścia.
4. **Pytanie-reakcja na końcu** („Który kraj obstawiałeś/aś?”) i to samo pytanie w opisie – przeciw zeru komentarzy.
5. Każdy tydzień porównujemy: pominięcia i średni czas dla 2 najlepszych i 1 najsłabszej rolki.

## 0a. Tryb „100 tys.” – co musi mieć każda rolka

Treść:
1. **Mit albo „oczywista odpowiedź”, którą powie babcia i kolega z pracy** – i która jest błędna (wzór: „Najwięcej stref czasowych nie ma Rosja”). Jeśli temat trzeba tłumaczyć, jest za wąski. Prawo i finanse też w tej formie: „rekord / zaskakująca liczba”, nie poradnik.
2. **Liczby-bohaterowie:** min. 3 konkretne liczby w rolce, w tym **1 porównanie do Polski** (miasto, odległość, pensja, cena chleba, liczba mieszkańców). Porównania licz w kodzie.
3. **Kontrowersja z 1b w pierwszych 2 s:** „wszyscy się mylą”, „to wykroczenie”, „tracisz pieniądze”. Zawsze prawdziwa i ze źródłem.
4. **Wypłata:** ostatnia plansza z treścią to „dlaczego” albo twist, a nie podsumowanie.

Obraz i montaż (silnik robi to domyślnie od 1.11, `"moc": "mocna"`):
- **Kadr nigdy nie stoi.** Kamera stale najeżdża (4,5% na planszę), kadr pulsuje na bicie muzyki, uderzenia liczb i pieczątki mają mocniejszy wstrząs.
- W obrębie planszy **coś się dzieje co ok. 1,5 s:** licznik, marker, pieczątka MIT, iskry. Plansza z samym tekstem to najwyżej jedna na rolkę.
- **Haczyk 3–6 słów,** największy krój, żółte słowo-szok, widoczny od klatki 0. Okładka = haczyk.
- Zjawisko, które da się pokazać (kosmos, ciało, auto), dostaje **scenę 3D** (`szkola-klamala-3d`), gdy jest czas na render.
- Cięcia na bicie co 3–6 s. Zasada czytania obowiązuje bez wyjątków – mniej słów, nie krótsze plansze.

Dystrybucja (bez niej 100 tys. jest mało prawdopodobne):
- **Trial Reels** na IG: 2 warianty haczyka, zwycięzca idzie normalnie.
- **TikTok tego samego dnia**, 1–2 h po IG. Odpowiedzi na komentarze **filmem** (TikTok „odpowiedz wideo”) – gotowa plansza z odpowiedzią.
- **Wspólne posty (IG „Zaproś współtwórcę”)** z większymi kontami edukacyjnymi – najsilniejszy sposób na zasięg poza obserwującymi. Propozycja w raporcie co tydzień.
- **Promocja zwycięzców** na TikToku: rolka rosnąca szybciej niż średnia, mały budżet, cel „obserwujący”.
- Przypięty komentarz z pytaniem, przy którym ludzie się kłócą, w granicach z CLAUDE.md.

## 1. Szablon A: pętla ciekawości (zamiast MIT → FAKT na planszy 2)

| # | Plansza | Czas | Zadanie |
|---|---|---|---|
| 1 | **Haczyk** | 2,5–3 s | stawka albo sprzeczność, 4–8 słów, widoczny od klatki 0; **bez odpowiedzi** |
| 2 | **Napięcie** | 3–4 s | „Większość myśli, że…” / „Szkoła uczyła…” – wzmacnia mit, nadal bez odpowiedzi |
| 3 | **Odpowiedź** | 4–5 s | fakt z liczbą (duża liczba, licznik, pieczątka MIT) – ok. 50–70% filmu |
| 4 | **Twist** | 4–5 s | drugi, jeszcze mocniejszy fakt albo „co z tego wynika dla Ciebie” |
| 5 | **Pętla / wysłanie** | 3–4 s | jedno zdanie do wysłania („Wyślij komuś, kto…”) lub pytanie, które odsyła do haczyka; źródło |
| + | logo | 2,8 s | automatycznie |

- **4–5 plansz, cel 20–28 s** z logo (minimum Michała: 4 plansze, 20 s). Dłużej tylko, gdy każda sekunda niesie nowy fakt (TikTok nie płaci w Polsce za > 1 min).
- **Budżet słów: maks. ok. 10–12 słów na planszę** (outro do 18). Zasada czytania zostaje – mniej słów = krótsza plansza = wyższy odsetek obejrzeń do końca.
- Źródło: krótko na planszy odpowiedzi albo outro, pełne w opisie. Nie na każdej planszy.
- Etykieta „SZKOŁA KŁAMAŁA · PRZEDMIOT” tylko na haczyku (rozpoznawalność serii).

## 1'. Szablon B: stos liczb / rekord (wzór ISS i Francji, po 1,1 tys.)

| # | Plansza | Zadanie |
|---|---|---|
| 1 | **Haczyk** | stwierdzenie zaprzeczające oczywistej odpowiedzi („Najwięcej stref czasowych nie ma Rosja. Ani USA.”), 3–8 słów, bez pytania |
| 2 | **MIT → FAKT** | przekreślenie lub pieczątka MIT, odpowiedź z liczbą (pierwsza „wypłata” już po ok. 4 s) |
| 3 | **Liczba 2** | porównanie do Polski („jak z Poznania do Zakopanego”) |
| 4 | **Liczba 3** | jeszcze mocniejsza liczba (prędkość, kwota, czas) |
| 5 | **Dlaczego?** | wyjaśnienie, które zmienia sposób myślenia |
| 6 | **Reakcja** | pytanie, na które każdy zna swoją odpowiedź („Który kraj obstawiałeś/aś?”) + „Wyślij komuś, kto…” + źródło |

- 5–6 plansz, 25–32 s z logo. Każda plansza ma **nową liczbę albo nowe „dlaczego”**. Plansza bez nowej informacji wypada.
- Działa przy mitach powszechnych, gdzie odpowiedź nie zaskakuje sama, ale zaskakuje skala (liczby).
- Wybór: A, gdy odpowiedź sama jest szokiem (data, kwota, kara). B, gdy mamy kilka mocnych liczb i porównanie do Polski. W raporcie zapisz, którego szablonu użyto, a w `docs/wyniki.md` – kolumnę „szablon”.

## 1a. Kilkukrotne obejrzenie (decyzja Michała 31.10 – priorytet)

Każda rolka musi mieć **co najmniej 2** z tych mechanizmów:
- **Pętla:** ostatnia plansza kończy się zdaniem, które wraca do haczyka (np. haczyk „Grób nie jest Twój na zawsze” → koniec „…więc czy na pewno jest Twój?”), a cięcie do logo i z powrotem do haczyka jest płynne.
- **Twist na końcu**, który zmienia sens początku – widz wraca, żeby „zobaczyć to jeszcze raz”.
- **Liczba do sprawdzenia:** konkret (kwota, rok, procent), który chce się przeczytać drugi raz albo pokazać komuś.
- **Szybki ostatni fakt:** ostatnia plansza z treścią krótka (≤ 8 słów) – widz nie zdąży „przetrawić” i ogląda ponownie (zasada czytania nadal obowiązuje).
- **Detal w tle:** liczba/słowo w konturze tła lub mała etykieta, które zauważa się dopiero za drugim razem.

## 1b. Kontrowersja (decyzja Michała 31.10 – mocna, ale w granicach)

Treść ma być **na tyle kontrowersyjna, by zatrzymać i wywołać dyskusję** – zawsze prawdziwa i ze źródłem:
- „Wszyscy tak robią, a to błąd / wykroczenie / strata pieniędzy” (prawo, motoryzacja, finanse).
- „Szkoła/rodzice uczyli źle” – podważenie powszechnego przekonania.
- Osobista stawka: pieniądze, rodzina, kara, zdrowie (bez porad), własność.
- Liczba, która oburza lub zaskakuje („20 lat i grób może być użyty ponownie”).
- Uczciwy spór dwóch stron (Spór tygodnia) – pytanie, przy którym ludzie się kłócą w komentarzach.

**Granice bez wyjątków (CLAUDE.md):** polityka, religia, szczepionki i spory medyczne, płeć, migracja, teorie spiskowe, atakowanie osób i instytucji, drastyczne treści. Kontrowersja = zaskakujący fakt, nie atak i nie światopogląd. Haczyk musi spełnić obietnicę (zawiedzione oczekiwania obniżają zasięg).

## 2. Biblioteka haczyków (pierwsza plansza)

| Typ | Wzór | Przykład |
|---|---|---|
| Stawka osobista | „Twój/Twoja … nie jest …” | „Grób bliskich nie jest Twój na zawsze” |
| Sprzeczność | „… jest starsze/szybsze/tańsze niż …?” | „Halloween jest starsze niż Polska?” |
| Strata | „Tracisz … , bo …” | „Tracisz 19% odsetek i nawet o tym nie wiesz” |
| Zakaz / kara | „Za to dostaniesz mandat, a robisz to codziennie” | „Rozgrzewasz auto? To 100 zł mandatu” |
| Szkoła kłamała | „W szkole uczyli, że … Błąd.” | „W szkole uczyli, że na ISS nie ma grawitacji” |
| Liczba-szok | „[liczba] … – i to legalne” | „20 lat. Potem grób może dostać ktoś inny” |
| Pytanie-test | „Tylko 1 na 10 osób wie, …” – **tylko gdy mamy źródło na tę liczbę** | – |

Zasady: konkret zamiast ogólnika („100 zł mandatu”, nie „kara”); słowo „Ty/Twój” albo bliska osoba; bez clickbaitu, który nie spełnia obietnicy (Instagram obniża zasięg za „zawiedzione oczekiwania”).

## 3. Powód do wysłania (sends)

Każdy scenariusz musi mieć **adresata**: „wyślij mamie / kierowcy / komuś, kto…”. Najlepsze tematy: pieniądze, prawo w codziennym życiu, zdrowie bez porad, rodzina, samochód, „wszyscy tak robią, a to błąd”. Sprawdzian: czy da się dokończyć zdanie „Muszę to pokazać ___, bo ___”?

## 4. Serie i rozpoznawalność

- Stały numer w opisie i na haczyku małą etykietą: „Szkoła kłamała #N”.
- Serie tematyczne: „Prawo, którego nie znasz”, „Mit tygodnia”, „Pieniądze bez ściemy”, „Kierowcy, stop”.
- Jeden kolor/efekt charakterystyczny dla serii (np. pieczątka MIT dla „Mit tygodnia”).

## 5. Dźwięk

- **Instagram:** nasz podkład (oryginalny dźwięk – inni mogą go użyć, to dodatkowe wejścia).
- **TikTok:** plik `_efekty` (+ wersja 1080) i **dźwięk z trendów** dodany w aplikacji, oryginał ok. 30%. Na TikToku dźwięk z trendów to dodatkowy sygnał dystrybucji.
- Treść zawsze czytelna bez dźwięku.

## 6. SEO i opis

- Pierwsze zdanie opisu = fraza, którą ktoś wpisze w wyszukiwarkę („opłata za grób 20 lat”, „podatek od lokaty ile”).
- Te same słowa kluczowe na planszy haczyka (TikTok czyta tekst z obrazu).
- 3–5 hashtagów, w tym 1 serii (#szkolaklamala) i 1–2 tematyczne z wyszukiwanych.
- Przypięty komentarz: źródło + jedno prawdziwe pytanie do dyskusji.

## 7. Ocena scenariusza przed renderem (0–2 pkt za każdy punkt)

1. Haczyk ≤ 8 słów: stwierdzenie zaprzeczające oczywistej odpowiedzi (nie pytanie, nie akapit), czytelne od klatki 0.
2. Struktura szablonu A (odpowiedź na ok. 50–70%) albo B (co plansza nowa liczba, „dlaczego” na końcu).
3. Twist / drugi fakt na końcu.
4. Wyraźny adresat do wysłania.
5. Temat szeroki (dotyczy większości dorosłych w Polsce).
6. Każda plansza ≤ 12 słów (outro ≤ 18), całość 20–28 s (A) lub 25–32 s (B), bez planszy bez nowej informacji.
7. Min. 3 liczby-bohaterowie, w tym 1 porównanie do Polski (policzone w kodzie).
8. Fakty ze źródłem, zgodne z granicami z CLAUDE.md (to warunek konieczny – 0 pkt = odrzucenie).
9. Co najmniej 2 mechanizmy kilkukrotnego obejrzenia (1a).
10. Kontrowersja z 1b – zatrzymuje i prowokuje dyskusję, w granicach marki.

Minimum do renderu: **15/20**.

Wynik i krótkie uzasadnienie podaj Michałowi razem ze scenariuszem do zatwierdzenia.

## 8. Publikacja i testy

- Instagram: **Trial Reels** (najpierw do nieobserwujących) dla 1 z 2 wariantów haczyka; zwycięzcę publikować normalnie.
- TikTok: 1–2 h po Instagramie, ta sama rolka; pierwsze 60 min po publikacji – odpowiadać na komentarze.
- Gdy rolka po 2–3 h rośnie wyraźnie szybciej niż średnia → promocja (TikTok: tylko filmy, cel „obserwujący”).

## 9. Pętla uczenia się

Co tydzień poproś Michała o zrzuty statystyk rolek (IG: wyświetlenia, średni czas oglądania, wysłania, zapisy; TT: średni czas, obejrzenia do końca, źródło ruchu). Zapisz w `docs/wyniki.md`: temat, haczyk, długość, wynik. Po 3–4 tygodniach: więcej tematów i typów haczyków, które wygrywają, mniej tych, które przegrywają – i zaktualizuj ten skill.
